def generate_recommendations(record):
    issues = record.get("issues", [])
    metrics = record.get("metrics", {})

    recommendations = []

    for issue in issues:

        if "Low index usage" in issue:
            recommendations.append(
                "Investigate missing indexes. Check slow queries and add indexes on filter/join columns."
            )

        if "High number of connections" in issue:
            recommendations.append(
                "Consider connection pooling (PgBouncer) or review application connection handling."
            )

        if "Low cache hit ratio" in issue:
            recommendations.append(
                "Increase shared_buffers or analyze queries causing disk reads."
            )

        if "Long running queries" in issue:
            recommendations.append(
                "Identify long-running queries and optimize them using EXPLAIN ANALYZE."
            )

    if not recommendations:
        recommendations.append("Database is healthy. No action required.")

    return recommendations


if __name__ == "__main__":
    sample = {
        "db_name": "Ecom",
        "health": {"score": 90},
        "metrics": {"index_usage_ratio": 0.0},
        "issues": ["Low index usage"]
    }

    recs = generate_recommendations(sample)

    print("\nRecommendations:")
    for r in recs:
        print(f"- {r}")