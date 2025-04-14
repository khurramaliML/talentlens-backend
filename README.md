# Install all dependencies.
- Run `pip install -r requirements.txt`

# How to run locally without postgres or docker.
- in database/core.py change the DATABASE_URL to sqlite
- run `uvicorn src.main:app --reload`
