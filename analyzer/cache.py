# ==============================================================================
# Project: anti-ddos (In-Memory Cache Manager)
# Author: Mr.Rm19
# GitHub: https://github.com/Rm19x
# Description: High-performance memory management using Redis.
# ==============================================================================

import redis

class AntiDDoSCacheManager:
    def __init__(self, config):
        cache_cfg = config.get("cache", {})
        self.host = cache_cfg.get("redis_host", "localhost")[cite: 2]
        self.port = cache_cfg.get("redis_port", 6379)[cite: 2]
        self.db = cache_cfg.get("redis_db", 0)[cite: 2]
        self.client = None
        self.connect()

    def connect(self):
        """Membangun koneksi ke Redis dengan mekanisme penanganan kegagalan."""
        try:
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                decode_responses=True
            )
            # Uji koneksi ping nyata
            self.client.ping()
            print(f"[+] Cache.py: Berhasil terhubung ke Redis Cache di {self.host}:{self.port}")
        except Exception as e:
            print(f"[-] Cache.py Kritis: Gagal terhubung ke Redis Server! Error: {e}")
            self.client = None

    def get_ban_status(self, ip):
        """Memeriksa apakah IP sudah ada dalam daftar blokir aktif di cache."""
        if not self.client:
            return None
        try:
            return self.client.get(f"banned:{ip}")
        except Exception:
            return None

    def set_ban_status(self, ip, jail_time, reason):
        """Menandai IP sebagai 'banned' di memori RAM selama durasi jail time."""
        if not self.client:
            return False
        try:
            return self.client.setex(f"banned:{ip}", jail_time, reason)
        except Exception as e:
            print(f"[-] Gagal menyimpan status ban IP {ip} ke Redis: {e}")
            return False
