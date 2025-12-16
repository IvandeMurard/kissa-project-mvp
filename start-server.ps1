# Script pour lancer le serveur Kissa avec logs visibles
# Double-cliquez sur ce fichier ou exécutez-le depuis PowerShell

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SERVEUR KISSA - DÉMARRAGE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Les logs apparaîtront ci-dessous en temps réel." -ForegroundColor Yellow
Write-Host "Pour arrêter le serveur, appuyez sur Ctrl+C" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Activer l'environnement virtuel
& ".\venv\Scripts\Activate.ps1"

# Forcer Python à ne pas bufferiser les sorties pour voir les logs en temps réel
$env:PYTHONUNBUFFERED = "1"

# Lancer le serveur
uvicorn api:app --reload --host 127.0.0.1 --port 8000

# Si le serveur s'arrête, afficher un message
Write-Host ""
Write-Host "Serveur arrêté." -ForegroundColor Red
Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# --- Arrêter le serveur Kissa (kill) ---
# Cette partie permet de terminer tous les processus uvicorn (équivalent batch)
Get-Process uvicorn -ErrorAction SilentlyContinue | ForEach-Object {
    try {
        Stop-Process -Id $_.Id -Force
        Write-Host "Processus uvicorn arrêté. (kill)" -ForegroundColor Red
    } catch {
        Write-Host "Impossible d'arrêter uvicorn (non trouvé ou déjà stoppé)." -ForegroundColor Yellow
    }
}

# --- Nettoyer les fichiers temporaires créés lors de l'analyse de vinyles ---
# Supprime tous les fichiers commençant par "temp_" dans le dossier courant
$tempFiles = Get-ChildItem -Path . -Filter "temp_*" -File -ErrorAction SilentlyContinue
foreach ($file in $tempFiles) {
    try {
        Remove-Item $file.FullName -Force
        Write-Host ("Supprimé: " + $file.Name) -ForegroundColor DarkGray
    } catch {
        Write-Host ("Erreur suppression: " + $file.Name) -ForegroundColor Yellow
    }
}
Write-Host ""
Write-Host "Démarrage du serveur Kissa..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"
$env:PYTHONUNBUFFERED = "1"
uvicorn api:app --reload --host 127.0.0.1 --port 8000
