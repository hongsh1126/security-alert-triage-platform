import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib


def main() -> None:
    records = [json.loads(line) for line in Path("data/train.jsonl").read_text().splitlines() if line.strip()]
    x = [row["input"] for row in records]
    y = [row["output"].split("|")[0] for row in records]
    model = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
                      ("classifier", LogisticRegression(max_iter=500))])
    model.fit(x, y)
    Path("artifacts").mkdir(exist_ok=True)
    joblib.dump(model, "artifacts/baseline.joblib")
    print("Saved artifacts/baseline.joblib (demonstration baseline; not production evidence)")


if __name__ == "__main__":
    main()
