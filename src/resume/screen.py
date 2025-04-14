from groq import Groq
import os

def scan_resume(resume_text: str, job_description: str) -> dict:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    # Ensure the API key is set
    if not client.api_key:
        raise ValueError("GROQ_API_KEY is not set. Please set it in your environment variables.")

    # Construct the prompt for the chat completion
    prompt = f"""
    You are an AI assistant specialized in analyzing resumes for software engineering job applications.
    Given a candidate's resume and a job description, perform a detailed analysis to extract and assess the following:

    1. Extract all *relevant technical and soft skills explicitly or implicitly mentioned in the resume.
    2. Calculate the *total years of professional experience* based on work history, internships, or significant freelance projects.
    3. Identify and categorize projects into appropriate domains such as:
    - Artificial Intelligence
    - Machine Learning
    - Natural Language Processing
    - Computer Vision
    - Generative AI
    - Data Science
    - Web Development
    - Frontend
    - Backend
    - DevOps
    - Cloud Computing
    4. From the projects, extract all technologies, frameworks, and tools used and assign them to the above domains where applicable.
    5. Analyze the *relevance of the resume to the job description* by comparing:
    - Skills match
    - Educational background
    - Years of experience
    - Project relevance
    6. Generate a match score (0 to 100) based on overall alignment with the job requirements.
    7. Scoring formula:
    - Skills match: 30%
    - Experience: 20%
    - Project relevance: 20%
    - Education: 10%
    - Soft skills: 10%
    - Overall impression: 10%
    8. Set match: true if score is ≥ 75 and there is a good match in at least 3 core areas (skills, experience, projects).

    Return the output strictly in the following valid JSON format:
    {{
        "match": <True or False>,
        "score": <score from 0 to 100>,
        "skills": [
            "skill_1",
            "skill_2",
            ...
        ],
        "total_experience": "<years of experience>",
        "technologies": [
            "technology_1",
            "technology_2",
            ...
        ],
        "projects": [
            {{
                "name": "<project_name>",
                "domain": "<one of the predefined domains>",
                "technologies": ["tech_1", "tech_2", ...]
            }},
            ...
        ],
        "comments": "<Concise summary of findings, such as key skills, strong matches, or gaps>"
    }}

    Resume:
    {resume_text}

    Job Description:
    {job_description}
    """
    # print(prompt)
    # Call the chat completion endpoint with the prompt
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    response = chat_completion.choices[0].message.content
    return response