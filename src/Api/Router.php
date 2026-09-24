<?php
/**
 * Anti-DDOS by Mr.Rm19
 * GitHub: https://github.com/Rm19x
 * Author: Ramdan Maulana
 */

namespace Rm19x\AntiDdos\Api;

use Rm19x\AntiDdos\Analytics\Reporter;
use Rm19x\AntiDdos\Pusat\IPReputation;

class Router
{
    private IPReputation $reputation;
    private Reporter $reporter;

    public function __construct(IPReputation $reputation, Reporter $reporter)
    {
        $this->reputation = $reputation;
        $this->reporter = $reporter;
    }

    public function handleRequest(): void
    {
        header('Content-Type: application/json');
        $endpoint = $_GET['endpoint'] ?? '';

        switch ($endpoint) {
            case 'stats':
                echo json_encode($this->reporter->generateSummary());
                break;

            case 'block-ip':
                $ip = $_POST['ip'] ?? '';
                if (filter_var($ip, FILTER_VALIDATE_IP)) {
                    $this->reputation->addToBlacklist($ip);
                    echo json_encode(['status' => 'success', 'message' => "IP {$ip} blocked"]);
                } else {
                    echo json_encode(['status' => 'error', 'message' => 'Invalid IP']);
                }
                break;

            default:
                http_response_code(404);
                echo json_encode(['status' => 404, 'message' => 'Endpoint not found']);
                break;
        }
        exit();
    }
}