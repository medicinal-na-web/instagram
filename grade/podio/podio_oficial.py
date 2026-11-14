"""Pódio animado (9:16, 8 s, 30 fps) no PADRÃO OFICIAL (doc 09, seção 0, 13/11/2026).
- Fundo: foto real, sem filtro de cor; escurecimento suave só nas faixas de texto e do pódio.
- Texto branco. Fontes: Playfair (título, palavra-chave Bold Italic 1,6x, nomes) + Poppins (rótulo e números). Sem mono.
- Degraus em vidro fosco branco, números escuros. Story sem logo; tudo entre 14% e 80% da altura.
Uso: python3 -I podio_oficial.py <foto> <saida.mp4> "<CATEGORIA>" "<1º>" "<2º>" "<3º>" "<n1>" "<n2>" "<n3>" """
import subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageStat
A = Path(__file__).resolve().parent.parent / "assets"
W, H, FPS, DUR = 1080, 1920, 30, 8.0
BR, ESC = (255, 255, 255), (38, 32, 28)
def pf(peso=400, it=False, tam=60):
    f = ImageFont.truetype(str(A/"fonts"/("PlayfairDisplay-Italic.ttf" if it else "PlayfairDisplay.ttf")), tam); f.set_variation_by_axes([peso]); return f
POP = lambda t: ImageFont.truetype(str(A/"fonts"/"Poppins-Bold.ttf"), t)
def ease(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3
def esp(d, cx, y, txt, f, cor, tr, a=255):
    w = sum(f.getlength(c) for c in txt) + tr*(len(txt)-1); x = cx - w/2
    for c in txt: d.text((x, y), c, font=f, fill=cor+(a,), anchor="ls"); x += f.getlength(c) + tr
def quebra(txt, f, maxw):
    ps, ls, at = txt.split(), [], ""
    for p in ps:
        t = (at + " " + p).strip()
        if f.getlength(t) > maxw and at: ls.append(at); at = p
        else: at = t
    return ls + [at]
def fundo(foto):
    im = Image.open(foto).convert("RGB"); r = max(W/im.width, H/im.height)
    im = im.resize((round(im.width*r), round(im.height*r)), Image.LANCZOS); x = (im.width-W)//2; y = (im.height-H)//2; im = im.crop((x, y, x+W, y+H))
    media = ImageStat.Stat(im.convert("L").crop((140, 380, W-140, 1560))).mean[0]
    forca = 0.30 + 0.28 * max(0, (media - 150) / 105)  # mesma regra do padrao.py
    ov = Image.new("L", (W, H), 0); d = ImageDraw.Draw(ov); c0, c1 = 220, 1700
    for y in range(H):
        t = 0 if y < c0 or y > c1 else min(1, (y - c0) / 260, (c1 - y) / 260)
        d.line([(0, y), (W, y)], fill=round(255 * forca * t))
    return Image.composite(Image.new("RGB", (W, H), (18, 14, 12)), im, ov).convert("RGBA")
def quadro(bg, t, cat, nomes, nums):
    im = bg.copy(); camada = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(camada)
    a0 = round(255 * ease(t / 0.6))
    esp(d, W/2, 470, f"PÓDIO DA MANIPULAÇÃO · {cat.upper()}", POP(30), BR, 8, a0)
    d.text((W/2, 590), "o que mais entrou", font=pf(400, False, 76), fill=BR+(a0,), anchor="ms")
    d.text((W/2, 715), "nas fórmulas", font=pf(700, True, 122), fill=BR+(a0,), anchor="ms")
    d.text((W/2, 790), "últimos 90 dias", font=pf(400, True, 44), fill=BR+(a0,), anchor="ms")
    base = 1420; larg = 290; xs = {2: 95, 1: 395, 3: 695}; alt = {1: 430, 2: 330, 3: 250}
    vidro = {1: 235, 2: 200, 3: 170}; ini = {3: 1.0, 2: 2.2, 1: 3.4}
    for pos in (3, 2, 1):
        p = ease((t - ini[pos]) / 0.9)
        if p <= 0: continue
        h = alt[pos] * p; x = xs[pos]
        d.rounded_rectangle([x, base - h, x + larg, base], 14, fill=BR + (round(vidro[pos] * p),))
        d.text((x + larg/2, base - h + 90), f"{pos}º", font=POP(64 if pos == 1 else 54), fill=ESC + (round(255*p),), anchor="ms")
        an = ease((t - ini[pos] - 0.6) / 0.6)
        if an > 0:
            fn = pf(700, True, 48 if pos == 1 else 42); linhas = quebra(nomes[pos-1], fn, larg - 10)
            y = base - h - 40 - 54 * (len(linhas) - 1)
            for l in linhas: d.text((x + larg/2, y), l, font=fn, fill=BR + (round(255*an),), anchor="ms"); y += 54
            d.text((x + larg/2, base - h + 152), nums[pos-1], font=POP(38), fill=ESC + (round(255*an),), anchor="ms")
            d.text((x + larg/2, base - h + 192), "NOTA", font=POP(22), fill=ESC + (round(255*an),), anchor="ms")
    af = round(255 * ease((t - 5.6) / 0.7))
    if af: d.text((W/2, 1520), "qual deles está na sua rotina?", font=pf(400, False, 56), fill=BR + (af,), anchor="ms")
    return Image.alpha_composite(im, camada).convert("RGB")
if __name__ == "__main__":
    foto, saida, cat, n1, n2, n3, c1, c2, c3 = sys.argv[1:10]; bg = fundo(foto)
    with tempfile.TemporaryDirectory() as td:
        for i in range(int(FPS * DUR)):
            quadro(bg, i / FPS, cat, [n1, n2, n3], [c1, c2, c3]).save(f"{td}/f{i:04d}.png")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{td}/f%04d.png", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-movflags", "+faststart", saida], check=True)
        quadro(bg, DUR - 0.01, cat, [n1, n2, n3], [c1, c2, c3]).save(saida.replace(".mp4", "-capa.jpg"), quality=90)
