from dataclasses import asdict, dataclass
from typing import Any


VALID_SEVERITIES = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}


@dataclass(frozen=True)
class Alert:
    alert_id: str
    title: str
    description: str
    source: str = "unknown"

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Alert":
        missing = [k for k in ("alert_id", "title", "description") if not value.get(k)]
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")
        return cls(**{k: value[k] for k in ("alert_id", "title", "description", "source") if k in value})


@dataclass(frozen=True)
class Prediction:
    alert_id: str
    severity: str
    category: str
    confidence: float
    recommendation: str
    model_version: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

