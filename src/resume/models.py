from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database.core import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    recruiter_id = Column(Integer, index=True)
    job_id = Column(Integer, index=True)
    username = Column(String, index=True)
    resume_url = Column(String, nullable=False)
    shortlisted = Column(Boolean, default=False)
    rank = Column(Integer, default=0)