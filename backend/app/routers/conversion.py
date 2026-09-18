from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.services import conversion_service
from app.schemas.conversion import ConversionCreate, ConversionUpdate, Conversion
from app.schemas.user import User
from app.core.database import get_db
from app.core.security import get_current_active_user


router = APIRouter(
    prefix="/conversions",
    tags=["conversions"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Conversion)
def create_conversion(conversion: ConversionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return conversion_service.create_conversion(db=db, conversion=conversion)


@router.get("/{conversion_id}", response_model=Conversion)
def read_conversion(conversion_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_conversion = conversion_service.get_conversion(db, conversion_id=conversion_id)
    if db_conversion is None:
        raise HTTPException(status_code=404, detail="Conversion not found")
    return db_conversion


@router.get("/by_prospect/{prospect_id}", response_model=List[Conversion])
def read_conversions_by_prospect(prospect_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100, current_user: User = Depends(get_current_active_user)):
    conversions = conversion_service.get_conversions_by_prospect(db, prospect_id=prospect_id, skip=skip, limit=limit)
    return conversions


@router.put("/{conversion_id}", response_model=Conversion)
def update_conversion(conversion_id: int, conversion: ConversionUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_conversion = conversion_service.update_conversion(db, conversion_id=conversion_id, conversion=conversion)
    if db_conversion is None:
        raise HTTPException(status_code=404, detail="Conversion not found")
    return db_conversion


@router.delete("/{conversion_id}", response_model=Conversion)
def delete_conversion(conversion_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_conversion = conversion_service.delete_conversion(db, conversion_id=conversion_id)
    if db_conversion is None:
        raise HTTPException(status_code=404, detail="Conversion not found")
    return db_conversion