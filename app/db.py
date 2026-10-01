"""Base de datos local (SQLite): canciones, playlists, ajustes y caché."""
import json
import sqlite3
import threading
import time

SCHEMA = """
CREATE TABLE IF NOT EXISTS tracks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE NOT NULL,
    title TEXT, artist TEXT, track TEXT,
    duration REAL, thumb TEXT, source TEXT,
    tags TEXT, genres TEXT,
    added_at REAL, last_played REAL,
    plays INTEGER DEFAULT 0, skips INTEGER DEFAULT 0, liked INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS playlists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL, source_url TEXT, created_at REAL
);
CREATE TABLE IF NOT EXISTS playlist_items (
    playlist_id INTEGER, track_id INTEGER, pos INTEGER,
    PRIMARY KEY (playlist_id, track_id)
);
CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, value TEXT, ts REAL);
CREATE TABLE IF NOT EXISTS hidden_recs (key TEXT PRIMARY KEY);
"""

TRACK_COLS = ("id", "url", "title", "artist", "track", "duration", "thumb", "source",
              "tags", "genres", "added_at", "last_played", "plays", "skips", "liked")


class DB:
    def __init__(self, path):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.lock = threading.RLock()
        with self.lock:
            self.conn.executescript(SCHEMA)
            self.conn.commit()

    # ---------- helpers ----------
    def _q(self, sql, args=(), one=False):
        with self.lock:
            cur = self.conn.execute(sql, args)
            rows = cur.fetchall()
        rows = [self._row(r) for r in rows]
        return (rows[0] if rows else None) if one else rows

    def _x(self, sql, args=()):
        with self.lock:
            cur = self.conn.execute(sql, args)
            self.conn.commit()
            return cur.lastrowid

    @staticmethod
    def _row(r):
        d = dict(r)
        for k in ("tags", "genres"):
            if k in d:
                try:
                    d[k] = json.loads(d[k]) if d[k] else []
                except ValueError:
                    d[k] = []
        if "liked" in d:
            d["liked"] = bool(d["liked"])
        return d

    # ---------- canciones ----------
    def add_track(self, t):
        """Inserta o actualiza una canción por URL. Devuelve su id."""
        existing = self._q("SELECT id FROM tracks WHERE url=?", (t["url"],), one=True)
        if existing:
            self._x("""UPDATE tracks SET title=COALESCE(?,title), artist=COALESCE(?,artist),
                       track=COALESCE(?,track), duration=COALESCE(?,duration),
                       thumb=COALESCE(?,thumb) WHERE id=?""",
                    (t.get("title"), t.get("artist"), t.get("track"), t.get("duration"),
                     t.get("thumb"), existing["id"]))
            return existing["id"]
        return self._x(
            """INSERT INTO tracks (url,title,artist,track,duration,thumb,source,tags,added_at)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (t["url"], t.get("title"), t.get("artist"), t.get("track"), t.get("duration"),
             t.get("thumb"), t.get("source"), json.dumps(t.get("tags") or []), time.time()))

    def get_track(self, tid):
        return self._q("SELECT * FROM tracks WHERE id=?", (tid,), one=True)

    def track_by_url(self, url):
        return self._q("SELECT * FROM tracks WHERE url=?", (url,), one=True)

    def tracks(self, search="", order="added", liked_only=False):
        sql = "SELECT * FROM tracks WHERE 1=1"
        args = []
        if search:
            sql += " AND (title LIKE ? OR artist LIKE ? OR genres LIKE ?)"
            s = f"%{search}%"
            args += [s, s, s]
        if liked_only:
            sql += " AND liked=1"
        sql += {"added": " ORDER BY added_at DESC",
                "plays": " ORDER BY plays DESC, added_at DESC",
                "title": " ORDER BY title COLLATE NOCASE",
                "artist": " ORDER BY artist COLLATE NOCASE, title COLLATE NOCASE"}.get(order, " ORDER BY added_at DESC")
        return self._q(sql, args)

    def delete_track(self, tid):
        self._x("DELETE FROM playlist_items WHERE track_id=?", (tid,))
        self._x("DELETE FROM tracks WHERE id=?", (tid,))

    def set_liked(self, tid, liked):
        self._x("UPDATE tracks SET liked=? WHERE id=?", (1 if liked else 0, tid))

    def set_genres(self, tid, genres):
        self._x("UPDATE tracks SET genres=? WHERE id=?", (json.dumps(genres), tid))

    def set_meta(self, tid, artist, track):
        self._x("UPDATE tracks SET artist=?, track=?, genres=NULL WHERE id=?", (artist, track, tid))

    def tracks_without_genres(self):
        return self._q("SELECT * FROM tracks WHERE genres IS NULL")

    def count_play(self, tid):
        self._x("UPDATE tracks SET plays=plays+1, last_played=? WHERE id=?", (time.time(), tid))

    def count_skip(self, tid):
        self._x("UPDATE tracks SET skips=skips+1 WHERE id=?", (tid,))

    # ---------- playlists ----------
    def create_playlist(self, name, source_url=None):
        return self._x("INSERT INTO playlists (name, source_url, created_at) VALUES (?,?,?)",
                       (name, source_url, time.time()))

    def playlists(self):
        return self._q("""SELECT p.*, COUNT(i.track_id) AS count FROM playlists p
                          LEFT JOIN playlist_items i ON i.playlist_id=p.id
                          GROUP BY p.id ORDER BY p.created_at DESC""")

    def rename_playlist(self, pid, name):
        self._x("UPDATE playlists SET name=? WHERE id=?", (name, pid))

    def delete_playlist(self, pid):
        self._x("DELETE FROM playlist_items WHERE playlist_id=?", (pid,))
        self._x("DELETE FROM playlists WHERE id=?", (pid,))

    def add_to_playlist(self, pid, tids):
        row = self._q("SELECT COALESCE(MAX(pos),0) AS m FROM playlist_items WHERE playlist_id=?", (pid,), one=True)
        pos = row["m"] if row else 0
        for tid in tids:
            pos += 1
            self._x("INSERT OR IGNORE INTO playlist_items (playlist_id, track_id, pos) VALUES (?,?,?)",
                    (pid, tid, pos))

    def remove_from_playlist(self, pid, tid):
        self._x("DELETE FROM playlist_items WHERE playlist_id=? AND track_id=?", (pid, tid))

    def playlist_tracks(self, pid):
        return self._q("""SELECT t.* FROM playlist_items i JOIN tracks t ON t.id=i.track_id
                          WHERE i.playlist_id=? ORDER BY i.pos""", (pid,))

    # ---------- ajustes y caché ----------
    def get_setting(self, key, default=None):
        r = self._q("SELECT value FROM settings WHERE key=?", (key,), one=True)
        if not r:
            return default
        try:
            return json.loads(r["value"])
        except ValueError:
            return r["value"]

    def set_setting(self, key, value):
        self._x("INSERT OR REPLACE INTO settings (key, value) VALUES (?,?)", (key, json.dumps(value)))

    def cache_get(self, key, max_age):
        r = self._q("SELECT value, ts FROM cache WHERE key=?", (key,), one=True)
        if r and time.time() - r["ts"] < max_age:
            return json.loads(r["value"])
        return None

    def cache_set(self, key, value):
        self._x("INSERT OR REPLACE INTO cache (key, value, ts) VALUES (?,?,?)",
                (key, json.dumps(value), time.time()))

    def hide_rec(self, key):
        self._x("INSERT OR IGNORE INTO hidden_recs (key) VALUES (?)", (key.lower(),))

    def hidden_recs(self):
        return {r["key"] for r in self._q("SELECT key FROM hidden_recs")}
