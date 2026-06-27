#!/bin/bash
# ==============================================================================
# Project: anti-ddos (Automated Self-Healing Monitor daemon)
# Author: Mr.Rm19
# GitHub: https://github.com/Rm19x
# Description: [Fitur 43] Monitors anti-ddos container health and auto-restarts 
#              the core service if a crash or failure is detected.
# ==============================================================================

# Nama kontainer core anti-ddos sesuai dengan konfigurasian docker-compose.yml
CONTAINER_NAME="anti-ddos-core"

# File log internal untuk mencatat aktivitas pemulihan sistem
LOG_FILE="/var/log/anti_ddos_firewall.log"

# Mengambil penanda waktu saat ini
get_timestamp() {
    date "+%Y-%m-%d %H:%M:%S"
}

# 1. Memeriksa apakah Docker Engine berjalan di server host
if ! command -v docker &> /dev/null; then
    echo "[$(get_timestamp)] [SELF_HEALING_ERROR] Perintah 'docker' tidak ditemukan di sistem host!" >> "$LOG_FILE"
    exit 1
fi

# 2. Mengecek status keaktifan kontainer (apakah bernilai 'true' atau 'false')
IS_RUNNING=$(docker inspect -f '{{.State.Running}}' "$CONTAINER_NAME" 2>/dev/null)

if [ "$IS_RUNNING" == "true" ]; then
    # Kontainer berjalan normal, sekarang lakukan pengecekan via HTTP Health Endpoint [Fitur 50]
    # Mengirim request ke endpoint /health yang disediakan oleh FastAPI backend
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)
    
    if [ "$HTTP_STATUS" -ne 200 ]; then
        echo "[$(get_timestamp)] [CRITICAL] Kontainer $CONTAINER_NAME aktif tetapi /health merespon dengan status: $HTTP_STATUS!" >> "$LOG_FILE"
        echo "[*] Memicu restart layanan secara aman..."
        docker restart "$CONTAINER_NAME" >> "$LOG_FILE" 2>&1
        echo "[$(get_timestamp)] [RECOVERED] Layanan berhasil dinyalakan ulang via Health-Check trigger." >> "$LOG_FILE"
    fi

elif [ "$IS_RUNNING" == "false" ]; then
    # Kontainer terdeteksi mati/stopped (Crash)
    echo "[$(get_timestamp)] [ALERT] Kontainer $CONTAINER_NAME terdeteksi MATI/CRASH!" >> "$LOG_FILE"
    echo "[*] Memulai pemulihan otomatis layanan core..."
    docker start "$CONTAINER_NAME" >> "$LOG_FILE" 2>&1
    echo "[$(get_timestamp)] [RECOVERED] Layanan berhasil dihidupkan kembali secara otomatis." >> "$LOG_FILE"

else
    # Kontainer belum dibuat atau tidak ditemukan namanya di sistem
    echo "[$(get_timestamp)] [ALERT] Kontainer $CONTAINER_NAME tidak ditemukan di sistem!" >> "$LOG_FILE"
    echo "[*] Mencoba membangunkan via docker-compose..."
    # Lompat ke direktori root anti-ddos dan jalankan compose ulang secara detached
    cd "$(dirname "$0")/.." && docker-compose up -d >> "$LOG_FILE" 2>&1
fi