# ==============================================================================
# Project: anti-ddos (Email Alerting System)
# Author: Mr.Rm19
# GitHub: https://github.com/Rm19x
# Description: Secure SMTP async notification engine.
# ==============================================================================

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading

class AntiDDoSNotifier:
    def __init__(self, config):
        self.config = config
        self.email_cfg = config.get("alerting", {}).get("email", {})[cite: 2]
        self.enabled = self.email_cfg.get("enabled", False)[cite: 2]

    def _send_email_worker(self, ip, reason):
        """Fungsi pekerja internal yang berjalan di thread terpisah (Non-Blocking)."""
        try:
            smtp_server = self.email_cfg.get("smtp_server")[cite: 2]
            smtp_port = self.email_cfg.get("smtp_port")[cite: 2]
            sender = self.email_cfg.get("sender_email")[cite: 2]
            receiver = self.email_cfg.get("receiver_email")[cite: 2]
            password = self.email_cfg.get("smtp_password")[cite: 2]

            # Inisialisasi Konten Email
            msg = MIMEMultipart()
            msg['From'] = f"anti-ddos Guard <{sender}>"
            msg['To'] = receiver
            msg['Subject'] = f"[ALERT] DDoS Attack Blocked Successfully on Your Server!"

            body = f"""
            Dear Sahabat,

            Sistem pertahanan keamanan 'anti-ddos' yang dikembangkan oleh Mr.Rm19 telah mendeteksi dan menggagalkan serangan baru pada infrastruktur web server Anda.

            Berikut adalah rincian ancaman yang berhasil diredam:
            -------------------------------------------------------------
            [!] Alamat IP Penyerang : {ip}
            [!] Alasan Pemblokiran  : {reason}
            [!] Tindakan Keamanan   : Drop Connection via Linux Firewall (iptables)
            -------------------------------------------------------------

            Sistem akan terus memantau lalu lintas jaringan secara real-time demi menjaga kestabilan domain sahabat.

            Salam Keamanan,
            anti-ddos Security Core (by Mr.Rm19)
            GitHub: https://github.com/Rm19x
            """
            msg.attach(MIMEText(body, 'plain'))

            # Proses Pengiriman via SMTP SSL/TLS
            server = smtplib.SMTP(smtp_server, smtp_port)[cite: 2]
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
            server.quit()
            print(f"[+] Notifikasi Email berhasil dikirim ke {receiver} untuk IP {ip}.")
        except Exception as e:
            print(f"[-] Gagal mengirim Email Alert via SMTP: {e}")

    def send_attack_alert(self, ip, reason):
        """Memicu pengiriman email tanpa mengganggu performa utama analyzer."""
        if not self.enabled:
            return

        # Menggunakan Threading agar program utama pembaca log tidak hang/menunggu SMTP response
        email_thread = threading.Thread(target=self._send_email_worker, args=(ip, reason))
        email_thread.daemon = True
        email_thread.start()