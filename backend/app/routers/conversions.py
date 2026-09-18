from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.conversion import ConversionCreate, ConversionOut
from app.services.crm import conversion_service

router = APIRouter()


@router.get("/", response_model=list[ConversionOut])
def list_conversions(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return conversion_service.list(db)


@router.post("/", response_model=ConversionOut, status_code=201)
def convert_prospect(
    payload: ConversionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return conversion_service.convert(db, payload, current_user.id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
