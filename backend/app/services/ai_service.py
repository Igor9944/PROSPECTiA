import json
import re
from datetime import datetime, timezone

import httpx
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.ai_evaluation import AIEvaluation
from app.models.company import Company
from app.models.prospect import Prospect
from app.schemas.ai_evaluation import AIAnalysisOut
from app.services.qualification import qualify_prospect, score_level


class AIProvider:
    name = "none"

    def analyze(self, db: Session, prospect: Prospect) -> AIAnalysisOut:
        raise NotImplementedError


class LocalAIProvider(AIProvider):
    name = "none"

    def analyze(self, db: Session, prospect: Prospect) -> AIAnalysisOut:
        qualification = qualify_prospect(db, prospect)
        company: Company | None = prospect.company or db.get(Company, prospect.company_id)
        industry = company.industry if company else "votre secteur"
        name = company.name if company else "l'entreprise"
        needs = [
            f"Modernisation du SI {industry.lower()}",
            "Sécurisation des accès et de la donnée",
            "Accompagnement infogérance / cloud",
        ]
        next_action = "Planifier un appel de découverte de 20 minutes."
        if qualification.score >= 81:
            next_action = "Contacter le décideur aujourd'hui et proposer un diagnostic."
        elif qualification.score >= 61:
            next_action = "Envoyer un message personnalisé puis relancer sous 3 jours."
        elif qualification.score <= 30:
            next_action = "Enrichir la fiche et revoir dans 30 jours."

        message = (
            f"Bonjour,\n\n"
            f"Je travaille avec des entreprises du secteur {industry} pour fiabiliser leur SI. "
            f"{name} pourrait bénéficier d'un diagnostic court sur la sécurité et l'exploitation. "
            f"Seriez-vous disponible 20 minutes cette semaine ?\n\nCordialement"
        )
        reasoning = " | ".join(f"{item.label} (+{item.points}) : {item.explanation}" for item in qualification.criteria)
        recommendation = (
            f"Prospect {score_level(qualification.score)} ({qualification.score}/100). {next_action} "
            f"Priorité suggérée : {qualification.priority.value}."
        )
        return AIAnalysisOut(
            score=qualification.score,
            reasoning=reasoning,
            recommendation=recommendation,
            potential_needs=needs,
            suggested_priority=qualification.priority.value,
            next_action=next_action,
            outreach_message=message,
            provider=self.name,
        )


class OpenAIProvider(LocalAIProvider):
    name = "openai"

    def analyze(self, db: Session, prospect: Prospect) -> AIAnalysisOut:
        # Sans clé, on retombe sur le moteur local pour rester opérationnel.
        if not settings.ai_api_key:
            fallback = super().analyze(db, prospect)
            fallback.provider = "none"
            return fallback
        result = super().analyze(db, prospect)
        result.provider = "openai"
        result.recommendation = f"[OpenAI prêt] {result.recommendation}"
        return result


class GoogleAIProvider(LocalAIProvider):
    name = "google"

    def _build_prompt(self, db: Session, prospect: Prospect) -> str:
        qualification = qualify_prospect(db, prospect)
        company = prospect.company or db.get(Company, prospect.company_id)
        industry = company.industry if company else "votre secteur"
        name = company.name if company else "l'entreprise"
        notes = prospect.notes or "Aucune note disponible"
        return (
            "Tu es un assistant commercial B2B. Analyse ce prospect et réponds uniquement en JSON valide, "
            "sans bloc de code ni explication hors JSON. La structure exacte doit être : "
            '{"score": number, "reasoning": "string", "recommendation": "string", "potential_needs": ["string"], '
            '"suggested_priority": "LOW|MEDIUM|HIGH|VERY_HIGH", "next_action": "string", "outreach_message": "string"}. '
            f"Entreprise: {name}. Secteur: {industry}. Notes: {notes}. "
            f"Score de qualification local: {qualification.score}. "
            f"Critères: " + " | ".join(f"{criterion.label}:{criterion.points}:{criterion.explanation}" for criterion in qualification.criteria)
        )

    @staticmethod
    def _extract_json_payload(raw_text: str) -> dict:
        cleaned = raw_text.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned)
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            cleaned = match.group(0)
        return json.loads(cleaned)

    def analyze(self, db: Session, prospect: Prospect) -> AIAnalysisOut:
        api_key = settings.ai_api_key
        if not api_key:
            fallback = super().analyze(db, prospect)
            fallback.provider = "none"
            return fallback

        try:
            response = httpx.post(
                "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent",
                params={"key": api_key},
                json={
                    "contents": [{"parts": [{"text": self._build_prompt(db, prospect)}]}],
                    "generationConfig": {
                        "temperature": 0.2,
                        "topP": 0.8,
                    },
                },
                timeout=30.0,
            )
            response.raise_for_status()
            payload = response.json()
            text = payload["candidates"][0]["content"]["parts"][0]["text"]
            data = self._extract_json_payload(text)
            model = AIAnalysisOut.model_validate(data)
            model.provider = "google"
            return model
        except Exception:
            fallback = super().analyze(db, prospect)
            fallback.provider = "none"
            return fallback


def get_ai_provider() -> AIProvider:
    provider = (settings.AI_PROVIDER or "none").lower()
    if provider in {"openai", "gpt", "openai_chat"}:
        return OpenAIProvider()
    if provider in {"google", "gemini", "google_ai"}:
        return GoogleAIProvider()
    return LocalAIProvider()


def analyze_and_store(db: Session, prospect: Prospect) -> AIAnalysisOut:
    analysis = get_ai_provider().analyze(db, prospect)
    evaluation = AIEvaluation(
        prospect_id=prospect.id,
        score=analysis.score,
        reasoning=analysis.reasoning,
        recommendation=analysis.recommendation,
    )
    db.add(evaluation)
    prospect.score = analysis.score
    prospect.priority = analysis.suggested_priority
    prospect.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(evaluation)
    return analysis
