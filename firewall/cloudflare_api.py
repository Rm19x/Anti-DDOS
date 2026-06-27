# ==============================================================================
# Project: anti-ddos (Cloudflare Edge Mitigation Integration)
# Author: Mr.Rm19
# GitHub: https://github.com/Rm19x
# Description: Blocks malicious IPs at Cloudflare Edge network via API.
# ==============================================================================

import requests
import json
import sys

# Membaca konfigurasi terpusat
CONFIG_PATH = "config.json"

def load_cloudflare_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
            return config.get("cloudflare", {})
    except Exception as e:
        print(f"[-] Gagal membaca file konfigurasi untuk Cloudflare API: {e}")
        return {}

def block_ip_on_cloudflare(ip_address, reason):
    """[Fitur 14] Mengirimkan request POST ke Cloudflare API untuk melakukan ban IP."""
    cf_cfg = load_cloudflare_config()
    
    # Validasi apakah integrasi Cloudflare diaktifkan oleh pengguna
    if not cf_cfg.get("enabled", False):
        print("[*] Cloudflare API: Integrasi dinonaktifkan di config.json. Melewati.")
        return False

    api_token = cf_cfg.get("api_token")
    zone_id = cf_cfg.get("zone_id")

    if not api_token or not zone_id or "YOUR_" in api_token:
        print("[-] Cloudflare API Error: Token API atau Zone ID belum dikonfigurasi dengan benar!")
        return False

    # Endpoint URL resmi Cloudflare API V4 untuk Firewall Access Rules
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/access_rules/rules"

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    # Payload data untuk memblokir IP di seluruh edge network Cloudflare
    payload = {
        "mode": "block",  # Aksi: Blokir total akses
        "configuration": {
            "target": "ip",
            "value": ip_address
        },
        "notes": f"AntidDoS AutoBan by Mr.Rm19 - Reason: {reason}"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        res_data = response.json()

        if response.status_code == 200 and res_data.get("success"):
            print(f"[+] Cloudflare API: Berhasil memblokir IP {ip_address} di level Edge DNS Global.")
            return True
        else:
            errors = res_data.get("errors", [])
            print(f"[-] Cloudflare API Gagal: {errors}")
            return False
            
    except Exception as e:
        print(f"[-] Exception terjadi saat menghubungi Cloudflare API: {e}")
        return False

if __name__ == "__main__":
    # Script menerima argumen dari CLI (contoh: python cloudflare_api.py 1.1.1.1 "HTTP Flood")
    if len(sys.argv) < 3:
        print("[-] Penggunaan: python cloudflare_api.py [IP] [REASON]")
        sys.exit(1)

    target_ip = sys.argv[1]
    ban_reason = sys.argv[2]
    block_ip_on_cloudflare(target_ip, ban_reason)