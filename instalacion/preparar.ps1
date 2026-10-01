# Prepara el Python propio de Miausic, sus librerías y el motor de audio (lo ejecuta el instalador).
param([Parameter(Mandatory = $true)][string]$Carpeta)
$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'

$uv = Join-Path $Carpeta 'instalacion\uv.exe'
$venv = Join-Path $Carpeta '.venv'
$py = Join-Path $venv 'Scripts\python.exe'
$env:UV_PYTHON_INSTALL_DIR = Join-Path $Carpeta 'python'
$env:UV_PYTHON_PREFERENCE = 'only-managed'
$env:UV_CACHE_DIR = Join-Path $env:LOCALAPPDATA 'Miausic\cache'
$env:UV_LINK_MODE = 'copy'
$env:UV_NO_PROGRESS = '1'

function Ejecutar($descripcion, [scriptblock]$bloque, $codigo) {
    Write-Output $descripcion
    & $bloque 2>&1 | ForEach-Object { "   $_" }
    if ($LASTEXITCODE -ne 0) {
        Write-Output "ERROR: $descripcion (código $LASTEXITCODE)"
        exit $codigo
    }
}

Ejecutar 'Descargando Python 3.12 (solo la primera vez)...' { & $uv python install 3.12 } 11
Ejecutar 'Creando el entorno de Miausic...' { & $uv venv $venv --python 3.12 --allow-existing } 12
Ejecutar 'Instalando librerías (reproductor, links, ventana)...' { & $uv pip install --python $py --upgrade -r (Join-Path $Carpeta 'requirements.txt') } 13
Ejecutar 'Descargando el motor de audio (mpv) y Deno...' { & $py (Join-Path $Carpeta 'setup_deps.py') } 14
Ejecutar 'Comprobando que todo funcione...' { & $py -c "import os,sys; sys.path.insert(0, os.path.join(r'$Carpeta','app')); import paths; paths.setup_bin_path(); import webview, mpv, yt_dlp; print('Todo en orden')" } 15
exit 0
