# Script pour lancer le frontend Kissa
# Double-cliquez sur ce fichier ou exécutez-le depuis PowerShell

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  FRONTEND KISSA - DÉMARRAGE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Le frontend sera accessible sur : http://localhost:3000" -ForegroundColor Yellow
Write-Host "Pour arrêter, appuyez sur Ctrl+C" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier que node_modules existe
if (-not (Test-Path "node_modules")) {
    Write-Host "Installation des dépendances..." -ForegroundColor Yellow
    npm install
}

# Lancer le serveur de développement
npm run dev

# Si le serveur s'arrête
Write-Host ""
Write-Host "Frontend arrêté." -ForegroundColor Red
Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

