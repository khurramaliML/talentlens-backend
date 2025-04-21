from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from database.core import get_db
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from auth.models import Recruiter, Candidate
from auth.schemas import Token, RecruiterSchema, CandidateSchema
from fastapi.security import OAuth2PasswordBearer
from database.core import get_db
from auth.utils import verify_password, get_password_hash, create_access_token
from jose import JWTError, jwt
from auth.utils import SECRET_KEY, ALGORITHM

router = APIRouter(
    prefix="/auth", 
    tags=["auth"]
)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/recruiter/signup", response_model=RecruiterSchema)
def register_recruiter(user: RecruiterSchema, db: Session = Depends(get_db)):
    db_user = db.query(Recruiter).filter(Recruiter.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    new_user = Recruiter(
        full_name=user.full_name,
        email=user.email,
        phone_number=user.phone_number,
        job_title=user.job_title,
        company_name=user.company_name,
        industry=user.industry,
        company_website=user.company_website,
        company_size=user.company_size,
        is_recruiter=bool(user.is_recruiter),
        hashed_password=get_password_hash(user.hashed_password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/candidate/signup", response_model=CandidateSchema)
def register_candidate(user: CandidateSchema, db: Session = Depends(get_db)):
    db_user = db.query(Candidate).filter(Candidate.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    new_user = Candidate(
        full_name=user.full_name,
        email=user.email,
        phone_number=user.phone_number,
        dob=user.dob,
        gender=user.gender,
        address=user.address,
        experience=user.experience,
        skills=user.skills,
        linkedin=user.linkedin,
        portfolio=user.portfolio,
        is_candidate=bool(user.is_candidate),
        hashed_password=get_password_hash(user.hashed_password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# @router.post("/login", response_model=Token)
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == form_data.username).first()
#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
#     token = create_access_token(data={"sub": user.email})
#     return {
#         "first_name": user.first_name,
#         "last_name": user.last_name,
#         "email": user.email,
#         "is_recruiter": user.is_recruiter,
#         "is_candidate": user.is_candidate,
#         "phone_number": user.phone_number,
#         "address": user.address,
#         "access_token": token, 
#         "token_type": "bearer"}

# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     user = db.query(User).filter(User.email == username).first()
#     if user is None:
#         raise credentials_exception
#     return user

# @router.get("/protected")
# def protected_route(current_user: User = Depends(get_current_user)):
#     return {"message": f"Hello, {current_user.email}!"}