<?php
/**
 * Anti-DDOS by Mr.Rm19
 * GitHub: https://github.com/Rm19x
 * Author: Ramdan Maulana
 */

namespace Rm19x\AntiDdos\Analytics;

class Logger
{
    private string $logFile;

    public function __construct(string $logPath = __DIR__ . '/../../storage/logs/attack.log')
    {
        $this->logFile = $logPath;
    }

    public function logBlockedRequest(string $ip, string $reason): void
    {
        $directory = dirname($this->logFile);
        if (!is_dir($directory)) {
            @mkdir($directory, 0755, true);
        }

        $entry = sprintf(
            "[%s] IP: %s | Reason: %s | URI: %s | UA: %s\n",
            date('Y-m-d H:i:s'),
            $ip,
            $reason,
            $_SERVER['REQUEST_URI'] ?? 'N/A',
            $_SERVER['HTTP_USER_AGENT'] ?? 'N/A'
        );

        file_put_contents($this->logFile, $entry, FILE_APPEND | LOCK_EX);
    }
}