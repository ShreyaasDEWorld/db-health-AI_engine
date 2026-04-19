def analyze_metrics(metrics):
    issues = []
    score = 100

    data = metrics.get("data", {})

    # -----------------------------
    # 1. Connections
    # -----------------------------
    if data.get("total_connections", 0) > 100:
        issues.append("High number of connections")
        score -= 10

    if data.get("active_connections", 0) > 50:
        issues.append("Too many active connections")
        score -= 10

    # -----------------------------
    # 2. Locks
    # -----------------------------
    if data.get("waiting_locks", 0) > 0:
        issues.append("Lock contention detected")
        score -= 15

    # -----------------------------
    # 3. Deadlocks
    # -----------------------------
    if data.get("deadlocks", 0) > 0:
        issues.append("Deadlocks detected")
        score -= 20

    # -----------------------------
    # 4. Slow Queries
    # -----------------------------
    slow_q = data.get("slow_queries", 0)
    if isinstance(slow_q, int) and slow_q > 5:
        issues.append("High number of slow queries")
        score -= 15

    # -----------------------------
    # 5. Cache Hit Ratio
    # -----------------------------
    if data.get("cache_hit_ratio", 1) < 0.9:
        issues.append("Low cache hit ratio")
        score -= 10

    # -----------------------------
    # 6. Temp Files
    # -----------------------------
    if data.get("temp_files", 0) > 100:
        issues.append("High temp file usage (possible memory issue)")
        score -= 10

    # -----------------------------
    # 7. Long Running Queries
    # -----------------------------
    if data.get("long_running_queries", 0) > 0:
        issues.append("Long running queries detected")
        score -= 10

    # -----------------------------
    # 8. Index Usage
    # -----------------------------
    
    idx = data.get("index_scans") or 0
    seq = data.get("seq_scans") or 0

    if (idx + seq) > 0:
        ratio = idx / (idx + seq)
        if ratio < 0.7:
            issues.append("Low index usage (too many sequential scans)")
            score -= 10

    # -----------------------------
    # Severity
    # -----------------------------
    if score >= 90:
        severity = "HEALTHY"
    elif score >= 70:
        severity = "WARNING"
    else:
        severity = "CRITICAL"

    return {
        "db_name": metrics["db_name"],
        "score": score,
        "severity": severity,
        "issues": issues
    }