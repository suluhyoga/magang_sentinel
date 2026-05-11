import requests
import time
from apscheduler.schedulers.background import BackgroundScheduler
from database.db import save_prediction
from core.ai_engine import ai_engine
from config.settings import AUTO_SCRAPE_INTERVAL, SCRAPER_API_URL

processed_ids = set()

def fetch_and_process():
    if len(processed_ids) > 5000:
        processed_ids.clear()

    try:
        response = requests.get(SCRAPER_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        for item in data:
            external_id = str(item.get("id"))
            if not external_id or external_id in processed_ids:
                continue

            raw_text = item.get("content") or item.get("text") or item.get("caption")
            if not raw_text:
                continue

            result = ai_engine.predict_all(raw_text)
            
            if result is None:
                processed_ids.add(external_id)
                continue

            sent, s_conf, top, t_conf, emg, loc, clean_text = result

            save_prediction(
                external_id=external_id, 
                text=clean_text, 
                sentiment=sent, 
                sentiment_conf=s_conf, 
                topic=top, 
                topic_conf=t_conf, 
                emergency=emg, 
                location=loc
            )

            processed_ids.add(external_id)
            print(f"✅ Tersimpan ID: {external_id} | Topik: {top} | Teks Bersih: {clean_text[:30]}...")

    except requests.exceptions.ConnectionError:
        print("⚠️ Scheduler: Gagal koneksi ke Scraper (localhost:9000).")
    except Exception as e:
        print(f"❌ Scheduler Error: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler(daemon=True)
    # Mengambil interval dari .env (secara default 15 detik)
    scheduler.add_job(fetch_and_process, "interval", seconds=AUTO_SCRAPE_INTERVAL, id="scraper_job")
    scheduler.start()
    print(f"🚀 Auto-Scraping Job Started (Interval: {AUTO_SCRAPE_INTERVAL}s)")