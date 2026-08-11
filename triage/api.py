from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .service import TriageService


app = FastAPI(title="Security Alert Triage API", version="0.1.0")
service = TriageService()


class AlertRequest(BaseModel):
    alert_id: str
    title: str
    description: str
    source: str = "unknown"


class FeedbackRequest(BaseModel):
    alert_id: str
    model_version: str
    predicted_severity: str
    analyst_decision: str
    corrected_severity: str | None = None
    analyst_note: str = Field(default="", max_length=2000)


@app.get("/health")
def health() -> dict:
    return {"status": "healthy", "model_version": service.model.version}


@app.post("/v1/triage")
def triage(request: AlertRequest) -> dict:
    try:
        return service.triage(request.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/v1/feedback")
def feedback(request: FeedbackRequest) -> dict:
    try:
        return service.save_feedback(request.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/v1/feedback/metrics")
def feedback_metrics() -> dict:
    return service.feedback.metrics()

