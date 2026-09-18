from datetime import date
from typing import Optional

from pydantic import BaseModel


class ReportFilters(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    assigned_to: Optional[int] = None
    industry: Optional[str] = None
    status: Optional[str] = None


class ReportSummary(BaseModel):
    generated: int
    qualified: int
    contacted: int
    converted: int
    lost: int
    conversion_rate: float
    potential_value: float
    converted_value: float
    by_status: dict[str, int]
    by_priority: dict[str, int]
    by_industry: dict[str, int]
    evolution: list[dict]
    monthly_conversions: list[dict]
