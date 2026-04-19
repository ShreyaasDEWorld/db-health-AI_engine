import os

os.system("python collector/db_metrics.py")
os.system("python analytics/history_analyzer.py")
os.system("python ai_engine/ai_recommender.py")