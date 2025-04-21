from pydantic import BaseModel
from typing import Optional

class ResumeSchema(BaseModel):
    id: int
    recruiter_id: int
    job_id: int
    username: str
    resume_url: str
    shortlisted: Optional[bool] = False
    rank: Optional[int] = None
