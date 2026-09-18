from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, payload: UserCreate) -> User:
    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=get_password_hash(payload.password),
        role=payload.role.value if hasattr(payload.role, "value") else payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, email: str, password: str) -> User | None:
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    user = get_user_by_email(db, email)
    logger.debug(f"User found: {user}")
    if not user:
        logger.debug("No user found")
        return None
    logger.debug(f"User active: {user.is_active}")
    if not user.is_active:
        logger.debug("User not active")
        return None
    logger.debug(f"Verifying password for: {email}")
    logger.debug(f"Password hash starts with: {user.password_hash[:30]}")
    result = verify_password(password, user.password_hash)
    logger.debug(f"Verify password result: {result}")
    if not result:
        return None
    return user


def issue_token(user: User) -> dict:
    token = create_access_token(user.email, timedelta(minutes=60))
    return {"access_token": token, "token_type": "bearer"}
