import os
from fastapi import UploadFile
import pdfplumber
import re
import json

def save_resume(file: UploadFile, recruiter_id: int, job_id: int, username: str) -> str:
    dir_path = f"uploads/recruiter_{recruiter_id}/job_{job_id}"
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, f"{username}_{file.filename}")
    
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    
    return file_path

def pdf_to_text(pdf_path):
  with pdfplumber.open(pdf_path) as pdf:
        for pages in pdf.pages:
            text = pages.extract_text() + "\n"
  return text.strip()

def parse_response(response: str) -> None:
    json_match = re.search(r"\{.*\}", response, re.DOTALL)
    if json_match:
        json_text = json_match.group(0)

        # Convert JSON string to Python object
        try:
            data = json.loads(json_text)
            return data
        except json.JSONDecodeError as e:
            return {"error": "Invalid JSON format", "details": str(e)}
    else:
        return {"error": "No JSON found in response"}