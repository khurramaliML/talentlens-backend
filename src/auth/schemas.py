from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBaseSchema(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    hashed_password: str
    is_active: Optional[bool] = True

class RecruiterSchema(UserBaseSchema):
    job_title: str
    company_name: str
    industry: str
    company_website: str
    company_size: str
    is_recruiter: Optional[bool] = True

class CandidateSchema(UserBaseSchema):
    dob: str
    gender: str
    address: str
    experience: str
    skills: str
    linkedin: str
    portfolio: str
    resume: str
    is_candidate: Optional[bool] = True

class Token(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    is_recruiter: bool = False
    is_candidate: bool = False
    phone_number: str | None = None
    address: str | None = None
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: str | None = None