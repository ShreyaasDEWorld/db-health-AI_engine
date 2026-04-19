import sys
from pathlib import Path

# ✅ Fix import path FIRST
sys.path.append(str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
import os

# Load .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

from openai import OpenAI

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🔥 Import history analyzer functions
from analytics.history_analyzer import (
    load_all_logs,
    summarize_by_db,
    generate_ai_summary
)


def generate_ai_recommendation(record, history_summary):
    prompt = f"""
You are a senior database performance engineer.

Analyze the database health using BOTH current data and historical trends.

OUTPUT FORMAT (STRICT):
- Root Cause (max 3 bullet points)
- Recommendations (max 5 bullet points, no repetition)

DO NOT repeat points.
DO NOT duplicate numbering.

IMPORTANT:
If score is high but issue frequency is high, treat it as a hidden problem.

DATA:

Database: {record['db_name']}
Score: {record['health']['score']}
Issues: {record['issues']}

History:
{history_summary}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a senior database performance engineer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    # 🔥 Sample current record
    sample = {
        "db_name": "Ecom",
        "health": {"score": 90},
        "issues": ["Low index usage"]
    }

    # 🔥 Load real history
    records = load_all_logs()
    summary = summarize_by_db(records)
    history = generate_ai_summary(summary)

    # 🔥 Generate AI output
    result = generate_ai_recommendation(sample, history)

    print("\nAI Recommendation:\n")
    print(result)