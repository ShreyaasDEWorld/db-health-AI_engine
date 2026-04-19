# DB Health Engine

A multi-database monitoring tool with:
- Health scoring
- Issue detection
- JSON logging
- AI-ready data pipeline

## Overview
Agent-based system to monitor database health, detect anomalies, and generate AI-driven recommendations.

## Features
- Multi-database support (PostgreSQL)
- Health metrics collection
- Trend analysis
- Anomaly detection
- AI-based recommendations
- 
## Architecture
collector → logs → trend_analysis → AI engine → reports


## Run

```bash
python collector/db_metrics.py
python analytics/history_analyzer.py
python analytics/trend_analysis.py
python ai_engine/ai_trend_engine.py
