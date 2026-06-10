@echo off
chcp 65001 >nul
echo.
echo  ============================================
echo   Generateur de Cartes -- Demarrage
echo  ============================================
echo.

if not exist venv (
    echo  Le venv n'existe pas. Lancez setup.bat d'abord.
    pause & exit /b 1
)

call venv\Scripts\activate.bat
python app.py

echo.
echo  Serveur arrete.
pause
