# Script pour arrêter le serveur backend Kissa
# Double-cliquez sur ce fichier ou exécutez-le depuis PowerShell

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ARRÊT DU SERVEUR BACKEND" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Arrêter les processus Python/uvicorn liés à Kissa
$processes = Get-Process | Where-Object {
    ($_.ProcessName -like "*python*" -or $_.ProcessName -like "*uvicorn*") -and
    $_.Path -like "*kissa*"
}

if ($processes) {
    Write-Host "🛑 Arrêt de $($processes.Count) processus..." -ForegroundColor Yellow
    $processes | Stop-Process -Force
    Start-Sleep -Seconds 1
    Write-Host "✅ Serveur backend arrêté" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Aucun processus backend actif" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

