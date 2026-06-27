/* ==============================================================================
 * Project: anti-ddos (Dashboard Core Logic Engine)
 * Author: Mr.Rm19
 * GitHub: https://github.com/Rm19x
 * Description: Asynchronous API polling, theme switcher, and manual unban handlers.
 * ============================================================================== */

document.addEventListener("DOMContentLoaded", () => {
    const htmlElement = document.documentElement;
    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');

    // 1. [Fitur 29] Logika Pengendali Tema (Dark / Light Mode)
    themeToggleBtn.addEventListener('click', () => {
        if (htmlElement.classList.contains('dark')) {
            htmlElement.classList.remove('dark');
            themeIcon.className = "fa-solid fa-moon";
            localStorage.setItem('theme', 'light');
        } else {
            htmlElement.classList.add('dark');
            themeIcon.className = "fa-solid fa-sun";
            localStorage.setItem('theme', 'dark');
        }
    });

    // Sinkronisasi tema tersimpan di local storage browser
    if (localStorage.getItem('theme') === 'light') {
        htmlElement.classList.remove('dark');
        themeIcon.className = "fa-solid fa-moon";
    }

    // Eksekusi pemuatan data perdana saat halaman siap
    fetchAttackData();
    checkServerHealth();

    // 2. Loop Polling Otomatis: Sinkronisasi data live setiap 3 detik sekali
    setInterval(() => {
        fetchAttackData();
        checkServerHealth();
    }, 3000);
});

// Format bilangan detik menjadi string Menit:Detik yang mudah dibaca manusia
function formatTime(seconds) {
    if (seconds < 0) return "Permanent / Expired";
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}m ${secs}s`;
}

// [Fitur 22] Mengambil Data Serangan Nyata dari Backend API FastAPI
async function fetchAttackData() {
    try {
        const response = await fetch('/api/v1/attacks');
        const data = await response.json();
        
        document.getElementById('stat-total-blocked').innerText = data.total_blocked;
        
        const tbody = document.getElementById('attacker-table-body');
        const noAttacksMsg = document.getElementById('no-attacks-msg');
        tbody.innerHTML = '';

        if (data.total_blocked === 0) {
            noAttacksMsg.classList.remove('hidden');
        } else {
            noAttacksMsg.classList.add('hidden');
            data.attackers.forEach(attacker => {
                const tr = document.createElement('tr');
                tr.className = "hover:bg-gray-50/50 dark:hover:bg-gray-700/30 transition attack-radar-effect";
                tr.innerHTML = `
                    <td class="px-6 py-4 font-mono font-bold text-red-500 dark:text-red-400">${attacker.ip}</td>
                    <td class="px-6 py-4"><span class="bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300 px-2 py-1 rounded text-xs font-medium">${attacker.reason}</span></td>
                    <td class="px-6 py-4 font-medium"><i class="fa-regular fa-clock mr-1 text-gray-400"></i> ${formatTime(attacker.remaining_jail_time_sec)}</td>
                    <td class="px-6 py-4 text-right">
                        <button onclick="releaseIp('${attacker.ip}')" class="text-xs bg-green-500 hover:bg-green-600 text-white font-semibold px-3 py-1.5 rounded-lg shadow-sm transition">
                            <i class="fa-solid fa-unlock mr-1"></i> Unban
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }
    } catch (error) {
        console.error("[-] Gagal memuat data mitigasi serangan:", error);
    }
}

// Fungsi Eksekutor Tombol Manual Melepas Blokir IP via DELETE Request API
async function releaseIp(ip) {
    if (confirm(`Apakah Anda yakin ingin membebaskan IP ${ip} sekarang?`)) {
        try {
            const response = await fetch(`/api/v1/unban/${ip}`, { method: 'DELETE' });
            if (response.ok) {
                fetchAttackData();
            } else {
                alert("Gagal membebaskan IP target dari memory cache.");
            }
        } catch (error) {
            console.error("[-] Error saat eksekusi unban:", error);
        }
    }
}

// [Fitur 50] Pengecekan Kesehatan Endpoint Integrasi Sistem
async function checkServerHealth() {
    const healthStatus = document.getElementById('stat-health');
    try {
        const response = await fetch('/health');
        if (response.ok) {
            healthStatus.innerText = "ONLINE";
            healthStatus.className = "text-3xl font-bold mt-1 text-green-500";
        } else {
            healthStatus.innerText = "ERROR";
            healthStatus.className = "text-3xl font-bold mt-1 text-yellow-500";
        }
    } catch {
        healthStatus.innerText = "OFFLINE";
        healthStatus.className = "text-3xl font-bold mt-1 text-red-500";
    }
}
