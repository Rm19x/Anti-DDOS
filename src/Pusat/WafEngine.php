<?php
/**
 * Anti-DDOS by Mr.Rm19
 * GitHub: https://github.com/Rm19x
 * Author: Ramdan Maulana
 */

namespace Rm19x\AntiDdos\Pusat;

class WafEngine
{
    private array $sqliPatterns = [
        '/union\s+select/i',
        '/select\s+.*\s+from/i',
        '/insert\s+into/i',
        '/drop\s+database/i',
        '/drop\s+table/i'
    ];

    private array $xssPatterns = [
        '/<script\b[^>]*>(.*?)<\/script>/is',
        '/javascript\s*:/i',
        '/onerror\s*=/i',
        '/onload\s*=/i'
    ];

    public function inspectPayload(): bool
    {
        $input = file_get_contents('php://input') . json_encode($_GET) . json_encode($_POST);

        foreach ($this->sqliPatterns as $pattern) {
            if (preg_match($pattern, $input)) {
                return false;
            }
        }

        foreach ($this->xssPatterns as $pattern) {
            if (preg_match($pattern, $input)) {
                return false;
            }
        }

        return true;
    }
}