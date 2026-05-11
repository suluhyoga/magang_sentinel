# 🚀 Sentinel AI — Sistem Klasifikasi Laporan Masyarakat (POLDA)

**Sentinel AI** adalah engine kecerdasan buatan berbasis Natural Language Processing (NLP) yang dirancang untuk membantu Kepolisian Daerah (POLDA) dalam mengklasifikasikan laporan maupun unggahan masyarakat secara otomatis.

Sistem ini menggunakan arsitektur **IndoBERT** yang telah dioptimasi dengan teknik **Linear Probing** untuk mendeteksi:

- Sentimen
- Topik
- Status Kegawatdaruratan (Emergency)

secara real-time dan efisien.

---

# 🛠️ Tech Stack & Architecture

- **Framework:** FastAPI (Python 3.10)
- **AI Models:** IndoBERT-base-p1
  - Sentiment Classifier
  - Topic Classifier
  - Emergency Classifier
- **Database:** SQLite
- **Containerization:** Docker & Docker Compose
- **Scheduler:** APScheduler
- **Optimization Technique:** Linear Probing (Extreme Freezing Layer)

---

# 📁 Struktur Folder

```plaintext
sentinel_ai/
├── config/                 # Pengaturan global aplikasi & AI
├── core/                   # Otak utama AI (Preprocessing, Inference, Logic)
│   ├── ai_engine.py        # Handler pemuatan 3 model IndoBERT
│   ├── train_*.py          # Script pelatihan tiap kategori
│   └── ...
├── database/               # Penyimpanan lokal (SQLite)
├── dataset/                # Dataset mentah (.csv) untuk retraining
├── model/                  # Folder bobot model (.bin/.safetensors)
├── Dockerfile              # Instruksi build container
├── docker-compose.yml      # Orkestrasi container & volume
├── requirements.txt        # Dependency project
├── retrain_manager.py      # Logic Champion vs Challenger
└── main.py                 # Entry point FastAPI
```

---

# ⚠️ Persiapan Sebelum Menjalankan

Karena file model AI berukuran besar, folder `model/` tidak disertakan dalam repository (`.gitignore`).

## Langkah Persiapan

1. Dapatkan folder `model/` dari pengembang.
2. Pastikan folder tersebut memiliki sub-folder berikut:

```plaintext
model/
├── indobert_sentiment/
├── topic_classifier/
└── emergency_classifier/
```

3. Letakkan folder `model/` di direktori utama project sebelum menjalankan aplikasi atau build Docker.

---

# 🚀 Cara Menjalankan (Deployment)

## 1. Menggunakan Docker (Rekomendasi)

Pastikan Docker dan Docker Compose sudah terinstal.

Jalankan perintah berikut:

```bash
docker-compose up -d --build
```

Aplikasi akan berjalan pada:

```plaintext
http://localhost:8000
```

---

# 💻 Spesifikasi Minimum Server (VPS)

| Komponen | Minimum |
|---|---|
| CPU | 2–4 Cores |
| RAM | 4 GB |
| Storage | SSD Recommended |

## ⚠️ Penting

Karena proses retraining model cukup berat, sangat disarankan membuat **Swap Memory minimal 4 GB** pada Ubuntu Server untuk mencegah:

- Out of Memory (OOM)
- Container crash saat training
- Server freeze

---

# 📡 API Endpoints

| Method | Endpoint | Deskripsi |
|---|---|---|
| GET | `/` | Health check aplikasi |
| POST | `/result/predict` | Prediksi Sentimen, Topik, Lokasi, dan Emergency |
| POST | `/admin/retrain/{model_type}` | Trigger retraining model manual |

---

# 🧠 Logika Retrain — Champion vs Challenger

Sistem menggunakan pendekatan **Champion vs Challenger** agar model tidak langsung diganti setelah retraining.

## Mekanisme

1. Sistem melatih **Model Challenger**.
2. Challenger dibandingkan dengan **Champion Model** (model aktif).
3. Evaluasi dilakukan menggunakan **F1-Score**.
4. Jika Challenger memiliki performa lebih baik:
   - Sistem melakukan **Hot Swapping**
   - Model baru langsung aktif
   - Server tetap berjalan tanpa downtime

---

# 🔥 Fitur Utama

- Real-time NLP Classification
- Multi-Task IndoBERT Classification
- Emergency Detection
- Automatic Retraining
- Champion vs Challenger Strategy
- Hot Model Swapping
- Dockerized Deployment
- Lightweight SQLite Logging
- CPU Optimized Inference

---

# 📌 Catatan

Project ini dikembangkan untuk mendukung otomatisasi analisis laporan masyarakat pada lingkungan Kepolisian menggunakan teknologi Artificial Intelligence berbasis NLP Bahasa Indonesia.

---
