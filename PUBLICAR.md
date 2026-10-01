# Cómo publicar Miausic (guía para Andrés)

Funciona igual que con Miauia.

## La primera vez

1. Sube el proyecto con `subir_a_github.bat` (o con GitHub Desktop).
2. Para que otras personas puedan descargar y actualizar, el repositorio debe ser **público**.
   - Tu biblioteca NO se sube: vive en `%APPDATA%\Miausic`, fuera de esta carpeta.

## Publicar una versión (la primera y cada actualización)

1. Haz tus cambios y súbelos (commit + push).
2. Ve a https://github.com/skol25/miausic → **Releases → Draft a new release**.
3. En *Choose a tag* escribe la versión nueva con una **v** adelante, por ejemplo `v1.0.0`, `v1.0.1`, `v1.1.0`
   (siempre más alta que la anterior) → *Create new tag*.
4. Escribe qué cambió (eso lo verá la gente al actualizar) y toca **Publish release**.
5. En unos 3 minutos GitHub construye solo el instalador `Miausic-Setup-1.0.0.exe` y lo agrega al release
   (lo ves en la pestaña **Actions** mientras trabaja).

Listo: quien tenga Miausic instalada verá "✨ Nueva versión" en el menú y podrá actualizar con un clic.
El enlace para compartir es: https://github.com/skol25/miausic/releases/latest

## Construir el instalador en tu PC (opcional)

Instala NSIS (https://nsis.sourceforge.io) y ejecuta:

```
python herramientas/construir.py --version 1.0.0 --repo skol25/miausic
```

Queda en `dist\Miausic-Setup-1.0.0.exe`.
