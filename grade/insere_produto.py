"""Inserção de produto em cena gerada por IA. Procedimento obrigatório: docs/10-insercao-de-produto.md.

Funções em uso no procedimento:
  px_por_cm(...)            escala da cena a partir de um objeto de referência de tamanho conhecido
  razao_elipse(...)         ângulo da câmera (elipse da boca de copo/tigela/tampa)
  insere_foto(...)          insere a FOTO REAL recortada do produto (sem deformar: curvatura_extra=0)
  verifica_fidelidade(...)  compara o produto na arte final com a foto original (aprovação automática)

Funções antigas (insere, recoloca_rotulo) ficaram para registro do teste de 08/11/2026; não usar em produção:
partem do mockup 3D, que tem proporção errada e não é foto.
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


def insere_foto(cena, recorte_png, base_centro, largura_corpo, frac_corpo=662/755, curvatura_extra=0.0,
                cor_tampa=(240, 236, 228), luz_esq=1.12, luz_dir=0.72, cor_luz=(255, 240, 224), sombra_dir=(0.9, -0.12),
                sombra_forca=140, sombra_blur=None, sombra_escuro=0.4,
                contato_elipse=0.12, contato_escuro=0.18, afunda=3, base_escurece=0.5, base_faixa=0.10):
    """Insere uma FOTO REAL recortada do produto (PNG com transparência, tampa e alça reais).
    largura_corpo: largura do corpo na cena, em px (medir contra o copo/tigela).
    frac_corpo: largura do corpo / largura do recorte (o recorte inclui a alça).
    curvatura_extra: quanto a câmera da cena olha mais de cima que a da foto (razão da elipse extra / 2).
    luz_esq/luz_dir: ganho de luz nas laterais, para seguir a direção da luz da cena."""
    import numpy as np
    rc = Image.open(recorte_png).convert('RGBA') if isinstance(recorte_png, str) else recorte_png
    w = int(largura_corpo / frac_corpo); h = int(rc.height * w / rc.width)
    rc = rc.resize((w, h), Image.LANCZOS)
    e = max(1, int(largura_corpo * curvatura_extra))
    # 1) curvatura extra (câmera mais alta): colunas do corpo descem em arco; tampa ganha topo em elipse
    out = Image.new('RGBA', (w, h + 2 * e), (0, 0, 0, 0))
    cx0 = 0; cw = int(largura_corpo)
    for x in range(w):
        u = (x - cx0) / max(1, cw - 1) * 2 - 1
        dy = int(round(e * math.sqrt(max(0, 1 - u * u)))) if -1 <= u <= 1 else 0
        out.paste(rc.crop((x, 0, x + 1, h)), (x, e + dy))
    topo = Image.new('RGBA', out.size, (0, 0, 0, 0)); td = ImageDraw.Draw(topo)
    td.ellipse((1, 0, cw - 2, 2 * e + 3), fill=cor_tampa + (255,))
    out = Image.alpha_composite(topo, out) if False else Image.alpha_composite(out, Image.new('RGBA', out.size, (0,0,0,0)))
    base_alpha = out.split()[3]
    topo_alpha = topo.split()[3]
    merged = Image.alpha_composite(topo, out)  # corpo por cima; o topo só aparece onde abriu espaço
    # 2) luz da cena: gradiente lateral + cor
    rgb = merged.convert('RGB'); a = merged.split()[3]
    g = Image.new('L', (rgb.width, 1))
    for x in range(rgb.width):
        t = x / (rgb.width - 1); g.putpixel((x, 0), int(255 * (luz_esq + (luz_dir - luz_esq) * t) / 1.3))
    g = g.resize(rgb.size)
    arr = np.asarray(rgb).astype(float) / 255
    gl = np.asarray(g).astype(float)[..., None] / 255 * 1.3
    arr = np.clip(arr * gl, 0, 1) * (np.array(cor_luz) / 255)
    rgb = Image.fromarray((arr * 255).astype(np.uint8))
    ox = int(base_centro[0] - cw / 2); oy = int(base_centro[1] - (h + 2 * e)) + afunda
    cena = cena.convert('RGB').copy()
    # 3) manchas de luz da cena
    reg = cena.crop((ox, oy, ox + rgb.width, oy + rgb.height)).convert('L').filter(ImageFilter.GaussianBlur(5))
    st = reg.resize((1, 1), Image.BOX).getpixel((0, 0)) or 1
    mod = reg.point(lambda v: max(0, min(255, int(255 * min(1.3, (v / st) ** 0.5) / 1.3))))
    arr = np.asarray(rgb).astype(float) * (np.asarray(mod).astype(float)[..., None] / 255 * 1.3)
    rgb = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    # 4) sombras de contato e projetada
    camada = Image.new('L', cena.size, 0); cd = ImageDraw.Draw(camada)
    bx0, bx1, by = ox, ox + cw, oy + rgb.height - e
    dx, dy = sombra_dir[0] * h, sombra_dir[1] * h
    # sombra projetada: parte da base e vai para o lado oposto à luz (dx<0 = luz da direita)
    cd.polygon([(bx0, by), (bx1, by), (bx1 + dx, by + dy), (bx0 + dx, by + dy)], fill=sombra_forca)
    camada = camada.filter(ImageFilter.GaussianBlur(sombra_blur or max(8, cw // 9)))
    # contato: oclusão sob toda a base (elipse do apoio no ângulo da cena) + linha escura no ponto de apoio
    contato = Image.new('L', cena.size, 0); ct = ImageDraw.Draw(contato)
    eh = contato_elipse * cw
    ct.ellipse((ox - cw * 0.03, by - eh * 0.9, ox + cw * 1.03, by + eh * 0.35), fill=200)
    contato = contato.filter(ImageFilter.GaussianBlur(max(3, cw // 30)))
    nucleo = Image.new('L', cena.size, 0); nd = ImageDraw.Draw(nucleo)
    nd.ellipse((ox + cw * 0.01, by - eh * 0.25, ox + cw * 0.99, by + eh * 0.12), fill=255)
    nucleo = nucleo.filter(ImageFilter.GaussianBlur(2))
    escuro_ct = ImageChops.multiply(ImageEnhance.Brightness(cena).enhance(contato_escuro), Image.new('RGB', cena.size, (255, 232, 215)))
    cena = Image.composite(escuro_ct, cena, ImageChops.lighter(contato.point(lambda v: int(v * 0.75)), nucleo))
    somb = camada
    escuro = ImageChops.multiply(ImageEnhance.Brightness(cena).enhance(sombra_escuro), Image.new('RGB', cena.size, (255, 236, 222)))
    cena = Image.composite(escuro, cena, somb)
    # 4b) oclusão no próprio produto: a parte de baixo escurece perto da superfície
    gb = Image.new('L', (1, rgb.height), 255)
    f0 = int(rgb.height * (1 - base_faixa))
    for y in range(f0, rgb.height):
        k = (y - f0) / max(1, rgb.height - f0); gb.putpixel((0, y), int(255 * (1 - (1 - base_escurece) * k ** 1.5)))
    gb = gb.resize(rgb.size)
    rgb = ImageChops.multiply(rgb, Image.merge('RGB', [gb] * 3))
    # 5) light wrap, nitidez e grão
    fundo = cena.crop((ox, oy, ox + rgb.width, oy + rgb.height)).filter(ImageFilter.GaussianBlur(8))
    borda = ImageChops.subtract(a, a.filter(ImageFilter.MinFilter(5))).filter(ImageFilter.GaussianBlur(1.5))
    rgb = Image.composite(Image.blend(rgb, fundo, 0.4), rgb, borda).filter(ImageFilter.GaussianBlur(0.5))
    n = Image.effect_noise(rgb.size, 22).convert('RGB'); rgb = Image.blend(rgb, ImageChops.add(rgb, n, 2, -128), 0.12)
    fin = rgb.convert('RGBA'); fin.putalpha(a)
    res = cena.convert('RGBA'); res.alpha_composite(fin, (ox, oy)); return res.convert('RGB')



def px_por_cm(tamanho_px, tamanho_cm):
    """Escala da cena: tamanho medido em px de um objeto de referência / tamanho real em cm.
    O objeto de referência deve estar na MESMA profundidade em que o produto vai ficar."""
    return tamanho_px / tamanho_cm


def razao_elipse(largura_px, altura_px):
    """Razão altura/largura da elipse vista (boca do copo, borda da tigela, tampa do produto).
    Cena e foto do produto precisam ter razões parecidas (tolerância ±0,03)."""
    return altura_px / largura_px


def verifica_fidelidade(arte, recorte_png, caixa, limite=0.90):
    """Compara o produto na arte final com a foto original recortada.
    caixa = (x0, y0, x1, y1) onde o recorte foi colado (tamanho final do recorte na cena).
    Compara detalhes (passa-alta da luminância) dentro da máscara do recorte, o que ignora
    ajuste global de luz/cor e pega qualquer letra, logo ou forma alterada.
    Retorna (aprovado, correlação)."""
    import numpy as np
    rc = Image.open(recorte_png).convert('RGBA') if isinstance(recorte_png, str) else recorte_png
    x0, y0, x1, y1 = caixa
    rc = rc.resize((x1 - x0, y1 - y0), Image.LANCZOS)
    alvo = arte.convert('RGB').crop(caixa)
    hp = lambda im: (np.asarray(im.convert('L')).astype(float)
                     - np.asarray(im.convert('L').filter(ImageFilter.GaussianBlur(3))).astype(float))
    a, b = hp(rc.convert('RGB')), hp(alvo)
    m = np.asarray(rc.split()[3].filter(ImageFilter.MinFilter(5))) > 200
    c = float(np.corrcoef(a[m], b[m])[0, 1])
    return c >= limite, round(c, 3)
