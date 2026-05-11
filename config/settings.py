import os
from dotenv import load_dotenv

# Membaca file .env
load_dotenv()

# --- APP SETTINGS ---
APP_ENV = os.getenv("APP_ENV", "development")
APP_DEBUG = os.getenv("APP_DEBUG", "True").lower() in ("true", "1", "t")
APP_PORT = int(os.getenv("APP_PORT", 8000))
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")

# --- SECURITY & CORS ---
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
# Parsing string CORS yang dipisah koma menjadi list
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# --- DATABASE SETTINGS ---
# Mengambil path SQLite yang bersih (menghapus format sqlite:///)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database/sentinel_ai.db")
DB_PATH = DATABASE_URL.replace("sqlite:///", "")

# --- AI & INFERENCE SETTINGS ---
MODEL_DIR_SENTIMENT = os.getenv("MODEL_DIR_SENTIMENT", "./model/indobert_sentiment")
MODEL_DIR_TOPIC = os.getenv("MODEL_DIR_TOPIC", "./model/topic_classifier")
MODEL_DIR_EMERGENCY = os.getenv("MODEL_DIR_EMERGENCY", "./model/emergency_classifier")

MAX_SEQ_LENGTH = int(os.getenv("MAX_SEQ_LENGTH", 128))
AUTO_SCRAPE_INTERVAL = int(os.getenv("AUTO_SCRAPE_INTERVAL", 15))

SCRAPER_API_URL = os.getenv("SCRAPER_API_URL", "http://localhost:9000/posts")