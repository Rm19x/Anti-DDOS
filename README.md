# Anti-DDOS by Mr.Rm19

Anti-DDOS by Mr.Rm19  pustaka keamanan berbasis PHP dan Redis yang dirancang untuk memberikan perlindungan   dari serangan Denial of Service (DoS/DDoS), scraping otomatis, serta aktivitas bot berbahaya.

## rootz@Rmd.n3i :~#

Proyek ini dibangun menggunakan arsitektur  berorientasi objek yang dibagi menjadi beberapa komponen utama:

- Pusat : Mengelola analisis lalu lintas, kalkulasi ambang batas request (rate limiting), deteksi perilaku bot, tantangan JavaScript, serta manajemen reputasi IP.
- Analytics: Mengelola pencatatan insiden serangan, sistem notifikasi Telegram, dan pembuatan laporan rekapitulasi.
- API: Menyediakan endpoint RESTful untuk integrasi dan pengontrolan pihak ketiga.
- Public & Dashboard: Antarmuka tantangan verifikasi pengguna dan dasbor pemantauan kondisi lalu lintas secara langsung.

##  Sistem

- PHP 
- Ekstensi PHP Redis
- Ekstensi PHP JSON



## Cara Penggunaan

Pastikan Redis server sudah berjalan di lingkungan server Anda.

Tempatkan folder proyek di dalam direktori aplikasi web Anda.

Muat berkas bootstrap.php pada titik masuk (entry point) utama aplikasi web Anda, sebelum kode lain dieksekusi:
```text
<?php
require_once __DIR__ . '/anti-ddos-mr-rm19/bootstrap.php';

// Kode aplikasi web Anda
```
---
## fiture
- Adaptive Dynamic Rate Limiting & Burst Protection

- Behavioral Threat Scoring & Headless Browser Detection

- JavaScript Challenge Verification

- IP Blacklisting, Whitelisting, dan Auto-Jail berbasis Redis

- Web Application Firewall (Penginspeksian SQLi dan XSS)

- Integrasi Notifikasi Alert Telegram

- Dasbor Pemantauan Lalu Lintas Real-Time
---
