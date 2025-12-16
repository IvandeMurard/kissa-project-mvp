@echo off
REM Script batch pour lancer le serveur Kissa
REM Double-cliquez sur ce fichier

echo.
echo ========================================
echo   SERVEUR KISSA - DEMARRAGE
echo ========================================
echo.
echo Les logs apparaîtront ci-dessous en temps reel.
echo Pour arreter le serveur, appuyez sur Ctrl+C
echo.
echo ========================================
echo.

cd /d "%~dp0"
call venv\Scripts\activate.bat

REM Forcer Python à ne pas bufferiser les sorties pour voir les logs en temps réel
set PYTHONUNBUFFERED=1

uvicorn api:app --reload --host 127.0.0.1 --port 8000

echo.
echo Serveur arrete.
pause

REM Alternative : Lancement sans mode --reload (prod)
REM Pour lancer en mode production, décommentez la ligne suivante et commentez la ligne avec --reload ci-dessus :
REM uvicorn api:app --host 127.0.0.1 --port 8000
REM Pour arrêter le serveur automatiquement (processus batch), décommentez la ligne suivante :
REM taskkill /F /IM "uvicorn.exe"
REM --- Arrêter le serveur Kissa (kill) ---
REM Cette commande termine tous les processus uvicorn.exe
taskkill /F /IM "uvicorn.exe" >nul 2>&1
echo Serveur Kissa stoppé (kill).
REM Nettoyer les fichiers temporaires créés lors de l'analyse de vinyles
REM Supprime tous les fichiers commençant par "temp_" dans le dossier courant
del /Q temp_*

REM (Facultatif) Afficher le nombre de fichiers supprimés
REM for %%f in (temp_*) do echo Supprime: %%f
REM --- DEMARRER LE SERVEUR ---
echo Démarrage du serveur Kissa...
call venv\Scripts\activate.bat
set PYTHONUNBUFFERED=1
uvicorn api:app --reload --host 127.0.0.1 --port 8000

REM --- Arrêter le serveur Kissa (kill) ---
taskkill /F /IM "uvicorn.exe" >nul 2>&1
echo Serveur Kissa stoppé (kill).
Get-Process | Where-Object {$_.ProcessName -like "*python*" -or $_.ProcessName -like "*uvicorn*"} | Where-Object {$_.Path -like "*kissa*"} | Stop-Process -Force
REM --- Arrêt complète des processus python/uvicorn liés à Kissa (équivalent PowerShell) ---
REM Nécessite PowerShell : Arrête tous les processus Python/uvicorn dans le dossier "kissa"
powershell -Command "Get-Process | Where-Object { ($_.ProcessName -like '*python*' -or $_.ProcessName -like '*uvicorn*') -and $_.Path -like '*kissa*' } | Stop-Process -Force"
echo Relance du serveur Kissa...
call venv\Scripts\activate.bat
set PYTHONUNBUFFERED=1
uvicorn api:app --reload --host 127.0.0.1 --port 8000
REM --- Arrêter tous les processus Kissa python/uvicorn (kill complet) ---
REM (Option batch + PowerShell pour couvrir tous les cas)
taskkill /F /IM "uvicorn.exe" >nul 2>&1
taskkill /F /IM "python.exe" >nul 2>&1
powershell -Command "Get-Process | Where-Object { ($_.ProcessName -like '*python*' -or $_.ProcessName -like '*uvicorn*') -and $_.Path -like '*kissa*' } | Stop-Process -Force"
echo Tous les processus Kissa ont été stoppés.
cd /d "%~dp0"
call venv\Scripts\activate.bat
set PYTHONUNBUFFERED=1
uvicorn api:app --reload --host 127.0.0.1 --port 8000
