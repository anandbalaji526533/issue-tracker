
from fastapi import FastAPI

from app.database import engine, Base
from app import models
from app.routers import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Issue Tracker API",
    description="API for managing projects, issues and comments",
    version="1.0.0"
)

app.include_router(auth.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Issue Tracker API"
    }
