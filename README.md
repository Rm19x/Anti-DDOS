#  anti ddos

[![Docker Support](https://img.shields.io/badge/Docker-Supported-blue?logo=docker&logoColor=white)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-v1.0-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Redis](https://img.shields.io/badge/Redis-Cache-red?logo=redis&logoColor=white)](https://redis.io/)
[![Cloudflare Integration](https://img.shields.io/badge/Cloudflare-Edge_Mitigation-orange?logo=cloudflare&logoColor=white)](https://www.cloudflare.com/)

Sistem pertahanan dan mitigasi serangan DDoS otomatis (*Automated Threat Intelligence Suite*) yang dirancang untuk menganalisis log akses web server secara *real-time*, mendeteksi anomali perilaku (*behavioral analysis*), serta mengeksekusi pemblokiran instan langsung di tingkat kernel OS (`iptables`) maupun jaringan global (*Cloudflare Edge*). Dilengkapi dengan Web UI Dashboard modern untuk pemantauan terpusat.

---

##  Fitur Utama

### 1. Deteksi Cerdas & Analisis Perilaku (*Behavioral Analysis*)
* **Dynamic Rate Limiting (RPM)**: Membatasi jumlah request per menit secara dinamis berdasarkan konfigurasi. Ambang batas limit otomatis diperketat ($2\times$ lebih ketat) jika IP mencurigakan mencoba mengakses URI sensitif (seperti `/admin`, `/login`, `/api/v1/auth`).
* **Intelligent Burst Detection**: Mampu mendeteksi serangan banjir *request* berkecepatan tinggi dalam jendela hitungan detik (HTTP Flood) untuk membedakan pengguna biasa dengan script bot serangan.
* **Signature-Based Attack Detection**: Memblokir otomatis perkakas stress-tester populer secara *real-time* seperti *LOIC, HOIC, Xerxes, Slowloris, Hulk, GoldenEye*.
* **Advanced Protection Rules**: Penyaringan ketat terhadap metode HTTP yang diizinkan (`allowed_methods`) serta daftar hitam User-Agent berbahaya (*sqlmap, nikto, dirbuster, Hydra*).
* **GeoIP & ASN Network Inspector**: Memvalidasi lokasi negara (MaxMind GeoIP2) dan jaringan penyedia hosting (ASN) untuk memblokir lalu lintas dari wilayah atau provider yang dinilai berbahaya.

### 2. Eksekutor Jaringan & Pengerasan Keamanan (*Mitigation & Hardening*)
* **Linux Kernel Dropper via `iptables`**: Memutus koneksi IP penyerang secara mutlak menggunakan aksi `DROP` pada rantai firewall `INPUT` mesin host secara otomatis.
* **Cloudflare Global Edge Synchronization**: Jika diaktifkan, sistem akan mengirimkan instruksi pemblokiran ke Cloudflare Firewall Access Rules API, menghentikan penyerang langsung di jaringan terluar sebelum menyentuh server Anda.
* **SYN Flood Kernel Hardening**: Script optimasi stack jaringan Linux untuk mengaktifkan TCP SYN Cookies, menaikkan kapasitas backlog antrean (`somaxconn` & `tcp_max_syn_backlog` ke 10240), serta mempercepat pembersihan koneksi mati.
* **Smart Whitelist Registry Fail-Safe**: Sistem perlindungan berlapis agar IP penting (localhost, IP administrator, IP server, Googlebot) tidak akan pernah terblokir secara tidak sengaja melalui file `whitelist.txt` dan pengecekan memori.

### 3. Pemantauan & Pemulihan Mandiri (*UI & Self-Healing*)
* **Web Monitoring Dashboard**: Panel kontrol UI modern berbasis Tailwind CSS dengan skema warna adaptif (*Dark Mode* / *Light Mode*) untuk memantau aktivitas serangan.
* **Asynchronous Live Polling**: Logika frontend berbasis JavaScript yang melakukan *polling* otomatis setiap 3 detik untuk menyajikan data serangan aktual secara *real-time* tanpa memuat ulang halaman.
* **Manual Unban Management**: Menyediakan kontrol penuh bagi administrator untuk membebaskan IP dari daftar blokir secara manual langsung dari Dashboard UI dengan satu klik (`DELETE` request API).
* **Asynchronous SMTP Notification**: Mengirim notifikasi email alert mendetail (*IP, Alasan, Tindakan Security*) secara *non-blocking* menggunakan *multi-threading* Python agar tidak mengganggu performa utama mesin pembaca log.
* **Autonomous Self-Healing Daemon**: Skrip pengawas independen yang berjalan di host untuk menguji endpoint `/health` internal dan melakukan pemulihan otomatis (*auto-restart*) jika layanan kontainer mengalami *crash*.

---

##  Panduan Cara Pakai

###  Prasyarat Sistem
* Sistem Operasi berbasis **Linux** (Ubuntu 20.04/22.04/24.04 atau distro Debian-*based* lainnya).
* **Docker** dan **Docker Compose** sudah terpasang di server host.
* Web server (**Nginx** atau **Apache**) berjalan di host dan memproduksi file log ke direktori `/var/log`.
* Database MaxMind GeoIP (`GeoLite2-Country.mmdb` dan `GeoLite2-ASN.mmdb`) diletakkan pada direktori `/var/lib/GeoIP/` di server host (jika fitur GeoIP diaktifkan).

###  Langkah-Langkah Deployment

 **Eksekusi Pengerasan Jaringan Jurnal (SYN Flood Hardening)**
 ```
chmod +x firewall/sysctl_tweak.sh
sudo ./firewall/sysctl_tweak.sh   
```
***Konfigurasi Parameter Sistem***

Buka file config.json menggunakan text editor (misal nano) dan sesuaikan parameter batas request, whitelist, serta kredensial API jika diperlukan:
```
{
    "server": {
        "log_paths": ["/var/log/nginx/access.log"],
        "health_check_port": 8000
    },
    "mitigation": {
        "max_requests_per_minute": 60,
        "max_burst_requests": 15,
        "jail_time_seconds": 3600
    }
}
```
 ***Daftarkan IP Aman pada Registry***

Buka file firewall/whitelist.txt dan masukkan IP publik perangkat Anda atau IP server Anda agar tidak terkena pemblokiran otomatis oleh firewall:
```
contoh
127.0.0.1
::1
103.111.22.33
```
***Build dan Jalankan Docker Container***

Jalankan perintah berikut untuk membangun (build) image kontainer dan menjalankannya di latar belakang (detached mode):
```
docker-compose up -d --build
```
Catatan: Aplikasi core dikonfigurasikan menggunakan network_mode: "host" dan kapabilitas NET_ADMIN agar kontainer dapat memanipulasi tabel iptables utama pada mesin host secara legal.

***Aktifkan Daemon Self-Healing***
```
crontab -e
* * * * * /bin/bash /path/to/anti-ddos/self_healing.sh >/dev/null 2>&1
```

**Pemantauan log internalz**

```
tail -f /var/log/anti_ddos_firewall.log
```

<img src="https://raw.githubusercontent.com/Rm19x/Anti-DDOS/refs/heads/main/antiddos.png">

## Author : Mr.Rm19 - ramdan19id@gmail.com 
