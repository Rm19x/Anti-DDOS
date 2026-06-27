# Menggunakan base image Python resmi yang ringan
FROM python:3.10-slim

# Mengatur environment variable agar Python tidak menulis file .pyc ke disk
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Mengatur working directory di dalam kontainer
WORKDIR /app

# Menginstal dependensi sistem yang diperlukan (termasuk iptables untuk eksekutor)
RUN apt-get update && apt-get install -y --no-install-recommends \
    iptables \
    iproute2 \
    && rm -rf /var/lib/apt/lists/*

# Menyalin file requirements ke dalam kontainer
COPY analyzer/requirements.txt /app/analyzer/requirements.txt

# Menginstal dependensi Python
RUN pip install --no-cache-dir -r /app/analyzer/requirements.txt
RUN mkdir -p /var/log/nginx && touch /var/log/nginx/access.log
# Menyalin seluruh struktur kode ke dalam kontainer
COPY . /app/

# Memberikan akses eksekusi pada skrip firewall dan shell scripts
RUN chmod +x /app/firewall/*.sh /app/self_healing.sh

# Membuka port untuk Health-Check Endpoint dan Dashboard FastAPI
EXPOSE 8000

# Perintah default untuk menjalankan program utama analyzer
CMD ["python", "analyzer/main.py"]
