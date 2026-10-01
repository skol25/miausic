@echo off
chcp 65001 >nul
title Creando Miausic.exe
cd /d "%~dp0"
REM Opcional: crea una version .exe que no necesita Python (carpeta dist\Miausic)
".venv\Scripts\python.exe" -m pip install -q pyinstaller
".venv\Scripts\python.exe" -m PyInstaller --noconfirm --windowed --name "Miausic" ^
  --icon "app\michi.ico" --add-data "app\ui;ui" --paths app ^
  --collect-submodules yt_dlp --hidden-import webview.platforms.edgechromium ^
  "app\main.py"
xcopy /e /i /y "bin" "dist\Miausic\bin" >nul
echo.
echo   Listo! Tu app esta en: dist\Miausic\Miausic.exe
pause
