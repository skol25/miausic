"""Descarga lo que Michi Music necesita en la carpeta bin/:
- libmpv-2.dll  (el motor de audio, de mpv)
- deno.exe      (lo usa yt-dlp para que YouTube funcione bien)
"""
import io
import json
import os
import re
import sys
import urllib.request
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(ROOT, "bin")
os.makedirs(BIN, exist_ok=True)
UA = {"User-Agent": "MichiMusic-setup"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def mpv():
    dest = os.path.join(BIN, "libmpv-2.dll")
    if os.path.isfile(dest):
        print("  [ok] libmpv-2.dll ya estaba")
        return True
    print("  Descargando el motor de audio (mpv)...")
    try:
        rel = json.loads(get("https://api.github.com/repos/shinchiro/mpv-winbuild-cmake/releases/latest"))
        assets = rel.get("assets", [])
        pick = None
        for a in assets:
            if re.match(r"^mpv-dev-x86_64-\d{8}.*\.7z$", a["name"]):
                pick = a
                break
        if not pick:
            pick = next(a for a in assets if a["name"].startswith("mpv-dev-x86_64") and a["name"].endswith(".7z"))
        print("   ", pick["name"], f'({pick["size"] // 1_000_000} MB)')
        data = get(pick["browser_download_url"])
        arch = os.path.join(BIN, "_mpv.7z")
        with open(arch, "wb") as f:
            f.write(data)
        tmp = os.path.join(BIN, "_mpv")
        os.makedirs(tmp, exist_ok=True)
        extracted = False
        try:
            import py7zr
            with py7zr.SevenZipFile(arch) as z:
                z.extractall(path=tmp)
            extracted = True
        except Exception as e:  # noqa: BLE001
            print("    py7zr no pudo, probando otra forma...", e)
        if not extracted:
            import shutil
            import subprocess
            for cmd in (["tar", "-xf", arch, "-C", tmp],
                        [shutil.which("7z") or r"C:\Program Files\7-Zip\7z.exe", "x", "-y", f"-o{tmp}", arch]):
                try:
                    subprocess.run(cmd, check=True, capture_output=True)
                    extracted = True
                    break
                except Exception:  # noqa: BLE001
                    continue
        found = None
        for dp, _, fs in os.walk(tmp):
            for fn in fs:
                if fn.lower() in ("libmpv-2.dll", "mpv-2.dll"):
                    found = os.path.join(dp, fn)
        if not found:
            raise RuntimeError("no encontré libmpv-2.dll dentro del archivo")
        os.replace(found, dest)
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
        os.remove(arch)
        print("  [ok] libmpv-2.dll")
        return True
    except Exception as e:  # noqa: BLE001
        print("  [!] No pude descargar mpv:", e)
        print("      Descárgalo a mano: https://github.com/shinchiro/mpv-winbuild-cmake/releases")
        print("      (archivo mpv-dev-x86_64-....7z) y copia libmpv-2.dll dentro de la carpeta bin")
        return False


def deno():
    dest = os.path.join(BIN, "deno.exe")
    if os.path.isfile(dest):
        print("  [ok] deno.exe ya estaba")
        return True
    print("  Descargando Deno (ayuda a yt-dlp con YouTube)...")
    try:
        data = get("https://github.com/denoland/deno/releases/latest/download/deno-x86_64-pc-windows-msvc.zip")
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            with open(dest, "wb") as f:
                f.write(z.read("deno.exe"))
        print("  [ok] deno.exe")
        return True
    except Exception as e:  # noqa: BLE001
        print("  [!] No pude descargar Deno:", e)
        print("      Algunas canciones de YouTube podrían fallar. Vuelve a intentar más tarde.")
        return False


if __name__ == "__main__":
    ok = mpv()
    deno()
    sys.exit(0 if ok else 1)
