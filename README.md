# Miausic

Reproductor de música liviano para Windows con el michi pixel art de MiauIA.
Pegas links (YouTube, YouTube Music, SoundCloud, Bandcamp y más), los guardas en tu
biblioteca o en playlists, y Michi aprende tus géneros para recomendarte música nueva.
No necesita Chrome.

## Instalar

1. Descarga el proyecto (botón **Code → Download ZIP**) y descomprímelo.
2. Doble clic en `instalar.bat`.
3. Abre **Miausic** desde el Escritorio.

Para las recomendaciones, en la app ve a **Ajustes** y pega tu clave gratis de Last.fm.
Si un link de YouTube deja de funcionar, ejecuta `actualizar.bat`.

## Cómo está hecho

- **yt-dlp** lee los links de casi cualquier sitio.
- **mpv** (libmpv) reproduce solo el audio, gastando muy poco.
- **pywebview** muestra la interfaz con el motor web que ya trae Windows.
- **SQLite** guarda tu biblioteca en `%APPDATA%\Miausic`.
- **Last.fm** da los géneros y artistas parecidos para las recomendaciones.
