from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager

from core.ai_engine import ai_engine
from database.db import init_db, save_prediction
from scheduler import start_scheduler
import retrain_manager
from config.settings import ALLOWED_ORIGINS

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Sentinel AI Booting Sequence Initiated...")
    init_db()
    try:
        start_scheduler()
    except Exception as e:
        print(f"⚠️ Peringatan Scheduler: {e}")
    yield
    print("🛑 System offline.")

app = FastAPI(title="Sentinel AI API", lifespan=lifespan)

# Menerapkan CORS Middleware dari .env
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictRequest(BaseModel):
    text: str

@app.post("/result/predict")
async def predict(data: PredictRequest):
    if not data.text or len(data.text.strip()) < 5:
        raise HTTPException(status_code=400, detail="Teks terlalu pendek")

    try:
        # Panggil Engine (mendapatkan data yang sudah disterilkan)
        analysis_result = ai_engine.predict_all(data.text)
        
        if analysis_result is None:
            return {"status": "ignored", "message": "Teks dianggap spam atau noise"}

        sent, s_conf, top, t_conf, emg, loc, clean_text = analysis_result

        # SIMPAN clean_text KE DATABASE
        save_prediction(None, clean_text, sent, s_conf, top, t_conf, emg, loc)

        return {
            "status": "success",
            "data": {
                "original_text": data.text,
                "clean_text": clean_text,
                "sentiment": sent,
                "topic": top,
                "is_emergency": bool(emg),
                "location": loc
            }
        }
    except Exception as e:
        print(f"❌ Error Mesin Inferensi: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Rute ini akan dipanggil oleh tombol "Retrain Model" di Dashboard
@app.post("/admin/retrain/{model_type}")
async def trigger_retrain(model_type: str, background_tasks: BackgroundTasks):
    valid_models = ["sentiment", "topic", "emergency"]
    if model_type not in valid_models:
        raise HTTPException(status_code=400, detail="Tipe model tidak valid!")

    # Jalankan retrain di background
    background_tasks.add_task(retrain_manager.retrain_model, model_type)
    
    return {
        "status": "processing",
        "message": f"Proses retrain untuk model '{model_type}' sedang berjalan di latar belakang. Silakan cek log server."
    }