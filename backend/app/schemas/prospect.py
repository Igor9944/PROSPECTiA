from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import ProspectPriority, ProspectStatus
from app.schemas.company import CompanyOut
from app.schemas.user import UserOut


class ProspectBase(BaseModel):
    company_id: int
    assigned_to: Optional[int] = None
    score: float = Field(default=0, ge=0, le=100)
    priority: ProspectPriority = ProspectPriority.MEDIUM
    status: ProspectStatus = ProspectStatus.NEW
    notes: Optional[str] = None
    estimated_value: Optional[float] = None


class ProspectCreate(ProspectBase):
    pass


class ProspectUpdate(BaseModel):
    assigned_to: Optional[int] = None
    score: Optional[float] = Field(default=None, ge=0, le=100)
    priority: Optional[ProspectPriority] = None
    status: Optional[ProspectStatus] = None
    notes: Optional[str] = None
    estimated_value: Optional[float] = None


class StatusUpdate(BaseModel):
    status: ProspectStatus


class PriorityUpdate(BaseModel):
    priority: ProspectPriority


class AssignUpdate(BaseModel):
    assigned_to: int


class QualificationCriterion(BaseModel):
    label: str
    points: int
    explanation: str


class QualificationOut(BaseModel):
    score: int
    level: str
    priority: ProspectPriority
    criteria: list[QualificationCriterion]
    summary: str


class ProspectOut(ProspectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    company: Optional[CompanyOut] = None
    assigned_user: Optional[UserOut] = None


class ProspectListOut(BaseModel):
    items: list[ProspectOut]
    total: int
    page: int
    page_size: int
