"""Lee links de cualquier sitio con yt-dlp: canciones sueltas, playlists y búsquedas."""
import re
import threading
import time

import yt_dlp

from paths import deno_path

_JUNK = re.compile(
    r"\s*[\(\[\{][^\)\]\}]*(official|oficial|video|audio|lyric|letra|visualizer|"
    r"visualiser|hd|hq|4k|mv|m/v|en vivo|live session|remaster)[^\)\]\}]*[\)\]\}]",
    re.I)
_CHANNEL_JUNK = re.compile(r"(\s*-\s*topic$|vevo$|\s*official$|\s*oficial$)", re.I)
_SEPS = (" - ", " – ", " — ", " | ")


def _base_opts():
    opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "noprogress": True,
        "socket_timeout": 20,
    }
    d = deno_path()
    if d:
        opts["js_runtimes"] = {"deno": {"path": d}}
    return opts


def clean_title(t):
    return re.sub(r"\s{2,}", " ", _JUNK.sub("", t or "")).strip()


def split_artist_title(info):
    """Devuelve (artista, título) lo mejor posible."""
    artist = info.get("artist") or info.get("creator")
    track = info.get("track")
    if artist and track:
        return artist.split(",")[0].strip(), clean_title(track)
    title = clean_title(info.get("title") or "")
    for sep in _SEPS:
        if sep in title:
            a, t = title.split(sep, 1)
            if a.strip() and t.strip():
                return a.strip(), t.strip()
    ch = info.get("uploader") or info.get("channel") or ""
    ch = _CHANNEL_JUNK.sub("", ch).strip()
    return (ch or None), title


def _thumb(info):
    th = info.get("thumbnail")
    if th:
        return th
    thumbs = info.get("thumbnails") or []
    if thumbs:
        # Preferimos una mediana para no cargar imágenes gigantes
        mid = thumbs[len(thumbs) // 2] if len(thumbs) > 2 else thumbs[-1]
        return mid.get("url")
    vid = info.get("id")
    if vid and "youtube" in (info.get("ie_key") or info.get("extractor") or "").lower():
        return f"https://i.ytimg.com/vi/{vid}/mqdefault.jpg"
    return None


def _entry_url(e):
    url = e.get("webpage_url") or e.get("url") or ""
    if url and not url.startswith("http"):
        ie = (e.get("ie_key") or "").lower()
        if "youtube" in ie:
            url = f"https://www.youtube.com/watch?v={url}"
    if "youtube.com/watch" in url or "youtu.be/" in url:
        m = re.search(r"(?:v=|youtu\.be/)([\w-]{11})", url)
        if m:
            url = f"https://www.youtube.com/watch?v={m.group(1)}"
    return url


def normalize(info, source=None):
    artist, track = split_artist_title(info)
    return {
        "url": _entry_url(info),
        "title": clean_title(info.get("title")) or info.get("url"),
        "artist": artist,
        "track": track,
        "duration": info.get("duration"),
        "thumb": _thumb(info),
        "source": source or info.get("extractor_key") or info.get("ie_key") or "web",
        "tags": (info.get("tags") or [])[:20] + (info.get("genres") or []) + (
            [info["genre"]] if info.get("genre") else []),
    }


def inspect(url, limit=300):
    """Mira qué hay detrás de un link. Devuelve canción o playlist (sin reproducir)."""
    url = url.strip()
    opts = _base_opts()
    opts.update({"extract_flat": "in_playlist", "playlistend": limit})
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
    if info.get("_type") in ("playlist", "multi_video") or info.get("entries") is not None:
        entries = []
        for e in info.get("entries") or []:
            if not e:
                continue
            n = normalize(e, source=info.get("extractor_key"))
            if n["url"]:
                entries.append(n)
        return {
            "type": "playlist",
            "title": info.get("title") or "Playlist",
            "uploader": info.get("uploader") or info.get("channel"),
            "url": info.get("webpage_url") or url,
            "thumb": _thumb(info) or (entries[0]["thumb"] if entries else None),
            "entries": entries,
        }
    t = normalize(info)
    if not t["url"] or not t["url"].startswith("http"):
        t["url"] = url
    return {"type": "track", "track": t}


class StreamCache:
    """Guarda por un rato la URL de audio para no volver a pedirla."""

    def __init__(self, ttl=3 * 3600):
        self.ttl = ttl
        self.data = {}
        self.lock = threading.Lock()

    def get(self, key):
        with self.lock:
            v = self.data.get(key)
            if v and time.time() - v[0] < self.ttl:
                return v[1]
        return None

    def put(self, key, value):
        with self.lock:
            self.data[key] = (time.time(), value)


_cache = StreamCache()


def resolve_stream(url):
    """Devuelve {stream, headers, info} con el mejor audio disponible."""
    hit = _cache.get(url)
    if hit:
        return hit
    opts = _base_opts()
    opts.update({"format": "bestaudio[acodec=opus]/bestaudio/best", "noplaylist": True})
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
    if info.get("entries"):
        info = next(e for e in info["entries"] if e)
    stream = info.get("url")
    headers = info.get("http_headers") or {}
    if not stream and info.get("requested_formats"):
        f = info["requested_formats"][0]
        stream, headers = f.get("url"), f.get("http_headers") or headers
    res = {"stream": stream, "headers": headers, "info": normalize(info)}
    _cache.put(url, res)
    return res


def search_one(query):
    """Busca en YouTube y devuelve la primera canción (para recomendaciones)."""
    opts = _base_opts()
    opts.update({"extract_flat": "in_playlist"})
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=False)
    for e in info.get("entries") or []:
        if e:
            return normalize(e, source="Youtube")
    return None
