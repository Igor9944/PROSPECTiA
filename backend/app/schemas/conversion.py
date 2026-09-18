from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.enums import Department


class ConversionCreate(BaseModel):
    prospect_id: int
    department: Department
    value: Optional[float] = None
    notes: Optional[str] = None


class ConversionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    prospect_id: int
    converted_by: int
    converted_at: datetime
    department: str
    value: Optional[float] = None
    notes: Optional[str] = None
