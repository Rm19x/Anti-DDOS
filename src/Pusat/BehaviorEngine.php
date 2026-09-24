<?php
/**
 * Anti-DDOS by Mr.Rm19
 * GitHub: https://github.com/Rm19x
 * Author: Ramdan Maulana
 */

namespace Rm19x\AntiDdos\Pusat;

class BehaviorEngine
{
    private \Redis $redis;

    public function __construct(\Redis $redis)
    {
        $this->redis = $redis;
    }

    public function evaluateThreatScore(string $ip): int
    {
        $score = 0;

        if ($this->isKnownHeadlessBrowser()) {
            $score += 50;
        }

        if ($this->isUserAgentSpoofed()) {
            $score += 30;
        }

        if (!$this->hasValidReferer()) {
            $score += 10;
        }

        return $score;
    }

    private function isKnownHeadlessBrowser(): bool
    {
        $userAgent = strtolower($_SERVER['HTTP_USER_AGENT'] ?? '');
        $headlessSignatures = ['headlesschrome', 'puppeteer', 'selenium', 'playwright', 'phantomjs', 'python-requests'];

        foreach ($headlessSignatures as $sig) {
            if (strpos($userAgent, $sig) !== false) {
                return true;
            }
        }
        return false;
    }

    private function isUserAgentSpoofed(): bool
    {
        $userAgent = $_SERVER['HTTP_USER_AGENT'] ?? '';
        if (empty($userAgent) || strlen($userAgent) < 10) {
            return true;
        }
        return false;
    }

    private function hasValidReferer(): bool
    {
        if ($_SERVER['REQUEST_METHOD'] === 'POST' && empty($_SERVER['HTTP_REFERER'])) {
            return false;
        }
        return true;
    }
}