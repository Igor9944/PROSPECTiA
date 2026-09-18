from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.prospect import (
    AssignUpdate,
    PriorityUpdate,
    ProspectCreate,
    ProspectListOut,
    ProspectOut,
    ProspectUpdate,
    QualificationOut,
    StatusUpdate,
)
from app.services.crm import prospect_service

router = APIRouter()


@router.get("/", response_model=ProspectListOut)
def list_prospects(
    search: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    industry: str | None = None,
    assigned_to: int | None = None,
    min_score: float | None = None,
    city: str | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort: str = "created_at",
    order: str = "desc",
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    items, total = prospect_service.list_filtered(
        db,
        search=search,
        status=status,
        priority=priority,
        industry=industry,
        assigned_to=assigned_to,
        min_score=min_score,
        city=city,
        date_from=date_from,
        date_to=date_to,
        page=page,
        page_size=page_size,
        sort=sort,
        order=order,
    )
    return {"items": items, "total": total, "page": page, "page_size": page_size}


@router.get("/pipeline", response_model=list[ProspectOut])
def pipeline(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    items, _ = prospect_service.list_filtered(db, page=1, page_size=100)
    return items


@router.get("/{prospect_id}", response_model=ProspectOut)
def get_prospect(prospect_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    prospect = prospect_service.get(db, prospect_id)
    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect introuvable")
    return prospect


@router.post("/", response_model=ProspectOut, status_code=201)
def create_prospect(payload: ProspectCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return prospect_service.create(db, payload)


@router.patch("/{prospect_id}", response_model=ProspectOut)
def update_prospect(
    prospect_id: int,
    payload: ProspectUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    prospect = prospect_service.get(db, prospect_id)
    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect introuvable")
    return prospect_service.update(db, prospect, payload)


@router.delete("/{prospect_id}")
def delete_prospect(prospect_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    prospect = prospect_service.get(db, prospect_id)
    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect introuvable")
    prospect_service.delete(db, prospect)
    return {"ok": True}


@router.patch("/{prospect_id}/status", response_model=ProspectOut)
def change_status(
    prospect_id: int,
    payload: StatusUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    prospect = prospect_service.get(db, prospect_id)
    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect introuvable")
    return prospect_service.update(db, prospect, ProspectUpdate(status=payload.status))


@router.patch("/{prospect_id}/priority", response_model=ProspectOut)
def change_priority(
    prospect_id: int,
    payload: PriorityUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    prospect = prospect_service.get(db, prospect_id)
    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect introuvable")
    return prospect_service.update(db, prospect, ProspectUpdate(priority=payload.priority))


@router.patch("/{prospect_id}/assign", response_model=ProspectOut)
def assign_prospect(
    prospect_id: int,
    payload: AssignUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    prospect = prospect_service.get(db, prospect_id)
    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect introuvable")
    return prospect_service.update(db, prospect, ProspectUpdate(assigned_to=payload.assigned_to))


@router.post("/{prospect_id}/qualify", response_model=QualificationOut)
def qualify(prospect_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    prospect = prospect_service.get(db, prospect_id)
    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect introuvable")
    return prospect_service.apply_qualification(db, prospect)
