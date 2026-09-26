from fastapi import FastAPI

app = FastAPI(
    title="CloudOps AI",
    description=(
        "Enterprise Multi-Modal Agentic AI & "
        "Cloud Intelligence Platform"
    ),
    version="0.1.0",
)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "cloudops-ai",
        "version": "0.1.0",
    }


@app.get("/")
def root():
    return {
        "name": "CloudOps AI",
        "description": "Enterprise Agentic AI Platform",
        "status": "running",
    }
