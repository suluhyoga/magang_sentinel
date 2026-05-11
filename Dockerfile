# 1. Gunakan Python versi 3.10 yang ringan sebagai base
FROM python:3.10-slim

# 2. Bikin folder khusus bernama /app di dalam kontainer
WORKDIR /app

# 3. Copy daftar library yang dibutuhkan dan install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy seluruh file proyek Sentinel AI kamu ke dalam kontainer
COPY . .

# 5. Beri tahu Docker bahwa aplikasi ini butuh port 8000
EXPOSE 8000

# 6. Perintah wajib untuk menyalakan FastAPI saat kontainer jalan
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]