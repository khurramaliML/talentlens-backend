from fastapi import FastAPI
from auth.router import router as auth_router
from resume.router import router as resume_router

def register_routes(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(resume_router)