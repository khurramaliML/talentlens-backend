from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from database.core import get_db
from resume.models import Resume
from resume.schemas import ResumeSchema
from resume.utils import save_resume
import os
from resume.utils import save_resume, pdf_to_text, parse_response
from resume.screen import scan_resume

router = APIRouter(
    prefix="/resume",
    tags=["resume"],
)

@router.post("/upload/")
def upload_resume(
    recruiter_id: int,
    job_id: int,
    username: str,
    file: UploadFile,
    db: Session = Depends(get_db),
):
    # Save the file
    resume_path = save_resume(file, recruiter_id, job_id, username)
    
    # Save details in the database
    new_resume = Resume(
        recruiter_id=recruiter_id,
        job_id=job_id,
        username=username,
        resume_url=resume_path,
    )
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return {"message": "Resume uploaded successfully", "resume_id": new_resume.id}


@router.get("/scan/")
def scan_resumes(recruiter_id: int, job_id: int, db: Session = Depends(get_db)):
    resumes = db.query(Resume).filter(
        Resume.recruiter_id == recruiter_id and Resume.job_id == job_id
    ).all()
    os.getcwd()
    job_description = """AI developer needed have a BS degree related to CS field in LUMS universaity must.
    Must have 2 years of experience in Full Stack development.
    Must have experience in Python, Java, C++ and C#."""
    for resume in resumes:
        resume_path = os.path.join(
            os.getcwd(), resume.resume_url
        )
        resume_text = pdf_to_text(resume_path)
        result = scan_resume(resume_text, job_description)
        response = parse_response(result)

        resume.rank = response.get("score")
        resume.shortlisted = bool(response.get("match"))
        db.commit()
        return response


@router.get("/all")
def list_all_resumes(recruiter_id: int, job_id: int, db: Session = Depends(get_db)):
    resumes = db.query(Resume).filter(
        Resume.recruiter_id == recruiter_id and Resume.job_id == job_id
    ).all()

    return resumes


@router.get("/shortlisted/")
def list_shortlisted_resumes(recruiter_id: int, job_id: int, db: Session = Depends(get_db)):
    resumes = db.query(Resume).filter(Resume.shortlisted == True).all()

    return [
        {"id": r.id, "recruiter_id": r.recruiter_id, "job_id": r.job_id, "username": r.username, "resume_url": r.resume_url}
        for r in resumes
    ]