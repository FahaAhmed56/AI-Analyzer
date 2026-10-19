"""Run: uvicorn api.main:app --reload"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from src.matcher import analyze

app = FastAPI(title="Resume Match Lab API", version="1.0.0", description="Demo-only text similarity; not a hiring decision tool")

class MatchRequest(BaseModel):
    resume: str = Field(min_length=15, max_length=100_000)
    job_description: str = Field(min_length=15, max_length=100_000)

@app.get('/health')
def health():
    return {"status": "ok"}

@app.post('/analyze')
def match(payload: MatchRequest):
    try:
        return analyze(payload.resume, payload.job_description)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
