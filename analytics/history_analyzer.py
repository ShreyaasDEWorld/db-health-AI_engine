import json
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"


def load_all_logs():
    records = []

    files = sorted(LOG_DIR.glob("health_*.jsonl"))

    for file in files:
        with open(file) as f:
            for line in f:
                try:
                    records.append(json.loads(line))
                except:
                    pass

    return records


def summarize_by_db(records):
    summary = {}

    for r in records:
        db = r.get("db_name")

        # Handle old + new format
        if "health" in r:
            score = r["health"]["score"]
            issues = r.get("issues", [])
        elif "analysis" in r:
            score = r["analysis"]["score"]
            issues = r["analysis"].get("issues", [])
        else:
            continue

        if db not in summary:
            summary[db] = {
                "count": 0,
                "total_score": 0,
                "issues": 0
            }

        summary[db]["count"] += 1
        summary[db]["total_score"] += score

        if issues:
            summary[db]["issues"] += 1

    return summary

def print_summary(summary):
    print("\n===== DB HEALTH SUMMARY =====\n")

    for db, data in summary.items():
        avg_score = data["total_score"] / data["count"]
        issue_pct = (data["issues"] / data["count"]) * 100

        print(f"Database : {db}")
        print(f"Runs     : {data['count']}")
        print(f"Avg Score: {round(avg_score, 2)}")
        print(f"Issue %  : {round((data['issues']/data['count'])*100, 2)}%")
        print("-----------------------------")

def get_worst_db(summary):
    worst_db = None
    lowest_score = 101

    for db, data in summary.items():
        avg_score = data["total_score"] / data["count"]

        if avg_score < lowest_score:
            lowest_score = avg_score
            worst_db = db

    return worst_db, lowest_score

def generate_ai_summary(summary):
    lines = []

    for db, data in summary.items():
        avg_score = data["total_score"] / data["count"]
        issue_pct = (data["issues"] / data["count"]) * 100

        lines.append(
            f"{db}: Avg Score {round(avg_score,2)}, Issue Frequency {round(issue_pct,2)}%"
        )

    worst_db, score = get_worst_db(summary)

    lines.append(f"Worst performing database is {worst_db}")

    return "\n".join(lines)

if __name__ == "__main__":
    records = load_all_logs()
    summary = summarize_by_db(records)

    print_summary(summary)

    # ✅ Add this
    worst_db, score = get_worst_db(summary)

    print("\n🚨 WORST DB:")
    print(f"{worst_db} (Avg Score: {round(score, 2)})")