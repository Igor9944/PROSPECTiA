from sqlalchemy.orm import Session
from app.models.ai_evaluation import AIEvaluation
from app.schemas.ai_evaluation import AIEvaluationCreate, AIEvaluationUpdate


def get_ai_evaluation(db: Session, evaluation_id: int):
    return db.query(AIEvaluation).filter(AIEvaluation.id == evaluation_id).first()


def get_ai_evaluations_by_prospect(db: Session, prospect_id: int, skip: int = 0, limit: int = 100):
    return db.query(AIEvaluation).filter(AIEvaluation.prospect_id == prospect_id).offset(skip).limit(limit).all()


def create_ai_evaluation(db: Session, evaluation: AIEvaluationCreate):
    db_evaluation = AIEvaluation(**evaluation.dict())
    db.add(db_evaluation)
    db.commit()
    db.refresh(db_evaluation)
    return db_evaluation


def update_ai_evaluation(db: Session, evaluation_id: int, evaluation: AIEvaluationUpdate):
    db_evaluation = db.query(AIEvaluation).filter(AIEvaluation.id == evaluation_id).first()
    if db_evaluation:
        update_data = evaluation.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_evaluation, key, value)
        db.commit()
        db.refresh(db_evaluation)
    return db_evaluation


def delete_ai_evaluation(db: Session, evaluation_id: int):
    db_evaluation = db.query(AIEvaluation).filter(AIEvaluation.id == evaluation_id).first()
    if db_evaluation:
        db.delete(db_evaluation)
        db.commit()
    return db_evaluation