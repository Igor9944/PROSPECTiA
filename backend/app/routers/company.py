from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.services import company_service
from app.schemas.company import CompanyCreate, CompanyUpdate, Company
from app.schemas.user import User
from app.core.database import get_db
from app.core.security import get_current_active_user


router = APIRouter(
    prefix="/companies",
    tags=["companies"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Company)
def create_company(company: CompanyCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return company_service.create_company(db=db, company=company)


@router.get("/{company_id}", response_model=Company)
def read_company(company_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_company = company_service.get_company(db, company_id=company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company


@router.get("/", response_model=List[Company])
def read_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    companies = company_service.get_companies(db, skip=skip, limit=limit)
    return companies


@router.put("/{company_id}", response_model=Company)
def update_company(company_id: int, company: CompanyUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_company = company_service.update_company(db, company_id=company_id, company=company)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company


@router.delete("/{company_id}", response_model=Company)
def delete_company(company_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_company = company_service.delete_company(db, company_id=company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company