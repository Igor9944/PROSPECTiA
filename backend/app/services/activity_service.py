from sqlalchemy.orm import Session
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityUpdate


def get_activity(db: Session, activity_id: int):
    return db.query(Activity).filter(Activity.id == activity_id).first()


def get_activities_by_prospect(db: Session, prospect_id: int, skip: int = 0, limit: int = 100):
    return db.query(Activity).filter(Activity.prospect_id == prospect_id).offset(skip).limit(limit).all()


def create_activity(db: Session, activity: ActivityCreate):
    db_activity = Activity(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


def update_activity(db: Session, activity_id: int, activity: ActivityUpdate):
    db_activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if db_activity:
        update_data = activity.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_activity, key, value)
        db.commit()
        db.refresh(db_activity)
    return db_activity


def delete_activity(db: Session, activity_id: int):
    db_activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if db_activity:
        db.delete(db_activity)
        db.commit()
    return db_activity