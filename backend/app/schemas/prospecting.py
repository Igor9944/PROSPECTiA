from pydantic import BaseModel


class ProspectingSearch(BaseModel):
    industry: str | None = None
    city: str | None = None
    country: str | None = None
    min_employees: int | None = None
    max_employees: int | None = None
    company_type: str | None = None
    keywords: str | None = None
    needs: str | None = None


class ProspectingResult(BaseModel):
    name: str
    industry: str
    city: str
    country: str
    employee_count: int
    website: str
    description: str
    potential_score: int
    company_type: str
    source: str = "demo"
