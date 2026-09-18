from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.services import ai_evaluation_service
from app.schemas.ai_evaluation import AIEvaluationCreate, AIEvaluationUpdate, AIEvaluation
from app.schemas.user import User
from app.core.database import get_db
from app.core.security import get_current_active_user


router = APIRouter(
    prefix="/ai_evaluations",
    tags=["ai_evaluations"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=AIEvaluation)
def create_ai_evaluation(evaluation: AIEvaluationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return ai_evaluation_service.create_ai_evaluation(db=db, evaluation=evaluation)


@router.get("/{evaluation_id}", response_model=AIEvaluation)
def read_ai_evaluation(evaluation_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_evaluation = ai_evaluation_service.get_ai_evaluation(db, evaluation_id=evaluation_id)
    if db_evaluation is None:
        raise HTTPException(status_code=404, detail="AI evaluation not found")
    return db_evaluation


@router.get("/by_prospect/{prospect_id}", response_model=List[AIEvaluation])
def read_ai_evaluations_by_prospect(prospect_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100, current_user: User = Depends(get_current_active_user)):
    evaluations = ai_evaluation_service.get_ai_evaluations_by_prospect(db, prospect_id=prospect_id, skip=skip, limit=limit)
    return evaluations


@router.put("/{evaluation_id}", response_model=AIEvaluation)
def update_ai_evaluation(evaluation_id: int, evaluation: AIEvaluationUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_evaluation = ai_evaluation_service.update_ai_evaluation(db, evaluation_id=evaluation_id, evaluation=evaluation)
    if db_evaluation is None:
        raise HTTPException(status_code=404, detail="AI evaluation not found")
    return db_evaluation


@router.delete("/{evaluation_id}", response_model=AIEvaluation)
def delete_ai_evaluation(evaluation_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_evaluation = ai_evaluation_service.delete_ai_evaluation(db, evaluation_id=evaluation_id)
    if db_evaluation is None:
        raise HTTPException(status_code=404, detail="AI evaluation not found")
    return db_evaluation