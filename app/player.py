"""Reproductor de solo audio con mpv (muy liviano) + cola de reproducción."""
import random
import threading
import time
import traceback

import mpv

import resolver

PLAY_COUNT_SECONDS = 30  # a partir de aquí cuenta como "escuchada"


class Player:
    def __init__(self, db, on_change=None):
        self.db = db
        self.on_change = on_change or (lambda: None)
        self.mpv = mpv.MPV(
            video=False, vid="no", ytdl=False, terminal=False,
            audio_display="no", cache="yes", demuxer_max_bytes="16MiB",
            demuxer_max_back_bytes="4MiB", keep_open="no", idle="yes",
        )
        self.mpv.volume = float(db.get_setting("volume", 80))
        self.queue = []          # lista de canciones (dict)
        self.order = []          # orden real (para aleatorio)
        self.pos = -1            # posición dentro de order
        self.shuffle = bool(db.get_setting("shuffle", False))
        self.repeat = db.get_setting("repeat", "off")  # off | all | one
        self.status = "idle"     # idle | loading | playing | paused | error
        self.error = None
        self.current = None
        self._started_at = None
        self._counted = False
        self._token = 0
        self._lock = threading.RLock()
        threading.Thread(target=self._watch, daemon=True).start()

    # ---------- cola ----------
    def set_queue(self, tracks, start=0):
        with self._lock:
            self.queue = list(tracks)
            self._build_order(max(0, min(start, len(self.queue) - 1)))
        self._play_current()

    def add_to_queue(self, tracks, next_up=False):
        with self._lock:
            if not self.queue:
                self.set_queue(tracks)
                return
            base = len(self.queue)
            self.queue.extend(tracks)
            new = list(range(base, base + len(tracks)))
            if next_up:
                self.order[self.pos + 1:self.pos + 1] = new
            else:
                self.order.extend(new)
        self.on_change()

    def _build_order(self, start):
        idx = list(range(len(self.queue)))
        if self.shuffle:
            rest = [i for i in idx if i != start]
            random.shuffle(rest)
            self.order = [start] + rest
            self.pos = 0
        else:
            self.order = idx
            self.pos = start

    def jump(self, queue_index):
        with self._lock:
            if queue_index in self.order:
                self._mark_skip()
                self.pos = self.order.index(queue_index)
        self._play_current()

    # ---------- controles ----------
    def toggle(self):
        if self.status in ("playing", "paused"):
            self.mpv.pause = not self.mpv.pause
            self.status = "paused" if self.mpv.pause else "playing"
        elif self.queue:
            self._play_current()
        self.on_change()

    def next(self, auto=False):
        with self._lock:
            if not self.order:
                return
            if not auto:
                self._mark_skip()
            if auto and self.repeat == "one":
                pass  # repetimos la misma
            elif self.pos + 1 < len(self.order):
                self.pos += 1
            elif self.repeat == "all" or not auto:
                self.pos = 0
            else:
                self.status = "idle"
                self.on_change()
                return
        self._play_current()

    def prev(self):
        try:
            if (self.mpv.time_pos or 0) > 5:
                self.mpv.seek(0, "absolute")
                return
        except Exception:
            pass
        with self._lock:
            if self.pos > 0:
                self.pos -= 1
        self._play_current()

    def seek(self, seconds):
        try:
            self.mpv.seek(float(seconds), "absolute")
        except Exception:
            pass

    def set_volume(self, v):
        v = max(0, min(130, float(v)))
        self.mpv.volume = v
        self.db.set_setting("volume", v)

    def set_shuffle(self, on):
        with self._lock:
            self.shuffle = bool(on)
            self.db.set_setting("shuffle", self.shuffle)
            if self.queue and self.order:
                cur = self.order[self.pos]
                self._build_order(cur)
        self.on_change()

    def set_repeat(self, mode):
        self.repeat = mode if mode in ("off", "all", "one") else "off"
        self.db.set_setting("repeat", self.repeat)
        self.on_change()

    def stop(self):
        self._token += 1
        try:
            self.mpv.stop()
        except Exception:
            pass
        self.status = "idle"
        self.on_change()

    # ---------- reproducción ----------
    def _play_current(self):
        with self._lock:
            if not self.order or self.pos < 0:
                return
            track = self.queue[self.order[self.pos]]
            self._token += 1
            token = self._token
        self.current = track
        self.status = "loading"
        self.error = None
        self._started_at = None
        self._counted = False
        self.on_change()
        threading.Thread(target=self._load, args=(track, token), daemon=True).start()

    def _load(self, track, token):
        try:
            url = track.get("url")
            if not url:  # recomendación: se busca en YouTube al momento
                found = resolver.search_one(track.get("query") or f'{track.get("artist")} {track.get("title")}')
                if not found:
                    raise RuntimeError("No encontré esta canción")
                track.update({k: v for k, v in found.items() if k in ("url", "thumb", "duration")})
                url = track["url"]
            res = resolver.resolve_stream(url)
            if token != self._token:
                return
            if not track.get("thumb"):
                track["thumb"] = res["info"].get("thumb")
            if not track.get("duration"):
                track["duration"] = res["info"].get("duration")
            headers = res.get("headers") or {}
            fields = [f"{k}: {v}" for k, v in headers.items()
                      if k.lower() in ("user-agent", "referer", "origin", "cookie")]
            self.mpv["http-header-fields"] = ",".join(f.replace(",", "\\,") for f in fields)
            self.mpv.play(res["stream"] or url)
            self.mpv.pause = False
            self._started_at = time.time()
            self.status = "playing"
        except Exception as e:  # noqa: BLE001
            if token != self._token:
                return
            traceback.print_exc()
            self.status = "error"
            self.error = str(e).split("\n")[0][:200]
            self.on_change()
            # Saltamos a la siguiente después de un momento
            time.sleep(2.5)
            if token == self._token:
                self.next(auto=True)
            return
        self.on_change()

    def _mark_skip(self):
        t = self.current
        if t and t.get("id") and self.status in ("playing", "paused") and not self._counted:
            self.db.count_skip(t["id"])

    def _watch(self):
        """Revisa cada medio segundo si terminó la canción o si ya cuenta como escuchada."""
        while True:
            time.sleep(0.5)
            try:
                if self.status not in ("playing", "paused"):
                    continue
                t = self.current
                pos = self.mpv.time_pos or 0
                if (not self._counted and t and t.get("id") and pos >= PLAY_COUNT_SECONDS):
                    self._counted = True
                    self.db.count_play(t["id"])
                if self.status == "playing" and self.mpv.idle_active and self._started_at \
                        and time.time() - self._started_at > 3:
                    if t and t.get("id") and not self._counted:
                        dur = t.get("duration") or 0
                        if dur and dur < PLAY_COUNT_SECONDS:
                            self.db.count_play(t["id"])
                    self._counted = True
                    self.next(auto=True)
            except Exception:
                traceback.print_exc()

    # ---------- estado para la interfaz ----------
    def state(self):
        try:
            pos = self.mpv.time_pos or 0
            dur = self.mpv.duration or (self.current or {}).get("duration") or 0
        except Exception:
            pos, dur = 0, 0
        return {
            "status": self.status,
            "error": self.error,
            "track": self.current,
            "position": pos,
            "duration": dur,
            "volume": self.mpv.volume,
            "shuffle": self.shuffle,
            "repeat": self.repeat,
            "queue_index": self.order[self.pos] if self.order and 0 <= self.pos < len(self.order) else -1,
            "has_queue": bool(self.queue),
        }

    def queue_view(self):
        with self._lock:
            items = []
            for n, qi in enumerate(self.order):
                t = self.queue[qi]
                items.append({"qi": qi, "now": n == self.pos, "past": n < self.pos,
                              "title": t.get("track") or t.get("title"), "artist": t.get("artist"),
                              "thumb": t.get("thumb"), "duration": t.get("duration")})
            return items

    def shutdown(self):
        try:
            self.mpv.terminate()
        except Exception:
            pass
