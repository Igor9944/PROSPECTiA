from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.ai_evaluation import AIEvaluation
from app.models.user import User
from app.schemas.ai_evaluation import AIAnalysisOut, AIEvaluationOut
from app.services.ai_service import analyze_and_store
from app.services.crm import prospect_service

router = APIRouter()


@router.post("/prospects/{prospect_id}/analyze", response_model=AIAnalysisOut)
def analyze_prospect(prospect_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    prospect = prospect_service.get(db, prospect_id)
    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect introuvable")
    return analyze_and_store(db, prospect)


@router.get("/prospects/{prospect_id}/evaluations", response_model=list[AIEvaluationOut])
def list_evaluations(prospect_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return (
        db.query(AIEvaluation)
        .filter(AIEvaluation.prospect_id == prospect_id)
        .order_by(AIEvaluation.created_at.desc())
        .all()
    )
