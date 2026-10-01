"""Rutas de la app: funciona igual en desarrollo y empaquetada como .exe."""
import os
import sys

FROZEN = getattr(sys, "frozen", False)

# Carpeta del programa (donde están app/, bin/, etc.)
if FROZEN:
    ROOT = os.path.dirname(sys.executable)
    UI_DIR = os.path.join(getattr(sys, "_MEIPASS", ROOT), "ui")
else:
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    UI_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui")

BIN_DIR = os.path.join(ROOT, "bin")

# Datos del usuario (biblioteca, ajustes) en %APPDATA%\Miausic
if os.name == "nt" and os.environ.get("APPDATA"):
    DATA_DIR = os.path.join(os.environ["APPDATA"], "Miausic")
else:
    DATA_DIR = os.path.join(os.path.expanduser("~"), ".miausic")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "michi.db")


def setup_bin_path():
    """Pone bin/ (libmpv, deno) al inicio del PATH para que se encuentren."""
    if os.path.isdir(BIN_DIR):
        os.environ["PATH"] = BIN_DIR + os.pathsep + os.environ.get("PATH", "")
        if os.name == "nt" and hasattr(os, "add_dll_directory"):
            try:
                os.add_dll_directory(BIN_DIR)
            except OSError:
                pass


def deno_path():
    exe = "deno.exe" if os.name == "nt" else "deno"
    p = os.path.join(BIN_DIR, exe)
    return p if os.path.isfile(p) else None
