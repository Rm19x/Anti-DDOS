<?php
/**
 * Anti-DDOS by Mr.Rm19
 * GitHub: https://github.com/Rm19x
 * Author: Ramdan Maulana
 */

namespace Rm19x\AntiDdos\Pusat;

class IPReputation
{
    private \Redis $redis;

    public function __construct(\Redis $redis)
    {
        $this->redis = $redis;
    }

    public function isBlacklisted(string $ip): bool
    {
        return (bool)$this->redis->sIsMember("anti_ddos:blacklist", $ip) || (bool)$this->redis->get("anti_ddos:jail:" . $ip);
    }

    public function isWhitelisted(string $ip): bool
    {
        return (bool)$this->redis->sIsMember("anti_ddos:whitelist", $ip);
    }

    public function autoJail(string $ip, int $durationSeconds = 3600): void
    {
        $this->redis->setex("anti_ddos:jail:" . $ip, $durationSeconds, 1);
    }

    public function addToBlacklist(string $ip): void
    {
        $this->redis->sAdd("anti_ddos:blacklist", $ip);
    }

    public function addToWhitelist(string $ip): void
    {
        $this->redis->sAdd("anti_ddos:whitelist", $ip);
    }
}