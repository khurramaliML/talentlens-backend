from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database.core import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    recruiter_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    username = Column(String, ForeignKey("users.id"))
    resume_url = Column(String, nullable=False)
    shortlisted = Column(Boolean, default=False)
    rank = Column(Integer, default=None)