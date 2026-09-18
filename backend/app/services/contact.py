from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate

def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()

def get_contacts_by_prospect(db: Session, prospect_id: int, skip: int = 0, limit: int = 100):
    return db.query(Contact).filter(Contact.prospect_id == prospect_id).offset(skip).limit(limit).all()

def create_contact(db: Session, contact: ContactCreate):
    db_contact = Contact(
        prospect_id=contact.prospect_id,
        first_name=contact.first_name,
        last_name=contact.last_name,
        job_title=contact.job_title,
        email=contact.email,
        phone=contact.phone,
        linkedin_url=str(contact.linkedin_url) if contact.linkedin_url else None
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, contact_id: int, contact_update: ContactUpdate):
    db_contact = get_contact(db, contact_id)
    if db_contact:
        update_data = contact_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == "linkedin_url" and value is not None:
                value = str(value)
            setattr(db_contact, field, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    db_contact = get_contact(db, contact_id)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact