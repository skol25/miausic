@echo off
chcp 65001 >nul
title Instalando Miausic
cd /d "%~dp0"
echo.
echo   =====================================
echo     Miausic - instalacion
echo   =====================================
echo.

REM 1) Buscar Python (3.12 de preferencia)
set "PY="
py -3.12 --version >nul 2>&1 && set "PY=py -3.12"
if not defined PY (py -3.13 --version >nul 2>&1 && set "PY=py -3.13")
if not defined PY (py -3.11 --version >nul 2>&1 && set "PY=py -3.11")
if not defined PY if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"

if not defined PY (
  echo   No encontre Python. Lo instalo con winget...
  winget install -e --id Python.Python.3.12 --scope user --accept-package-agreements --accept-source-agreements
  if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
  ) else (
    echo.
    echo   [!] No pude instalar Python solo.
    echo       Instala Python 3.12 desde https://www.python.org/downloads/
    echo       y vuelve a abrir este archivo.
    pause
    exit /b 1
  )
)
echo   [ok] Python: %PY%

REM 2) Entorno propio de la app
if not exist ".venv\Scripts\python.exe" (
  echo   Creando el entorno de la app...
  %PY% -m venv .venv || (echo   [!] Fallo creando el entorno & pause & exit /b 1)
)
echo   Instalando librerias (puede tardar un par de minutos)...
".venv\Scripts\python.exe" -m pip install --upgrade pip -q
".venv\Scripts\python.exe" -m pip install -r requirements.txt -q || (echo   [!] Fallo instalando librerias & pause & exit /b 1)
echo   [ok] Librerias

REM 3) Motor de audio y Deno
".venv\Scripts\python.exe" setup_deps.py

REM 4) Accesos directos en el Escritorio y en el menu Inicio
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ws = New-Object -ComObject WScript.Shell;" ^
  "$dirs = @([Environment]::GetFolderPath('Desktop'), (Join-Path ([Environment]::GetFolderPath('Programs')) ''));" ^
  "foreach ($d in $dirs) { $s = $ws.CreateShortcut((Join-Path $d 'Miausic.lnk'));" ^
  "$s.TargetPath = '%~dp0.venv\Scripts\pythonw.exe'; $s.Arguments = '\"%~dp0app\main.py\"';" ^
  "$s.WorkingDirectory = '%~dp0'; $s.IconLocation = '%~dp0app\michi.ico'; $s.Save() }"
echo   [ok] Acceso directo "Miausic" en tu Escritorio
echo.
echo   Listo! Abre Miausic desde el Escritorio.
echo.
pause
