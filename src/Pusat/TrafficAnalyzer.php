<?php
/**
 * Anti-DDOS by Mr.Rm19
 * GitHub: https://github.com/Rm19x
 * Author: Ramdan Maulana
 */

namespace Rm19x\AntiDdos\Pusat;

class TrafficAnalyzer
{
    private \Redis $redis;
    private array $config;

    public function __construct(\Redis $redis, array $config)
    {
        $this->redis = $redis;
        $this->config = $config;
    }

    public function analyzeRequest(string $ip): bool
    {
        if ($this->isSlowHttpAttack()) {
            return false;
        }

        if ($this->isPayloadExceeded()) {
            return false;
        }

        return $this->checkRateLimit($ip) && $this->checkBurstLimit($ip);
    }

    private function checkRateLimit(string $ip): bool
    {
        $key = "anti_ddos:rate:" . $ip;
        $max = $this->config['rate_limit']['max_requests'];
        $window = $this->config['rate_limit']['time_window'];

        $current = $this->redis->get($key);

        if ($current && (int)$current >= $max) {
            return false;
        }

        if (!$current) {
            $this->redis->setex($key, $window, 1);
        } else {
            $this->redis->incr($key);
        }

        return true;
    }

    private function checkBurstLimit(string $ip): bool
    {
        $key = "anti_ddos:burst:" . $ip;
        $max = $this->config['rate_limit']['burst_limit'];
        $window = $this->config['rate_limit']['burst_window'];

        $current = $this->redis->get($key);

        if ($current && (int)$current >= $max) {
            return false;
        }

        if (!$current) {
            $this->redis->setex($key, $window, 1);
        } else {
            $this->redis->incr($key);
        }

        return true;
    }

    private function isSlowHttpAttack(): bool
    {
        if (isset($_SERVER['CONTENT_LENGTH']) && empty($_POST) && $_SERVER['REQUEST_METHOD'] === 'POST') {
            return true;
        }
        return false;
    }

    private function isPayloadExceeded(): bool
    {
        $maxSize = 10 * 1024 * 1024;
        if (isset($_SERVER['CONTENT_LENGTH']) && (int)$_SERVER['CONTENT_LENGTH'] > $maxSize) {
            return true;
        }
        return false;
    }
}