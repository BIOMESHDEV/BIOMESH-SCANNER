@echo off
setlocal EnableDelayedExpansion
title BIOMESH V4.0 - Diagnostic et Resolution by Brisk

:: ============================================================
::   BIOMESH V4.0 — by Brisk
::   run.bat — Lanceur avec elevation administrateur
:: ============================================================

:: Verification droits admin
net session >nul 2>&1
if %errorlevel% equ 0 goto :ADMIN_OK

:ELEVATE
cls
echo.
echo  ============================================================
echo   BIOMESH V4.0 - Elevation des privileges...
echo   Ce script requiert les droits Administrateur.
echo  ============================================================
echo.
powershell -NoProfile -Command "Start-Process cmd.exe -ArgumentList '/c cd /d \"%~dp0\" ^&^& \"%~f0\"' -Verb RunAs"
exit /b 0

:ADMIN_OK
cls
cd /d "%~dp0"

:: Activer ANSI
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1

:: Activer UTF-8 apres les echos
chcp 65001 >nul 2>&1

:: Couleurs ANSI
set "RST=[0m"
set "BLD=[1m"
set "DIM=[2m"
set "B1=[38;5;27m"
set "B2=[38;5;33m"
set "B3=[38;5;39m"
set "B4=[38;5;45m"
set "B5=[38;5;51m"
set "GRN=[92m"
set "YLW=[93m"
set "RED=[91m"
set "WHT=[97m"

echo.
echo  %B1%======================================================================%RST%
echo.
echo  %B2%  ██████╗ ██╗ ██████╗ ███╗   ███╗███████╗███████╗██╗  ██╗%RST%
echo  %B3%  ██╔══██╗██║██╔═══██╗████╗ ████║██╔════╝██╔════╝██║  ██║%RST%
echo  %B4%  ██████╔╝██║██║   ██║██╔████╔██║█████╗  ███████╗███████║%RST%
echo  %B3%  ██╔══██╗██║██║   ██║██║╚██╔╝██║██╔══╝  ╚════██║██╔══██║%RST%
echo  %B2%  ██████╔╝██║╚██████╔╝██║ ╚═╝ ██║███████╗███████║██║  ██║%RST%
echo  %B1%  ╚═════╝ ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝%RST%
echo.
echo  %B3%  ================================================================%RST%
echo  %B4%       DIAGNOSTIC ^& RESOLUTION SYSTEME WINDOWS  V4.0%RST%
echo  %DIM%                       by Brisk%RST%
echo  %B3%  ================================================================%RST%
echo.

echo  %GRN%  [OK]%RST%  Droits Administrateur   : OK
echo  %GRN%  [OK]%RST%  Repertoire              : %~dp0
echo  %DIM%  [*]   Date / Heure           : %DATE% %TIME%%RST%
echo.

:: Verification Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo  %RED%  ================================================================%RST%
    echo  %RED%  ERREUR - Python introuvable%RST%
    echo  %RED%  ================================================================%RST%
    echo.
    echo  %WHT%  Python n'est pas installe ou pas dans le PATH systeme.%RST%
    echo.
    echo  %YLW%  Solution :%RST%
    echo  %WHT%    1. Telecharger Python : https://www.python.org/downloads/%RST%
    echo  %WHT%    2. Cocher "Add Python to PATH" a l'installation%RST%
    echo  %WHT%    3. Relancer ce script%RST%
    echo.
    echo  %B1%  ================================================================%RST%
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo  %B3%  [OK]%RST%  Python detecte          : %PYVER%
echo.

:: Installation dependances
echo  %B2%  ================================================================%RST%
echo  %B3%   Installation / Verification des dependances pip...%RST%
echo  %B2%  ================================================================%RST%
echo.

if exist "%~dp0requirements.txt" (
    pip install -r "%~dp0requirements.txt" --quiet --disable-pip-version-check >nul 2>&1
    if %errorlevel% equ 0 (
        echo  %GRN%  [OK]%RST%  Dependances installes avec succes.
    ) else (
        echo  %YLW%  [!]   Certains modules n'ont pas pu etre installes.%RST%
        echo  %DIM%        Le script Python tentera de les reinstaller.%RST%
    )
) else (
    pip install psutil wmi requests pywin32 --quiet --disable-pip-version-check >nul 2>&1
)
echo.

:: Verification main.py
if not exist "%~dp0main.py" (
    echo.
    echo  %RED%  ================================================================%RST%
    echo  %RED%  ERREUR - Fichier main.py introuvable%RST%
    echo  %RED%  ================================================================%RST%
    echo.
    echo  %WHT%  Assurez-vous que main.py est dans le meme dossier que run.bat.%RST%
    echo.
    pause
    exit /b 1
)

:: Lancement
echo  %B2%  ================================================================%RST%
echo  %B3%   Lancement de BIOMESH V4.0...%RST%
echo  %DIM%   Certaines etapes peuvent prendre plusieurs minutes.%RST%
echo  %B2%  ================================================================%RST%
echo.
timeout /t 2 /nobreak >nul

python "%~dp0main.py"
set EXITCODE=%errorlevel%

:: Fin
echo.
echo  %B2%  ================================================================%RST%
echo  %B3%   BIOMESH V4.0 - Session terminee.%RST%
echo  %B2%  ================================================================%RST%
echo.

if exist "%~dp0rapport.html" (
    echo  %B4%  [*]   Ouverture du rapport HTML...%RST%
    timeout /t 2 /nobreak >nul
    start "" "%~dp0rapport.html"
)

if exist "%~dp0logs.txt" (
    echo  %DIM%  [*]   Rapport texte : %~dp0logs.txt%RST%
)

echo.
pause
endlocal
exit /b %EXITCODE%
