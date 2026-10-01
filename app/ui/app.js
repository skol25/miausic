/* Miausic — interfaz */
"use strict";

const ICONS = {
  link:'<path d="M10 14a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/><path d="M14 10a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/>',
  library:'<path d="M4 4v16M9 4v16"/><path d="M14 4l5 16"/>',
  heart:'<path d="M12 20s-7-4.4-9-9a5 5 0 0 1 9-3 5 5 0 0 1 9 3c-2 4.6-9 9-9 9z"/>',
  sparkle:'<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/>',
  chart:'<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
  gear:'<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.6 1.6 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.6 1.6 0 0 0-2.7 1.1V21a2 2 0 1 1-4 0v-.1A1.6 1.6 0 0 0 9 19.4a1.6 1.6 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1A1.6 1.6 0 0 0 3.3 14H3a2 2 0 1 1 0-4h.1A1.6 1.6 0 0 0 4.6 9a1.6 1.6 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1A1.6 1.6 0 0 0 10 3.1V3a2 2 0 1 1 4 0v.1a1.6 1.6 0 0 0 2.7 1.1l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.6 1.6 0 0 0 1.1 2.7H21a2 2 0 1 1 0 4h-.1a1.6 1.6 0 0 0-1.5 1.3z"/>',
  plus:'<path d="M12 5v14M5 12h14"/>',
  x:'<path d="M6 6l12 12M18 6L6 18"/>',
  play:'<path d="M7 4.5v15l12.5-7.5z"/>',
  pause:'<path d="M7 4h3.5v16H7zM13.5 4H17v16h-3.5z"/>',
  next:'<path d="M5 5l10 7-10 7z"/><path d="M19 5v14"/>',
  prev:'<path d="M19 5L9 12l10 7z"/><path d="M5 5v14"/>',
  shuffle:'<path d="M16 3h5v5M4 20L21 3M21 16v5h-5M15 15l6 6M4 4l5 5"/>',
  repeat:'<path d="M17 2l4 4-4 4"/><path d="M3 11V9a3 3 0 0 1 3-3h15M7 22l-4-4 4-4"/><path d="M21 13v2a3 3 0 0 1-3 3H3"/>',
  repeat1:'<path d="M17 2l4 4-4 4"/><path d="M3 11V9a3 3 0 0 1 3-3h15M7 22l-4-4 4-4"/><path d="M21 13v2a3 3 0 0 1-3 3H3"/><path d="M11 10h1v5"/>',
  queue:'<path d="M3 6h13M3 12h13M3 18h9"/><path d="M17 15l5 3-5 3z"/>',
  volume:'<path d="M11 5L6 9H3v6h3l5 4z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M18.5 5.5a9 9 0 0 1 0 13"/>',
  mini:'<rect x="3" y="4" width="18" height="16" rx="2"/><rect x="12" y="12" width="7" height="6" rx="1"/>',
  more:'<circle cx="5" cy="12" r="1.2"/><circle cx="12" cy="12" r="1.2"/><circle cx="19" cy="12" r="1.2"/>',
  save:'<path d="M12 4v12M6 10l6 6 6-6M5 20h14"/>',
  list:'<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
  trash:'<path d="M3 6h18M8 6V4h8v2M6 6l1 14h10l1-14"/>',
  edit:'<path d="M4 20h4L20 8l-4-4L4 16z"/>',
  search:'<circle cx="11" cy="11" r="7"/><path d="M21 21l-5-5"/>',
  refresh:'<path d="M21 12a9 9 0 1 1-3-6.7L21 8"/><path d="M21 3v5h-5"/>',
  clip:'<rect x="8" y="3" width="8" height="4" rx="1"/><path d="M16 5h2a2 2 0 0 1 2 2v13a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2h2"/>',
  ext:'<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
  next_up:'<path d="M4 6h12M4 12h8M4 18h8"/><path d="M16 12v8M12 16h8"/>',
};
const ic = (n) => `<i data-icon="${n}"><svg viewBox="0 0 24 24">${ICONS[n] || ""}</svg></i>`;
function paintIcons(root = document) {
  root.querySelectorAll("i[data-icon]:not(:has(svg))").forEach(el => {
    el.innerHTML = `<svg viewBox="0 0 24 24">${ICONS[el.dataset.icon] || ""}</svg>`;
  });
}
/* ---------- Michi en pixel art (mismos sprites y colores que MiauIA) ---------- */
const MICHI_CFG = { pelaje: "#2b2b31", manchas: "#f4f1ea", ojos: "#c5e063", nariz: "#f09ab0", color_accesorio: "#e5484d" };
const _rgb = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
const _hex = c => "#" + c.map(v => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, "0")).join("");
const _mez = (a, b, t) => { const x = _rgb(a), y = _rgb(b); return _hex(x.map((v, i) => v + (y[i] - v) * t)); };
function michiColores(p) {  // patrón esmoquin, igual que en MiauIA
  const pel = p.pelaje, man = p.manchas;
  return { G: pel, T: pel, U: pel, Q: pel, o: _mez(pel, "#08080c", 0.6), M: pel, m: _mez(pel, "#000000", 0.28),
    H: _mez(pel, "#ffffff", 0.22), S: man, B: man, F: man, b: _mez(man, "#000000", 0.18), E: p.ojos, P: "#15151a",
    W: "#ffffff", N: p.nariz, Z: "#cfd4dc", R: "#e5484d", K: "#5b8def", k: "#3c63b0", A: p.color_accesorio,
    Y: "#f2c94c", C: "#ff5c8a" };
}
const MCOL = michiColores(MICHI_CFG), _frames = new Map();
function michiFrame(anim, i) {
  const key = anim + i;
  if (_frames.has(key)) return _frames.get(key);
  const S = window.MICHI_SPRITES, q = S.animaciones[anim].cuadros[i];
  const c = document.createElement("canvas"); c.width = S.ancho; c.height = S.alto;
  const x = c.getContext("2d");
  q.filas.forEach((fila, y) => [...fila].forEach((ch, xx) => { if (ch !== ".") { x.fillStyle = MCOL[ch] || "#f0f"; x.fillRect(xx, y, 1, 1); } }));
  for (const [ax, ay, ch] of (q.acc.collar || [])) { x.fillStyle = MCOL[ch]; x.fillRect(ax, ay, 1, 1); }
  _frames.set(key, c);
  return c;
}
let michiFiesta = 0;  // hasta cuándo festeja
function michiFestejar() { michiFiesta = performance.now() + 1500; }
function michiAnimAuto() {
  if (performance.now() < michiFiesta) return "festejar";
  const st = S.state?.status;
  return st === "playing" ? "audifonos" : st === "loading" ? "escuchar" : st === "error" ? "sentado" : "dormir";
}
function michiTick() {
  const S2 = window.MICHI_SPRITES; if (!S2) return;
  const now = performance.now(), auto = michiAnimAuto();
  document.querySelectorAll("canvas.michi-px").forEach(cv => {
    if (!cv.offsetParent) return;  // no se ve: no gastamos nada
    const anim = cv.dataset.mood === "auto" ? auto : (cv.dataset.anim || "sentado");
    const A = S2.animaciones[anim], i = Math.floor(now / 1000 * A.fps) % A.cuadros.length;
    const k = anim + i; if (cv._k === k) return; cv._k = k;
    if (cv.width !== S2.ancho) { cv.width = S2.ancho; cv.height = S2.alto; }
    const x = cv.getContext("2d"); x.imageSmoothingEnabled = false;
    x.clearRect(0, 0, cv.width, cv.height); x.drawImage(michiFrame(anim, i), 0, 0);
  });
}
setInterval(michiTick, 125);  // 8 cuadros por segundo como máximo
const MICHI = (anim = "sentado") => anim === "auto" ? `<canvas class="michi-px" data-mood="auto"></canvas>` : `<canvas class="michi-px" data-anim="${anim}"></canvas>`;
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const fmt = (s) => { s = Math.max(0, Math.floor(s || 0)); const h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60), x = String(s % 60).padStart(2, "0"); return h ? `${h}:${String(m).padStart(2, "0")}:${x}` : `${m}:${x}`; };
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];

let api = null;
async function call(name, ...args) {
  try {
    const r = await api[name](...args);
    if (r && typeof r === "object" && !Array.isArray(r) && r.error) { toast(r.error, true); return null; }
    return r;
  } catch (e) { toast(String(e.message || e), true); return null; }
}

const S = { view: "add", playlistId: null, state: null, lastInspect: null, playlists: [], recs: null, librarySearch: "", libraryOrder: "added" };

/* ---------- utilidades de UI ---------- */
let toastT;
function toast(msg, err = false) {
  const t = $("#toast"); t.textContent = msg; t.className = "toast show" + (err ? " err" : "");
  clearTimeout(toastT); toastT = setTimeout(() => t.className = "toast", err ? 4200 : 2200);
}
function modal(html, onOk) {
  const bg = $("#modalBg"), m = $("#modal");
  m.innerHTML = html; paintIcons(m); bg.classList.add("show");
  const close = () => bg.classList.remove("show");
  const inp = m.querySelector("input"); if (inp) { inp.focus(); inp.select(); }
  m.querySelectorAll("[data-close]").forEach(b => b.onclick = close);
  const ok = m.querySelector("[data-ok]");
  if (ok) ok.onclick = async () => { if (await onOk(m) !== false) close(); };
  m.onkeydown = (e) => { if (e.key === "Enter" && ok) ok.click(); if (e.key === "Escape") close(); };
  bg.onclick = (e) => { if (e.target === bg) close(); };
}
function ask(title, value = "", placeholder = "") {
  return new Promise(res => {
    let done = false;
    modal(`<h3>${esc(title)}</h3><input value="${esc(value)}" placeholder="${esc(placeholder)}">
      <div class="row-actions"><button class="btn" data-close>Cancelar</button><button class="btn primary" data-ok>Listo</button></div>`,
      (m) => { done = true; res(m.querySelector("input").value.trim()); });
    const obs = setInterval(() => { if (!$("#modalBg").classList.contains("show")) { clearInterval(obs); if (!done) res(null); } }, 200);
  });
}
function menu(x, y, items) {
  const m = $("#menu");
  m.innerHTML = items.map((it, i) => it === "-" ? "<hr>" : `<button data-i="${i}" class="${it.danger ? "danger" : ""}">${ic(it.icon || "plus")}${esc(it.label)}</button>`).join("");
  m.classList.add("show");
  const r = m.getBoundingClientRect();
  m.style.left = Math.min(x, innerWidth - r.width - 8) + "px";
  m.style.top = Math.min(y, innerHeight - r.height - 8) + "px";
  m.querySelectorAll("button").forEach(b => b.onclick = (e) => { e.stopPropagation(); m.classList.remove("show"); items[+b.dataset.i].run(); });
}
document.addEventListener("click", () => $("#menu").classList.remove("show"));
document.addEventListener("contextmenu", e => { if (!e.target.closest("input")) e.preventDefault(); });

async function pickPlaylist(tids) {
  const pls = await call("playlists") || [];
  const items = [{ label: "Nueva playlist…", icon: "plus", run: async () => {
    const name = await ask("Nueva playlist", "", "Ej: Para estudiar");
    if (!name) return;
    await call("create_playlist", name, tids); toast(`Agregada a "${name}"`); loadPlaylists();
  } }];
  if (pls.length) items.push("-");
  pls.slice(0, 12).forEach(p => items.push({ label: p.name, icon: "list", run: async () => {
    await call("add_to_playlist", p.id, tids); toast(`Agregada a "${p.name}"`); loadPlaylists();
  } }));
  return items;
}

/* ---------- navegación ---------- */
function go(view, extra) {
  S.view = view; if (view === "playlist") S.playlistId = extra;
  $$(".nav button").forEach(b => b.classList.toggle("active", b.dataset.view === view));
  $$(".pl-item").forEach(b => b.classList.toggle("active", view === "playlist" && +b.dataset.id === S.playlistId));
  render();
}
async function render() {
  const v = $("#view"); v.scrollTop = 0;
  const views = { add: viewAdd, library: () => viewLibrary(false), liked: () => viewLibrary(true), foryou: viewForYou, taste: viewTaste, settings: viewSettings, playlist: viewPlaylist };
  await (views[S.view] || viewAdd)(v);
  paintIcons(v);
}

async function loadPlaylists() {
  S.playlists = await call("playlists") || [];
  $("#plList").innerHTML = S.playlists.map(p => `<button class="pl-item${S.view === "playlist" && S.playlistId === p.id ? " active" : ""}" data-id="${p.id}">
    ${ic("list")}<span class="pl-name">${esc(p.name)}</span><span class="pl-count">${p.count}</span></button>`).join("")
    || `<div class="hint" style="padding:6px 10px">Aún no tienes playlists</div>`;
  $$(".pl-item").forEach(b => b.onclick = () => go("playlist", +b.dataset.id));
}

/* ---------- lista de canciones (se usa en varias vistas) ---------- */
function trackList(tracks, opts = {}) {
  const cur = S.state?.track;
  const head = `<div class="t-row t-head"><div class="t-n">${opts.checks ? '<input type="checkbox" id="checkAll" checked>' : "#"}</div><div></div><div>Título</div><div>Géneros</div><div class="t-dur">Dur.</div><div></div></div>`;
  const rows = tracks.map((t, i) => {
    const now = cur && ((t.id && cur.id === t.id) || (cur.url && cur.url === t.url));
    const genres = (t.genres || []).slice(0, 2).map(g => `<span class="chip">${esc(g)}</span>`).join("") || (t.saved === false ? '<span class="chip">sin guardar</span>' : "");
    return `<div class="t-row${now ? " now" : ""}" data-i="${i}" data-url="${esc(t.url || "")}">
      <div class="t-n">${opts.checks ? `<input type="checkbox" class="pick" data-i="${i}" ${t.saved ? "" : "checked"}>` : i + 1}</div>
      <div class="t-thumb" style="background-image:url('${esc(t.thumb || "")}')"><button data-act="play" title="Reproducir">${ic("play")}</button></div>
      <div style="min-width:0"><div class="t-title">${esc(t.track || t.title)}</div><div class="t-artist">${esc(t.artist || t.source || "")}</div></div>
      <div class="t-genres">${genres}</div>
      <div class="t-dur">${t.duration ? fmt(t.duration) : ""}</div>
      <div class="t-acts">
        ${t.id ? `<button class="icon-btn sm like${t.liked ? " on" : ""}" data-act="like" title="Me gusta">${ic("heart")}</button>` : ""}
        <button class="icon-btn sm" data-act="more" title="Más">${ic("more")}</button>
      </div></div>`;
  }).join("");
  return `<div class="tracks">${head}${rows}</div>`;
}
function bindTrackList(root, tracks, opts = {}) {
  $$(".t-row[data-i]", root).forEach(row => {
    const i = +row.dataset.i, t = tracks[i];
    row.ondblclick = () => playList(tracks, i);
    row.querySelector('[data-act="play"]').onclick = (e) => { e.stopPropagation(); playList(tracks, i); };
    const like = row.querySelector('[data-act="like"]');
    if (like) like.onclick = async (e) => {
      e.stopPropagation(); const r = await call("toggle_like", t.id);
      if (r === null) return; t.liked = r; like.classList.toggle("on", r); if (r) michiFestejar();
      if (!r && S.view === "liked") render();
    };
    row.querySelector('[data-act="more"]').onclick = async (e) => {
      e.stopPropagation();
      const items = [
        { label: "Reproducir a continuación", icon: "next_up", run: () => call("enqueue", [t], true).then(() => toast("Sonará después")) },
        { label: "Agregar a la cola", icon: "queue", run: () => call("enqueue", [t], false).then(() => toast("Agregada a la cola")) },
      ];
      if (t.id) {
        items.push({ label: "Agregar a playlist…", icon: "list", run: async () => { const r = row.getBoundingClientRect(); setTimeout(async () => menu(r.right - 220, r.top, await pickPlaylist([t.id])), 0); } });
        items.push({ label: "Corregir artista / título", icon: "edit", run: () => editMeta(t) });
      } else {
        items.push({ label: "Guardar en biblioteca", icon: "save", run: async () => { const r = await call("save_tracks", [t]); if (r) { t.id = r.ids[0]; t.saved = true; toast("Guardada"); render(); } } });
      }
      items.push({ label: "Abrir link original", icon: "ext", run: () => call("open_link", t.url) });
      if (opts.playlistId && t.id) items.push("-", { label: "Quitar de esta playlist", icon: "x", run: async () => { await call("remove_from_playlist", opts.playlistId, t.id); loadPlaylists(); render(); } });
      if (t.id && !opts.playlistId) items.push("-", { label: "Borrar de la biblioteca", icon: "trash", danger: true, run: async () => { await call("delete_track", t.id); toast("Borrada"); loadPlaylists(); render(); } });
      menu(e.clientX, e.clientY, items);
    };
    row.oncontextmenu = (e) => { e.preventDefault(); row.querySelector('[data-act="more"]').onclick(e); };
  });
}
function editMeta(t) {
  modal(`<h3>Corregir datos</h3><p class="sub" style="margin-bottom:12px">Así Michi entiende mejor el género.</p>
    <input id="mA" placeholder="Artista" value="${esc(t.artist || "")}"><input id="mT" placeholder="Canción" value="${esc(t.track || t.title || "")}">
    <div class="row-actions"><button class="btn" data-close>Cancelar</button><button class="btn primary" data-ok>Guardar</button></div>`,
    async (m) => { await call("edit_meta", t.id, $("#mA", m).value, $("#mT", m).value); toast("Listo, buscando su género…"); render(); });
}
async function playList(tracks, i) {
  const clean = tracks.map(t => ({ ...t }));
  await call("play", clean, i);
  poll();
}

/* ---------- Vista: agregar link ---------- */
async function viewAdd(v) {
  v.innerHTML = `
    <div class="hero">${MICHI("auto")}
      <div style="flex:1;min-width:0">
        <h1>¿Qué escuchamos hoy?</h1>
        <div class="sub">Pega un link de YouTube, YouTube Music, SoundCloud, Bandcamp… una canción o una playlist entera.</div>
        <div class="paste">
          <input id="urlIn" placeholder="https://…" spellcheck="false">
          <button class="btn" id="pasteBtn" title="Pegar">${ic("clip")}Pegar</button>
          <button class="btn primary" id="goBtn">Abrir</button>
        </div>
        <div class="hint">Consejo: también puedes pegar el link en cualquier momento con Ctrl+V.</div>
      </div>
    </div>
    <div id="result"></div>`;
  const inp = $("#urlIn", v);
  $("#goBtn", v).onclick = () => openUrl(inp.value);
  inp.onkeydown = (e) => { if (e.key === "Enter") openUrl(inp.value); };
  $("#pasteBtn", v).onclick = async () => {
    try { inp.value = (await navigator.clipboard.readText()).trim(); openUrl(inp.value); }
    catch { inp.focus(); toast("Usa Ctrl+V para pegar"); }
  };
  if (S.lastInspect) showResult(S.lastInspect);
  updateMichi();
}
async function openUrl(url) {
  url = (url || "").trim();
  if (!/^https?:\/\//i.test(url)) { toast("Eso no parece un link", true); return; }
  if (S.view !== "add") { go("add"); await new Promise(r => setTimeout(r, 30)); }
  $("#urlIn").value = url;
  $("#result").innerHTML = `<div class="loading-row"><span class="spinner"></span>Michi está revisando el link…</div>`;
  const r = await call("inspect", url);
  if (!r) { $("#result").innerHTML = ""; return; }
  S.lastInspect = r; showResult(r);
}
function showResult(r) {
  const box = $("#result");
  if (r.type === "track") {
    const t = r.track;
    box.innerHTML = `<div class="result-card">
      <div class="cover wide" style="background-image:url('${esc(t.thumb || "")}')"></div>
      <div style="min-width:0"><div class="kind">Canción</div><h2>${esc(t.track || t.title)}</h2>
        <div class="sub">${esc(t.artist || "")} ${t.duration ? "· " + fmt(t.duration) : ""} · ${esc(t.source || "")}</div>
        <div class="row-actions">
          <button class="btn primary" id="rPlay">${ic("play")}Reproducir</button>
          <button class="btn" id="rSave" ${t.saved ? "disabled" : ""}>${ic("save")}${t.saved ? "Ya está guardada" : "Guardar"}</button>
          <button class="btn" id="rPl">${ic("list")}A una playlist</button>
          <button class="btn" id="rQ">${ic("queue")}A la cola</button>
        </div></div></div>`;
    paintIcons(box);
    const ensure = async () => { if (t.id) return t.id; const s = await call("save_tracks", [t]); if (s) { t.id = s.ids[0]; t.saved = true; loadPlaylists(); } return t.id; };
    $("#rPlay").onclick = async () => { await ensure(); playList([t], 0); };
    $("#rSave").onclick = async () => { if (await ensure()) { michiFestejar(); toast("Guardada en tu biblioteca"); showResult(r); } };
    $("#rPl").onclick = async (e) => { e.stopPropagation(); const id = await ensure(); if (id) menu(e.clientX, e.clientY, await pickPlaylist([id])); };
    $("#rQ").onclick = () => call("enqueue", [t]).then(() => toast("Agregada a la cola"));
    return;
  }
  const es = r.entries;
  const total = es.reduce((a, e) => a + (e.duration || 0), 0);
  box.innerHTML = `<div class="result-card">
      <div class="cover" style="background-image:url('${esc(r.thumb || "")}')"></div>
      <div style="min-width:0"><div class="kind">Playlist</div><h2>${esc(r.title)}</h2>
        <div class="sub">${esc(r.uploader || "")} · ${es.length} canciones${total ? " · " + fmt(total) : ""}</div>
        <div class="row-actions">
          <button class="btn primary" id="rPlayAll">${ic("play")}Reproducir todo</button>
          <button class="btn" id="rSavePl">${ic("list")}Guardar como playlist</button>
          <button class="btn" id="rSaveSel">${ic("save")}Guardar seleccionadas</button>
        </div></div></div>
    <div id="plEntries">${trackList(es, { checks: true })}</div>`;
  paintIcons(box);
  bindTrackList(box, es);
  const all = $("#checkAll"); if (all) all.onchange = () => $$(".pick", box).forEach(c => c.checked = all.checked);
  const picked = () => $$(".pick", box).filter(c => c.checked).map(c => es[+c.dataset.i]);
  $("#rPlayAll").onclick = async () => {
    const s = await call("save_tracks", es);  // se guardan para contar lo que escuchas
    if (s) s.ids.forEach((id, i) => { es[i].id = id; es[i].saved = true; });
    playList(es, 0); loadPlaylists(); showResult(r);
  };
  $("#rSavePl").onclick = async () => {
    const name = await ask("Nombre de la playlist", r.title);
    if (!name) return;
    const s = await call("save_tracks", es, name, r.url);
    if (s) { michiFestejar(); toast(`Playlist "${name}" guardada`); await loadPlaylists(); go("playlist", s.playlist_id); }
  };
  $("#rSaveSel").onclick = async () => {
    const p = picked(); if (!p.length) return toast("Marca al menos una");
    const s = await call("save_tracks", p);
    if (s) { s.ids.forEach((id, i) => { p[i].id = id; p[i].saved = true; }); toast(`${p.length} guardadas en tu biblioteca`); showResult(r); }
  };
}

/* ---------- Vista: biblioteca y favoritas ---------- */
async function viewLibrary(likedOnly, keepFocus = false) {
  const v = $("#view");
  const tracks = await call("library", S.librarySearch, S.libraryOrder, likedOnly) || [];
  const title = likedOnly ? "Favoritas" : "Biblioteca";
  if (!keepFocus) {
    v.innerHTML = `<div class="view-head"><div><h1>${title}</h1><div class="sub" id="libCount"></div></div>
      <div class="row-actions"><button class="btn primary" id="playAll">${ic("play")}Reproducir</button><button class="btn" id="shufAll">${ic("shuffle")}Aleatorio</button></div></div>
      <div class="tools"><label class="search">${ic("search")}<input id="libSearch" placeholder="Buscar canción, artista o género" value="${esc(S.librarySearch)}"></label>
        <select id="libOrder"><option value="added">Recientes</option><option value="plays">Más escuchadas</option><option value="artist">Artista</option><option value="title">Título</option></select></div>
      <div id="libList"></div>`;
    $("#libOrder").value = S.libraryOrder;
    let deb; $("#libSearch").oninput = (e) => { S.librarySearch = e.target.value; clearTimeout(deb); deb = setTimeout(() => viewLibrary(likedOnly, true), 220); };
    $("#libOrder").onchange = (e) => { S.libraryOrder = e.target.value; viewLibrary(likedOnly, true); };
  }
  $("#libCount").textContent = `${tracks.length} canciones`;
  $("#playAll").onclick = () => tracks.length && playList(tracks, 0);
  $("#shufAll").onclick = async () => { if (!tracks.length) return; await call("shuffle", true); playList(tracks, Math.floor(Math.random() * tracks.length)); };
  const list = $("#libList");
  if (!tracks.length) {
    list.innerHTML = `<div class="empty">${MICHI("dormir")}<b>${S.librarySearch ? "No encontré nada" : likedOnly ? "Aún no tienes favoritas" : "Tu biblioteca está vacía"}</b>
      <span>${S.librarySearch ? "Prueba con otra palabra." : likedOnly ? "Toca el corazón de las canciones que más te gusten." : "Pega un link en “Agregar link” para empezar."}</span></div>`;
  } else { list.innerHTML = trackList(tracks); bindTrackList(list, tracks); }
  paintIcons(v);
}

/* ---------- Vista: playlist ---------- */
async function viewPlaylist(v) {
  const p = S.playlists.find(x => x.id === S.playlistId);
  if (!p) return go("library");
  const tracks = await call("playlist_tracks", p.id) || [];
  const total = tracks.reduce((a, t) => a + (t.duration || 0), 0);
  v.innerHTML = `<div class="view-head"><div><div class="sub" style="text-transform:uppercase;font-size:11px;letter-spacing:1px;color:var(--accent);font-weight:700">Playlist</div><h1>${esc(p.name)}</h1>
      <div class="sub">${tracks.length} canciones${total ? " · " + fmt(total) : ""}</div></div>
    <div class="row-actions"><button class="btn primary" id="plPlay">${ic("play")}Reproducir</button><button class="btn" id="plShuf">${ic("shuffle")}Aleatorio</button>
      <button class="icon-btn" id="plMore">${ic("more")}</button></div></div><div id="plTracks"></div>`;
  const list = $("#plTracks", v);
  if (tracks.length) { list.innerHTML = trackList(tracks); bindTrackList(list, tracks, { playlistId: p.id }); }
  else list.innerHTML = `<div class="empty">${MICHI("dormir")}<b>Playlist vacía</b><span>Agrega canciones desde la biblioteca con el botón “…”.</span></div>`;
  $("#plPlay", v).onclick = () => tracks.length && playList(tracks, 0);
  $("#plShuf", v).onclick = async () => { if (!tracks.length) return; await call("shuffle", true); playList(tracks, Math.floor(Math.random() * tracks.length)); };
  $("#plMore", v).onclick = (e) => { e.stopPropagation(); menu(e.clientX - 180, e.clientY, [
    { label: "Cambiar nombre", icon: "edit", run: async () => { const n = await ask("Nuevo nombre", p.name); if (n) { await call("rename_playlist", p.id, n); await loadPlaylists(); render(); } } },
    ...(p.source_url ? [{ label: "Abrir link original", icon: "ext", run: () => call("open_link", p.source_url) }] : []),
    "-", { label: "Borrar playlist", icon: "trash", danger: true, run: async () => { await call("delete_playlist", p.id); toast("Playlist borrada"); await loadPlaylists(); go("library"); } },
  ]); };
}

/* ---------- Vista: Para ti ---------- */
const PALETTE = [["#ff9a4d", "#b8452a"], ["#5b8cff", "#2b3f99"], ["#33c08f", "#16624a"], ["#d76bff", "#6a2b99"], ["#ffcc4d", "#a2661c"], ["#ff5c7a", "#8f2440"], ["#4dd2ff", "#1d6a8f"]];
const hash = (s) => [...s].reduce((a, c) => (a * 31 + c.charCodeAt(0)) >>> 0, 7);
async function viewForYou(v, refresh = false) {
  v.innerHTML = `<div class="view-head"><div><h1>Para ti</h1><div class="sub">Michi escogió estas según lo que escuchas y te gusta.</div></div>
    <div class="row-actions"><button class="btn primary" id="recPlay">${ic("play")}Reproducir todo</button><button class="btn" id="recRef">${ic("refresh")}Nuevas sugerencias</button></div></div>
    <div id="recBody"><div class="loading-row"><span class="spinner"></span>Michi está buscando música para ti…</div></div>`;
  paintIcons(v);
  $("#recRef", v).onclick = () => viewForYou(v, true);
  const r = await call("recommendations", refresh);
  const body = $("#recBody", v);
  if (!r) { body.innerHTML = ""; return; }
  if (r.need_key) {
    body.innerHTML = `<div class="empty">${MICHI("sentado")}<b>Falta un pasito</b><span>Para recomendarte música, Michi necesita una clave gratis de Last.fm.</span>
      <button class="btn primary" id="goSet" style="margin-top:8px">${ic("gear")}Configurarla (2 minutos)</button></div>`;
    paintIcons(body); $("#goSet").onclick = () => go("settings"); return;
  }
  if (r.empty || !r.items.length) {
    body.innerHTML = `<div class="empty">${MICHI("dormir")}<b>${r.empty ? "Primero guarda algunas canciones" : "Todavía no tengo suficientes pistas"}</b>
      <span>Mientras más escuches y marques con ♥, mejores serán las sugerencias.</span></div>`; return;
  }
  const items = r.items;
  body.innerHTML = `<div class="recs">${items.map((x, i) => {
    const [a, b] = PALETTE[hash(x.artist) % PALETTE.length];
    const initials = x.artist.split(/\s+/).slice(0, 2).map(w => w[0] || "").join("").toUpperCase();
    return `<div class="rec" data-i="${i}">
      <div class="art" style="background:linear-gradient(135deg,${a},${b})">${esc(initials)}<button class="playo" data-act="play">${ic("play")}</button></div>
      <div class="r-title" title="${esc(x.title)}">${esc(x.title)}</div><div class="r-artist">${esc(x.artist)}</div>
      <div class="r-why">${esc(x.reason)}</div>
      <div class="r-acts"><button class="icon-btn sm" data-act="save" title="Guardar en biblioteca">${ic("plus")}</button>
        <button class="icon-btn sm" data-act="queue" title="A la cola">${ic("queue")}</button>
        <button class="icon-btn sm" data-act="hide" title="No me interesa" style="margin-left:auto">${ic("x")}</button></div></div>`;
  }).join("")}</div>`;
  paintIcons(body);
  const asTrack = (x) => ({ title: x.title, track: x.title, artist: x.artist, query: x.query, url: x.url, thumb: x.thumb, rec_key: x.key });
  $("#recPlay", v).onclick = () => playList(items.map(asTrack), 0);
  $$(".rec", body).forEach(el => {
    const x = items[+el.dataset.i];
    el.querySelector('[data-act="play"]').onclick = () => playList(items.map(asTrack), +el.dataset.i);
    el.querySelector('[data-act="queue"]').onclick = () => call("enqueue", [asTrack(x)]).then(() => toast("Agregada a la cola"));
    el.querySelector('[data-act="save"]').onclick = async (e) => {
      const b = e.currentTarget; b.innerHTML = '<span class="spinner" style="width:14px;height:14px;border-width:2px"></span>';
      const s = await call("save_rec", x); if (s) { toast("Guardada en tu biblioteca"); michiFestejar(); el.remove(); } else { b.innerHTML = ic("plus"); }
    };
    el.querySelector('[data-act="hide"]').onclick = async () => { await call("hide_rec", x.key); el.style.opacity = .3; setTimeout(() => el.remove(), 200); };
  });
}

/* ---------- Vista: mis gustos ---------- */
async function viewTaste(v) {
  const p = await call("profile");
  if (!p) return;
  const max = Math.max(1, ...p.genres.map(g => g.pct));
  v.innerHTML = `<div class="view-head"><div><h1>Mis gustos</h1><div class="sub">Lo que Michi aprendió de ti.</div></div></div>
    ${!p.has_key ? `<div class="michi-says">${MICHI("sentado")}<div><b>Conecta Last.fm para ver tus géneros.</b><br>Es gratis y toma dos minutos. <a style="color:var(--accent);cursor:pointer" id="goSet">Ir a Ajustes</a></div></div>` : ""}
    ${p.has_key && p.pending ? `<div class="michi-says">${MICHI("escuchar")}<div><b>Michi está revisando ${p.pending} canciones…</b><br>Vuelve en un ratito para ver los géneros completos.</div></div>` : ""}
    <div class="stats">
      <div class="stat"><div class="v">${p.total_tracks}</div><div class="l">canciones guardadas</div></div>
      <div class="stat"><div class="v">${p.total_plays}</div><div class="l">veces escuchadas</div></div>
      <div class="stat"><div class="v" style="text-transform:capitalize">${esc(p.genres[0]?.name || "—")}</div><div class="l">tu género principal</div></div>
    </div>
    <div class="cols">
      <div class="card"><h3>Tus géneros</h3>${p.genres.length ? p.genres.map(g => `<div class="gbar"><div class="n">${esc(g.name)}</div><div class="track"><div style="width:${(g.pct / max * 100).toFixed(1)}%"></div></div><div class="p">${g.pct}%</div></div>`).join("") : '<div class="sub">Aún no hay datos.</div>'}</div>
      <div class="card"><h3>Tus artistas</h3><div class="alist">${p.artists.length ? p.artists.map((a, i) => `<div><b>${i + 1}. ${esc(a.name)}</b><span>${a.score} pts</span></div>`).join("") : '<div class="sub">Aún no hay datos.</div>'}</div></div>
    </div>`;
  const gs = $("#goSet", v); if (gs) gs.onclick = () => go("settings");
}

/* ---------- Vista: ajustes ---------- */
async function viewSettings(v) {
  const s = await call("settings") || {};
  v.innerHTML = `<div class="view-head"><div><h1>Ajustes</h1></div></div>
    <div class="setting"><h3>Recomendaciones (Last.fm)</h3>
      <p>Michi usa Last.fm para saber el género de cada canción y encontrar artistas parecidos. Es gratis:</p>
      <ol><li>Entra a <a id="lfmLink">last.fm/api/account/create</a> e inicia sesión (o crea una cuenta).</li>
        <li>En “Application name” escribe <code>Miausic</code>. Lo demás puede quedar vacío.</li>
        <li>Copia la <b>API key</b> que te da y pégala aquí abajo.</li></ol>
      <div class="field"><input id="lfmKey" placeholder="API key de Last.fm" value="${esc(s.lastfm_key || "")}" spellcheck="false"><button class="btn primary" id="lfmSave">Guardar</button></div>
    </div>
    <div class="setting"><h3>Versión</h3>
      <p>Tienes Miausic <b>${esc(s.version || "")}</b>. <span id="updMsg"></span></p>
      <div class="row-actions" style="margin-top:10px"><button class="btn" id="updCheck">${ic("refresh")}Buscar actualizaciones</button>
        <button class="btn primary" id="updGo" style="display:none">${ic("save")}Actualizar ahora</button></div></div>
    <div class="setting"><h3>Atajos</h3>
      <p><code>Espacio</code> reproducir/pausar · <code>Ctrl+→</code> siguiente · <code>Ctrl+←</code> anterior · <code>Ctrl+V</code> pegar un link · teclas multimedia del teclado.</p></div>
    <div class="setting"><h3>Tus datos</h3><p>Todo se guarda solo en tu PC, en:<br><code>${esc(s.data_dir || "")}</code></p>
      ${s.deno === false ? '<p style="color:#ff9a9a;margin-top:8px">No encontré Deno en la carpeta bin. Algunos videos de YouTube pueden fallar: vuelve a ejecutar <code>instalar.bat</code>.</p>' : ""}</div>`;
  const showUpd = (u) => {
    if (!u) return;
    $("#updMsg").textContent = u.sin_red ? "No pude revisar (¿sin internet?)." : u.hay ? `Hay una versión nueva: ${u.version} ✨` : "Estás al día.";
    $("#updGo").style.display = u.hay && u.instalado ? "" : "none";
    if (u.hay && !u.instalado) $("#updMsg").textContent += " Descárgala desde GitHub (estás usando la carpeta de desarrollo).";
  };
  $("#updCheck", v).onclick = async () => { $("#updMsg").textContent = "Revisando…"; showUpd(await call("check_update", true)); };
  $("#updGo", v).onclick = () => startUpdate();
  $("#lfmLink", v).onclick = () => call("open_link", "https://www.last.fm/api/account/create");
  $("#lfmSave", v).onclick = async () => {
    const b = $("#lfmSave"); b.disabled = true; b.textContent = "Probando…";
    const r = await call("save_lastfm_key", $("#lfmKey").value);
    b.disabled = false; b.textContent = "Guardar";
    if (r) { michiFestejar(); toast("¡Listo! Michi ya puede recomendarte música"); }
  };
}

/* ---------- Reproductor ---------- */
let dragging = false;
function updatePlayer(st) {
  S.state = st;
  const t = st.track;
  $("#pTitle").textContent = t ? (t.track || t.title || "Sin título") : "Nada sonando";
  $("#pArtist").textContent = st.status === "error" ? "No se pudo reproducir: " + (st.error || "")
    : st.status === "loading" ? "Cargando…" : t ? (t.artist || "") : "Pega un link para empezar";
  const th = $("#pThumb");
  if (t && t.thumb) { th.style.backgroundImage = `url('${t.thumb}')`; th.classList.add("has-img"); }
  else { th.style.backgroundImage = ""; th.classList.remove("has-img"); }
  const playing = st.status === "playing";
  const pb = $("#pPlay"); pb.innerHTML = ic(playing || st.status === "loading" ? "pause" : "play");
  pb.classList.toggle("loading", st.status === "loading");
  const like = $("#pLike"); like.style.visibility = t && t.id ? "visible" : "hidden"; like.classList.toggle("on", !!(t && t.liked));
  $("#pShuffle").classList.toggle("on", st.shuffle);
  const rp = $("#pRepeat"); rp.classList.toggle("on", st.repeat !== "off"); rp.innerHTML = ic(st.repeat === "one" ? "repeat1" : "repeat");
  rp.title = { off: "Repetir: no", all: "Repetir: todas", one: "Repetir: esta" }[st.repeat];
  if (!dragging) {
    const pct = st.duration ? Math.min(100, st.position / st.duration * 100) : 0;
    $("#pFill").style.width = pct + "%"; $("#pKnob").style.left = pct + "%";
    $("#pPos").textContent = fmt(st.position); $("#pDur").textContent = fmt(st.duration);
  }
  if (document.activeElement !== $("#pVol")) $("#pVol").value = st.volume;
  document.title = t && playing ? `${t.track || t.title} · Miausic` : "Miausic";
  updateMichi();
}
function updateMichi() { michiTick(); }
let lastKey = "";
async function poll() {
  const st = await call("state");
  if (st) {
    updatePlayer(st);
    const key = (st.track?.url || st.track?.query || "") + st.queue_index;
    if (key !== lastKey) { lastKey = key; markNowPlaying(); if ($("#queuePanel").classList.contains("open")) renderQueue(); }
  }
}
function markNowPlaying() {
  const t = S.state?.track; if (!t) return;
  // Resalta la fila que suena sin recargar la vista
  $$(".t-row[data-url]").forEach(r => r.classList.toggle("now", !!t.url && r.dataset.url === t.url));
}
async function renderQueue() {
  const q = await call("queue") || [];
  const box = $("#queueList");
  box.innerHTML = q.length ? q.map(x => `<div class="q-item${x.now ? " now" : ""}${x.past ? " past" : ""}" data-qi="${x.qi}">
    <div class="q-th" style="background-image:url('${esc(x.thumb || "")}')"></div><div><div class="q-t">${esc(x.title)}</div><div class="q-a">${esc(x.artist || "")}</div></div></div>`).join("")
    : `<div class="empty" style="padding:30px 10px">${MICHI("dormir")}<span>La cola está vacía</span></div>`;
  $$(".q-item", box).forEach(el => el.onclick = () => call("jump", +el.dataset.qi).then(poll));
  const now = $(".q-item.now", box); if (now) now.scrollIntoView({ block: "center" });
}

function bindPlayer() {
  $("#pPlay").onclick = () => call("toggle").then(poll);
  $("#pNext").onclick = () => call("next").then(poll);
  $("#pPrev").onclick = () => call("prev").then(poll);
  $("#pShuffle").onclick = () => call("shuffle", !S.state?.shuffle).then(poll);
  $("#pRepeat").onclick = () => { const n = { off: "all", all: "one", one: "off" }[S.state?.repeat || "off"]; call("repeat", n).then(poll); };
  $("#pLike").onclick = async () => { const t = S.state?.track; if (t?.id) { if (await call("toggle_like", t.id)) michiFestejar(); poll(); if (["library", "liked", "playlist"].includes(S.view)) render(); } };
  let vt; $("#pVol").oninput = (e) => { clearTimeout(vt); vt = setTimeout(() => call("volume", +e.target.value), 60); };
  $("#pQueue").onclick = () => { $("#queuePanel").classList.toggle("open"); renderQueue(); };
  $("#closeQueue").onclick = () => $("#queuePanel").classList.remove("open");
  $("#pMini").onclick = async () => { const on = !document.body.classList.contains("mini"); document.body.classList.toggle("mini", on); await call("mini", on); };
  const bar = $("#pBar");
  const seekTo = (e) => { const r = bar.getBoundingClientRect(); const p = Math.max(0, Math.min(1, (e.clientX - r.left) / r.width)); return p; };
  bar.onmousedown = (e) => {
    if (!S.state?.duration) return; dragging = true;
    const move = (ev) => { const p = seekTo(ev); $("#pFill").style.width = p * 100 + "%"; $("#pKnob").style.left = p * 100 + "%"; $("#pPos").textContent = fmt(p * S.state.duration); };
    const up = (ev) => { document.removeEventListener("mousemove", move); document.removeEventListener("mouseup", up); dragging = false; call("seek", seekTo(ev) * S.state.duration).then(poll); };
    document.addEventListener("mousemove", move); document.addEventListener("mouseup", up); move(e);
  };
  document.addEventListener("keydown", (e) => {
    const typing = e.target.closest("input, textarea");
    if (e.code === "Space" && !typing) { e.preventDefault(); $("#pPlay").click(); }
    if (e.ctrlKey && e.key === "ArrowRight" && !typing) $("#pNext").click();
    if (e.ctrlKey && e.key === "ArrowLeft" && !typing) $("#pPrev").click();
  });
  document.addEventListener("paste", (e) => {
    if (e.target.closest("input")) return;
    const txt = (e.clipboardData?.getData("text") || "").trim();
    if (/^https?:\/\//i.test(txt)) openUrl(txt);
  });
}

/* ---------- actualizaciones (igual que en Miauia) ---------- */
async function startUpdate() {
  if (!(await call("do_update"))) return;
  toast("Descargando la versión nueva…");
  const t = setInterval(async () => {
    const e = await call("update_status"); if (!e) return;
    if (e.fase === "descargando") toast(`Descargando… ${Math.round(e.progreso * 100)}%`);
    if (e.fase === "instalando") { clearInterval(t); toast("Instalando. Miausic se volverá a abrir sola."); }
    if (e.fase === "error") { clearInterval(t); toast("No se pudo actualizar: " + e.error, true); }
  }, 700);
}
async function checkUpdateQuiet() {
  const u = await api.check_update(false).catch(() => null);
  if (!u || !u.hay || !u.instalado) return;
  const b = document.createElement("button");
  b.className = "update-pill"; b.innerHTML = `${ic("sparkle")}Nueva versión ${esc(u.version)}`;
  b.onclick = () => { b.remove(); startUpdate(); };
  $(".nav.bottom").prepend(b);
}

/* ---------- arranque ---------- */
async function start() {
  api = window.pywebview.api;
  paintIcons();
  $$(".nav button").forEach(b => b.onclick = () => go(b.dataset.view));
  $("#newPlaylist").onclick = async () => { const n = await ask("Nueva playlist", "", "Ej: Para estudiar"); if (n) { const id = await call("create_playlist", n); await loadPlaylists(); go("playlist", id); } };
  bindPlayer();
  await loadPlaylists();
  render();
  poll(); setInterval(poll, 800);
  setTimeout(checkUpdateQuiet, 4000);
}
if (window.pywebview && window.pywebview.api) start();
else window.addEventListener("pywebviewready", start);
