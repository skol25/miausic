# Miausic

Reproductor de música liviano para Windows con el michi pixel art de MiauIA.
Pegas links (YouTube, YouTube Music, SoundCloud, Bandcamp y más), los guardas en tu
biblioteca o en playlists, y Michi aprende tus géneros para recomendarte música nueva.
No necesita Chrome.

## Instalar

Descarga **Miausic-Setup.exe** desde [la última versión](https://github.com/skol25/miausic/releases/latest),
ábrelo y sigue los pasos. El instalador prepara todo solo y la app se actualiza sola cuando hay versión nueva.

(Para desarrollo también puedes usar `instalar.bat` desde esta carpeta.)

Para las recomendaciones, en la app ve a **Ajustes** y pega tu clave gratis de Last.fm.
Si un link de YouTube deja de funcionar, ejecuta `actualizar.bat`.

## Cómo está hecho

- **yt-dlp** lee los links de casi cualquier sitio.
- **mpv** (libmpv) reproduce solo el audio, gastando muy poco.
- **pywebview** muestra la interfaz con el motor web que ya trae Windows.
- **SQLite** guarda tu biblioteca en `%APPDATA%\Miausic`.
- **Last.fm** da los géneros y artistas parecidos para las recomendaciones.
