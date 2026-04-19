import sys
from pathlib import Path
from datetime import datetime
import json

# Fix path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
import os
from openai import OpenAI

# Load env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Paths
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"

TIMESTAMP = datetime.now().strftime("%d%m%Y_%H-%M-%S")
OUTPUT_FILE = LOG_DIR / f"ai_trend_{TIMESTAMP}.txt"


# ✅ Get latest JSON metrics file
def get_latest_metrics_file():
    files = sorted(LOG_DIR.glob("metrics_summary_*.json"))
    return files[-1] if files else None


def run_ai_trend():

    summary_file = get_latest_metrics_file()

    if not summary_file:
        print("❌ No metrics_summary JSON file found. Run trend_analysis first.")
        return

    print(f"Using file: {summary_file.name}")

    # ✅ Load JSON
    with open(summary_file) as f:
        metrics_data = json.load(f)

    # Convert JSON → readable string for AI
    formatted_data = json.dumps(metrics_data, indent=2)

    prompt = f"""
You are a database performance expert.

Analyze the following aggregated database metrics and provide:

- Key Observations
- Root Causes
- Recommendations

Focus on trends and inefficiencies.

DATA:
{formatted_data}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a senior database performance engineer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    result = response.choices[0].message.content

    print("\n=== AI TREND ANALYSIS ===\n")
    print(result)

    with open(OUTPUT_FILE, "w") as f:
        f.write(result)

    print(f"\n✅ Saved AI trend report: {OUTPUT_FILE}")


if __name__ == "__main__":
    run_ai_trend()