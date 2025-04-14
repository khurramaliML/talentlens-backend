from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    is_recruiter: bool = False
    is_candidate: bool = False
    phone_number: str | None = None
    address: str | None = None

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