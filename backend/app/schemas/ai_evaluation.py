from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AIAnalysisOut(BaseModel):
    score: float
    reasoning: str
    recommendation: str
    potential_needs: list[str]
    suggested_priority: str
    next_action: str
    outreach_message: str
    provider: str = "none"


class AIEvaluationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    prospect_id: int
    score: float
    reasoning: str
    recommendation: str
    created_at: datetime
    potential_needs: Optional[list[str]] = None
    suggested_priority: Optional[str] = None
    next_action: Optional[str] = None
    outreach_message: Optional[str] = None
    provider: Optional[str] = None
