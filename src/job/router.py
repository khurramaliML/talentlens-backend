from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from database.core import get_db
from job.models import Job
from job.schemas import JobSchema
import os

router = APIRouter(
    prefix="/job",
    tags=["job"],
)

@router.post("/", response_model=JobSchema)
def create_job(job: JobSchema, db: Session = Depends(get_db)):
    db_job = Job(
        company_title=job.company_title,
        job_title=job.job_title,
        job_description=job.job_description,
        education=job.education,
        experience=job.experience,
        skills=job.skills,
        location=job.location,
        salary=job.salary,
        job_type=job.job_type,
        application_deadline=job.application_deadline,
        contact_email=job.contact_email,
        is_active=job.is_active,
        recruiter_id=job.recruiter_id
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/{job_id}", response_model=JobSchema)
def get_job(job_id: int, db: Session = Depends(get_db)):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

@router.put("/{job_id}", response_model=JobSchema)
def update_job(job_id: int, job: JobSchema, db: Session = Depends(get_db)):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    for key, value in job.model_dump().items():
        setattr(db_job, key, value)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(db_job)
    db.commit()
    return {"detail": "Job deleted successfully"}
