from datetime import date, datetime

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models.company import Company
from app.models.conversion import Conversion
from app.models.enums import ProspectStatus
from app.models.prospect import Prospect


def _base_query(db: Session, assigned_to=None, industry=None, status=None, start_date=None, end_date=None):
    query = db.query(Prospect).join(Company)
    if assigned_to:
        query = query.filter(Prospect.assigned_to == assigned_to)
    if industry:
        query = query.filter(Company.industry == industry)
    if status:
        query = query.filter(Prospect.status == status)
    if start_date:
        query = query.filter(Prospect.created_at >= datetime.combine(start_date, datetime.min.time()))
    if end_date:
        query = query.filter(Prospect.created_at <= datetime.combine(end_date, datetime.max.time()))
    return query


def build_report(db: Session, **filters) -> dict:
    query = _base_query(db, **{k: v for k, v in filters.items() if k != "status" or True})
    prospects = query.all()
    generated = len(prospects)
    qualified = sum(1 for item in prospects if item.status not in {ProspectStatus.NEW.value})
    contacted = sum(
        1
        for item in prospects
        if item.status in {
            ProspectStatus.CONTACTED.value,
            ProspectStatus.FOLLOW_UP.value,
            ProspectStatus.NEGOTIATION.value,
            ProspectStatus.CONVERTED.value,
        }
    )
    converted = sum(1 for item in prospects if item.status == ProspectStatus.CONVERTED.value)
    lost = sum(1 for item in prospects if item.status == ProspectStatus.LOST.value)
    conversion_rate = round((converted / generated) * 100, 1) if generated else 0
    potential_value = sum(item.estimated_value or 0 for item in prospects)
    converted_value = sum(
        (conversion.value or 0)
        for conversion in db.query(Conversion).all()
        if any(item.id == conversion.prospect_id for item in prospects)
    )
    by_status: dict[str, int] = {}
    by_priority: dict[str, int] = {}
    by_industry: dict[str, int] = {}
    for item in prospects:
        by_status[item.status] = by_status.get(item.status, 0) + 1
        by_priority[item.priority] = by_priority.get(item.priority, 0) + 1
        industry = item.company.industry if item.company else "Autre"
        by_industry[industry] = by_industry.get(industry, 0) + 1

    evolution_rows = (
        db.query(func.strftime("%Y-%m-%d", Prospect.created_at), func.count(Prospect.id))
        .group_by(func.strftime("%Y-%m-%d", Prospect.created_at))
        .order_by(func.strftime("%Y-%m-%d", Prospect.created_at))
        .all()
    )
    monthly = (
        db.query(func.strftime("%Y-%m", Conversion.converted_at), func.count(Conversion.id), func.coalesce(func.sum(Conversion.value), 0))
        .group_by(func.strftime("%Y-%m", Conversion.converted_at))
        .order_by(func.strftime("%Y-%m", Conversion.converted_at))
        .all()
    )
    return {
        "generated": generated,
        "qualified": qualified,
        "contacted": contacted,
        "converted": converted,
        "lost": lost,
        "conversion_rate": conversion_rate,
        "potential_value": potential_value,
        "converted_value": converted_value,
        "by_status": by_status,
        "by_priority": by_priority,
        "by_industry": by_industry,
        "evolution": [{"date": row[0], "count": row[1]} for row in evolution_rows],
        "monthly_conversions": [{"month": row[0], "count": row[1], "value": row[2]} for row in monthly],
    }


def dashboard_kpis(db: Session) -> dict:
    report = build_report(db)
    today_follow_ups = []
    from app.services.crm import follow_up_service

    today_follow_ups = follow_up_service.list(db, "today")
    overdue = follow_up_service.list(db, "overdue")
    priorities = (
        db.query(Prospect)
        .options(joinedload(Prospect.company))
        .filter(Prospect.priority.in_(["HIGH", "VERY_HIGH"]))
        .order_by(Prospect.score.desc())
        .limit(8)
        .all()
    )
    return {
        **report,
        "total": report["generated"],
        "new": report["by_status"].get("NEW", 0),
        "to_follow": report["by_status"].get("FOLLOW_UP", 0) + len(overdue),
        "today_follow_ups": today_follow_ups,
        "priority_prospects": priorities,
    }
