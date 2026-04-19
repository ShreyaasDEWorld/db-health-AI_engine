from pathlib import Path
from datetime import datetime

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

#TIMESTAMP = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
TIMESTAMP = datetime.now().strftime("%d%m%Y_%H-%M-%S")
REPORT_FILE = LOG_DIR / f"report_{TIMESTAMP}.txt"

def save_readable_report(raw_data, analysis):
    data = raw_data.get("data", {})

    with open(REPORT_FILE, "a") as f:
        f.write("\n==============================\n")
        f.write(f"Database : {raw_data['db_name']}\n")
        f.write(f"Time     : {raw_data.get('timestamp', '')}\n")

        # 🔹 Health Summary
        f.write("\n--- Health Summary ---\n")
        f.write(f"Score    : {analysis['score']}\n")
        f.write(f"Severity : {analysis['severity']}\n")

        # 🔹 Issues
        f.write("\n--- Issues ---\n")
        if analysis["issues"]:
            for issue in analysis["issues"]:
                f.write(f" - {issue}\n")
        else:
            f.write(" - No issues detected\n")

        # 🔹 Metrics
        f.write("\n--- Metrics ---\n")
        f.write(f"Total Connections     : {data.get('total_connections')}\n")
        f.write(f"Active Connections    : {data.get('active_connections')}\n")
        f.write(f"DB Size (bytes)       : {data.get('db_size_bytes')}\n")
        f.write(f"Cache Hit Ratio       : {data.get('cache_hit_ratio')}\n")
        f.write(f"Temp Files            : {data.get('temp_files')}\n")
        f.write(f"Temp Bytes            : {data.get('temp_bytes')}\n")
        f.write(f"Slow Queries          : {data.get('slow_queries')}\n")
        f.write(f"Long Running Queries  : {data.get('long_running_queries')}\n")
        f.write(f"Deadlocks             : {data.get('deadlocks')}\n")
        f.write(f"Waiting Locks         : {data.get('waiting_locks')}\n")

        # 🔹 Scan Info
        f.write("\n--- Scan Statistics ---\n")
        f.write(f"Index Scans           : {data.get('index_scans')}\n")
        f.write(f"Sequential Scans      : {data.get('seq_scans')}\n")

        # 🔹 Transactions
        f.write("\n--- Transactions ---\n")
        f.write(f"Committed             : {data.get('transactions_committed')}\n")
        f.write(f"Rolled Back           : {data.get('transactions_rolled_back')}\n")

        # 🔹 Top Tables
        f.write("\n--- Top Tables ---\n")
        top_tables = data.get("top_tables", [])
        if top_tables:
            for t in top_tables:
                f.write(f" - {t['table']} ({t['size']} bytes)\n")
        else:
            f.write(" - No table data\n")

        f.write("\n==============================\n")

def print_readable_report(raw_data, analysis):
    data = raw_data.get("data", {})

    print("\n==============================")
    print(f"Database : {raw_data['db_name']}")
    print(f"Time     : {raw_data.get('timestamp', '')}")

    print("\n--- Health Summary ---")
    print(f"Score    : {analysis['score']}")
    print(f"Severity : {analysis['severity']}")

    print("\n--- Issues ---")
    if analysis["issues"]:
        for issue in analysis["issues"]:
            print(f" - {issue}")
    else:
        print(" - No issues detected")

    print("\n--- Metrics ---")
    print(f"Total Connections     : {data.get('total_connections')}")
    print(f"Active Connections    : {data.get('active_connections')}")
    print(f"Cache Hit Ratio       : {data.get('cache_hit_ratio')}")
    print(f"Slow Queries          : {data.get('slow_queries')}")

    print("\n--- Scan Statistics ---")
    print(f"Index Scans           : {data.get('index_scans')}")
    print(f"Sequential Scans      : {data.get('seq_scans')}")

    print("==============================")