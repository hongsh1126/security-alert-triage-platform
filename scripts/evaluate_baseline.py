"""Evaluate the demonstration baseline without overstating tiny synthetic results."""
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix


def main() -> None:
    model_path = Path("artifacts/baseline.joblib")
    data_path = Path("data/generated/alerts.jsonl")
    if not model_path.exists() or not data_path.exists():
        raise SystemExit("Run `python scripts/generate_demo_data.py` and `python scripts/train_baseline.py` first")
    model = joblib.load(model_path)
    frame = pd.read_json(data_path, lines=True)
    text = frame["title"].fillna("") + " " + frame["description"].fillna("")
    predicted = model.predict(text)
    labels = sorted(frame["label"].unique())
    print("DEMO-ONLY evaluation on tiny synthetic data; do not report as benchmark performance.\n")
    print(classification_report(frame["label"], predicted, labels=labels, zero_division=0))
    print("Confusion matrix; rows=true, columns=predicted")
    print(pd.DataFrame(confusion_matrix(frame["label"], predicted, labels=labels), index=labels, columns=labels))


if __name__ == "__main__":
    main()
