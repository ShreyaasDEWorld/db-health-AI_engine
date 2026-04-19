import json
from datetime import datetime
from pathlib import Path


# Create logs folder
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Timestamp for file
TIMESTAMP = datetime.now().strftime("%d%m%Y_%H-%M-%S")
LOG_FILE = LOG_DIR / f"health_{TIMESTAMP}.jsonl"




def save_health_report(raw_data, analysis):

    


    record = {
        "timestamp": datetime.now().strftime("%d%m%Y_%H:%M:%S"),
        "db_name": raw_data["db_name"],
        "raw": raw_data,
        "analysis": analysis
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(record, default=str) + "\n")