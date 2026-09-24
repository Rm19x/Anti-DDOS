<?php
/**
 * Anti-DDOS by Mr.Rm19
 * GitHub: https://github.com/Rm19x
 * Author: Ramdan Maulana
 */

require_once __DIR__ . '/src/Pusat/TrafficAnalyzer.php';

use Rm19x\AntiDdos\Pusat\TrafficAnalyzer;

$config = require __DIR__ . '/config/app.php';

try {
    $redis = new Redis();
    $redis->connect($config['redis']['host'], $config['redis']['port'], $config['redis']['timeout']);
} catch (\Exception $e) {
    return;
}

$clientIp = $_SERVER['HTTP_CF_CONNECTING_IP'] 
    ?? $_SERVER['HTTP_X_FORWARDED_FOR'] 
    ?? $_SERVER['REMOTE_ADDR'] 
    ?? '0.0.0.0';

if (strpos($clientIp, ',') !== false) {
    $clientIp = trim(explode(',', $clientIp)[0]);
}

$analyzer = new TrafficAnalyzer($redis, $config);

if (!$analyzer->analyzeRequest($clientIp)) {
    http_response_code(429);
    header('Content-Type: application/json');
    header('Retry-After: 60');
    echo json_encode([
        'status' => 429,
        'error' => 'Too Many Requests',
        'message' => 'Blocked by Anti-DDOS by Mr.Rm19'
    ]);
    exit();
}