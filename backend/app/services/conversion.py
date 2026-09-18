from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.conversion import Conversion
from app.schemas.conversion import ConversionCreate, ConversionUpdate

def get_conversion(db: Session, conversion_id: int):
    return db.query(Conversion).filter(Conversion.id == conversion_id).first()

def get_conversions_by_prospect(db: Session, prospect_id: int):
    return db.query(Conversion).filter(Conversion.prospect_id == prospect_id).all()

def get_conversions_by_user(db: Session, user_id: int):
    return db.query(Conversion).filter(Conversion.converted_by == user_id).all()

def create_conversion(db: Session, conversion: ConversionCreate):
    db_conversion = Conversion(
        prospect_id=conversion.prospect_id,
        converted_by=conversion.converted_by,
        department=conversion.department,
        value=conversion.value,
        notes=conversion.notes
    )
    db.add(db_conversion)
    db.commit()
    db.refresh(db_conversion)
    return db_conversion

def update_conversion(db: Session, conversion_id: int, conversion_update: ConversionUpdate):
    db_conversion = get_conversion(db, conversion_id)
    if db_conversion:
        update_data = conversion_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_conversion, field, value)
        db.commit()
        db.refresh(db_conversion)
    return db_conversion

def delete_conversion(db: Session, conversion_id: int):
    db_conversion = get_conversion(db, conversion_id)
    if db_conversion:
        db.delete(db_conversion)
        db.commit()
    return db_conversion

def get_conversion_count(db: Session):
    return db.query(Conversion).count()

def get_total_converted_value(db: Session):
    result = db.query(Conversion.value).filter(Conversion.value.isnot(None)).all()
    return sum([r[0] for r in result if r[0] is not None])