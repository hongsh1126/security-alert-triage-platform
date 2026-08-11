from __future__ import annotations

from .feedback import FeedbackStore
from .model import load_model
from .schemas import Alert


class TriageService:
    def __init__(self, feedback_path: str = "data/feedback.db") -> None:
        self.model = load_model()
        self.feedback = FeedbackStore(feedback_path)

    def triage(self, payload: dict) -> dict:
        return self.model.predict(Alert.from_dict(payload)).to_dict()

    def save_feedback(self, payload: dict) -> dict:
        return {"feedback_id": self.feedback.add(payload), "status": "recorded"}

