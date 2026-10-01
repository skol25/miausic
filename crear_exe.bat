@echo off
chcp 65001 >nul
title Creando Michi Music.exe
cd /d "%~dp0"
REM Opcional: crea una version .exe que no necesita Python (carpeta dist\Michi Music)
".venv\Scripts\python.exe" -m pip install -q pyinstaller
".venv\Scripts\python.exe" -m PyInstaller --noconfirm --windowed --name "Michi Music" ^
  --icon "app\michi.ico" --add-data "app\ui;ui" --paths app ^
  --collect-submodules yt_dlp --hidden-import webview.platforms.edgechromium ^
  "app\main.py"
xcopy /e /i /y "bin" "dist\Michi Music\bin" >nul
echo.
echo   Listo! Tu app esta en: dist\Michi Music\Michi Music.exe
pause
