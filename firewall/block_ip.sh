#!/bin/bash
# ==============================================================================
# Project: anti-ddos (Linux Kernel Firewall IP Blocker)
# Author: Mr.Rm19
# GitHub: https://github.com/Rm19x
# Description: Drops malicious traffic instantly at the OS level using iptables.
# ==============================================================================

# Memastikan argumen IP dikirim oleh program utama
IP_TARGET=$1
REASON=$2

if [ -z "$IP_TARGET" ]; then
    echo "[-] Error: IP target tidak ditentukan!"
    exit 1
fi

# Lokasi file log internal pertahanan firewall
LOG_FILE="/var/log/anti_ddos_firewall.log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# Memeriksa apakah IP yang masuk sudah pernah diblokir sebelumnya untuk menghindari duplikasi rule
iptables -C INPUT -s "$IP_TARGET" -j DROP &>/dev/null

if [ $? -ne 0 ]; then
    # [Fitur 13] Mengeksekusi pemutusan koneksi nyata dengan aksi DROP (mengabaikan paket)
    iptables -A INPUT -s "$IP_TARGET" -j DROP
    
    # Catat aksi pemblokiran ke dalam file log sistem
    echo "[$TIMESTAMP] [BANNED] IP: $IP_TARGET | Reason: $REASON" >> "$LOG_FILE"
    echo "[+] Firewall: Sukses memblokir IP $IP_TARGET di tingkat kernel Linux."
else
    echo "[*] Firewall: IP $IP_TARGET sudah berada dalam daftar blokir iptables."
fi
