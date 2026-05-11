import sqlite3
import hashlib

DB_NAME = "sentinel_ai.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def generate_text_hash(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            external_id TEXT UNIQUE,
            text TEXT,
            text_hash TEXT UNIQUE,
            sentiment TEXT,
            sentiment_conf REAL,
            topic TEXT,
            topic_conf REAL,
            emergency INTEGER,
            location TEXT,
            verified_topic TEXT,
            verified_at TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_prediction(
    external_id,
    text,
    sentiment,
    sentiment_conf,
    topic,
    topic_conf,
    emergency,
    location
):
    conn = get_connection()
    cursor = conn.cursor()

    text_hash = generate_text_hash(text)

    try:
        cursor.execute("""
            INSERT INTO predictions (
                external_id,
                text,
                text_hash,
                sentiment,
                sentiment_conf,
                topic,
                topic_conf,
                emergency,
                location
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            external_id,
            text,
            text_hash,
            sentiment,
            sentiment_conf,
            topic,
            topic_conf,
            emergency,
            location
        ))

        conn.commit()
        print(f"💾 Saved ID {external_id}")

    except sqlite3.IntegrityError:
        print(f"⚠ Duplicate detected (ID or Text), skipped")

    finally:
        conn.close()