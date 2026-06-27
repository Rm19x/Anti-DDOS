# ==============================================================================
# Project: anti-ddos (Core Engine Tailer)
# Author: Mr.Rm19
# GitHub: https://github.com/Rm19x
# Description: Multi-log real-time reader and threat mitigator.
# ==============================================================================

import re
import os
import sys
import json
import time
import subprocess
from redis import Redis
from rules import DDoSDefenderRules

# Menghubungkan path konfigurasi eksternal
CONFIG_PATH = "config.json"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

# CLF (Common Log Format) Regular Expression parser
# Menangkap IP, Method, URI, Status, dan User-Agent
LOG_PARSER = re.compile(
    r'(?P<ip>\S+)\s+\S+\s+\S+\s+\[.*?\]\s+"(?P<method>\S+)\s+(?P<uri>\S+)\s+\S+"\s+(?P<status>\d+)\s+\d+\s+"[^"]*"\s+"(?P<user_agent>[^"]*)"'
)

def trigger_firewall_block(ip, reason):
    """Memanggil program eksekutor firewall nyata secara langsung."""
    print(f"[!] TRIGGER BAN: IP {ip} diblokir karena -> {reason}")
    try:
        # Menjalankan skrip eksekutor di folder firewall
        subprocess.Popen(["/bin/bash", "firewall/block_ip.sh", ip, reason], 
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        print(f"[-] Gagal mengeksekusi firewall/block_ip.sh: {e}")

def follow_multi_logs(log_paths):
    """[Fitur 42] Generator non-blocking untuk membaca banyak log secara berkala."""
    files = []
    for path in log_paths:
        if os.path.exists(path):
            f = open(path, "r")
            # Langsung lompat ke baris terakhir saat aplikasi dinyalakan
            f.seek(0, os.SEEK_END)
            files.append((f, path))
            print(f"[+] Berhasil memantau log web server: {path}")
        else:
            print(f"[-] Berkas log tidak ditemukan (diabaikan): {path}")

    if not files:
        print("[-] Kritis: Tidak ada file log yang bisa dipantau. Keluar.")
        sys.exit(1)

    while True:
        line_read = False
        for f, path in files:
            line = f.readline()
            if line:
                line_read = True
                yield line
        if not line_read:
            time.sleep(0.1) # Istirahat sejenak jika tidak ada traffic masuk

def main():
    print("==================================================")
    print("   anti-ddos Core Engine Protection Activated     ")
    print("   Created by: Mr.Rm19 (github.com/Rm19x)         ")
    print("==================================================")

    config = load_config()
    
    # Inisialisasi In-Memory Cache Redis [Fitur 41]
    cache_cfg = config.get("cache", {})
    redis_client = Redis(
        host=cache_cfg.get("redis_host", "localhost"),
        port=cache_cfg.get("redis_port", 6379),
        db=cache_cfg.get("redis_db", 0),
        decode_responses=True
    )
    
    # Inisialisasi engine rule analyzer
    analyzer = DDoSDefenderRules(config, redis_client)
    log_paths = config.get("server", {}).get("log_paths", [])

    print("[*] Mulai membaca lalu lintas data jaringan...")
    for log_line in follow_multi_logs(log_paths):
        match = LOG_PARSER.match(log_line)
        if match:
            data = match.groupdict()
            ip = data["ip"]
            user_agent = data["user_agent"]
            method = data["method"]
            uri = data["uri"]

            # Evaluasi paket data log lewat rules engine
            is_malicious, reason = analyzer.evaluate_traffic(ip, user_agent, method, uri)
            
            if is_malicious:
                # Cek apakah IP sudah ditandai terblokir di Redis agar tidak memicu duplikasi ban
                ban_status_key = f"banned:{ip}"
                if not redis_client.get(ban_status_key):
                    # Set status banned di Redis dengan masa kadaluarsa sesuai jail time
                    jail_time = config.get("mitigation", {}).get("jail_time_seconds", 3600)
                    redis_client.setex(ban_status_key, jail_time, reason)
                    
                    # Eksekusi blokir fisik di firewall
                    trigger_firewall_block(ip, reason)

if __name__ == "__main__":
    main()
