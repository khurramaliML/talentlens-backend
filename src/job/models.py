from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database.core import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    company_title = Column(String)
    job_title = Column(String)
    job_description = Column(String)
    education = Column(String, nullable=True)
    experience = Column(Float, nullable=True)
    skills = Column(String, nullable=False)
    location = Column(String)
    salary = Column(Float, nullable=True)
    job_type = Column(String)
    application_deadline = Column(String, nullable=True)
    contact_email = Column(String)
    is_active = Column(Boolean)
    recruiter_id = Column(Integer, ForeignKey("users.id"))
    recruiter = relationship("Recruiter", back_populates="jobs")