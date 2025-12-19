@echo off
REM Script batch pour lancer le frontend Kissa
REM Double-cliquez sur ce fichier

echo.
echo ========================================
echo   FRONTEND KISSA - DEMARRAGE
echo ========================================
echo.
echo Le frontend sera accessible sur : http://localhost:3000
echo Pour arreter, appuyez sur Ctrl+C
echo.
echo ========================================
echo.

cd /d "%~dp0"

REM Vérifier que node_modules existe
if not exist "node_modules" (
    echo Installation des dependances...
    call npm install
)

REM Lancer le serveur de développement
call npm run dev

echo.
echo Frontend arrete.
pause

