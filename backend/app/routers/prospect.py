from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.services import prospect_service, ai_service
from app.schemas.prospect import ProspectCreate, ProspectUpdate, Prospect
from app.schemas.ai_evaluation import AIEvaluation
from app.schemas.user import User
from app.core.database import get_db
from app.core.security import get_current_active_user


router = APIRouter(
    prefix="/prospects",
    tags=["prospects"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Prospect)
def create_prospect(prospect: ProspectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return prospect_service.create_prospect(db=db, prospect=prospect)


@router.get("/{prospect_id}", response_model=Prospect)
def read_prospect(prospect_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_prospect = prospect_service.get_prospect(db, prospect_id=prospect_id)
    if db_prospect is None:
        raise HTTPException(status_code=404, detail="Prospect not found")
    return db_prospect


@router.get("/", response_model=List[Prospect])
def read_prospects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    prospects = prospect_service.get_prospects(db, skip=skip, limit=limit)
    return prospects


@router.put("/{prospect_id}", response_model=Prospect)
def update_prospect(prospect_id: int, prospect: ProspectUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_prospect = prospect_service.update_prospect(db, prospect_id=prospect_id, prospect=prospect)
    if db_prospect is None:
        raise HTTPException(status_code=404, detail="Prospect not found")
    return db_prospect


@router.delete("/{prospect_id}", response_model=Prospect)
def delete_prospect(prospect_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_prospect = prospect_service.delete_prospect(db, prospect_id=prospect_id)
    if db_prospect is None:
        raise HTTPException(status_code=404, detail="Prospect not found")
    return db_prospect


@router.post("/{prospect_id}/ai-evaluation", response_model=AIEvaluation)
def create_ai_evaluation_for_prospect(
    prospect_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Generate AI evaluation (or fallback)
    ai_evaluation_data = ai_service.evaluate_prospect(db, prospect_id)
    # Save to database
    return ai_evaluation_service.create_ai_evaluation(db=db, evaluation=ai_evaluation_data)