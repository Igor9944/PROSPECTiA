from fastapi import APIRouter

from app.routers import (
    activities,
    ai,
    auth,
    companies,
    contacts,
    conversions,
    follow_ups,
    prospecting,
    prospects,
    reports,
    users,
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
api_router.include_router(prospects.router, prefix="/prospects", tags=["prospects"])
api_router.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
api_router.include_router(activities.router, prefix="/activities", tags=["activities"])
api_router.include_router(follow_ups.router, prefix="/follow-ups", tags=["follow-ups"])
api_router.include_router(conversions.router, prefix="/conversions", tags=["conversions"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(prospecting.router, prefix="/prospecting", tags=["prospecting"])
