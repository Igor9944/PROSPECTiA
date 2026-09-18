from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.services import follow_up_service
from app.schemas.follow_up import FollowUpCreate, FollowUpUpdate, FollowUp
from app.schemas.user import User
from app.core.database import get_db
from app.core.security import get_current_active_user


router = APIRouter(
    prefix="/follow_ups",
    tags=["follow_ups"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=FollowUp)
def create_follow_up(follow_up: FollowUpCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return follow_up_service.create_follow_up(db=db, follow_up=follow_up)


@router.get("/{follow_up_id}", response_model=FollowUp)
def read_follow_up(follow_up_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_follow_up = follow_up_service.get_follow_up(db, follow_up_id=follow_up_id)
    if db_follow_up is None:
        raise HTTPException(status_code=404, detail="Follow up not found")
    return db_follow_up


@router.get("/by_prospect/{prospect_id}", response_model=List[FollowUp])
def read_follow_ups_by_prospect(prospect_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100, current_user: User = Depends(get_current_active_user)):
    follow_ups = follow_up_service.get_follow_ups_by_prospect(db, prospect_id=prospect_id, skip=skip, limit=limit)
    return follow_ups


@router.put("/{follow_up_id}", response_model=FollowUp)
def update_follow_up(follow_up_id: int, follow_up: FollowUpUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_follow_up = follow_up_service.update_follow_up(db, follow_up_id=follow_up_id, follow_up=follow_up)
    if db_follow_up is None:
        raise HTTPException(status_code=404, detail="Follow up not found")
    return db_follow_up


@router.delete("/{follow_up_id}", response_model=FollowUp)
def delete_follow_up(follow_up_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_follow_up = follow_up_service.delete_follow_up(db, follow_up_id=follow_up_id)
    if db_follow_up is None:
        raise HTTPException(status_code=404, detail="Follow up not found")
    return db_follow_up