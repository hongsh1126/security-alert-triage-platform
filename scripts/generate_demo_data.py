import json
from pathlib import Path


def main() -> None:
    source = Path("data/train.jsonl")
    target = Path("data/generated/alerts.jsonl")
    target.parent.mkdir(parents=True, exist_ok=True)
    records = []
    lines = [line for line in source.read_text(encoding="utf-8").splitlines() if line.strip()]
    for index, line in enumerate(lines, 1):
        item = json.loads(line)
        records.append({"alert_id": f"demo-{index:03d}", "title": item["instruction"],
                        "description": item["input"], "label": item["output"].split("|")[0]})
    target.write_text("\n".join(json.dumps(x) for x in records) + "\n", encoding="utf-8")
    print(f"Wrote {len(records)} alerts to {target}")


if __name__ == "__main__":
    main()
