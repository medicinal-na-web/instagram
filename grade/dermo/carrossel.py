"""Carrossel de feed do Dermo-day (4:5, 1080x1350), modelo F do doc 09.
Regras: uma ideia por lâmina; no máximo 2 fontes (Playfair + IBM Plex Mono); sem caixa, faixa ou etiqueta;
numeração e linha fina; nota curta em mono; logo oficial (feed). Fundo off-white, com uma lâmina marinho (E)
e duas fotográficas (capa com o produto de referência ofuscado; bancada).
Uso: python3 -I carrossel.py <conteudo.json> <pasta_saida>
"""
import json, random, sys
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "campanha-nov"))
from modelos import frase_linhas, desenha_frase, COR, A
W, H, N = 1080, 1350, 6
MONO = lambda t: ImageFont.truetype(str(A/"fonts"/"IBMPlexMono-Regular.ttf"), t)
def logo(img, cor):
    lg = Image.open(A/"logo"/f"medicinal-palavra-{cor}.png").convert("RGBA"); lg = lg.resize((170, round(lg.height*170/lg.width)), Image.LANCZOS)
    img.alpha_composite(lg, (60, 60))
def num(d, i, cor):
    t = f"{i:02d} / {N:02d}"; f = MONO(24); d.text((W - 60 - f.getlength(t), 92), t, font=f, fill=cor)
def grao(img, forca=6):
    rnd = random.Random(7); g = Image.effect_noise((W, H), 40).convert("L").point(lambda v: 128 + (v - 128) * forca // 40)
    return Image.composite(img, Image.merge("RGBA", [ImageChops.overlay(c, g) for c in img.convert("RGB").split()] + [img.getchannel("A")]), Image.new("L", (W, H), 235))
def nota(d, y, txt, cor):
    d.line([(W/2 - 36, y), (W/2 + 36, y)], fill=cor, width=2)
    f = MONO(30); d.text((W/2, y + 64), txt, font=f, fill=cor, anchor="ms")
def lamina_texto(i, fundo, frase, txt_nota, cor, cor_k, logo_cor, tam=78):
    img = Image.new("RGBA", (W, H), COR[fundo] + (255,)); d = ImageDraw.Draw(img); logo(img, logo_cor); num(d, i, cor)
    linhas = frase_linhas(frase, tam, W - 200); alt = len(linhas) * tam * 1.3 + (150 if txt_nota else 0)
    y = desenha_frase(d, W, (H - alt) / 2 - 10, linhas, tam, cor, cor_k)
    if txt_nota: nota(d, y + 50, txt_nota, cor)
    return grao(img)
def capa(c):
    # produto de referência ofuscado sobre areia com luz de janela (gradiente lateral) e sombra de contato
    base = Image.new("RGB", (W, H), COR["areia"]); luz = Image.new("L", (W, H), 0); dl = ImageDraw.Draw(luz)
    for x in range(W): dl.line([(x, 0), (x, H)], fill=round(46 * (1 - x / W) ** 1.6))
    base = Image.composite(Image.new("RGB", (W, H), (255, 246, 232)), base, luz)
    src = Image.open(c["foto_referencia"]).convert("RGB"); bg = src.getpixel((5, 5))
    src = Image.merge("RGB", [ch.point(lambda v, b=b: min(255, round(v * 255 / max(b, 1) * 1.05))) for ch, b in zip(src.split(), bg)])
    m = tuple(c["marca"]); src.paste(src.crop(m).filter(ImageFilter.GaussianBlur(10)), m[:2])
    p = src.crop(tuple(c["recorte"])).filter(ImageFilter.GaussianBlur(1.4)); alt = 860; p = p.resize((round(p.width*alt/p.height), alt), Image.LANCZOS)
    x, y = (W - p.width)//2, 300; reg = base.crop((x, y, x + p.width, y + p.height))
    mask = Image.new("L", p.size, 0); ImageDraw.Draw(mask).rectangle([40, 40, p.width - 40, p.height - 40], fill=255); mask = mask.filter(ImageFilter.GaussianBlur(30))
    base.paste(Image.composite(ImageChops.multiply(reg, p), reg, mask), (x, y))  # bordas esfumadas: o recorte não aparece
    img = base.convert("RGBA"); d = ImageDraw.Draw(img); logo(img, "marinho"); num(d, 1, COR["marinho"])
    desenha_frase(d, W, 150, frase_linhas(c["capa"], 64, W - 220), 64, COR["marinho"], COR["cafe"])
    return grao(img)
def bancada(c):
    foto = Image.open(c["foto_bancada"]).convert("RGB"); r = max(W/foto.width, H/foto.height)
    foto = foto.resize((round(foto.width*r), round(foto.height*r)), Image.LANCZOS); x = (foto.width-W)//2; foto = foto.crop((x, foto.height-H, x+W, foto.height))
    img = foto.convert("RGBA"); ov = Image.new("L", (W, H), 0); dv = ImageDraw.Draw(ov)
    for y in range(H): dv.line([(0, y), (W, y)], fill=round(255 * (0.08 + 0.40 * max(0, (y - 0.62*H)/(0.38*H)) ** 1.2)))
    img = Image.composite(Image.new("RGBA", (W, H), (0, 0, 0, 255)), img, ov); d = ImageDraw.Draw(img); logo(img, "branco"); num(d, 5, (255, 255, 255))
    desenha_frase(d, W, 1090, frase_linhas(c["manip_frase"], 62, W - 200), 62, (255, 255, 255), COR["areia"])
    return grao(img)
if __name__ == "__main__":
    c = json.load(open(sys.argv[1])); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    M, O, CA = COR["marinho"], COR["offwhite"], COR["caramelo"]
    laminas = [capa(c),
               lamina_texto(2, "offwhite", c["l2"], c["l2_nota"], M, M, "marinho"),
               lamina_texto(3, "marinho", c["l3"], c["l3_nota"], O, CA, "off-white"),
               lamina_texto(4, "offwhite", c["l4"], c["l4_nota"], M, M, "marinho"),
               bancada(c),
               lamina_texto(6, "offwhite", c["l6"], c["l6_nota"], M, M, "marinho", tam=88)]
    for i, im in enumerate(laminas, 1): im.convert("RGB").save(out/f"{c['slug']}-{i}.jpg", "JPEG", quality=92)
    print("ok")
