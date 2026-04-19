import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent.parent / "logs" / "health_report.jsonl"


def save_health_report(raw_data, analysis):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "db_name": raw_data["db_name"],
        "raw": raw_data,
        "analysis": analysis
    }

    # Ensure folder exists
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(record, default=str) + "\n")