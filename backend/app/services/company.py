from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate

def get_company(db: Session, company_id: int):
    return db.query(Company).filter(Company.id == company_id).first()

def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Company).offset(skip).limit(limit).all()

def create_company(db: Session, company: CompanyCreate):
    db_company = Company(
        name=company.name,
        industry=company.industry,
        website=str(company.website) if company.website else None,
        email=company.email,
        phone=company.phone,
        address=company.address,
        city=company.city,
        country=company.country,
        employee_count=company.employee_count,
        description=company.description,
        source=company.source
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def update_company(db: Session, company_id: int, company_update: CompanyUpdate):
    db_company = get_company(db, company_id)
    if db_company:
        update_data = company_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == "website" and value is not None:
                value = str(value)
            setattr(db_company, field, value)
        db.commit()
        db.refresh(db_company)
    return db_company

def delete_company(db: Session, company_id: int):
    db_company = get_company(db, company_id)
    if db_company:
        db.delete(db_company)
        db.commit()
    return db_company

def get_company_count(db: Session):
    return db.query(Company).count()