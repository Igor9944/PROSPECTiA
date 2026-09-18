from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.prospect import Prospect, PriorityEnum, StatusEnum
from app.schemas.prospect import ProspectCreate, ProspectUpdate
from app.models.company import Company
from app.models.user import User

def get_prospect(db: Session, prospect_id: int):
    return db.query(Prospect).filter(Prospect.id == prospect_id).first()

def get_prospects(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    company_id: Optional[int] = None,
    assigned_to: Optional[int] = None,
    status: Optional[StatusEnum] = None,
    priority: Optional[PriorityEnum] = None,
    min_score: Optional[float] = None,
    max_score: Optional[float] = None
):
    query = db.query(Prospect)

    if company_id:
        query = query.filter(Prospect.company_id == company_id)
    if assigned_to:
        query = query.filter(Prospect.assigned_to == assigned_to)
    if status:
        query = query.filter(Prospect.status == status)
    if priority:
        query = query.filter(Prospect.priority == priority)
    if min_score is not None:
        query = query.filter(Prospect.score >= min_score)
    if max_score is not None:
        query = query.filter(Prospect.score <= max_score)

    return query.offset(skip).limit(limit).all()

def create_prospect(db: Session, prospect: ProspectCreate):
    db_prospect = Prospect(
        company_id=prospect.company_id,
        assigned_to=prospect.assigned_to,
        score=prospect.score,
        priority=prospect.priority,
        status=prospect.status,
        notes=prospect.notes,
        estimated_value=prospect.estimated_value
    )
    db.add(db_prospect)
    db.commit()
    db.refresh(db_prospect)
    return db_prospect

def update_prospect(db: Session, prospect_id: int, prospect_update: ProspectUpdate):
    db_prospect = get_prospect(db, prospect_id)
    if db_prospect:
        update_data = prospect_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_prospect, field, value)
        db.commit()
        db.refresh(db_prospect)
    return db_prospect

def delete_prospect(db: Session, prospect_id: int):
    db_prospect = get_prospect(db, prospect_id)
    if db_prospect:
        db.delete(db_prospect)
        db.commit()
    return db_prospect

def get_prospect_count(db: Session):
    return db.query(Prospect).count()

def get_new_prospects_count(db: Session):
    return db.query(Prospect).filter(Prospect.status == StatusEnum.NEW).count()

def get_qualified_prospects_count(db: Session):
    return db.query(Prospect).filter(Prospect.status == StatusEnum.QUALIFIED).count()

def get_converted_prospects_count(db: Session):
    return db.query(Prospect).filter(Prospect.status == StatusEnum.CONVERTED).count()

def get_lost_prospects_count(db: Session):
    return db.query(Prospect).filter(Prospect.status == StatusEnum.LOST).count()

def get_prospects_to_follow_up_count(db: Session):
    return db.query(Prospect).filter(Prospect.status == StatusEnum.FOLLOW_UP).count()

def get_estimated_value(db: Session):
    result = db.query(Prospect.estimated_value).filter(Prospect.estimated_value.isnot(None)).all()
    return sum([r[0] for r in result if r[0] is not None])