import sys
from pathlib import Path
import json
from datetime import datetime

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

# Output file
TIMESTAMP = datetime.now().strftime("%d%m%Y_%H-%M-%S")
OUTPUT_FILE = LOG_DIR / f"ai_hc_recommendation_{TIMESTAMP}.txt"


# 🔥 Get latest JSON log file
def get_latest_log_file():
    files = sorted(LOG_DIR.glob("health_*.jsonl"))
    if not files:
        return None
    return files[-1]


# 🔥 AI call (NO history, only JSON)
def generate_ai_recommendation(record):
    prompt = f"""
You are a senior database performance engineer.

Analyze the database health and provide:

- Root Cause (max 3 bullet points)
- Recommendations (max 5 bullet points)

DATA:

Database: {record['db_name']}
Score: {record['analysis']['score']}
Severity: {record['analysis']['severity']}
Issues: {record['analysis']['issues']}

Metrics:
Connections: {record['raw']['data']['total_connections']}
Cache Hit Ratio: {record['raw']['data']['cache_hit_ratio']}
Slow Queries: {record['raw']['data']['slow_queries']}
Index Scans: {record['raw']['data']['index_scans']}
Sequential Scans: {record['raw']['data']['seq_scans']}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a database performance expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


# 🔥 Main runner
def run_ai():

    latest_file = get_latest_log_file()

    if not latest_file:
        print("❌ No JSON log file found")
        return

    print(f"Using file: {latest_file.name}")

    with open(latest_file) as f, open(OUTPUT_FILE, "w") as out:

        for line in f:
            record = json.loads(line)

            print(f"\n🔍 Running AI for {record['db_name']}...")

            ai_output = generate_ai_recommendation(record)

            # Print
            print("\nAI Recommendation:\n")
            print(ai_output)

            # Save
            out.write("\n==============================\n")
            out.write(f"Database : {record['db_name']}\n")
            out.write(ai_output + "\n")

    print(f"\n✅ Saved AI report: {OUTPUT_FILE}")


if __name__ == "__main__":
    run_ai()