from sqlalchemy.orm import Session
from app.models.conversion import Conversion
from app.schemas.conversion import ConversionCreate, ConversionUpdate


def get_conversion(db: Session, conversion_id: int):
    return db.query(Conversion).filter(Conversion.id == conversion_id).first()


def get_conversions_by_prospect(db: Session, prospect_id: int, skip: int = 0, limit: int = 100):
    return db.query(Conversion).filter(Conversion.prospect_id == prospect_id).offset(skip).limit(limit).all()


def create_conversion(db: Session, conversion: ConversionCreate):
    db_conversion = Conversion(**conversion.dict())
    db.add(db_conversion)
    db.commit()
    db.refresh(db_conversion)
    return db_conversion


def update_conversion(db: Session, conversion_id: int, conversion: ConversionUpdate):
    db_conversion = db.query(Conversion).filter(Conversion.id == conversion_id).first()
    if db_conversion:
        update_data = conversion.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_conversion, key, value)
        db.commit()
        db.refresh(db_conversion)
    return db_conversion


def delete_conversion(db: Session, conversion_id: int):
    db_conversion = db.query(Conversion).filter(Conversion.id == conversion_id).first()
    if db_conversion:
        db.delete(db_conversion)
        db.commit()
    return db_conversion