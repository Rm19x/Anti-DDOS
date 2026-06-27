# ==============================================================================
# Project: anti-ddos (Web Dashboard Backend API)
# Author: Mr.Rm19
# GitHub: https://github.com/Rm19x
# Description: FastAPI application providing endpoints for UI monitoring and 
#              health status reporting.
# ==============================================================================

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from redis import Redis
import json
import os

app = FastAPI(
    title="anti-ddos Control Dashboard by Mr.Rm19",
    description="Real-time monitoring panel for malicious traffic mitigation.",
    version="1.0"
)

# Konfigurasi Path File Induk
CONFIG_PATH = "config.json"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

config = load_config()
cache_cfg = config.get("cache", {})

# Inisialisasi Driver Redis Cache [Fitur 41]
redis_client = Redis(
    host=cache_cfg.get("redis_host", "localhost"),
    port=cache_cfg.get("redis_port", 6379),
    db=cache_cfg.get("redis_db", 0),
    decode_responses=True
)

# Mounting folder asset statis (CSS/JS) dan template HTML
# Pastikan folder dashboard/static dan dashboard/templates sudah dibuat
if os.path.isdir("dashboard/static"):
    app.mount("/static", StaticFiles(directory="dashboard/static"), name="static")

templates = Jinja2Templates(directory="dashboard/templates")


# 1. Endpoint Render Halaman Utama Dashboard (Web UI Viewer) [Fitur 22, 29]
@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    """Melempar halaman visual utama dengan dukungan Live Attack Map dan Dark Mode."""
    return templates.TemplateResponse("index.html", {"request": request, "author": "Mr.Rm19"})


# 2. [Fitur 50] Health-Check Endpoint untuk Sistem Monitoring Eksternal
@app.get("/health")
async def health_check():
    """Menyediakan jalur monitoring eksternal untuk mengecek kesehatan aplikasi core."""
    try:
        # Verifikasi apakah database RAM Redis dapat dijangkau dengan lancar
        redis_alive = redis_client.ping()
        if redis_alive:
            return JSONResponse(
                status_code=200,
                content={"status": "healthy", "engine": "anti-ddos", "cache_connected": True}
            )
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "reason": f"Cache engine integration failure: {str(e)}"}
        )


# 3. [Fitur 22] Live Stream API Data Serangan untuk Komponen Frontend UI
@app.get("/api/v1/attacks")
async def get_active_attacks():
    """Mengambil seluruh daftar IP penyerang yang saat ini aktif didekam di cache RAM."""
    try:
        # Mencari seluruh key di Redis yang memiliki awalan status banned
        keys = redis_client.keys("banned:*")
        active_bans = []

        for key in keys:
            ip_address = key.split(":")[1]
            reason = redis_client.get(key)
            # Mengambil sisa waktu hukuman (Time to Live) dari Redis
            ttl = redis_client.ttl(key)
            
            active_bans.append({
                "ip": ip_address,
                "reason": reason,
                "remaining_jail_time_sec": ttl
            })

        return {"total_blocked": len(active_bans), "attackers": active_bans}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failure: {str(e)}")


# 4. API Endpoint untuk Menghapus IP secara Manual Langsung Dari Dashboard UI
@app.delete("/api/v1/unban/{ip}")
async def manual_unban_ip(ip: str):
    """Menyediakan kontrol manual untuk membebaskan IP dari daftar blokir."""
    ban_key = f"banned:{ip}"
    if redis_client.exists(ban_key):
        redis_client.delete(ban_key)
        print(f"[+] Dashboard UI: Admin melakukan manual UNBAN pada IP: {ip}")
        return {"status": "success", "message": f"IP {ip} successfully unbanned manually."}
    else:
        raise HTTPException(status_code=404, detail="Target IP not found in active ban list.")
