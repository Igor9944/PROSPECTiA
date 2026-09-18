# Déploiement PROSPECTIA sur Railway

Monorepo : **backend** (FastAPI) + **frontend** (React/Vite) + **PostgreSQL**.

## 1. Créer le projet Railway

1. Va sur [railway.app](https://railway.app) → **New Project**
2. **Deploy from GitHub repo** → sélectionne `Igor9944/PROSPECTiA`
3. Ne déploie pas encore le service unique : on va créer 3 services.

## 2. PostgreSQL

1. Dans le projet → **+ New** → **Database** → **PostgreSQL**
2. Railway crée un service `Postgres` avec la variable `DATABASE_URL`

## 3. Backend (API)

1. **+ New** → **GitHub Repo** → même repo `PROSPECTiA`
2. Settings du service :
   - **Name** : `prospectia-api` (ou `backend`)
   - **Root Directory** : `backend`
   - **Watch Paths** : `/backend/**`
3. Variables (onglet **Variables**) :

```
DATABASE_URL=${{Postgres.DATABASE_URL}}
SECRET_KEY=<génère une clé longue aléatoire>
SEED_ON_START=true
AI_PROVIDER=none
ACCESS_TOKEN_EXPIRE_MINUTES=60
CORS_ORIGINS=https://${{frontend.RAILWAY_PUBLIC_DOMAIN}},http://localhost:5173,http://localhost:3000
```

> Remplace `frontend` par le **nom exact** du service frontend une fois créé.
> Ou mets `*` temporairement pour CORS si besoin de tester :
> `CORS_ORIGINS=*`

4. Settings → **Networking** → **Generate Domain** (ex: `prospectia-api-production.up.railway.app`)
5. Healthcheck : path `/health` (déjà dans `railway.toml`)

## 4. Frontend (SPA)

1. **+ New** → **GitHub Repo** → même repo
2. Settings :
   - **Name** : `frontend`
   - **Root Directory** : `frontend`
   - **Watch Paths** : `/frontend/**`
3. Variables de **build** (importantes pour Vite) :

```
VITE_API_URL=https://${{prospectia-api.RAILWAY_PUBLIC_DOMAIN}}/api
```

> Utilise le nom exact du service backend. L’URL doit finir par `/api`.

4. Networking → **Generate Domain**

## 5. Relier CORS correctement

Une fois les deux domaines générés, mets à jour sur le backend :

```
CORS_ORIGINS=https://TON-FRONTEND.up.railway.app,http://localhost:5173
```

Redeploy le backend.

## 6. Vérifications

| URL | Attendu |
|-----|---------|
| `https://API.../health` | `{"status":"healthy"}` |
| `https://API.../docs` | Swagger UI |
| `https://FRONTEND.../` | Page de login PROSPECTIA |

Comptes démo (si `SEED_ON_START=true`) :

| Rôle | Email | Mot de passe |
|------|-------|--------------|
| Admin | `admin@example.com` | `Admin123!` |
| Commercial | `commercial@example.com` | `Commercial123!` |
| Manager | `manager@example.com` | `Manager123!` |

## Notes

- Le backend convertit déjà `postgres://` → `postgresql://` (compatible Railway).
- Le frontend est servi par **Caddy** avec fallback SPA (`try_files` → `index.html`).
- `VITE_API_URL` est injecté **au build** : si tu changes l’URL de l’API, **rebuild** le frontend.
- Plan gratuit Railway : services s’endorment après inactivité ; le premier hit peut prendre ~30–60 s.

## CLI (optionnel)

```bash
npm i -g @railway/cli
railway login
railway link   # dans le repo
# puis configurer root directory / variables dans le dashboard
```
