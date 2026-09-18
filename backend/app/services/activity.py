from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityUpdate
from app.models.activity import ActivityTypeEnum

def get_activity(db: Session, activity_id: int):
    return db.query(Activity).filter(Activity.id == activity_id).first()

def get_activities_by_prospect(db: Session, prospect_id: int, skip: int = 0, limit: int = 100):
    return db.query(Activity).filter(Activity.prospect_id == prospect_id).offset(skip).limit(limit).all()

def get_activities_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Activity).filter(Activity.user_id == user_id).offset(skip).limit(limit).all()

def create_activity(db: Session, activity: ActivityCreate):
    db_activity = Activity(
        prospect_id=activity.prospect_id,
        user_id=activity.user_id,
        type=activity.type,
        subject=activity.subject,
        description=activity.description,
        scheduled_at=activity.scheduled_at,
        completed_at=activity.completed_at,
        result=activity.result
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def update_activity(db: Session, activity_id: int, activity_update: ActivityUpdate):
    db_activity = get_activity(db, activity_id)
    if db_activity:
        update_data = activity_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_activity, field, value)
        db.commit()
        db.refresh(db_activity)
    return db_activity

def delete_activity(db: Session, activity_id: int):
    db_activity = get_activity(db, activity_id)
    if db_activity:
        db.delete(db_activity)
        db.commit()
    return db_activity