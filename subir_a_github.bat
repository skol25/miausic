@echo off
title Subir Miausic a GitHub
cd /d "%~dp0"
where git >nul 2>nul
if errorlevel 1 (
  echo No tienes Git instalado. Instalandolo con winget...
  winget install -e --id Git.Git --silent --accept-package-agreements --accept-source-agreements
  set "PATH=%PATH%;%ProgramFiles%\Git\cmd"
)
git config --global --add safe.directory "%CD:\=/%"
echo.
echo Subiendo Miausic a https://github.com/skol25/miausic ...
echo (si se abre el navegador, inicia sesion en GitHub y autoriza)
echo.
git push -u origin main
echo.
if errorlevel 1 (echo Algo fallo. Manda una captura de esta ventana.) else (echo Listo! Miausic ya esta en GitHub.)
pause
