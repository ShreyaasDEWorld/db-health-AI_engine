import json
from pathlib import Path
from datetime import datetime

#LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
# Create logs folder
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Timestamp (ONE place only)
TIMESTAMP = datetime.now().strftime("%d%m%Y_%H-%M-%S")


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


def aggregate_metrics(records):
    summary = {}

    for r in records:
        db = r["db_name"]
        data = r["raw"]["data"]

        if db not in summary:
            summary[db] = {
                "runs": 0,
                "total_connections": 0,
                "avg_cache_hit": 0,
                "total_seq_scans": 0,
                "total_index_scans": 0,
                "slow_queries": 0
            }

        summary[db]["runs"] += 1
        summary[db]["total_connections"] += data.get("total_connections", 0)
        summary[db]["avg_cache_hit"] += data.get("cache_hit_ratio", 0)
        summary[db]["total_seq_scans"] += int(data.get("seq_scans") or 0)
        summary[db]["total_index_scans"] += int(data.get("index_scans") or 0)
        summary[db]["slow_queries"] += data.get("slow_queries", 0)

    # finalize averages
    for db in summary:
        runs = summary[db]["runs"]
        summary[db]["avg_connections"] = summary[db]["total_connections"] / runs
        summary[db]["avg_cache_hit"] = summary[db]["avg_cache_hit"] / runs

    return summary

def build_ai_metrics_summary(summary):
    lines = []

    for db, s in summary.items():
        lines.append(f"""
Database: {db}
Avg Connections: {round(s['avg_connections'],2)}
Avg Cache Hit: {round(s['avg_cache_hit'],4)}
Total Seq Scans: {s['total_seq_scans']}
Total Index Scans: {s['total_index_scans']}
Slow Queries: {s['slow_queries']}
""")

    return "\n".join(lines)


def aggregate_metrics(records):
    summary = {}

    for r in records:
        db = r["db_name"]
        data = r["raw"]["data"]

        if db not in summary:
            summary[db] = {
                "runs": 0,
                "total_connections": 0,
                "avg_cache_hit": 0,
                "total_seq_scans": 0,
                "total_index_scans": 0,
                "slow_queries": 0
            }

        summary[db]["runs"] += 1
        summary[db]["total_connections"] += data.get("total_connections", 0)
        summary[db]["avg_cache_hit"] += data.get("cache_hit_ratio", 0)
        summary[db]["total_seq_scans"] += int(data.get("seq_scans") or 0)
        summary[db]["total_index_scans"] += int(data.get("index_scans") or 0)
        summary[db]["slow_queries"] += data.get("slow_queries", 0)

    for db in summary:
        runs = summary[db]["runs"]
        summary[db]["avg_connections"] = summary[db]["total_connections"] / runs
        summary[db]["avg_cache_hit"] = summary[db]["avg_cache_hit"] / runs

    return summary

# Files
REPORT_FILE = LOG_DIR / f"report_{TIMESTAMP}.txt"
METRICS_FILE = LOG_DIR / f"metrics_summary_{TIMESTAMP}.txt"

def save_metrics_summary(text):
    with open(METRICS_FILE, "w") as f:
        f.write(text)

def save_metrics_summary_json(summary):
    path = Path(__file__).resolve().parent.parent / "logs" / f"metrics_summary_{TIMESTAMP}.json"
    
    with open(path, "w") as f:
        json.dump(summary, f, indent=2)

if __name__ == "__main__":
    records = load_all_logs()

    summary = aggregate_metrics(records)
    text = build_ai_metrics_summary(summary)
    
    # save both
    save_metrics_summary(text)
    save_metrics_summary_json(summary)

    

    print("\n=== METRICS SUMMARY ===\n")
    print(text)