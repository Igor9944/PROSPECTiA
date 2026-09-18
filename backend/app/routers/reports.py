from datetime import date
from io import StringIO

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.services.reports import build_report, dashboard_kpis

router = APIRouter()


@router.get("/summary")
def report_summary(
    start_date: date | None = None,
    end_date: date | None = None,
    assigned_to: int | None = None,
    industry: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return build_report(
        db,
        assigned_to=assigned_to,
        industry=industry,
        status=status,
        start_date=start_date,
        end_date=end_date,
    )


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    data = dashboard_kpis(db)
    data["today_follow_ups"] = [
        {
            "id": item.id,
            "prospect_id": item.prospect_id,
            "due_date": item.due_date,
            "notes": item.notes,
            "status": item.status,
            "assigned_to": item.assigned_to,
        }
        for item in data["today_follow_ups"]
    ]
    data["priority_prospects"] = [
        {
            "id": item.id,
            "score": item.score,
            "priority": item.priority,
            "status": item.status,
            "estimated_value": item.estimated_value,
            "company": {"id": item.company.id, "name": item.company.name} if item.company else None,
        }
        for item in data["priority_prospects"]
    ]
    return data


@router.get("/export.csv")
def export_csv(
    start_date: date | None = None,
    end_date: date | None = None,
    assigned_to: int | None = None,
    industry: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    report = build_report(
        db,
        assigned_to=assigned_to,
        industry=industry,
        status=status,
        start_date=start_date,
        end_date=end_date,
    )
    buffer = StringIO()
    buffer.write("metric,value\n")
    for key in ["generated", "qualified", "contacted", "converted", "lost", "conversion_rate", "potential_value", "converted_value"]:
        buffer.write(f"{key},{report[key]}\n")
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=rapport-prospection.csv"},
    )
