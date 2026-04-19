from pathlib import Path
from datetime import datetime

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

TIMESTAMP = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
REPORT_FILE = LOG_DIR / f"report_{TIMESTAMP}.txt"


def save_readable_report(raw_data, analysis):
    with open(REPORT_FILE, "a") as f:
        f.write("\n==============================\n")
        f.write(f"Database : {raw_data['db_name']}\n")
        f.write(f"Time     : {analysis.get('timestamp', '')}\n")
        f.write(f"Score    : {analysis['score']}\n")
        f.write(f"Severity : {analysis['severity']}\n")
        f.write("Issues:\n")

        if analysis["issues"]:
            for issue in analysis["issues"]:
                f.write(f" - {issue}\n")
        else:
            f.write(" - No issues detected\n")