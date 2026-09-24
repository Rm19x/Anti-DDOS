<?php
/**
 * Anti-DDOS by Mr.Rm19
 * GitHub: https://github.com/Rm19x
 * Author: Ramdan Maulana
 */

return [
    'app_name' => 'Anti-DDOS by Mr.Rm19',
    'version' => '1.0.0',
    'under_attack_mode' => false,
    'rate_limit' => [
        'max_requests' => 60,
        'time_window' => 60,
        'burst_limit' => 15,
        'burst_window' => 5,
    ],
    'redis' => [
        'host' => '127.0.0.1',
        'port' => 6379,
        'timeout' => 2.5,
    ],
];