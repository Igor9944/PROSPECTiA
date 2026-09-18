from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.company import CompanyCreate, CompanyOut, CompanyUpdate
from app.services.crm import company_service

router = APIRouter()


@router.get("/", response_model=list[CompanyOut])
def list_companies(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return company_service.list(db)


@router.get("/{company_id}", response_model=CompanyOut)
def get_company(company_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    company = company_service.get(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Entreprise introuvable")
    return company


@router.post("/", response_model=CompanyOut, status_code=201)
def create_company(payload: CompanyCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return company_service.create(db, payload)


@router.patch("/{company_id}", response_model=CompanyOut)
def update_company(
    company_id: int,
    payload: CompanyUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    company = company_service.get(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Entreprise introuvable")
    return company_service.update(db, company, payload)


@router.delete("/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    company = company_service.get(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Entreprise introuvable")
    company_service.delete(db, company)
    return {"ok": True}
