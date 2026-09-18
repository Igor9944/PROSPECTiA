from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.models import Activity, AIEvaluation, Company, Contact, Conversion, FollowUp, Prospect, User  # noqa: F401
from app.routers import api_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PROSPECTIA",
    description="CRM de prospection commerciale pour PME informatiques",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_PREFIX)


@app.on_event("startup")
def seed_if_requested() -> None:
    if not settings.SEED_ON_START:
        return
    from seed import seed

    seed()


@app.get("/")
def root():
    return {"name": settings.PROJECT_NAME, "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "healthy"}
