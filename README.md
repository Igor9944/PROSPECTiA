# PROSPECTIA (ProspectAI)

CRM de prospection commerciale — FastAPI + React.

**Frontend live :** [https://igor9944.github.io/PROSPECTiA/](https://igor9944.github.io/PROSPECTiA/)  
**API docs :** une fois le backend Render en ligne → `/docs`

Comptes de démo (après seed) :

| Rôle | Email | Mot de passe |
|---|---|---|
| Admin | `admin@example.com` | `Admin123!` |
| Commercial | `commercial@example.com` | `Commercial123!` |
| Manager | `manager@example.com` | `Manager123!` |

## Déploiement

### Frontend — GitHub Pages (automatique)

Chaque push sur `frontend/**` (ou un lancement manuel du workflow) construit le SPA et le publie sur GitHub Pages :

`https://igor9944.github.io/PROSPECTiA/`

Le workflow `Deploy Frontend to GitHub Pages` est déjà en place.

**Secret GitHub à ajouter** (Settings → Secrets and variables → Actions) :

- `VITE_API_URL` — URL publique de l’API, **avec** le suffixe `/api`  
  Exemple : `https://prospectia-api.onrender.com/api`

Sans ce secret, le frontend appelle `/api` (utile en local via le proxy Vite, pas sur Pages).

### Backend — Render (Blueprint)

1. Ouvre [Render](https://dashboard.render.com) → **New** → **Blueprint**
2. Branche le dépôt `Igor9944/PROSPECTiA` — le fichier `render.yaml` crée :
   - le service web `prospectia-api`
   - la base Postgres `prospectia-db`
3. Copie le *Deploy Hook* du service Render
4. Ajoute le secret GitHub `RENDER_DEPLOY_HOOK` avec cette URL
5. Mets `VITE_API_URL` (voir ci-dessus) puis relance le workflow frontend

Le backend expose `/health`. `SEED_ON_START=true` peuple la base au premier démarrage.

### Frontend — Vercel (optionnel)

Root Directory = `frontend`. `frontend/vercel.json` gère le routing SPA.  
Ajoute la variable d’environnement `VITE_API_URL` identique à celle de Pages.

> L’ancienne URL `frontend-mr-flx-s-projects.vercel.app` n’appartient pas à ce dépôt : elle est protégée par le SSO Vercel d’un autre compte. Ne plus l’utiliser.

## Lancer en local

### Docker Compose

```bash
docker compose up --build
```

- API : http://localhost:8000 (`/docs` pour Swagger)
- Front : http://localhost:3000

### Sans Docker

**Backend**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
python seed.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend**

```bash
cd frontend
npm ci
npm run dev
```

Le proxy Vite envoie `/api` vers `http://127.0.0.1:8000`.

## Stack

- **Backend :** FastAPI, SQLAlchemy 2, JWT, Alembic, Pytest
- **Frontend :** React 18, Vite, TypeScript, Tailwind, Recharts
- **CI :** GitHub Actions (pytest + build Pages)

## Variables d’environnement backend

Voir `backend/.env.example` :

- `DATABASE_URL` — SQLite en local, Postgres en production
- `SECRET_KEY` — signature JWT (obligatoire en prod)
- `CORS_ORIGINS` — origines autorisées, séparées par des virgules
- `SEED_ON_START` — `true` pour peupler la base au démarrage
- `AI_PROVIDER` / `AI_API_KEY` — qualification IA (`none` par défaut)

## Tests

```bash
cd backend && pytest -v
cd frontend && npm test
```
