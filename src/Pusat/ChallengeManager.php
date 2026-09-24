<?php
/**
 * Anti-DDOS by Mr.Rm19
 * GitHub: https://github.com/Rm19x
 * Author: Ramdan Maulana
 */

namespace Rm19x\AntiDdos\Pusat;

class ChallengeManager
{
    private \Redis $redis;

    public function __construct(\Redis $redis)
    {
        $this->redis = $redis;
    }

    public function requireJsChallenge(string $ip): void
    {
        $token = bin2hex(random_bytes(16));
        $this->redis->setex("anti_ddos:challenge:" . $ip, 300, $token);

        http_response_code(503);
        header('Content-Type: text/html; charset=utf-8');
        echo '<!DOCTYPE html><html><head><title>Just a moment...</title>';
        echo '<script>setTimeout(function(){ document.cookie = "rm19_token=' . $token . '; path=/"; location.reload(); }, 3000);</script>';
        echo '</head><body><h2>Verifying your browser before accessing the site...</h2><p>Anti-DDOS by Mr.Rm19</p></body></html>';
        exit();
    }

    public function verifyChallenge(string $ip): bool
    {
        $cookieToken = $_COOKIE['rm19_token'] ?? '';
        $storedToken = $this->redis->get("anti_ddos:challenge:" . $ip);

        if ($storedToken && $cookieToken === $storedToken) {
            return true;
        }
        return false;
    }
}