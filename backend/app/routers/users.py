from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user, require_roles
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services.auth import get_user_by_email
from app.services.crm import user_service

router = APIRouter()


@router.get("/directory", response_model=list[UserOut])
def directory(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return user_service.list(db)


@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.ADMIN))):
    return user_service.list(db)


@router.post("/", response_model=UserOut, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.ADMIN))):
    if get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    return user_service.create(db, payload)


@router.patch("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMIN)),
):
    user = user_service.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return user_service.update(db, user, payload)
