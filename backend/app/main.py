from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.models import Activity, AIEvaluation, Company, Contact, Conversion, FollowUp, Prospect, User  # noqa: F401
from app.routers import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    if settings.SEED_ON_START:
        from seed import seed

        seed()
    yield


app = FastAPI(
    title="PROSPECTIA",
    description="CRM de prospection commerciale pour PME informatiques",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_PREFIX)


@app.get("/")
def root():
    return {"name": settings.PROJECT_NAME, "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "healthy"}
