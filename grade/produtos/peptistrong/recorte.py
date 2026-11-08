"""Recorte da lata real do Peptistrong a partir da foto de 03/09/2025 (post @medicinalnaweb).

Fonte: g25/18051882080234910.jpg (1416x2518), baixada pelo workflow de leitura do feed.
Contornos desenhados à mão sobre a foto ampliada (coordenadas da foto original):
- tampa: retângulo de pontas arredondadas (a tampa real não tem canto vivo);
- corpo: retângulo até o CENTRO da elipse da base (sem degrau nos cantos) + elipse da base;
- alça: arame em polígono, com o VÃO interno aberto (o fundo da foto não entra).
"""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

CAIXA = (225, 1220, 980, 2215)   # recorte final (inclui alça)
CORPO_LARGURA = 662              # largura do corpo em px na foto (908-246)
BASE_ARCO = 45 / 995             # altura do arco da borda de baixo / altura do recorte

TAMPA_TOPO = (232, 1230, 940, 1262)   # elipse fina do topo (vista quase de lado)
TAMPA_SAIA = (232, 1246, 940, 1271)   # só a lateral da tampa; abaixo disso a largura é a do corpo (246-908)   # lateral da tampa, do centro da elipse para baixo
TAMPA_BRANCA = (232, 1229, 940, 1270)   # só o plástico branco (abaixo dele é o aro metálico da lata)
ALCA_EXTERNA = [(868, 1262), (942, 1258), (952, 1290), (962, 1330), (968, 1360), (950, 1370), (912, 1370), (895, 1347), (878, 1300)]
ALCA_VAO = [(886, 1279), (917, 1276), (924, 1300), (934, 1340), (929, 1356), (915, 1356), (901, 1336), (889, 1300)]


def mascara(foto):
    W, H = foto.size
    m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
    d.ellipse(TAMPA_TOPO, fill=255); d.rounded_rectangle(TAMPA_SAIA, radius=6, fill=255)
    d.rectangle((246, 1262, 908, 2165), fill=255)
    d.ellipse((244, 2120, 910, 2210), fill=255)
    al = Image.new('L', (W, H), 0); ad = ImageDraw.Draw(al)
    ad.polygon(ALCA_EXTERNA, fill=255); ad.polygon(ALCA_VAO, fill=0)
    m = ImageChopsLighter(m, al)
    return m.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.0))


def ImageChopsLighter(a, b):
    from PIL import ImageChops
    return ImageChops.lighter(a, b)


def recorta(foto_full, tampa_original=None):
    """foto_full: a foto inteira (pode estar reiluminada). tampa_original: foto sem reiluminar; o plástico
    branco da tampa volta ao tom real (o mapa de luz deixa o branco acinzentado), com transição suave."""
    m = mascara(foto_full)
    base = foto_full.convert('RGB')
    if tampa_original is not None:
        W, H = base.size
        tm = Image.new('L', (W, H), 0); td = ImageDraw.Draw(tm); td.ellipse(TAMPA_TOPO, fill=255); td.rectangle((232, 1246, 940, 1270), fill=255)
        tm = tm.filter(ImageFilter.GaussianBlur(5))
        quente = Image.fromarray(np.clip(np.asarray(tampa_original.convert('RGB')).astype(float)
                                         * np.array([1.04, 1.0, 0.93]), 0, 255).astype(np.uint8))
        base = Image.composite(quente, base, tm)
    can = base.crop(CAIXA).convert('RGBA'); can.putalpha(m.crop(CAIXA))
    return can
