from pydantic import BaseModel, EmailStr
from typing import Optional

class JobSchema(BaseModel):
    company_title: str
    job_title: str
    job_description: str
    education: str
    experience: float
    skills: str
    location: str
    salary: float
    job_type: str
    application_deadline: str
    contact_email: EmailStr
    is_active: Optional[bool] = True
    recruiter_id: Optional[int] = None