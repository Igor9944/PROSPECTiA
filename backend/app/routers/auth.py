from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserOut
from app.services.auth import authenticate, create_user, get_user_by_email, issue_token

router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    return create_user(db, payload)


@router.post("/login", response_model=Token)
async def login(request: Request, db: Session = Depends(get_db)):
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    content_type = request.headers.get("content-type", "")
    logger.debug(f"Content-Type: {content_type}")
    
    if "application/json" in content_type:
        body = await request.json()
        logger.debug(f"JSON body: {body}")
        email = body.get("email") or body.get("username")
        password = body.get("password")
    else:
        form = await request.form()
        logger.debug(f"Form data: {dict(form)}")
        email = form.get("username") or form.get("email")
        password = form.get("password")
    
    logger.debug(f"Parsed email: {email}")
    logger.debug(f"Parsed password: {'***' if password else None}")
    
    if not email or not password:
        raise HTTPException(status_code=422, detail="Email et mot de passe requis")
    user = authenticate(db, email, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou mot de passe incorrect")
    return issue_token(user)


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    return {"message": "Déconnexion réussie"}
