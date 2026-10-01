# -*- coding: utf-8 -*-
"""Actualizaciones de Miausic desde GitHub Releases (igual que en Miauia).

Cada versión publicada en GitHub trae un instalador "Miausic-Setup-X.Y.Z.exe". Miausic
revisa de vez en cuando si hay una versión más nueva y, si le das a "Actualizar",
descarga el instalador y lo ejecuta en silencio. Tu biblioteca no se toca: vive en
%APPDATA%\\Miausic, separada del programa."""
import json
import os
import re
import subprocess
import tempfile
import time
import traceback
import urllib.request

import paths
import version

CACHE = os.path.join(paths.DATA_DIR, "actualizacion.json")
CADA = 6 * 3600  # revisar como mucho cada 6 horas


def _tupla(v):
    return tuple(int(x) for x in re.findall(r"\d+", v or "0")[:3]) or (0,)


def instalado():
    """True cuando Miausic se instaló con el instalador (no la carpeta de desarrollo)."""
    return os.path.exists(os.path.join(paths.ROOT, "instalado.txt"))


def buscar(forzar=False):
    """Devuelve {"hay", "version", "actual", "url", "notas", "tamano"} o None si no se pudo revisar."""
    base = {"hay": False, "actual": version.VERSION, "instalado": instalado()}
    if not version.REPO_GITHUB:
        return base
    try:
        with open(CACHE, "r", encoding="utf-8") as f:
            cache = json.load(f)
        if not forzar and time.time() - cache.get("revisado", 0) < CADA:
            cache.update(base)
            cache["hay"] = bool(cache.get("url")) and _tupla(cache.get("version")) > _tupla(version.VERSION)
            return cache
    except Exception:  # noqa: BLE001
        pass
    url = f"https://api.github.com/repos/{version.REPO_GITHUB}/releases/latest"
    try:
        pet = urllib.request.Request(url, headers={"User-Agent": "Miausic", "Accept": "application/vnd.github+json"})
        with urllib.request.urlopen(pet, timeout=15) as r:
            datos = json.load(r)
    except Exception:  # noqa: BLE001
        traceback.print_exc()
        return None
    exe = next((a for a in datos.get("assets", []) if a["name"].lower().endswith(".exe")), None)
    info = {
        "version": (datos.get("tag_name") or "").lstrip("vV"),
        "url": exe["browser_download_url"] if exe else "",
        "tamano": exe["size"] if exe else 0,
        "notas": (datos.get("body") or "")[:2000],
        "revisado": time.time(),
    }
    try:
        with open(CACHE, "w", encoding="utf-8") as f:
            json.dump(info, f, ensure_ascii=False)
    except Exception:  # noqa: BLE001
        pass
    info.update(base)
    info["hay"] = bool(info["url"]) and _tupla(info["version"]) > _tupla(version.VERSION)
    return info


ESTADO = {"fase": "", "progreso": 0.0, "error": ""}


def instalar(info):
    """Descarga el instalador nuevo y lo ejecuta en silencio (/S). El instalador cierra
    Miausic, actualiza el programa y lo vuelve a abrir."""
    try:
        ESTADO.update(fase="descargando", progreso=0.0, error="")
        destino = os.path.join(tempfile.gettempdir(), f"Miausic-Setup-{info['version']}.exe")
        pet = urllib.request.Request(info["url"], headers={"User-Agent": "Miausic"})
        with urllib.request.urlopen(pet, timeout=60) as r, open(destino, "wb") as f:
            total = int(r.headers.get("Content-Length") or info.get("tamano") or 0)
            hecho = 0
            while True:
                trozo = r.read(1024 * 256)
                if not trozo:
                    break
                f.write(trozo)
                hecho += len(trozo)
                if total:
                    ESTADO["progreso"] = hecho / total
        ESTADO.update(fase="instalando", progreso=1.0)
        subprocess.Popen([destino, "/S", "/ACTUALIZAR"], creationflags=0x00000008 | 0x00000200)  # separado
        return True
    except Exception as e:  # noqa: BLE001
        traceback.print_exc()
        ESTADO.update(fase="error", error=str(e))
        return False
