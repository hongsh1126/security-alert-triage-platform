from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .schemas import Alert, Prediction


KEYWORDS = {
    "CRITICAL": ("ransomware", "disabled defender", "domain admin", "malware"),
    "HIGH": ("root login", "exfil", "unknown external", "brute force", "powershell"),
    "MEDIUM": ("service account", "new database", "policy", "unusual"),
}


class RuleModel:
    """Deterministic fallback that keeps the full product runnable without a GPU."""

    version = "rule-fallback-1.0"

    def predict(self, alert: Alert) -> Prediction:
        text = f"{alert.title} {alert.description}".lower()
        severity = "LOW"
        for candidate in ("CRITICAL", "HIGH", "MEDIUM"):
            if any(term in text for term in KEYWORDS[candidate]):
                severity = candidate
                break
        category = self._category(text)
        confidence = {"CRITICAL": .94, "HIGH": .86, "MEDIUM": .72, "LOW": .64}[severity]
        action = {
            "CRITICAL": "Isolate the affected asset and begin incident response immediately.",
            "HIGH": "Escalate to a security analyst and contain suspicious activity.",
            "MEDIUM": "Validate context and monitor related events.",
            "LOW": "Record and close after routine verification.",
        }[severity]
        return Prediction(alert.alert_id, severity, category, confidence, action, self.version)

    @staticmethod
    def _category(text: str) -> str:
        for term, label in (("login", "credential_access"), ("upload", "exfiltration"),
                            ("powershell", "execution"), ("dns", "network_activity")):
            if term in text:
                return label
        return "other"


def load_model() -> RuleModel:
    return RuleModel()

