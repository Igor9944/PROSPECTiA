from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.follow_up import FollowUp
from app.schemas.follow_up import FollowUpCreate, FollowUpUpdate
from app.models.follow_up import FollowUpStatusEnum
from datetime import datetime

def get_follow_up(db: Session, follow_up_id: int):
    return db.query(FollowUp).filter(FollowUp.id == follow_up_id).first()

def get_follow_ups_by_prospect(db: Session, prospect_id: int, skip: int = 0, limit: int = 100):
    return db.query(FollowUp).filter(FollowUp.prospect_id == prospect_id).offset(skip).limit(limit).all()

def get_follow_ups_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(FollowUp).filter(FollowUp.assigned_to == user_id).offset(skip).limit(limit).all()

def get_follow_ups_due_today(db: Session):
    today = datetime.now().date()
    return db.query(FollowUp).filter(
        FollowUp.due_date >= today,
        FollowUp.due_date < today + timedelta(days=1),
        FollowUp.status == FollowUpStatusEnum.PENDING
    ).all()

def get_overdue_follow_ups(db: Session):
    today = datetime.now()
    return db.query(FollowUp).filter(
        FollowUp.due_date < today,
        FollowUp.status == FollowUpStatusEnum.PENDING
    ).all()

def get_upcoming_follow_ups(db: Session, days: int = 7):
    today = datetime.now().date()
    future_date = today + timedelta(days=days)
    return db.query(FollowUp).filter(
        FollowUp.due_date >= today,
        FollowUp.due_date <= future_date,
        FollowUp.status == FollowUpStatusEnum.PENDING
    ).all()

def create_follow_up(db: Session, follow_up: FollowUpCreate):
    db_follow_up = FollowUp(
        prospect_id=follow_up.prospect_id,
        assigned_to=follow_up.assigned_to,
        due_date=follow_up.due_date,
        reminder_date=follow_up.reminder_date,
        status=follow_up.status,
        notes=follow_up.notes
    )
    db.add(db_follow_up)
    db.commit()
    db.refresh(db_follow_up)
    return db_follow_up

def update_follow_up(db: Session, follow_up_id: int, follow_up_update: FollowUpUpdate):
    db_follow_up = get_follow_up(db, follow_up_id)
    if db_follow_up:
        update_data = follow_up_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_follow_up, field, value)
        db.commit()
        db.refresh(db_follow_up)
    return db_follow_up

def delete_follow_up(db: Session, follow_up_id: int):
    db_follow_up = get_follow_up(db, follow_up_id)
    if db_follow_up:
        db.delete(db_follow_up)
        db.commit()
    return db_follow_up

from datetime import timedelta