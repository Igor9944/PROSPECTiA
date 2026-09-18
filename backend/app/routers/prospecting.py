from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.company import Company
from app.models.prospect import Prospect
from app.models.user import User
from app.schemas.company import CompanyCreate
from app.schemas.prospect import ProspectCreate, ProspectOut
from app.schemas.prospecting import ProspectingResult, ProspectingSearch
from app.services.crm import company_service, prospect_service
from app.services.prospecting import search_demo_companies

router = APIRouter()


@router.post("/search", response_model=list[ProspectingResult])
def search(payload: ProspectingSearch, _: User = Depends(get_current_user)):
    return search_demo_companies(payload)


@router.post("/import", response_model=ProspectOut, status_code=201)
def import_company(payload: CompanyCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = db.query(Company).filter(Company.name == payload.name).first()
    company = existing or company_service.create(db, payload)
    prospect = prospect_service.create(
        db,
        ProspectCreate(company_id=company.id, assigned_to=current_user.id, notes="Ajouté depuis la prospection."),
    )
    return prospect
