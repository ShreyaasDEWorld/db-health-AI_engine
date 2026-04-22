# DB Health Engine

A multi-database monitoring tool with:
- Health scoring
- Issue detection
- JSON logging
- AI-ready data pipeline

<<<<<<< HEAD
## Overview
Agent-based system to monitor database health, detect anomalies, and generate AI-driven recommendations.

## 🏗️ Architecture Diagram

```text
=======
>>>>>>> 4d0bc82 (Added AI trend analysis, anomaly detection, and JSON-based metrics pipeline and Orchestration Agent)
                ┌────────────────────┐
                │  DB Systems        │
                │ (PostgreSQL etc.)  │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │  Collector Layer   │
                │ db_metrics.py      │
                │ (collect metrics)  │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │  Logs (JSONL)      │
                │ health_*.jsonl     │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Trend Analysis     │
                │ trend_analysis.py  │
                │ - aggregation      │
                │ - anomaly detect   │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Metrics Summary    │
                │ metrics_*.json     │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ AI Engine          │
                │ ai_trend_engine.py │
                │ (LLM reasoning)    │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Reports            │
                │ ai_trend_*.txt     │
                │ report_*.txt       │
                └────────────────────┘
<<<<<<< HEAD
```

## Features
- Multi-database support (PostgreSQL)
- Health metrics collection
- Trend analysis
- Anomaly detection
- AI-based recommendations
- 
## Architecture
collector → logs → trend_analysis → AI engine → reports

## Agentic Flow

- Collector Agent → gathers DB metrics  
- Analyzer Agent → aggregates & detects anomalies  
- AI Agent → performs root cause analysis  
- Report Agent → generates human-readable output
- 
=======


                

>>>>>>> 4d0bc82 (Added AI trend analysis, anomaly detection, and JSON-based metrics pipeline and Orchestration Agent)
## Run

```bash
python collector/db_metrics.py
python analytics/history_analyzer.py
python analytics/trend_analysis.py
python ai_engine/ai_trend_engine.py
