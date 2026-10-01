@echo off
chcp 65001 >nul
title Actualizando Michi Music
cd /d "%~dp0"
echo   Actualizando yt-dlp (arregla links de YouTube que dejan de funcionar)...
".venv\Scripts\python.exe" -m pip install -U "yt-dlp[default]" -q
del /q "bin\deno.exe" 2>nul
".venv\Scripts\python.exe" setup_deps.py
echo   Listo!
pause
