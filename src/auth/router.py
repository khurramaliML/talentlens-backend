from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from auth.schemas import Token, UserRegister
from auth import service as auth_service
from auth.models import User
from database.core import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing = auth_service.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password_hash=auth_service.get_password_hash(user.password),
        is_recruiter=user.is_recruiter,
        is_candidate=user.is_candidate,
        phone_number=user.phone_number,
        address=user.address,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = auth_service.create_access_token(data={"sub": new_user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = auth_service.create_access_token(data={"sub": user.email})
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "is_recruiter": user.is_recruiter,
        "is_candidate": user.is_candidate,
        "phone_number": user.phone_number,
        "address": user.address,
        "access_token": token, 
        "token_type": "bearer"}