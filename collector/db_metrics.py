import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv
#from storage.db_config import get_all_db_configs
from pathlib import Path
from analyzer.health_rules import analyze_metrics
from storage.file_writer import save_health_report
from storage.report_writer import save_readable_report
from storage.report_writer import print_readable_report


env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


# -----------------------------
# Load DB configs from .env
# -----------------------------
def load_db_configs():
    db_list_env = os.getenv("DB_LIST")

    if not db_list_env:
        raise ValueError("DB_LIST not found in .env")

    db_list = [db.strip() for db in db_list_env.split(",")]

    # Common config
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    if not all([host, port, user, password]):
        raise ValueError("Missing common DB config in .env")

    configs = []

    for db in db_list:
        config = {
            "name": db,
            "host": host,
            "port": port,
            "database": db,
            "user": user,
            "password": password,
        }
        configs.append(config)

    return configs


# -----------------------------
# Core Metrics Collector
# -----------------------------
def collect_metrics(db_config):
    metrics = {
        "db_name": db_config["name"],
        #"timestamp": datetime.utcnow().isoformat(),
        "timestamp": datetime.now().isoformat(),
        "status": "OK",
        "data": {}
    }

    try:
        
        conn = psycopg2.connect(
            host=db_config["host"],
            port=db_config["port"],
            database=db_config["database"],
            user=db_config["user"],
            password=db_config["password"]
        )
        cur = conn.cursor()

        # -----------------------------
        # 1. Connections
        # -----------------------------
        cur.execute("SELECT count(*) FROM pg_stat_activity;")
        metrics["data"]["total_connections"] = cur.fetchone()[0]

        cur.execute("""
            SELECT count(*) 
            FROM pg_stat_activity 
            WHERE state = 'active';
        """)
        metrics["data"]["active_connections"] = cur.fetchone()[0]

        # -----------------------------
        # 2. Database Size
        # -----------------------------
        cur.execute("SELECT pg_database_size(current_database());")
        metrics["data"]["db_size_bytes"] = cur.fetchone()[0]

        # -----------------------------
        # 3. Locks
        # -----------------------------
        cur.execute("""
            SELECT count(*) 
            FROM pg_locks 
            WHERE NOT granted;
        """)
        metrics["data"]["waiting_locks"] = cur.fetchone()[0]

        # -----------------------------
        # 4. Deadlocks
        # -----------------------------
        cur.execute("""
            SELECT deadlocks 
            FROM pg_stat_database 
            WHERE datname = current_database();
        """)
        metrics["data"]["deadlocks"] = cur.fetchone()[0]

        # -----------------------------
        # 5. Transactions
        # -----------------------------
        cur.execute("""
            SELECT xact_commit, xact_rollback
            FROM pg_stat_database
            WHERE datname = current_database();
        """)
        tx = cur.fetchone()
        metrics["data"]["transactions_committed"] = tx[0]
        metrics["data"]["transactions_rolled_back"] = tx[1]

        # -----------------------------
        # 6. Cache Hit Ratio
        # -----------------------------
        cur.execute("""
            SELECT 
                blks_hit, blks_read
            FROM pg_stat_database
            WHERE datname = current_database();
        """)
        blks = cur.fetchone()
        if blks[0] + blks[1] > 0:
            hit_ratio = blks[0] / (blks[0] + blks[1])
        else:
            hit_ratio = 0
        metrics["data"]["cache_hit_ratio"] = round(hit_ratio, 4)

        # -----------------------------
        # 7. Temp Files (bad sign)
        # -----------------------------
        cur.execute("""
            SELECT temp_files, temp_bytes
            FROM pg_stat_database
            WHERE datname = current_database();
        """)
        temp = cur.fetchone()
        metrics["data"]["temp_files"] = temp[0]
        metrics["data"]["temp_bytes"] = temp[1]

        # -----------------------------
        # 8. Slow Queries (requires pg_stat_statements)
        # -----------------------------
        try:
            cur.execute("""
                SELECT count(*) 
                FROM pg_stat_statements 
                WHERE mean_exec_time > 1000;
            """)
            metrics["data"]["slow_queries"] = cur.fetchone()[0]
        except:
            metrics["data"]["slow_queries"] = "pg_stat_statements not enabled"

        # -----------------------------
        # 9. Long Running Queries
        # -----------------------------
        cur.execute("""
            SELECT count(*)
            FROM pg_stat_activity
            WHERE state = 'active'
            AND now() - query_start > interval '5 minutes';
        """)
        metrics["data"]["long_running_queries"] = cur.fetchone()[0]

        # -----------------------------
        # 10. Table Stats (Top Tables by Size)
        # -----------------------------
        cur.execute("""
            SELECT relname, pg_total_relation_size(relid)
            FROM pg_catalog.pg_statio_user_tables
            ORDER BY pg_total_relation_size(relid) DESC
            LIMIT 5;
        """)
        tables = cur.fetchall()
        metrics["data"]["top_tables"] = [
            {"table": t[0], "size": t[1]} for t in tables
        ]

        # -----------------------------
        # 11. Index Usage
        # -----------------------------
        cur.execute("""
            SELECT 
                sum(idx_scan), sum(seq_scan)
            FROM pg_stat_user_tables;
        """)
        scans = cur.fetchone()
        #metrics["data"]["index_scans"] = scans[0]
        metrics["data"]["index_scans"] = scans[0] or 0
        #metrics["data"]["seq_scans"] = scans[1]
        metrics["data"]["seq_scans"] = scans[1] or 0

        # -----------------------------
        # 12. Replication Lag (if applicable)
        # -----------------------------
        try:
            cur.execute("""
                SELECT 
                    EXTRACT(EPOCH FROM now() - pg_last_xact_replay_timestamp())
            """)
            lag = cur.fetchone()[0]
            metrics["data"]["replication_lag_sec"] = lag
        except:
            metrics["data"]["replication_lag_sec"] = "N/A"

        cur.close()
        conn.close()

    except Exception as e:
        metrics["status"] = "ERROR"
        metrics["error"] = str(e)

    return metrics


# -----------------------------
# Run for all DBs
# -----------------------------
def run_collection():
    dbs = load_db_configs()
    results = []

    for db in dbs:
        #print(f"Collecting metrics for {db['name']}...")
        print(f"\n🔍 Collecting metrics for {db['name']}...")
        result = collect_metrics(db)
        results.append(result)

    return results


if __name__ == "__main__":
    data = run_collection()

    for d in data:
        print("\n==============================")
        #print(f"Database: {d['db_name']}")
        

        if d["status"] == "OK":
            analysis = analyze_metrics(d)
            print_readable_report(d, analysis)

            print(f"Score: {analysis['score']}")
            print(f"Severity: {analysis['severity']}")
            print("Issues:")

            if analysis["issues"]:
                for issue in analysis["issues"]:
                    print(f" - {issue}")
            else:
                print(" - No issues detected")

            # ✅ SAVE TO FILE for AI
            save_health_report(d, analysis)
            # Save for human readable file
            save_readable_report(d, analysis)

        else:
            print("ERROR:", d["error"])