"""Carrossel de feed do Dermo-day (4:5, 1080x1350) na linguagem visual do Instagram de 2025 (doc 09).
Toda lâmina é foto (sem fundo chapado), em tons neutros e frios-quentes apagados (taupe, cinza quente),
texto branco centralizado: rótulo Poppins caixa alta espaçada OU frase Playfair com palavra-chave
Bold Italic branca e maior. No máximo 2 fontes por lâmina. Logo pequeno branco no canto. Sem caixa nem faixa.
Uso: python3 -I carrossel.py <conteudo.json> <pasta_saida>
"""
import json, sys
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "campanha-nov"))
from modelos import frase_linhas, desenha_frase, espacado, A
import logo_pos
ULTIMA = {"pos": None}
W, H = 1080, 1350; BR = (255, 255, 255); TAUPE = (196, 172, 160)
POP = lambda t: ImageFont.truetype(str(A/"fonts"/"Poppins-Bold.ttf"), t)
MONO = lambda t: ImageFont.truetype(str(A/"fonts"/"IBMPlexMono-Regular.ttf"), t)
FILTRO = False  # padrão oficial de 13/11/2026: sem filtro de cor (doc 09, seção 0)
def apagado(im, sat=0.62, contraste=0.9, tom=0.10):
    if not FILTRO: return im.convert("RGB")
    im = ImageEnhance.Color(im.convert("RGB")).enhance(sat); im = ImageEnhance.Contrast(im).enhance(contraste)
    return Image.blend(im, Image.new("RGB", im.size, TAUPE), tom)
def cobre(im, ancora=0.5):
    r = max(W/im.width, H/im.height); im = im.resize((round(im.width*r), round(im.height*r)), Image.LANCZOS)
    x = (im.width - W)//2; y = round((im.height - H) * ancora); return im.crop((x, y, x+W, y+H))
def escurece(im, base=0.08, extra=0.26, de=0.35):
    ov = Image.new("L", (W, H), 0); d = ImageDraw.Draw(ov)
    for y in range(H): d.line([(0, y), (W, y)], fill=round(255 * (base + extra * max(0, (y - de*H) / ((1-de)*H)))))
    return Image.composite(Image.new("RGB", (W, H), (20, 16, 14)), im, ov)
def logo(img):  # posição variável: canto mais calmo, nunca igual à lâmina anterior
    lg = Image.open(A/"logo"/"medicinal-palavra-branco.png").convert("RGBA"); lg = lg.resize((150, round(lg.height*150/lg.width)), Image.LANCZOS)
    ULTIMA["pos"] = logo_pos.aplica(img, lg, ULTIMA["pos"])
def fim(im):  # grão leve de filme
    if not FILTRO: return im.convert("RGB")
    g = Image.effect_noise((W, H), 18).convert("L"); return Image.blend(im.convert("RGB"), Image.merge("RGB", [ImageChops.overlay(c, g) for c in im.convert("RGB").split()]), 0.18)
def pf(t, it=False, peso=400):
    f = ImageFont.truetype(str(A/"fonts"/("PlayfairDisplay-Italic.ttf" if it else "PlayfairDisplay.ttf")), t); f.set_variation_by_axes([peso]); return f
def frase(img, y, txt, tam=64, k=1.75):
    """Como em 2025: linhas separadas por |; a linha entre *asteriscos* sai em Bold Italic branca, bem maior."""
    d = ImageDraw.Draw(img)
    for linha in txt.split("|"):
        linha = linha.strip(); chave = linha.startswith("*") and linha.endswith("*")
        f = pf(round(tam * k), True, 700) if chave else pf(tam); t = linha.strip("*"); tt = f.size
        # espaçamento entre letras levemente negativo (-2,5%)
        w = sum(f.getlength(ch) for ch in t) - 0.025 * tt * max(len(t) - 1, 0); x = (W - w) / 2; y += tt
        for ch in t: d.text((x, y), ch, font=f, fill=BR, anchor="ls"); x += f.getlength(ch) - 0.025 * tt
        y += tt * 0.18
    return y
def rotulo(img, y, txt, tam=40, track=12):
    espacado(ImageDraw.Draw(img), W/2, y, txt.upper(), POP(tam), BR, track)
def mono(img, y, txt, tam=38):
    d = ImageDraw.Draw(img); f = MONO(tam); w = f.getlength(txt); d.text(((W-w)/2, y), txt, font=f, fill=BR, anchor="ls")
    d.line([((W-w)/2, y + 11), ((W+w)/2, y + 11)], fill=BR, width=2)
def foto(caminho, ancora=0.5, **k): return escurece(apagado(cobre(Image.open(caminho), ancora)), **k).convert("RGBA")
def capa(c):
    # produto de referência ofuscado sobre fundo taupe com luz suave (como os fundos de 2025)
    base = Image.new("RGB", (W, H), TAUPE); luz = Image.new("L", (W, H), 0); dl = ImageDraw.Draw(luz)
    for x in range(W): dl.line([(x, 0), (x, H)], fill=round(70 * (1 - x / W) ** 1.4))
    base = Image.composite(Image.new("RGB", (W, H), (226, 210, 200)), base, luz)
    src = Image.open(c["foto_referencia"]).convert("RGB"); bg = src.getpixel((5, 5))
    src = Image.merge("RGB", [ch.point(lambda v, b=b: min(255, round(v * 255 / max(b, 1) * 1.05))) for ch, b in zip(src.split(), bg)])
    m = tuple(c["marca"]); src.paste(src.crop(m).filter(ImageFilter.GaussianBlur(10)), m[:2])
    p = apagado(src.crop(tuple(c["recorte"])).filter(ImageFilter.GaussianBlur(1.4)), sat=0.75, tom=0.0)
    alt = 900; p = p.resize((round(p.width*alt/p.height), alt), Image.LANCZOS)
    x, y = (W - p.width)//2 + 120, 400; reg = base.crop((x, y, x + p.width, y + p.height))
    mask = Image.new("L", p.size, 0); ImageDraw.Draw(mask).rectangle([40, 40, p.width-40, p.height-40], fill=255); mask = mask.filter(ImageFilter.GaussianBlur(30))
    base.paste(Image.composite(ImageChops.multiply(reg, p), reg, mask), (x, y))
    img = escurece(base, base=0.05, extra=0.18, de=0.5).convert("RGBA")
    y = frase(img, 170, c["capa"], 70, 1.6); mono(img, y + 70, c["capa_mono"]); logo(img)
    return fim(img)
def lamina(c, chave):
    L = c[chave]; img = foto(L["foto"], L.get("ancora", 0.5))
    if L.get("rotulo"): rotulo(img, L.get("y", 760), L["rotulo"], L.get("tam_rotulo", 58), 16)
    if L.get("frase"): y = frase(img, L.get("y", 700), L["frase"], L.get("tam", 72), 1.6)
    if L.get("mono"): mono(img, L.get("y_mono", (L.get("y", 700) + 95) if L.get("rotulo") else y + 70), L["mono"])
    logo(img); return fim(img)
if __name__ == "__main__":
    c = json.load(open(sys.argv[1])); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    laminas = [capa(c)] + [lamina(c, k) for k in ("l2", "l3", "l4", "l5", "l6")]
    for i, im in enumerate(laminas, 1): im.convert("RGB").save(out/f"{c['slug']}-{i}.jpg", "JPEG", quality=92)
    print("ok")
