"""Michi Music — reproductor de música liviano con recomendaciones."""
import functools
import os
import sys
import threading
import traceback
import webbrowser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import paths  # noqa: E402

paths.setup_bin_path()

import webview  # noqa: E402

import resolver  # noqa: E402
from db import DB  # noqa: E402
from player import Player  # noqa: E402
from recommender import Recommender  # noqa: E402


def safe(fn):
    """Atrapa errores para que la interfaz reciba un mensaje claro."""
    @functools.wraps(fn)
    def wrap(*a, **kw):
        try:
            return fn(*a, **kw)
        except Exception as e:  # noqa: BLE001
            traceback.print_exc()
            msg = str(e).split("\n")[0]
            msg = msg.replace("ERROR: ", "")
            return {"error": msg[:300] or "Algo salió mal"}
    return wrap


class Api:
    def __init__(self):
        self._db = DB(paths.DB_PATH)
        self._rec = Recommender(self._db)
        self._player = Player(self._db)
        self._window = None
        self._mini = False
        self._rec.enrich_async()

    # ---------- links ----------
    @safe
    def inspect(self, url):
        res = resolver.inspect(url)
        if res["type"] == "track":
            saved = self._db.track_by_url(res["track"]["url"])
            res["track"]["saved"] = bool(saved)
            if saved:
                res["track"]["id"] = saved["id"]
        else:
            for e in res["entries"]:
                s = self._db.track_by_url(e["url"])
                e["saved"] = bool(s)
                if s:
                    e["id"] = s["id"]
        return res

    @safe
    def save_tracks(self, tracks, playlist_name=None, source_url=None):
        ids = [self._db.add_track(t) for t in tracks if t.get("url")]
        pid = None
        if playlist_name:
            pid = self._db.create_playlist(playlist_name, source_url)
            self._db.add_to_playlist(pid, ids)
        self._rec.enrich_async()
        return {"ids": ids, "playlist_id": pid}

    @safe
    def save_rec(self, rec):
        """Guarda una recomendación en la biblioteca (busca su link si hace falta)."""
        t = dict(rec)
        if not t.get("url"):
            found = resolver.search_one(t.get("query"))
            if not found:
                return {"error": "No encontré esa canción en YouTube"}
            t.update({"url": found["url"], "thumb": found["thumb"], "duration": found["duration"]})
        t["track"] = rec.get("title")
        tid = self._db.add_track(t)
        self._db.set_meta(tid, rec.get("artist"), rec.get("title"))
        self._db.hide_rec(rec.get("key", ""))
        self._rec.enrich_async()
        return {"id": tid}

    # ---------- biblioteca ----------
    @safe
    def library(self, search="", order="added", liked_only=False):
        return self._db.tracks(search, order, liked_only)

    @safe
    def delete_track(self, tid):
        self._db.delete_track(tid)
        return True

    @safe
    def toggle_like(self, tid):
        t = self._db.get_track(tid)
        if not t:
            return False
        self._db.set_liked(tid, not t["liked"])
        cur = self._player.current
        if cur and cur.get("id") == tid:
            cur["liked"] = not t["liked"]
        return not t["liked"]

    @safe
    def edit_meta(self, tid, artist, title):
        self._db.set_meta(tid, artist.strip() or None, title.strip() or None)
        self._rec.enrich_async()
        return True

    # ---------- playlists ----------
    @safe
    def playlists(self):
        return self._db.playlists()

    @safe
    def playlist_tracks(self, pid):
        return self._db.playlist_tracks(pid)

    @safe
    def create_playlist(self, name, tids=None):
        pid = self._db.create_playlist(name)
        if tids:
            self._db.add_to_playlist(pid, tids)
        return pid

    @safe
    def add_to_playlist(self, pid, tids):
        self._db.add_to_playlist(pid, tids)
        return True

    @safe
    def remove_from_playlist(self, pid, tid):
        self._db.remove_from_playlist(pid, tid)
        return True

    @safe
    def rename_playlist(self, pid, name):
        self._db.rename_playlist(pid, name)
        return True

    @safe
    def delete_playlist(self, pid):
        self._db.delete_playlist(pid)
        return True

    # ---------- reproductor ----------
    @safe
    def play(self, tracks, start=0):
        self._player.set_queue(tracks, start)
        return True

    @safe
    def enqueue(self, tracks, next_up=False):
        self._player.add_to_queue(tracks, next_up)
        return True

    @safe
    def toggle(self):
        self._player.toggle()
        return True

    @safe
    def next(self):
        self._player.next()
        return True

    @safe
    def prev(self):
        self._player.prev()
        return True

    @safe
    def seek(self, sec):
        self._player.seek(sec)
        return True

    @safe
    def volume(self, v):
        self._player.set_volume(v)
        return True

    @safe
    def shuffle(self, on):
        self._player.set_shuffle(on)
        return True

    @safe
    def repeat(self, mode):
        self._player.set_repeat(mode)
        return True

    @safe
    def jump(self, qi):
        self._player.jump(qi)
        return True

    @safe
    def state(self):
        s = self._player.state()
        t = s.get("track")
        if t and t.get("id"):
            db_t = self._db.get_track(t["id"])
            if db_t:
                t["liked"] = db_t["liked"]
        return s

    @safe
    def queue(self):
        return self._player.queue_view()

    # ---------- gustos ----------
    @safe
    def profile(self):
        return self._rec.profile()

    @safe
    def recommendations(self, refresh=False):
        return self._rec.recommendations(refresh)

    @safe
    def hide_rec(self, key):
        self._db.hide_rec(key)
        return True

    # ---------- ajustes ----------
    @safe
    def settings(self):
        return {"lastfm_key": self._db.get_setting("lastfm_key", ""),
                "data_dir": paths.DATA_DIR,
                "deno": bool(paths.deno_path())}

    @safe
    def save_lastfm_key(self, key):
        key = (key or "").strip()
        if key and not self._rec.lfm.check_key(key):
            return {"error": "Esa clave no funcionó. Revisa que esté completa."}
        self._db.set_setting("lastfm_key", key)
        self._rec.enrich_async()
        return True

    @safe
    def open_link(self, url):
        webbrowser.open(url)
        return True

    @safe
    def mini(self, on):
        w = self._window
        self._mini = bool(on)
        if self._mini:
            w.resize(400, 175)
            w.on_top = True
        else:
            w.on_top = False
            w.resize(1180, 760)
        return self._mini


def setup_media_keys(api):
    """Teclas multimedia del teclado (opcional, solo Windows)."""
    try:
        import keyboard
        keyboard.add_hotkey("play/pause media", lambda: api.toggle(), suppress=False)
        keyboard.add_hotkey("next track", lambda: api.next(), suppress=False)
        keyboard.add_hotkey("previous track", lambda: api.prev(), suppress=False)
    except Exception:  # noqa: BLE001
        pass


def main():
    api = Api()
    window = webview.create_window(
        "Michi Music", os.path.join(paths.UI_DIR, "index.html"), js_api=api,
        width=1180, height=760, min_size=(380, 160), background_color="#101012",
    )
    api._window = window
    window.events.closed += lambda: api._player.shutdown()
    if os.name == "nt":
        threading.Thread(target=setup_media_keys, args=(api,), daemon=True).start()
    webview.start(debug=bool(os.environ.get("MICHI_DEBUG")), private_mode=False,
                  storage_path=os.path.join(paths.DATA_DIR, "webview"))
    os._exit(0)  # cierra todo (audio y atajos) al cerrar la ventana


if __name__ == "__main__":
    main()
