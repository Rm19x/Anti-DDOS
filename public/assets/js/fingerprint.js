/**
 * Anti-DDOS by Mr.Rm19
 * GitHub: https://github.com/Rm19x
 * Author: Ramdan Maulana
 */

(function() {
    function getCanvasFingerprint() {
        var canvas = document.createElement('canvas');
        var ctx = canvas.getContext('2d');
        ctx.textBaseline = "top";
        ctx.font = "14px 'Arial'";
        ctx.textBaseline = "alphabetic";
        ctx.fillStyle = "#f60";
        ctx.fillRect(125,1,62,20);
        ctx.fillStyle = "#069";
        ctx.fillText("Rm19x", 2, 15);
        ctx.fillStyle = "rgba(102, 204, 0, 0.7)";
        ctx.fillText("Rm19x", 4, 17);
        return canvas.toDataURL();
    }

    window.Rm19Fingerprint = {
        getFP: function() {
            return getCanvasFingerprint();
        }
    };
})();