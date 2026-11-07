
from fastapi import FastAPI

app = FastAPI(
    title="Notion Project Dashboard",
    description="Project management dashboard API",
    version="1.0.0"
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
