import tempfile
import unittest
from pathlib import Path

from triage.feedback import FeedbackStore
from triage.service import TriageService


class TriageTests(unittest.TestCase):
    def test_high_risk_alert(self):
        with tempfile.TemporaryDirectory() as tmp:
            service = TriageService(str(Path(tmp) / "feedback.db"))
            result = service.triage({"alert_id": "a1", "title": "SSH", "description": "root login after brute force"})
            self.assertEqual(result["severity"], "HIGH")
            self.assertEqual(result["category"], "credential_access")

    def test_feedback_loop_and_metrics(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = FeedbackStore(Path(tmp) / "feedback.db")
            row = {"alert_id": "a1", "model_version": "v1", "predicted_severity": "HIGH",
                   "analyst_decision": "approve", "analyst_note": "confirmed"}
            self.assertEqual(store.add(row), 1)
            self.assertEqual(store.metrics()["analyst_agreement"], 1.0)

    def test_correction_requires_label(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = FeedbackStore(Path(tmp) / "feedback.db")
            with self.assertRaises(ValueError):
                store.add({"alert_id": "a", "model_version": "v", "predicted_severity": "LOW",
                           "analyst_decision": "correct"})


if __name__ == "__main__":
    unittest.main()

