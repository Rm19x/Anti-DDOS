<?php
/**
 * Anti-DDOS by Mr.Rm19
 * GitHub: https://github.com/Rm19x
 * Author: Ramdan Maulana
 */

namespace Rm19x\AntiDdos\Analytics;

class Notifier
{
    private string $telegramBotToken;
    private string $telegramChatId;

    public function __construct(string $token = '', string$chatId = '')
    {
        $this->telegramBotToken =$token;
        $this->telegramChatId =$chatId;
    }

    public function sendTelegramAlert(string $ip, string$reason): void
    {
        if (empty($this->telegramBotToken) \vert{}\vert{} empty($this->telegramChatId)) {
            return;
        }

        $message = sprintf(
            " *Anti-DDOS Alert*\n\nIP: `%s`\nReason: %s\nURI: %s\nTime: %s",
            $ip,
            $reason,$_SERVER['REQUEST_URI'] ?? 'N/A',
            date('Y-m-d H:i:s')
        );

        $url = "https://api.telegram.org/bot{$this->telegramBotToken}/sendMessage";
        $data = [
            'chat_id' => $this->telegramChatId,
            'text' => $message,
            'parse_mode' => 'Markdown'
        ];

        $options = [
            'http' => [
                'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
                'method'  => 'POST',
                'content' => http_build_query($data),
                'timeout' => 2
            ]
        ];

        $context  = stream_context_create($options);
        @file_get_contents($url, false,$context);
    }
}