from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.follow_up import FollowUpCreate, FollowUpOut, FollowUpUpdate
from app.services.crm import follow_up_service

router = APIRouter()


@router.get("/", response_model=list[FollowUpOut])
def list_follow_ups(bucket: str | None = None, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return follow_up_service.list(db, bucket)


@router.post("/", response_model=FollowUpOut, status_code=201)
def create_follow_up(payload: FollowUpCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return follow_up_service.create(db, payload)


@router.patch("/{follow_up_id}", response_model=FollowUpOut)
def update_follow_up(
    follow_up_id: int,
    payload: FollowUpUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    follow_up = follow_up_service.get(db, follow_up_id)
    if not follow_up:
        raise HTTPException(status_code=404, detail="Relance introuvable")
    return follow_up_service.update(db, follow_up, payload)
