"""Carrossel de feed do Dermo-day (4:5, 1080x1350) no padrão do doc 09.
6 lâminas: capa (produto de referência ofuscado), o ativo (escada da vitamina A), por que virou febre,
cuidados, no seu manipulado (foto da bancada), chamada (comente DERMO). Logo oficial em todas (feed).
Uso: python3 -I carrossel.py <conteudo.json> <pasta_saida>
"""
import json, sys
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "campanha-nov"))
from modelos import frase_linhas, desenha_frase, espacado, COR, A
W, H = 1080, 1350
POP = lambda t: ImageFont.truetype(str(A/"fonts"/"Poppins-Bold.ttf"), t)
MONO = lambda t: ImageFont.truetype(str(A/"fonts"/"IBMPlexMono-Regular.ttf"), t)
def pf(t, it=False, peso=400):
    f = ImageFont.truetype(str(A/"fonts"/("PlayfairDisplay-Italic.ttf" if it else "PlayfairDisplay.ttf")), t); f.set_variation_by_axes([peso]); return f
def logo(img, cor):
    lg = Image.open(A/"logo"/f"medicinal-palavra-{cor}.png").convert("RGBA"); lg = lg.resize((150, round(lg.height*150/lg.width)), Image.LANCZOS)
    img.alpha_composite(lg, (64, 62))
def pagina(d, i, n, cor):
    t = f"{i}/{n}"; f = MONO(26); d.text((W - 64 - f.getlength(t), 92), t, font=f, fill=cor)
def tela(fundo):
    return Image.new("RGBA", (W, H), COR[fundo] + (255,))
def texto(d, y, frase, tam, cor, cor_k, maxw=W-200):
    return desenha_frase(d, W, y, frase_linhas(frase, tam, maxw), tam, cor, cor_k)
def corpo(d, y, txt, cor, tam=34, maxw=W-220, alt=1.45):
    f = pf(tam); palavras = txt.split(); linha = ""; 
    for p in palavras + [None]:
        t = (linha + " " + p).strip() if p else linha
        if p is None or f.getlength(t) > maxw:
            d.text((W/2, y), linha, font=f, fill=cor, anchor="ms"); y += tam * alt; linha = p or ""
        else: linha = t
    return y
def multiplica(img, foto, caixa, alt, y, marca=None, desfoque=1.6):
    src = Image.open(foto).convert("RGB"); bg = src.getpixel((5, 5))
    src = Image.merge("RGB", [c.point(lambda v, b=b: min(255, round(v * 255 / max(b, 1) * 1.05))) for c, b in zip(src.split(), bg)])
    if marca: src.paste(src.crop(marca).filter(ImageFilter.GaussianBlur(10)), marca[:2])
    p = src.crop(caixa).filter(ImageFilter.GaussianBlur(desfoque)); p = p.resize((round(p.width*alt/p.height), alt), Image.LANCZOS)
    x = (W - p.width)//2; base = img.convert("RGB"); reg = base.crop((x, y, x+p.width, y+p.height))
    base.paste(ImageChops.multiply(reg, p), (x, y)); return base.convert("RGBA")
def capa(c, n):
    img = tela("areia"); img = multiplica(img, c["foto_referencia"], tuple(c["recorte"]), 720, 150, tuple(c["marca"]))
    d = ImageDraw.Draw(img); logo(img, "marinho"); pagina(d, 1, n, COR["marinho"])
    espacado(d, W/2, 930, "DERMO-DAY · " + c["origem"].upper(), POP(26), COR["marinho"], 8)
    texto(d, 960, c["capa"], 68, COR["marinho"], COR["cafe"])
    return img
def ativo(c, n):
    img = tela("marinho"); d = ImageDraw.Draw(img); logo(img, "off-white"); pagina(d, 2, n, COR["offwhite"])
    espacado(d, W/2, 320, "O ATIVO DESTAQUE", POP(28), COR["caramelo"], 9)
    y = texto(d, 350, c["ativo_frase"], 68, COR["offwhite"], COR["caramelo"])
    # escada: degraus da família, destaque no ativo
    degraus = c["escada"]; n_d = len(degraus); x0, x1 = 150, W - 150; topo = y + 110; alt = 112
    for i, (nome, nota) in enumerate(degraus):
        yy = topo + i * (alt + 22); dest = nome.lower() == c["ativo"].lower()
        cor_box = COR["caramelo"] if dest else (28, 52, 94)
        d.rounded_rectangle([x0 + i*28, yy, x1 - (n_d-1-i)*28, yy + alt], radius=14, fill=cor_box)
        d.text((x0 + i*28 + 36, yy + alt/2 + 12), nome, font=pf(50, it=dest, peso=700 if dest else 400), fill=COR["marinho"] if dest else COR["offwhite"], anchor="ls")
        f = MONO(26); d.text((x1 - (n_d-1-i)*28 - 30 - f.getlength(nota), yy + alt/2 + 9), nota, font=f, fill=COR["marinho"] if dest else COR["areia"], anchor="ls")
    yb = topo + n_d * (alt + 22) + 50
    d.text((W/2, yb), c["escada_legenda"], font=MONO(24), fill=COR["areia"], anchor="ms")
    return img
def febre(c, n):
    img = tela("offwhite"); d = ImageDraw.Draw(img); logo(img, "marinho"); pagina(d, 3, n, COR["marinho"])
    espacado(d, W/2, 360, "POR QUE VIROU FEBRE", POP(28), COR["marinho"], 9)
    y = texto(d, 400, c["febre_frase"], 70, COR["marinho"], COR["caramelo"]); y += 70
    d.line([(W/2 - 40, y), (W/2 + 40, y)], fill=COR["caramelo"], width=2); y += 90
    for item in c["febre_itens"]:
        y = corpo(d, y, item, COR["marinho"], 40) + 40
    return img
def cuidados(c, n):
    img = tela("areia"); d = ImageDraw.Draw(img); logo(img, "marinho"); pagina(d, 4, n, COR["marinho"])
    espacado(d, W/2, 330, "ANTES DE USAR", POP(28), COR["marinho"], 9)
    y = texto(d, 370, c["cuidados_frase"], 70, COR["marinho"], COR["cafe"]) + 80
    for k, (titulo, txt) in enumerate(c["cuidados"]):
        d.text((150, y), f"0{k+1}", font=MONO(30), fill=COR["cafe"], anchor="ls")
        d.text((230, y), titulo, font=pf(46, it=True, peso=700), fill=COR["marinho"], anchor="ls")
        f = pf(34); d.text((230, y + 54), txt, font=f, fill=COR["marinho"], anchor="ls"); y += 150
    return img
def manipulado(c, n):
    foto = Image.open(c["foto_bancada"]).convert("RGB"); r = max(W/foto.width, H/foto.height)
    foto = foto.resize((round(foto.width*r), round(foto.height*r)), Image.LANCZOS); x = (foto.width-W)//2; foto = foto.crop((x, foto.height-H, x+W, foto.height))  # ancora embaixo: bancada no meio, mármore livre para o texto
    img = foto.convert("RGBA"); ov = Image.new("L", (W, H), 0); dv = ImageDraw.Draw(ov)
    for y in range(H): dv.line([(0, y), (W, y)], fill=round(255 * (0.08 + 0.42 * max(0, (y - 0.62*H)/(0.38*H)) ** 1.2)))
    img = Image.composite(Image.new("RGBA", (W, H), (0, 0, 0, 255)), img, ov)
    d = ImageDraw.Draw(img); logo(img, "branco"); pagina(d, 5, n, (255, 255, 255))
    espacado(d, W/2, 1100, "SOB MEDIDA NA MEDICINAL", POP(28), (255, 255, 255), 9)
    texto(d, 1125, c["manip_frase"], 58, (255, 255, 255), COR["areia"])
    return img
def chamada(c, n):
    img = tela("marinho"); d = ImageDraw.Draw(img); logo(img, "off-white"); pagina(d, 6, n, COR["offwhite"])
    y = texto(d, 430, c["cta_frase"], 72, COR["offwhite"], COR["caramelo"]) + 80
    f = MONO(40); t = c["cta"]; w = f.getlength(t); d.text(((W-w)/2, y), t, font=f, fill=COR["offwhite"], anchor="ls")
    d.line([((W-w)/2, y + 12), ((W+w)/2, y + 12)], fill=COR["offwhite"], width=2)
    corpo(d, y + 120, c["cta_nota"], COR["areia"], 30)
    return img
if __name__ == "__main__":
    c = json.load(open(sys.argv[1])); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    fs = [capa, ativo, febre, cuidados, manipulado, chamada]
    for i, fn in enumerate(fs, 1): fn(c, len(fs)).convert("RGB").save(out/f"{c['slug']}-{i}.jpg", "JPEG", quality=92)
    print("ok")
