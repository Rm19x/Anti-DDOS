#!/bin/bash
# ==============================================================================
# Project: anti-ddos (Linux Kernel Networking Stack Optimizer)
# Author: Mr.Rm19
# GitHub: https://github.com/Rm19x
# Description: Hardens sysctl parameters to mitigate heavy SYN Flood attacks.
# ==============================================================================

# Memastikan skrip dijalankan dengan hak akses root (Sudo)
if [ "$EUID" -ne 0 ]; then
  echo "[-] Error: Skrip ini wajib dijalankan menggunakan perintah sudo!"
  exit 1
fi

LOG_FILE="/var/log/anti_ddos_firewall.log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "[*] Memulai optimasi parameter kernel jaringan Linux..."

# 1. [Fitur 18] Mengaktifkan proteksi TCP SYN Cookies tingkat kernel
sysctl -w net.ipv4.tcp_syncookies=1

# 2. Meningkatkan kapasitas maksimum antrean backlog koneksi TCP (Mencegah drop koneksi baik)
sysctl -w net.core.somaxconn=10240
sysctl -w net.ipv4.tcp_max_syn_backlog=10240

# 3. Mempercepat waktu pembersihan koneksi mati (TCP FIN Timeout) agar RAM hemat
sysctl -w net.ipv4.tcp_fin_timeout=15

# 4. Membatasi alokasi percobaan ulang pengiriman ulang paket SYN-ACK
sysctl -w net.ipv4.tcp_synack_retries=2

# Menyimpan konfigurasi secara permanen ke file konfigurasi sistem agar tidak hilang saat reboot
cat << EOF >> /etc/sysctl.conf

# --- anti-ddos Kernel Network Tweaks by Mr.Rm19 ---
net.ipv4.tcp_syncookies = 1
net.core.somaxconn = 10240
net.ipv4.tcp_max_syn_backlog = 10240
net.ipv4.tcp_fin_timeout = 15
net.ipv4.tcp_synack_retries = 2
EOF

# Memuat ulang konfigurasi sysctl secara instan
sysctl -p

echo "[$TIMESTAMP] [SYSCTL_TWEAK] Jaringan kernel berhasil dioptimasi untuk mitigasi SYN Flood." >> "$LOG_FILE"
echo "[+] Sukses: Sistem operasi sekarang siap meredam serangan banjir paket jaringan (SYN Flood)!"