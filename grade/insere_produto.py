"""Insere a foto real de um produto (fundo branco) numa cena, com cuidado de naturalidade.

Regra do padrão (docs/09-padrao-visual.md, seção 12): escala coerente com objetos vizinhos,
perspectiva da câmera da cena (tampa e base em elipse), luz da cena sobre o produto
(direção, cor e manchas de luz), sombra de contato e sombra projetada, mesma nitidez e grão.
"""
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageChops
import math

def recorta(path, escuro=110):
    """Recorta só o corpo do produto (tira fundo, sombra de chão e aros do mockup)."""
    p = Image.open(path).convert('RGB'); g = p.convert('L'); W, H = g.size
    px = g.load()
    cols = [x for x in range(W) if sum(1 for y in range(0, H, 4) if px[x, y] < escuro) > (H / 4) * 0.35]
    x0, x1 = min(cols), max(cols)
    rows = [y for y in range(H) if sum(1 for x in range(x0, x1, 3) if px[x, y] < escuro) > ((x1 - x0) / 3) * 0.55]
    y0, y1 = min(rows), max(rows)
    # inclui a faixa colorida do topo (não é escura): sobe até encontrar o aro claro
    while y0 > 0 and sum(1 for x in range(x0, x1, 3) if px[x, y0 - 1] < 235) > ((x1 - x0) / 3) * 0.9: y0 -= 1
    m = 3; corpo = p.crop((x0 + m, y0 + m, x1 - m, y1 - m))
    out = corpo.convert('RGBA'); return out

def insere(cena, produto_png, base_centro, altura, largura=None, elipse=0.15, luz_x=0.25, cor_luz=(255, 222, 186),
           sombra_dir=(0.55, -0.30), cor_tampa=(232, 226, 214)):
    """cena: Image RGB. base_centro: (x, y) do centro da base na cena. altura: px do corpo.
    elipse: razão altura/largura da boca do cilindro vista pela câmera (medir no copo/tigela da cena).
    luz_x: posição (0-1) do brilho no cilindro (luz vindo da esquerda = valor baixo).
    sombra_dir: deslocamento do topo da sombra projetada, em fração da altura (x, y)."""
    can = recorta(produto_png) if isinstance(produto_png, str) else produto_png
    # largura: use a proporção da embalagem REAL (medida em foto), não a do mockup
    w = largura or int(can.width * altura / can.height); can = can.resize((w, altura), Image.LANCZOS)
    e = max(2, int(w * elipse / 2))  # semi-eixo menor da elipse
    rgb = can.convert('RGB'); a = can.split()[3]
    # 1) sombreamento cilíndrico com a luz da cena
    prof = Image.new('L', (w, 1))
    for x in range(w):
        u = x / (w - 1)
        v = 0.50 + 0.62 * math.exp(-((u - luz_x) / 0.24) ** 2) - 0.18 * u
        prof.putpixel((x, 0), max(0, min(255, int(v * 200))))
    prof = prof.resize((w, altura))
    rgb = ImageChops.multiply(rgb, Image.merge('RGB', [prof] * 3)); rgb = ImageEnhance.Brightness(rgb).enhance(1.25)
    rgb = ImageChops.multiply(rgb, Image.new('RGB', rgb.size, cor_luz))
    # brilho especular fino (embalagem plástica/metal)
    esp = Image.new('L', (w, 1))
    for x in range(w):
        u = x / (w - 1); esp.putpixel((x, 0), int(95 * math.exp(-((u - luz_x + 0.05) / 0.025) ** 2)))
    esp = esp.resize((w, altura)).filter(ImageFilter.GaussianBlur(2))
    rgb = ImageChops.add(rgb, Image.merge('RGB', [esp] * 3))
    # 2) curva do cilindro: topo e base viram arcos de elipse
    saia = max(3, int(altura * 0.035))
    H2 = altura + 2 * e + saia
    body = Image.new('RGBA', (w, H2), (0, 0, 0, 0)); src = rgb.convert('RGBA'); src.putalpha(a)
    for x in range(w):
        u = 2 * x / (w - 1) - 1; dy = int(round(e * math.sqrt(max(0, 1 - u * u))))
        body.paste(src.crop((x, 0, x + 1, altura)), (x, e + saia + dy))
    # 3) tampa em elipse (vista de cima)
    tampa = Image.new('RGBA', (w, H2), (0, 0, 0, 0)); td = ImageDraw.Draw(tampa)
    escura = tuple(int(c * 0.80) for c in cor_tampa) + (255,)
    td.rectangle((0, e, w - 1, e + saia), fill=escura); td.ellipse((0, saia, w - 1, 2 * e + saia), fill=escura)
    td.ellipse((0, 0, w - 1, 2 * e), fill=cor_tampa + (255,))
    td.ellipse((int(w * 0.06), int(e * 0.18), int(w * 0.94), int(2 * e - e * 0.18)), outline=tuple(int(c * 0.86) for c in cor_tampa) + (255,), width=max(1, w // 120))
    gt = Image.linear_gradient('L').rotate(90).resize((w, H2))  # tampa mais clara do lado da luz
    tampa_rgb = ImageChops.multiply(tampa.convert('RGB'), Image.merge('RGB', [gt.point(lambda v: 255 - v // 3)] * 3))
    tampa_rgb = ImageChops.multiply(tampa_rgb, Image.new('RGB', tampa_rgb.size, cor_luz)); tampa_rgb = ImageEnhance.Brightness(tampa_rgb).enhance(1.12)
    tt = tampa_rgb.convert('RGBA'); tt.putalpha(tampa.split()[3])
    obj = Image.alpha_composite(body, tt)
    ox = int(base_centro[0] - w / 2); oy = int(base_centro[1] - (altura + e + saia))  # base: ponto mais baixo do arco
    cena = cena.convert('RGB').copy()
    # 4) manchas de luz da cena (sombra de folhas etc.) sobre o produto
    reg = cena.crop((ox, oy, ox + w, oy + H2)).convert('L').filter(ImageFilter.GaussianBlur(6))
    st = reg.resize((1, 1), Image.BOX).getpixel((0, 0)) or 1
    mod = reg.point(lambda v: max(0, min(255, int(255 * min(1.35, (v / st) ** 0.7) / 1.35))))
    orgb = ImageChops.multiply(obj.convert('RGB'), Image.merge('RGB', [mod] * 3)); orgb = ImageEnhance.Brightness(orgb).enhance(1.3)
    obj2 = orgb.convert('RGBA'); obj2.putalpha(obj.split()[3])
    # 5) sombras: contato (oclusão) + projetada, deslocada para o lado oposto à luz
    camada = Image.new('L', cena.size, 0); cdw = ImageDraw.Draw(camada)
    bx0, bx1, by = ox, ox + w, oy + H2 - e
    dx, dy = sombra_dir[0] * altura, sombra_dir[1] * altura
    cdw.polygon([(bx0, by), (bx1, by), (bx1 + dx, by + dy), (bx0 + dx + w * 0.15, by + dy)], fill=150)
    camada = camada.filter(ImageFilter.GaussianBlur(max(8, w // 10)))
    contato = Image.new('L', cena.size, 0); cd = ImageDraw.Draw(contato)
    cd.ellipse((ox - w * 0.02, oy + H2 - 2 * e - 2, ox + w * 1.02, oy + H2 + 4), fill=210)
    contato = contato.filter(ImageFilter.GaussianBlur(max(3, w // 45)))
    somb = ImageChops.lighter(camada, contato)
    escuro = ImageEnhance.Brightness(cena).enhance(0.38)
    escuro = ImageChops.multiply(escuro, Image.new('RGB', cena.size, (255, 235, 220)))
    cena = Image.composite(escuro, cena, somb)
    # 6) light wrap: borda do produto pega um pouco da cor do fundo
    fundo = cena.crop((ox, oy, ox + w, oy + H2)).filter(ImageFilter.GaussianBlur(10))
    borda = ImageChops.subtract(obj2.split()[3], obj2.split()[3].filter(ImageFilter.MinFilter(7))).filter(ImageFilter.GaussianBlur(2))
    o_rgb = Image.composite(Image.blend(obj2.convert('RGB'), fundo, 0.45), obj2.convert('RGB'), borda)
    # 7) mesma nitidez e grão da cena
    o_rgb = o_rgb.filter(ImageFilter.GaussianBlur(0.7))
    n = Image.effect_noise(o_rgb.size, 24).convert('RGB'); o_rgb = Image.blend(o_rgb, ImageChops.add(o_rgb, n, 2, -128), 0.16)
    fin = o_rgb.convert('RGBA'); fin.putalpha(obj2.split()[3])
    out = cena.convert('RGBA'); out.alpha_composite(fin, (ox, oy)); return out.convert('RGB')


def recoloca_rotulo(cena_original, montagem, harmonizada, caixa_corpo, raio_luz=4):
    """Depois da harmonização por IA: devolve o rótulo ORIGINAL (da montagem), iluminado pela luz da IA.

    A IA acerta luz, tampa e sombras, mas costuma estragar texto de rótulo. Aqui o corpo do produto
    vem da montagem (texto fiel) multiplicado pela razão de luz IA/montagem (desfocada), e o resto
    da imagem vem da IA. caixa_corpo = (x0, y0, x1, y1) do rótulo na cena, sem a tampa.
    Conferir antes se a IA não moveu o produto (correlação de bordas)."""
    import numpy as np
    C = np.asarray(cena_original.convert('RGB')).astype(float)
    M = np.asarray(montagem.convert('RGB')).astype(float); A = np.asarray(harmonizada.convert('RGB')).astype(float)
    x0, y0, x1, y1 = caixa_corpo
    m = np.zeros(M.shape[:2], bool); m[y0:y1, x0:x1] = True; m &= (np.abs(M - C).sum(2) > 40)
    mk = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(2.5))
    k = np.asarray(mk).astype(float)[..., None] / 255
    bl = lambda im: np.asarray(im.convert('RGB').filter(ImageFilter.GaussianBlur(raio_luz))).astype(float) + 4
    R = np.clip(bl(harmonizada) / bl(montagem), 0.45, 2.2)
    rot = np.clip(M * R, 0, 255) * 0.88 + A * 0.12
    return Image.fromarray((A * (1 - k) + rot * k).astype(np.uint8))
