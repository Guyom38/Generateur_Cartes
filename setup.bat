@echo off
chcp 65001 >nul
echo.
echo  ============================================
echo   Generateur de Cartes -- Installation
echo  ============================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo  ERREUR : Python n'est pas installe ou absent du PATH.
    echo  Telechargez Python sur https://www.python.org/
    echo.
    pause
    exit /b 1
)

echo  [1/3] Creation de l'environnement virtuel...
python -m venv venv
if errorlevel 1 (
    echo  ERREUR lors de la creation du venv.
    pause & exit /b 1
)

echo  [2/3] Activation du venv...
call venv\Scripts\activate.bat

echo  [3/3] Installation des dependances...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo  ERREUR lors de pip install.
    pause & exit /b 1
)

echo.
echo  Installation terminee !
echo  Lancez start.bat pour demarrer l'application.
echo.
pause
