from sqlalchemy.orm import Session
from app.models.follow_up import FollowUp
from app.schemas.follow_up import FollowUpCreate, FollowUpUpdate


def get_follow_up(db: Session, follow_up_id: int):
    return db.query(FollowUp).filter(FollowUp.id == follow_up_id).first()


def get_follow_ups_by_prospect(db: Session, prospect_id: int, skip: int = 0, limit: int = 100):
    return db.query(FollowUp).filter(FollowUp.prospect_id == prospect_id).offset(skip).limit(limit).all()


def create_follow_up(db: Session, follow_up: FollowUpCreate):
    db_follow_up = FollowUp(**follow_up.dict())
    db.add(db_follow_up)
    db.commit()
    db.refresh(db_follow_up)
    return db_follow_up


def update_follow_up(db: Session, follow_up_id: int, follow_up: FollowUpUpdate):
    db_follow_up = db.query(FollowUp).filter(FollowUp.id == follow_up_id).first()
    if db_follow_up:
        update_data = follow_up.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_follow_up, key, value)
        db.commit()
        db.refresh(db_follow_up)
    return db_follow_up


def delete_follow_up(db: Session, follow_up_id: int):
    db_follow_up = db.query(FollowUp).filter(FollowUp.id == follow_up_id).first()
    if db_follow_up:
        db.delete(db_follow_up)
        db.commit()
    return db_follow_up