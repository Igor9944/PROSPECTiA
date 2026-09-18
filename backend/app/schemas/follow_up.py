from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.enums import FollowUpStatus


class FollowUpBase(BaseModel):
    prospect_id: int
    assigned_to: int
    due_date: datetime
    reminder_date: Optional[datetime] = None
    status: FollowUpStatus = FollowUpStatus.PENDING
    notes: Optional[str] = None


class FollowUpCreate(FollowUpBase):
    pass


class FollowUpUpdate(BaseModel):
    assigned_to: Optional[int] = None
    due_date: Optional[datetime] = None
    reminder_date: Optional[datetime] = None
    status: Optional[FollowUpStatus] = None
    notes: Optional[str] = None


class FollowUpOut(FollowUpBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
