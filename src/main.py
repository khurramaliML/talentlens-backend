from fastapi import FastAPI
from database.core import engine, Base
from api import register_routes

app = FastAPI()

@app.get("/")
def read_root():
    return {"Application": "AI Powered Interview API"}

Base.metadata.create_all(bind=engine)

register_routes(app)