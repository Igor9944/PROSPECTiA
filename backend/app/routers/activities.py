from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.activity import ActivityCreate, ActivityOut, ActivityUpdate
from app.services.crm import activity_service

router = APIRouter()


@router.get("/", response_model=list[ActivityOut])
def list_activities(prospect_id: int | None = None, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return activity_service.list(db, prospect_id)


@router.post("/", response_model=ActivityOut, status_code=201)
def create_activity(
    payload: ActivityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return activity_service.create(db, payload, current_user.id)


@router.patch("/{activity_id}", response_model=ActivityOut)
def update_activity(
    activity_id: int,
    payload: ActivityUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    activity = activity_service.get(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activité introuvable")
    return activity_service.update(db, activity, payload)
