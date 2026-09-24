<?php
/**
 * Anti-DDOS by Mr.Rm19
 * GitHub: https://github.com/Rm19x
 * Author: Ramdan Maulana
 */

namespace Rm19x\AntiDdos\Analytics;

class Reporter
{
    private string $logFile;

    public function __construct(string $logPath = __DIR__ . '/../../storage/logs/attack.log')
    {
        $this->logFile = $logPath;
    }

    public function generateSummary(): array
    {
        if (!file_exists($this->logFile)) {
            return [
                'total_blocked' => 0,
                'top_ips' => [],
                'reasons' => []
            ];
        }

        $lines = file($this->logFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
        $totalBlocked = count($lines);
        $ipCounts = [];
        $reasonCounts = [];

        foreach ($lines as $line) {
            if (preg_match('/IP:\s*(\S+)\s*\|\s*Reason:\s*([^|]+)/', $line, $matches)) {
                $ip = $matches[1];
                $reason = trim($matches[2]);

                $ipCounts[$ip] = ($ipCounts[$ip] ?? 0) + 1;
                $reasonCounts[$reason] = ($reasonCounts[$reason] ?? 0) + 1;
            }
        }

        arsort($ipCounts);
        arsort($reasonCounts);

        return [
            'total_blocked' => $totalBlocked,
            'top_ips' => array_slice($ipCounts, 0, 10, true),
            'reasons' => $reasonCounts
        ];
    }
}