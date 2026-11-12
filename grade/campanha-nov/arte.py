"""Arte da campanha no padrão do doc 09 (mesma regra do botão "Gerar arte" do portal).
Foto + frase (Playfair Display Regular; palavra entre *asteriscos* em Bold Italic 18% maior; espaçamento -2,5%;
minúscula no início de frase) + logo oficial branco 170 px a 60 px da borda. Texto branco; escurecimento 10% + gradiente até 20%.
Story 1080x1920 (frase no terço inferior, y=66%); feed 1080x1350 (frase no terço superior, y=230).
Uso: python3 -I arte.py <foto> <canal story|feed> <saida.jpg> "<frase>"
"""
import re, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
A = Path(__file__).resolve().parent.parent / "assets"
def fonte(k, tam):
    f = ImageFont.truetype(str(A / "fonts" / ("PlayfairDisplay-Italic.ttf" if k else "PlayfairDisplay.ttf")), round(tam * 1.18) if k else tam)
    f.set_variation_by_axes([700 if k else 400]); return f
def minus(t):
    return re.sub(r"(^|[.!?…]\s+)(\*?)([A-ZÀ-Ý])(?=[a-zà-ÿ]|\s)", lambda m: m.group(1) + m.group(2) + m.group(3).lower(), t)
def cobre(img, W, H):
    r = max(W / img.width, H / img.height); img = img.resize((round(img.width * r), round(img.height * r)), Image.LANCZOS)
    x, y = (img.width - W) // 2, (img.height - H) // 2; return img.crop((x, y, x + W, y + H))
def larg(txt, f, tam): return sum(f.getlength(c) for c in txt) - 0.025 * tam * max(len(txt) - 1, 0)
def arte(foto, canal, saida, frase, yfrac=None):
    W, H = 1080, (1920 if canal == "story" else 1350); tam = 70 if canal == "story" else 62
    img = cobre(Image.open(foto).convert("RGB"), W, H)
    yt = float(yfrac) if yfrac else (0.66 if canal == "story" else 230 / 1350)
    y0 = int(H * (yt - 0.04)); zona = img.crop((90, y0, W - 90, y0 + 320)).convert("L")
    claro = sum(zona.get_flattened_data() if hasattr(zona, "get_flattened_data") else zona.getdata()) / (zona.width * zona.height) > 160
    cor_txt = (16, 33, 64, 255) if claro else (255, 255, 255, 255)
    ov = Image.new("L", (W, H), 0); d = ImageDraw.Draw(ov)
    for y in range(H):
        g = (0.2 * min(1, max(0, (y - 0.40 * H) / (0.22 * H)))) if canal == "story" else (0.2 * min(1, max(0, 1 - (y - 0.30 * H) / (0.3 * H))))
        d.line([(0, y), (W, y)], fill=round(255 * (0.1 + g)))
    if not claro: img = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), img, ov)
    pal = [{"t": w.replace("*", ""), "k": "*" in w} for w in minus(" ".join(frase.split())).split(" ") if w]
    linhas, atual, lw = [], [], 0; maxw = W - 180
    for p in pal:
        f = fonte(p["k"], tam); p["w"] = larg(p["t"], f, tam); esp = f.getlength(" ")
        if atual and lw + p["w"] > maxw: linhas.append((atual, lw)); atual, lw = [], 0
        atual.append(p); lw += p["w"] + (esp if atual[:-1] or True else 0)
    if atual: linhas.append((atual, lw))
    txt = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dt = ImageDraw.Draw(txt)
    y = H * yt; alt = tam * 1.32
    for ps, w in linhas:
        w -= fonte(ps[-1]["k"], tam).getlength(" ")
        x = (W - w) / 2
        for p in ps:
            f = fonte(p["k"], tam); base = y + tam
            for c in p["t"]:
                dt.text((x, base), c, font=f, fill=cor_txt, anchor="ls"); x += f.getlength(c) - 0.025 * tam
            x += f.getlength(" ")
        y += alt
    sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sombra.putalpha(txt.getchannel("A").point(lambda a: 0 if claro else a * 0.25).filter(ImageFilter.GaussianBlur(6)))
    img = img.convert("RGBA"); img.alpha_composite(sombra); img.alpha_composite(txt)
    lg = Image.open(A / "logo" / ("medicinal-palavra-marinho.png" if claro else "medicinal-palavra-branco.png")).convert("RGBA"); lg = lg.resize((170, round(lg.height * 170 / lg.width)), Image.LANCZOS)
    img.alpha_composite(lg, (60, 60))
    img.convert("RGB").save(saida, "JPEG", quality=92)
if __name__ == "__main__":
    arte(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else None)
