import os

os.system("python collector/db_metrics.py")
os.system("python analytics/trend_analysis.py")
os.system("python ai_engine/ai_trend_engine.py")