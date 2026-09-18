from sqlalchemy.orm import Session
from app.models.prospect import Prospect
from app.schemas.prospect import ProspectCreate, ProspectUpdate


def get_prospect(db: Session, prospect_id: int):
    return db.query(Prospect).filter(Prospect.id == prospect_id).first()


def get_prospects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Prospect).offset(skip).limit(limit).all()


def create_prospect(db: Session, prospect: ProspectCreate):
    db_prospect = Prospect(**prospect.dict())
    db.add(db_prospect)
    db.commit()
    db.refresh(db_prospect)
    return db_prospect


def update_prospect(db: Session, prospect_id: int, prospect: ProspectUpdate):
    db_prospect = db.query(Prospect).filter(Prospect.id == prospect_id).first()
    if db_prospect:
        update_data = prospect.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_prospect, key, value)
        db.commit()
        db.refresh(db_prospect)
    return db_prospect


def delete_prospect(db: Session, prospect_id: int):
    db_prospect = db.query(Prospect).filter(Prospect.id == prospect_id).first()
    if db_prospect:
        db.delete(db_prospect)
        db.commit()
    return db_prospect