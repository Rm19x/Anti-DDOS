# ==============================================================================
# Project: anti-ddos (Core Rules Engine)
# Author: Mr.Rm19
# GitHub: https://github.com/Rm19x
# Description: Real-time traffic analyzer and signature-based DDoS detection.
# ==============================================================================

import re
import time

class DDoSDefenderRules:
    def __init__(self, config, redis_client):
        self.config = config
        self.redis = redis_client
        
        # Load rules from config.json
        mitigation = config.get("mitigation", {})
        rules = config.get("protection_rules", {})
        
        self.max_rpm = mitigation.get("max_requests_per_minute", 60)
        self.burst_window = mitigation.get("burst_window_seconds", 1)
        self.max_burst = mitigation.get("max_burst_requests", 15)
        
        self.allowed_methods = rules.get("allowed_methods", ["GET", "POST", "HEAD"])
        self.sensitive_uris = rules.get("sensitive_uris", [])
        self.ua_blacklist = [re.compile(ua, re.IGNORECASE) for ua in rules.get("user_agent_blacklist", [])]
        
        # [Fitur 49] Signature-based detection for popular stress-testers
        self.signature_patterns = [
            re.compile(r"(loic|hoic|xerxes|slowloris|hulk|goldeneye)", re.IGNORECASE)
        ]

    def is_whitelisted(self, ip):
        """Menghindari pemblokiran IP esensial milik owner/sahabat."""
        whitelist_ips = self.config.get("whitelist", {}).get("ips", [])
        return ip in whitelist_ips

    def check_signatures(self, user_agent, uri):
        """[Fitur 49] Memeriksa kecocokan pola signature alat attack populer."""
        if user_agent:
            for pattern in self.signature_patterns:
                if pattern.search(user_agent):
                    return True, "Signature Match: Known Attack Tool Detected"
            for pattern in self.ua_blacklist:
                if pattern.search(user_agent):
                    return True, "Blacklisted User-Agent Detected"
        return False, ""

    def check_http_rules(self, method, uri):
        """[Fitur 6, 7] Validasi metode HTTP dan halaman sensitif."""
        if method not in self.allowed_methods:
            return True, f"Unallowed HTTP Method: {method}"
        
        # Ekstra proteksi untuk URI sensitif (misal rate limit diperketat otomatis)
        for sensitive in self.sensitive_uris:
            if sensitive in uri:
                return False, "SENSITIVE_URI"
        
        return False, ""

    def evaluate_traffic(self, ip, user_agent, method, uri):
        """
        Melakukan evaluasi komprehensif terhadap traffic masuk secara real-time.
        Mengembalikan tuple: (is_malicious, reason)
        """
        if self.is_whitelisted(ip):
            return False, "Whitelisted"

        # 1. Cek Signature & User-Agent [Fitur 3, 49]
        is_bad_sig, reason = self.check_signatures(user_agent, uri)
        if is_bad_sig:
            return True, reason

        # 2. Cek Aturan HTTP (Method & URI) [Fitur 6, 7]
        is_bad_http, http_status = self.check_http_rules(method, uri)
        if is_bad_http:
            return True, http_status

        # Atur pengali pembatas jika mengakses halaman sensitif [Fitur 7]
        rpm_limit = self.max_rpm if http_status != "SENSITIVE_URI" else int(self.max_rpm / 2)

        current_time = int(time.time())
        minute_key = f"rate:{ip}:{current_time // 60}"
        burst_key = f"burst:{ip}:{current_time}"

        try:
            # 3. [Fitur 1] Dynamic Rate Limiting (Per Menit)
            current_rpm = self.redis.incr(minute_key)
            if current_rpm == 1:
                self.redis.expire(minute_key, 60)
            
            if current_rpm > rpm_limit:
                return True, f"Rate Limit Exceeded ({current_rpm}/{rpm_limit} RPM)"

            # 4. [Fitur 8 / Kelompok 1 - Behavioral] Burst Detection (Per Detik)
            current_burst = self.redis.incr(burst_key)
            if current_burst == 1:
                self.redis.expire(burst_key, self.burst_window + 1)
                
            if current_burst > self.max_burst:
                return True, f"Burst Attack Detected ({current_burst} req/sec)"

        except Exception as e:
            # Jika Redis bermasalah, fallback ke logging agar sistem tidak crash
            print(f"[-] Cache Exception: {e}")
            
        return False, ""