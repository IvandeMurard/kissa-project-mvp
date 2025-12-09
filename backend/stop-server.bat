@echo off
REM Script batch pour arrêter le serveur backend Kissa
REM Double-cliquez sur ce fichier

echo.
echo ========================================
echo   ARRET DU SERVEUR BACKEND
echo ========================================
echo.

REM Arrêter tous les processus uvicorn
taskkill /F /IM "uvicorn.exe" >nul 2>&1

REM Arrêter les processus Python liés à Kissa (si possible)
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST ^| findstr /I "PID"') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo Serveur backend arrete.
echo.
pause

