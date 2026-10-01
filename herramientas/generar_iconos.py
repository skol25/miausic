# -*- coding: utf-8 -*-
"""Genera los íconos de Miausic con el michi pixel art (los mismos sprites de Miauia)."""
import json
import os

from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SPRITES_JS = os.path.join(RAIZ, "app", "ui", "michi_sprites.js")

PELAJE, MANCHAS = "#2b2b31", "#f4f1ea"
NARANJA = (255, 154, 77, 255)
FONDO = (16, 16, 18, 255)


def _rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def _mez(a, b, t):
    a, b = _rgb(a), _rgb(b)
    return "#%02x%02x%02x" % tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


COLORES = dict(G=PELAJE, T=PELAJE, U=PELAJE, Q=PELAJE, o=_mez(PELAJE, "#08080c", .6), M=PELAJE,
               m=_mez(PELAJE, "#000000", .28), H=_mez(PELAJE, "#ffffff", .22), S=MANCHAS, B=MANCHAS, F=MANCHAS,
               b=_mez(MANCHAS, "#000000", .18), E="#c5e063", P="#15151a", W="#ffffff", N="#f09ab0", Z="#cfd4dc",
               R="#e5484d", K="#5b8def", k="#3c63b0", A="#e5484d", Y="#f2c94c", C="#ff5c8a")


def sprites():
    with open(SPRITES_JS, encoding="utf-8") as f:
        txt = f.read()
    return json.loads(txt[txt.index("{"):txt.rindex("}") + 1])


def michi(anim="audifonos", cuadro=1):
    """El michi recortado (sin espacio vacío alrededor)."""
    S = sprites()
    q = S["animaciones"][anim]["cuadros"][cuadro]
    img = Image.new("RGBA", (S["ancho"], S["alto"]), (0, 0, 0, 0))
    for y, fila in enumerate(q["filas"]):
        for x, c in enumerate(fila):
            if c != ".":
                img.putpixel((x, y), _rgb(COLORES[c]) + (255,))
    for x, y, c in q["acc"].get("collar", []):
        img.putpixel((x, y), _rgb(COLORES[c]) + (255,))
    return img.crop(img.getbbox())


def icono(lado):
    spr = michi()
    im = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, lado - 1, lado - 1], radius=max(2, lado // 5), fill=NARANJA)
    esc = max(1, (lado * 84 // 100) // max(spr.size))
    s = spr.resize((spr.width * esc, spr.height * esc), Image.NEAREST)
    im.alpha_composite(s, ((lado - s.width) // 2, (lado - s.height) // 2 + lado // 40))
    return im


if __name__ == "__main__":
    destino = os.path.join(RAIZ, "recursos")
    os.makedirs(destino, exist_ok=True)
    tamanos = [16, 24, 32, 48, 64, 128, 256]
    imgs = [icono(t) for t in tamanos]
    imgs[-1].save(os.path.join(destino, "miausic.ico"), sizes=[(t, t) for t in tamanos], append_images=imgs[:-1])
    imgs[-1].save(os.path.join(destino, "miausic.png"))
    imgs[-1].save(os.path.join(RAIZ, "app", "michi.ico"), sizes=[(t, t) for t in tamanos], append_images=imgs[:-1])
    # imagen lateral del instalador (164x314) y cabecera (150x57), formato BMP
    lateral = Image.new("RGBA", (164, 314), FONDO)
    ImageDraw.Draw(lateral).rectangle([0, 230, 164, 314], fill=NARANJA)
    gato = michi().resize((michi().width * 6, michi().height * 6), Image.NEAREST)
    lateral.alpha_composite(gato, ((164 - gato.width) // 2, 230 - gato.height + 6))
    lateral.convert("RGB").save(os.path.join(destino, "instalador_lateral.bmp"))
    cabecera = Image.new("RGBA", (150, 57), (255, 255, 255, 255))
    cabecera.alpha_composite(icono(48), (96, 4))
    cabecera.convert("RGB").save(os.path.join(destino, "instalador_cabecera.bmp"))
    print("Íconos listos en", destino)
