import os, shutil, sqlite3, subprocess, sys, torch
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from config.settings import DB_PATH
from core.ai_engine import ai_engine

BACKUP_DIR = "model/backups"

# Konfigurasi Lengkap SOTA untuk tiap model
MODEL_CONFIG = {
    "topic": {
        "db_col": "verified_topic",
        "csv_col": "topic",
        "script": "core/train_topic_model.py",
        "model_dir": "model/topic_classifier",
        "dataset_path": "dataset/topic_dataset.csv",
        "label_map": {"kriminal": 0, "lalu_lintas": 1, "pelayanan": 2, "sosial": 3, "lainnya": 4}
    },
    "sentiment": {
        "db_col": "verified_sentiment",
        "csv_col": "sentiment",
        "script": "core/train_sentiment_model.py",
        "model_dir": "model/indobert_sentiment",
        "dataset_path": "dataset/twitter_sentiment.csv",
        "label_map": {"negative": 0, "neutral": 1, "positive": 2}
    },
    "emergency": {
        "db_col": "verified_emergency",
        "csv_col": "label",
        "script": "core/train_emergency_model.py",
        "model_dir": "model/emergency_classifier",
        "dataset_path": "dataset/report_classifier.csv",
        # Emergency menggunakan int di script train-nya, kita buat string ke int map
        "label_map": {"0": 0, "1": 1, 0: 0, 1: 1} 
    }
}

def evaluate_model(model_dir, texts, true_labels):
    """Fungsi Evaluasi Independen (Ujian untuk Model)"""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(model_dir).to(device)
    model.eval()

    preds = []
    batch_size = 16
    with torch.no_grad():
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            inputs = tokenizer(batch_texts, return_tensors="pt", padding=True, truncation=True, max_length=128).to(device)
            outputs = model(**inputs)
            batch_preds = torch.argmax(outputs.logits, dim=1).cpu().numpy()
            preds.extend(batch_preds)

    # Menggunakan weighted F1-Score agar adil untuk kelas yang minoritas
    return f1_score(true_labels, preds, average="weighted")

def retrain_model(model_type):
    if model_type not in MODEL_CONFIG:
        return {"status": "failed", "reason": "Tipe model tidak valid"}

    print(f"\n🔄 [RETRAIN PIPELINE] Memulai proses retrain untuk: {model_type.upper()}")
    config = MODEL_CONFIG[model_type]
    
    # 1. TARIK DATA BARU DARI DATABASE
    conn = sqlite3.connect(DB_PATH)
    query = f"SELECT text, {config['db_col']} as {config['csv_col']} FROM predictions WHERE {config['db_col']} IS NOT NULL"
    new_data_df = pd.read_sql_query(query, conn)
    conn.close()

    if len(new_data_df) < 50: # Set ke 50 data baru sebagai syarat minimal retrain
        return {"status": "ignored", "reason": f"Data baru kurang (hanya {len(new_data_df)}), kumpulkan minimal 50 data validasi"}

    # 2. GABUNGKAN DATA LAMA DAN BARU (Continual Learning)
    old_data_df = pd.read_csv(config['dataset_path'], sep=';').dropna()
    
    # Konversi tipe data agar seragam
    new_data_df[config['csv_col']] = new_data_df[config['csv_col']].astype(str).str.lower()
    old_data_df[config['csv_col']] = old_data_df[config['csv_col']].astype(str).str.lower()
    
    combined_df = pd.concat([old_data_df, new_data_df], ignore_index=True)
    combined_df = combined_df.drop_duplicates(subset=['text']) # Hindari Data Leakage
    
    # 3. BUAT SOAL UJIAN YANG SAMA (Validation Set)
    # Harus pakai random_state=42 agar persis sama dengan yang dipakai di script training
    combined_df['mapped_label'] = combined_df[config['csv_col']].map(config['label_map'])
    combined_df = combined_df.dropna(subset=['mapped_label']) # Buang label yg tidak valid
    combined_df['mapped_label'] = combined_df['mapped_label'].astype(int)

    _, val_df = train_test_split(combined_df, test_size=0.15, stratify=combined_df['mapped_label'], random_state=42)
    
    test_texts = val_df['text'].tolist()
    test_labels = val_df['mapped_label'].tolist()

    # 4. UJI MODEL LAMA (THE CHAMPION)
    print("📊 Mengevaluasi Model Lama (Champion)...")
    try:
        old_f1 = evaluate_model(config["model_dir"], test_texts, test_labels)
        print(f"🏆 Skor Model Lama: {old_f1:.4f}")
    except Exception as e:
        print(f"⚠️ Model lama gagal dievaluasi (mungkin belum ada): {e}")
        old_f1 = 0.0

    # 5. BACKUP & SIMPAN DATASET BARU
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"{model_type}_{timestamp}")
    
    if os.path.exists(config["model_dir"]):
        shutil.copytree(config["model_dir"], backup_path)
    
    # Simpan dataset gabungan (Timpa dataset lama)
    combined_df[['text', config['csv_col']]].to_csv(config['dataset_path'], index=False, sep=';')

    # 6. LATIH MODEL BARU (THE CHALLENGER)
    print("🚀 Melatih Model Baru (Challenger) - Ini akan memakan waktu...")
    try:
        result = subprocess.run([sys.executable, config["script"]], capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Training Script Error:\n{result.stderr}")

        # 7. UJI MODEL BARU
        print("📊 Mengevaluasi Model Baru (Challenger)...")
        new_f1 = evaluate_model(config["model_dir"], test_texts, test_labels)
        print(f"⚔️ Skor Model Baru: {new_f1:.4f}")

        # 8. PERTANDINGAN (CHAMPION vs CHALLENGER)
        if new_f1 >= old_f1:
            print("✅ Model Baru Menang! Memperbarui AI Engine...")
            ai_engine.reload_models() # Load model baru ke memori
            # Opsional: Hapus backup untuk hemat disk
            shutil.rmtree(backup_path, ignore_errors=True) 
            return {
                "status": "success", 
                "message": "Retrain berhasil dan model ditingkatkan",
                "old_score": round(old_f1, 4),
                "new_score": round(new_f1, 4)
            }
        else:
            print("❌ Model Baru Lebih Buruk. Melakukan Rollback (Mengembalikan Model Lama)...")
            shutil.rmtree(config["model_dir"]) # Hapus model cacat
            shutil.copytree(backup_path, config["model_dir"]) # Kembalikan model master
            ai_engine.reload_models()
            return {
                "status": "rollback", 
                "message": "Retrain dibatalkan (Skor baru lebih rendah)",
                "old_score": round(old_f1, 4),
                "new_score": round(new_f1, 4)
            }

    except Exception as e:
        print(f"💥 TERJADI KESALAHAN FATAL: {e}")
        print("🔄 Melakukan Rollback Darurat...")
        if os.path.exists(backup_path):
            if os.path.exists(config["model_dir"]): 
                shutil.rmtree(config["model_dir"])
            shutil.copytree(backup_path, config["model_dir"])
            ai_engine.reload_models()
        return {"status": "error", "reason": str(e)}