from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


SCHEMA = """
CREATE TABLE IF NOT EXISTS feedback (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 alert_id TEXT NOT NULL,
 model_version TEXT NOT NULL,
 predicted_severity TEXT NOT NULL,
 analyst_decision TEXT NOT NULL CHECK(analyst_decision IN ('approve','reject','correct')),
 corrected_severity TEXT,
 analyst_note TEXT NOT NULL DEFAULT '',
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
)
"""


class FeedbackStore:
    def __init__(self, path: str | Path = "data/feedback.db") -> None:
        self.path = str(path)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.execute(SCHEMA)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def add(self, item: dict[str, Any]) -> int:
        if item.get("analyst_decision") not in {"approve", "reject", "correct"}:
            raise ValueError("analyst_decision must be approve, reject, or correct")
        if item["analyst_decision"] == "correct" and not item.get("corrected_severity"):
            raise ValueError("corrected_severity is required for correct decisions")
        values = (item["alert_id"], item["model_version"], item["predicted_severity"],
                  item["analyst_decision"], item.get("corrected_severity"), item.get("analyst_note", ""))
        with self._connect() as conn:
            cur = conn.execute("""INSERT INTO feedback
              (alert_id, model_version, predicted_severity, analyst_decision, corrected_severity, analyst_note)
              VALUES (?, ?, ?, ?, ?, ?)""", values)
            return int(cur.lastrowid)

    def recent(self, limit: int = 100) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM feedback ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [dict(row) for row in rows]

    def metrics(self) -> dict[str, Any]:
        with self._connect() as conn:
            total = conn.execute("SELECT COUNT(*) FROM feedback").fetchone()[0]
            approved = conn.execute("SELECT COUNT(*) FROM feedback WHERE analyst_decision='approve'").fetchone()[0]
            corrected = conn.execute("SELECT COUNT(*) FROM feedback WHERE analyst_decision='correct'").fetchone()[0]
        return {"total_reviews": total, "approved": approved, "corrected": corrected,
                "analyst_agreement": round(approved / total, 4) if total else None}

