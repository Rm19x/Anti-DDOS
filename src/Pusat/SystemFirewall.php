<?php
/**
 * Anti-DDOS by Mr.Rm19
 * GitHub: https://github.com/Rm19x
 * Author: Ramdan Maulana
 */

namespace Rm19x\AntiDdos\Pusat;

class SystemFirewall
{
    private bool $enableFail2ban;

    public function __construct(bool $enableFail2ban = false)
    {
        $this->enableFail2ban = $enableFail2ban;
    }

    public function banIpAtOsLevel(string $ip): void
    {
        if (!$this->enableFail2ban) {
            return;
        }

        if (filter_var($ip, FILTER_VALIDATE_IP)) {
            $command = sprintf("sudo iptables -A INPUT -s %s -j DROP", escapeshellarg($ip));
            @exec($command);
        }
    }

    public function unbanIpAtOsLevel(string $ip): void
    {
        if (!$this->enableFail2ban) {
            return;
        }

        if (filter_var($ip, FILTER_VALIDATE_IP)) {
            $command = sprintf("sudo iptables -D INPUT -s %s -j DROP", escapeshellarg($ip));
            @exec($command);
        }
    }
}