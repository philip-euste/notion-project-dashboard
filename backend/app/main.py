
from fastapi import FastAPI

from app.api.projects import router as projects_router
from app.api.sync import router as sync_router


app = FastAPI(
    title="Notion Project Dashboard",
    description="Project management dashboard API",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Notion Project Dashboard API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


app.include_router(projects_router)
app.include_router(sync_router)
