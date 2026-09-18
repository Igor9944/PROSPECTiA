from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.services import activity_service
from app.schemas.activity import ActivityCreate, ActivityUpdate, Activity
from app.schemas.user import User
from app.core.database import get_db
from app.core.security import get_current_active_user


router = APIRouter(
    prefix="/activities",
    tags=["activities"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Activity)
def create_activity(activity: ActivityCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return activity_service.create_activity(db=db, activity=activity)


@router.get("/{activity_id}", response_model=Activity)
def read_activity(activity_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_activity = activity_service.get_activity(db, activity_id=activity_id)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return db_activity


@router.get("/by_prospect/{prospect_id}", response_model=List[Activity])
def read_activities_by_prospect(prospect_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100, current_user: User = Depends(get_current_active_user)):
    activities = activity_service.get_activities_by_prospect(db, prospect_id=prospect_id, skip=skip, limit=limit)
    return activities


@router.put("/{activity_id}", response_model=Activity)
def update_activity(activity_id: int, activity: ActivityUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_activity = activity_service.update_activity(db, activity_id=activity_id, activity=activity)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return db_activity


@router.delete("/{activity_id}", response_model=Activity)
def delete_activity(activity_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_activity = activity_service.delete_activity(db, activity_id=activity_id)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return db_activity