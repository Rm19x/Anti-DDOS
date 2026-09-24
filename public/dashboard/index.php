<?php
/**
 * Anti-DDOS by Mr.Rm19
 * GitHub: https://github.com/Rm19x
 * Author: Ramdan Maulana
 */

require_once __DIR__ . '/../../src/Analytics/Reporter.php';

use Rm19x\AntiDdos\Analytics\Reporter;

$reporter = new Reporter();
$data = $reporter->generateSummary();
?>
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Dashboard - Anti-DDOS by Mr.Rm19</title>
    <style>
        body { font-family: monospace; background: #0f172a; color: #f8fafc; padding: 20px; }
        .card { background: #1e293b; padding: 20px; border-radius: 6px; margin-bottom: 20px; border: 1px solid #334155; }
        h1, h2 { color: #38bdf8; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #334155; padding: 8px; text-align: left; }
        th { background: #0f172a; color: #38bdf8; }
    </style>
</head>
<body>
    <h1>Anti-DDOS by Mr.Rm19 - Live Dashboard</h1>
    
    <div class="card">
        <h2>Total Request Diblokir: <?php echo $data['total_blocked']; ?></h2>
    </div>

    <div class="card">
        <h2>Top 10 IP Penyerang</h2>
        <table>
            <tr><th>Alamat IP</th><th>Jumlah Blokir</th></tr>
            <?php foreach ($data['top_ips'] as $ip => $count): ?>
            <tr><td><?php echo htmlspecialchars($ip); ?></td><td><?php echo $count; ?></td></tr>
            <?php endforeach; ?>
        </table>
    </div>

    <div class="card">
        <h2>Kategori Alasan Blokir</h2>
        <table>
            <tr><th>Alasan</th><th>Frekuensi</th></tr>
            <?php foreach ($data['reasons'] as $reason => $count): ?>
            <tr><td><?php echo htmlspecialchars($reason); ?></td><td><?php echo $count; ?></td></tr>
            <?php endforeach; ?>
        </table>
    </div>
</body>
</html>