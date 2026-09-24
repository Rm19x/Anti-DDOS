<?php
/**
 * Anti-DDOS by Mr.Rm19
 * GitHub: https://github.com/Rm19x
 * Author: Ramdan Maulana
 */

$token = $_GET['token'] ?? '';
?>
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Anti-DDOS by Mr.Rm19 - Verification</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #0d1117; color: #c9d1d9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .box { background: #161b22; padding: 30px; border-radius: 8px; border: 1px solid #30363d; text-align: center; max-width: 400px; }
        h2 { color: #58a6ff; margin-bottom: 10px; }
        .spinner { border: 4px solid #30363d; border-top: 4px solid #58a6ff; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 20px auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="box">
        <h2>Anti-DDOS by Mr.Rm19</h2>
        <p>Memeriksa browser Anda sebelum melanjutkan...</p>
        <div class="spinner"></div>
    </div>
    <script src="assets/js/fingerprint.js"></script>
    <script>
        setTimeout(function() {
            document.cookie = "rm19_token=<?php echo htmlspecialchars($token, ENT_QUOTES, 'UTF-8'); ?>; path=/";
            location.reload();
        }, 3000);
    </script>
</body>
</html>