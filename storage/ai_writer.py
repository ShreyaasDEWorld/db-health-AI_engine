from pathlib import Path
from datetime import datetime

# Create folder
AI_LOG_DIR = Path(__file__).resolve().parent.parent / "logs" / "ai_recommendations"
AI_LOG_DIR.mkdir(parents=True, exist_ok=True)

# One file per run
TIMESTAMP = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
AI_FILE = AI_LOG_DIR / f"ai_{TIMESTAMP}.txt"


def save_ai_recommendation(db_name, ai_output):
    with open(AI_FILE, "a") as f:
        f.write("\n==============================\n")
        f.write(f"Database : {db_name}\n")
        f.write(ai_output + "\n")