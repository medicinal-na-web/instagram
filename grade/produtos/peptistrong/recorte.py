"""Recorte da lata real do Peptistrong a partir da foto de 03/09/2025 (post @medicinalnaweb).

Fonte: g25/18051882080234910.jpg (1416x2518), baixada pelo workflow de leitura do feed.
Máscara geométrica: tampa (elipse fina + saia), corpo (retângulo até o CENTRO da elipse da base,
para não criar degrau nos cantos), base (elipse), alça (pixels claros e pouco saturados na região).
"""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

CAIXA = (225, 1220, 980, 2215)   # recorte final (inclui alça)
CORPO_LARGURA = 662              # largura do corpo em px na foto (908-246)


def mascara(foto):
    W, H = foto.size
    m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
    d.ellipse((232, 1228, 922, 1268), fill=255); d.rectangle((232, 1248, 922, 1292), fill=255)   # tampa
    d.rectangle((246, 1270, 908, 2165), fill=255)                                              # corpo até o centro da base
    d.ellipse((244, 2120, 910, 2210), fill=255)                                                # base
    A = np.asarray(foto).astype(int); box = (880, 1260, 975, 1375)
    sub = A[box[1]:box[3], box[0]:box[2]]
    alca = (sub.max(2) > 205) & ((sub.max(2) - sub.min(2)) < 60)
    m.paste(255, box, Image.fromarray((alca * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)))
    return m.filter(ImageFilter.GaussianBlur(1.2))


def recorta(foto_full, tampa_original=None):
    """foto_full: a foto inteira (pode estar reiluminada). tampa_original: foto sem reiluminar, para a
    faixa da tampa branca voltar ao tom real (o mapa de luz deixa a tampa acinzentada)."""
    m = mascara(foto_full)
    can = foto_full.crop(CAIXA).convert('RGBA'); can.putalpha(m.crop(CAIXA))
    if tampa_original is not None:
        L = np.asarray(can).astype(float); O = np.asarray(tampa_original.crop(CAIXA).convert('RGB')).astype(float)
        lid = np.zeros(L.shape[:2]); lid[0:75, :] = 1
        L[..., :3] = L[..., :3] * (1 - lid[..., None]) + O * np.array([1.0, 0.96, 0.88]) * lid[..., None]
        can = Image.fromarray(L.astype(np.uint8), 'RGBA')
    return can
