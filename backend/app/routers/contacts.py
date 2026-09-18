from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.contact import ContactCreate, ContactOut, ContactUpdate
from app.services.crm import contact_service, prospect_service

router = APIRouter()


@router.get("/", response_model=list[ContactOut])
def list_contacts(prospect_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    if not prospect_service.get(db, prospect_id):
        raise HTTPException(status_code=404, detail="Prospect introuvable")
    return contact_service.list_for_prospect(db, prospect_id)


@router.post("/", response_model=ContactOut, status_code=201)
def create_contact(payload: ContactCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return contact_service.create(db, payload)


@router.patch("/{contact_id}", response_model=ContactOut)
def update_contact(
    contact_id: int,
    payload: ContactUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    contact = contact_service.get(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact introuvable")
    return contact_service.update(db, contact, payload)


@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    contact = contact_service.get(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact introuvable")
    contact_service.delete(db, contact)
    return {"ok": True}
