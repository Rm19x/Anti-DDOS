# ==============================================================================
# Project: anti-ddos (GeoIP & ASN Lookup Module)
# Author: Mr.Rm19
# GitHub: https://github.com/Rm19x
# Description: Resolves IP location (Country) and ASN network details.
# ==============================================================================

import geoip2.database
import os

class GeoIPAnalyzer:
    def __init__(self, config):
        self.config = config
        protection_rules = config.get("protection_rules", {})
        self.blocked_countries = protection_rules.get("geoip_block_countries", [])
        self.blocked_asns = protection_rules.get("asn_block_list", [])

        # Lokasi database MaxMind GeoLite2 (.mmdb) di dalam server/kontainer
        self.country_db_path = "/var/lib/GeoIP/GeoLite2-Country.mmdb"
        self.asn_db_path = "/var/lib/GeoIP/GeoLite2-ASN.mmdb"

    def check_geoip_and_asn(self, ip):
        """
        [Fitur 4, 5] Memeriksa apakah IP berasal dari negara atau ASN yang diblokir.
        Mengembalikan tuple: (is_blocked, reason)
        """
        # 1. Jalankan Validasi GeoIP Negara [Fitur 4]
        if self.blocked_countries and os.path.exists(self.country_db_path):
            try:
                with geoip2.database.Reader(self.country_db_path) as reader:
                    response = reader.country(ip)
                    country_code = response.country.iso_code
                    if country_code in self.blocked_countries:
                        return True, f"GeoIP Blocked: Traffic from {country_code} is restricted"
            except Exception as e:
                # Log error internal tanpa menghentikan traffic flow
                print(f"[-] GeoIP Reader Exception untuk IP {ip}: {e}")

        # 2. Jalankan Validasi ASN (Autonomous System Number) [Fitur 5]
        if self.blocked_asns and os.path.exists(self.asn_db_path):
            try:
                with geoip2.database.Reader(self.asn_db_path) as reader:
                    response = reader.asn(ip)
                    asn = response.autonomous_system_number
                    if asn in self.blocked_asns:
                        return True, f"ASN Blocked: Hosting Provider network (ASN {asn}) restricted"
            except Exception as e:
                print(f"[-] ASN Reader Exception untuk IP {ip}: {e}")

        return False, ""