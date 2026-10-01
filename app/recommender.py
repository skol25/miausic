"""Géneros y recomendaciones con Last.fm + tu historial de escucha."""
import json
import random
import threading
import time
import traceback
import urllib.parse
import urllib.request
from collections import defaultdict

API = "https://ws.audioscrobbler.com/2.0/"
WEEK = 7 * 24 * 3600

# Etiquetas de Last.fm que no son géneros
NOT_GENRES = {
    "seen live", "favorites", "favourite", "favorite", "favourites", "love", "beautiful",
    "awesome", "female vocalists", "male vocalists", "female vocalist", "male vocalist",
    "my favorite", "under 2000 listeners", "spotify", "albums i own", "cool", "amazing",
    "best", "good", "great", "loved", "fav", "favs", "classic", "catchy", "sexy",
    "check out", "youtube", "music", "songs", "song", "all", "other", "misc", "various",
    "british", "american", "usa", "uk", "spanish", "english", "venezuela", "venezuelan",
    "mexico", "mexican", "colombia", "colombian", "argentina", "puerto rico", "latin america",
    "00s", "10s", "20s", "60s", "70s", "80s", "90s", "2000s", "2010s", "2020s",
    "singer-songwriter", "instrumental",
}

GENRE_ES = {
    "electronic": "electrónica", "hip-hop": "hip hop", "hip hop": "hip hop", "rap": "rap",
    "latin": "latina", "pop": "pop", "rock": "rock", "indie": "indie", "jazz": "jazz",
    "classical": "clásica", "reggaeton": "reguetón", "dance": "dance", "soul": "soul",
    "metal": "metal", "alternative": "alternativo", "alternative rock": "rock alternativo",
    "indie pop": "indie pop", "indie rock": "indie rock", "punk": "punk", "funk": "funk",
    "blues": "blues", "country": "country", "folk": "folk", "ambient": "ambient",
    "house": "house", "techno": "techno", "trap": "trap", "salsa": "salsa",
    "bachata": "bachata", "merengue": "merengue", "cumbia": "cumbia", "rnb": "r&b",
    "r&b": "r&b", "lo-fi": "lo-fi", "lofi": "lo-fi", "chillout": "chill", "chill": "chill",
    "soundtrack": "banda sonora", "latin pop": "pop latino", "rock en español": "rock en español",
    "electropop": "electropop", "synthpop": "synthpop", "k-pop": "k-pop", "dancehall": "dancehall",
    "reggae": "reggae", "drum and bass": "drum and bass", "dubstep": "dubstep",
}


def nice_genre(g):
    return GENRE_ES.get(g, g)


class LastFM:
    def __init__(self, db):
        self.db = db

    @property
    def key(self):
        return (self.db.get_setting("lastfm_key") or "").strip()

    def call(self, method, max_age=WEEK, **params):
        if not self.key:
            return None
        params = {k: v for k, v in params.items() if v}
        ck = method + "|" + json.dumps(params, sort_keys=True).lower()
        hit = self.db.cache_get(ck, max_age)
        if hit is not None:
            return hit
        q = urllib.parse.urlencode({"method": method, "api_key": self.key, "format": "json",
                                    "autocorrect": 1, **params})
        req = urllib.request.Request(API + "?" + q, headers={"User-Agent": "MichiMusic/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read().decode("utf-8"))
        except Exception:  # noqa: BLE001
            traceback.print_exc()
            return None
        if "error" in data:
            data = {}
        self.db.cache_set(ck, data)
        return data

    def check_key(self, key):
        q = urllib.parse.urlencode({"method": "tag.getTopTags", "api_key": key, "format": "json"})
        try:
            with urllib.request.urlopen(API + "?" + q, timeout=15) as r:
                data = json.loads(r.read().decode("utf-8"))
            return "error" not in data
        except Exception:  # noqa: BLE001
            return False

    @staticmethod
    def _tags(data, key):
        tags = ((data or {}).get(key) or {}).get("tag") or []
        if isinstance(tags, dict):
            tags = [tags]
        out = []
        for t in tags:
            name = (t.get("name") or "").strip().lower()
            try:
                count = int(t.get("count", 100))
            except (TypeError, ValueError):
                count = 100
            if name and name not in NOT_GENRES and count >= 10 and len(name) < 30:
                out.append(name)
        return out

    def genres_for(self, artist, track):
        if not artist:
            return []
        tags = []
        if track:
            tags = self._tags(self.call("track.getTopTags", artist=artist, track=track), "toptags")
        if len(tags) < 2:
            tags += [t for t in self._tags(self.call("artist.getTopTags", artist=artist), "toptags")
                     if t not in tags]
        return tags[:5]

    def similar_artists(self, artist, limit=10):
        d = self.call("artist.getSimilar", artist=artist, limit=limit) or {}
        arts = (d.get("similarartists") or {}).get("artist") or []
        return [(a["name"], float(a.get("match") or 0.5)) for a in arts if a.get("name")]

    def top_tracks(self, artist, limit=3):
        d = self.call("artist.getTopTracks", artist=artist, limit=limit) or {}
        tr = (d.get("toptracks") or {}).get("track") or []
        return [t["name"] for t in tr if t.get("name")][:limit]

    def tag_tracks(self, tag, limit=30):
        d = self.call("tag.getTopTracks", tag=tag, limit=limit) or {}
        tr = (d.get("tracks") or {}).get("track") or []
        return [((t.get("artist") or {}).get("name"), t.get("name")) for t in tr if t.get("name")]


class Recommender:
    def __init__(self, db):
        self.db = db
        self.lfm = LastFM(db)
        self._busy = threading.Lock()

    # ---------- géneros de cada canción ----------
    def enrich_pending(self):
        """En segundo plano: busca el género de las canciones que aún no lo tienen."""
        if not self.lfm.key or not self._busy.acquire(blocking=False):
            return
        try:
            for t in self.db.tracks_without_genres():
                g = self.lfm.genres_for(t.get("artist"), t.get("track") or t.get("title"))
                self.db.set_genres(t["id"], g)
                time.sleep(0.25)  # respetamos el límite de Last.fm
        finally:
            self._busy.release()

    def enrich_async(self):
        threading.Thread(target=self.enrich_pending, daemon=True).start()

    # ---------- perfil de gustos ----------
    @staticmethod
    def weight(t):
        return max(0.0, 1 + t["plays"] * 1.0 + (5 if t["liked"] else 0) - t["skips"] * 1.5)

    def profile(self):
        tracks = self.db.tracks()
        genres, artists = defaultdict(float), defaultdict(float)
        for t in tracks:
            w = self.weight(t)
            if t.get("artist"):
                artists[t["artist"]] += w
            gs = t.get("genres") or []
            for i, g in enumerate(gs):
                genres[g] += w * (1.0 - i * 0.15)
        total = sum(genres.values()) or 1
        top_g = sorted(genres.items(), key=lambda x: -x[1])[:12]
        top_a = sorted(artists.items(), key=lambda x: -x[1])[:10]
        return {
            "genres": [{"name": nice_genre(g), "raw": g, "pct": round(v * 100 / total, 1)} for g, v in top_g],
            "artists": [{"name": a, "score": round(v, 1)} for a, v in top_a],
            "total_tracks": len(tracks),
            "total_plays": sum(t["plays"] for t in tracks),
            "pending": len(self.db.tracks_without_genres()),
            "has_key": bool(self.lfm.key),
        }

    # ---------- recomendaciones ----------
    def recommendations(self, refresh=False):
        if not refresh:
            cached = self.db.cache_get("recs", 12 * 3600)
            if cached:
                hidden = self.db.hidden_recs()
                cached["items"] = [r for r in cached["items"] if r["key"] not in hidden]
                return cached
        if not self.lfm.key:
            return {"items": [], "need_key": True}
        prof = self.profile()
        tracks = self.db.tracks()
        if not tracks:
            return {"items": [], "empty": True}
        known_artists = {(t.get("artist") or "").lower() for t in tracks}
        known_tracks = {((t.get("artist") or "").lower(), (t.get("track") or t.get("title") or "").lower())
                        for t in tracks}
        hidden = self.db.hidden_recs()
        items, seen = [], set()

        def add(artist, title, reason, kind):
            k = f"{artist} - {title}".lower()
            if not artist or not title or k in seen or k in hidden:
                return False
            if (artist.lower(), title.lower()) in known_tracks:
                return False
            seen.add(k)
            items.append({"key": k, "artist": artist, "title": title, "reason": reason, "kind": kind,
                          "query": f"{artist} - {title}", "url": None, "thumb": None})
            return True

        # 1) Artistas parecidos a los que más escuchas
        cand = defaultdict(float)
        why = {}
        for a in prof["artists"][:6]:
            for name, match in self.lfm.similar_artists(a["name"], 12):
                if name.lower() in known_artists or name.lower() in hidden:
                    continue
                cand[name] += match * a["score"]
                why.setdefault(name, a["name"])
        for name, _ in sorted(cand.items(), key=lambda x: -x[1])[:10]:
            for title in self.lfm.top_tracks(name, 2):
                add(name, title, f"Porque escuchas {why[name]}", "artist")

        # 2) Lo mejor de tus géneros favoritos
        for g in prof["genres"][:4]:
            pool = [x for x in self.lfm.tag_tracks(g["raw"], 40) if x[0] and x[0].lower() not in known_artists]
            random.shuffle(pool)
            n = 0
            for artist, title in pool:
                if add(artist, title, f"Porque te gusta el {g['name']}", "genre"):
                    n += 1
                if n >= 4:
                    break

        # 3) Más de tus artistas favoritos que aún no guardaste
        for a in prof["artists"][:4]:
            for title in self.lfm.top_tracks(a["name"], 5):
                if add(a["name"], title, f"Más de {a['name']}", "more"):
                    break

        random.shuffle(items)
        items.sort(key=lambda r: {"artist": 0, "genre": 1, "more": 2}[r["kind"]] + random.random() * 1.6)
        result = {"items": items, "generated": time.time()}
        self.db.cache_set("recs", result)
        return result
