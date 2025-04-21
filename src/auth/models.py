from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from database.core import Base 

class UserBase(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

class Recruiter(UserBase):
    # __tablename__ = 'users'
    # __table_args__ = {'extend_existing': True}

    job_title = Column(String)
    company_name = Column(String)
    industry = Column(String)
    company_website = Column(String)
    company_size= Column(String)
    is_recruiter = Column(Boolean, default=False)
    jobs = relationship('Job', back_populates='recruiter', cascade="all, delete-orphan")

class Candidate(UserBase):
    # __tablename__ = 'users'
    # __table_args__ = {'extend_existing': True}

    dob = Column(String)
    gender = Column(String)
    address = Column(String)
    experience = Column(String)
    skills = Column(String,)
    linkedin = Column(String)
    portfolio = Column(String)
    resume = Column(String)
    is_candidate = Column(Boolean, default=False)