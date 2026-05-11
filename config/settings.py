import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, "database", "sentinel.db")
MODEL_PATH = os.path.join(BASE_DIR, "model", "indobert_sentiment")