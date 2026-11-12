"""Story animado do pódio (9:16, 8 s, 30 fps) no padrão do doc 09: fundo marinho, degraus areia/caramelo/off-white,
rótulos Poppins caixa alta, nomes em Playfair (palavra-chave Bold Italic caramelo), logo oficial off-white.
Uso: python3 -I podio_video.py <saida.mp4> "<CATEGORIA>" "<1º>" "<2º>" "<3º>" "<n1>" "<n2>" "<n3>" """
import subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
A = Path(__file__).resolve().parent.parent / "assets"
MAR, MAR2, OFF, AREIA, CAR = (16,33,64), (28,52,94), (238,231,218), (224,190,151), (191,145,98)
W, H, FPS, DUR = 1080, 1920, 30, 8.0
def pf(peso=400, it=False, tam=60):
    f = ImageFont.truetype(str(A/"fonts"/("PlayfairDisplay-Italic.ttf" if it else "PlayfairDisplay.ttf")), tam); f.set_variation_by_axes([peso]); return f
POP = lambda t: ImageFont.truetype(str(A/"fonts"/"Poppins-Bold.ttf"), t)
MONO = ImageFont.truetype(str(A/"fonts"/"IBMPlexMono-Regular.ttf"), 34)
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
def quadro(t, cat, nomes, nums, logo):
    im = Image.new("RGBA", (W, H), MAR + (255,)); d = ImageDraw.Draw(im)
    im.alpha_composite(logo, (60, 290))
    a0 = round(255 * ease(t / 0.6))
    esp(d, W/2, 440, "PÓDIO DA MANIPULAÇÃO", POP(30), OFF, 9, a0)
    esp(d, W/2, 505, cat.upper(), POP(30), CAR, 9, a0)
    f = pf(400, False, 74); fi = pf(700, True, 86)
    d.text((W/2, 620), "o que mais entrou", font=f, fill=OFF+(a0,), anchor="ms")
    d.text((W/2, 715), "nas fórmulas", font=fi, fill=CAR+(a0,), anchor="ms")
    d.text((W/2, 780), "últimos 90 dias", font=MONO, fill=AREIA+(a0,), anchor="ms")
    base = 1440; larg = 290; xs = {2: 95, 1: 395, 3: 695}; alt = {1: 440, 2: 340, 3: 260}
    cor = {1: OFF, 2: AREIA, 3: CAR}; ini = {3: 1.0, 2: 2.2, 1: 3.4}
    for pos in (3, 2, 1):
        p = ease((t - ini[pos]) / 0.9)
        if p <= 0: continue
        h = alt[pos] * p; x = xs[pos]
        d.rectangle([x, base - h, x + larg, base], fill=cor[pos] + (255,))
        num = POP(64) if pos == 1 else POP(54)
        d.text((x + larg/2, base - h + 90), f"{pos}º", font=num, fill=MAR + (round(255*p),), anchor="ms")
        an = ease((t - ini[pos] - 0.6) / 0.6)
        if an > 0:
            fn = pf(700, True, 46 if pos == 1 else 40); linhas = quebra(nomes[pos-1], fn, larg - 10)
            y = base - h - 40 - 52 * (len(linhas) - 1)
            for l in linhas: d.text((x + larg/2, y), l, font=fn, fill=OFF + (round(255*an),), anchor="ms"); y += 52
            d.text((x + larg/2, base - h + 150), nums[pos-1], font=POP(36), fill=MAR + (round(255*an),), anchor="ms")
            d.text((x + larg/2, base - h + 190), "nota", font=ImageFont.truetype(str(A/"fonts"/"IBMPlexMono-Regular.ttf"), 26), fill=MAR + (round(255*an),), anchor="ms")
    af = round(255 * ease((t - 5.6) / 0.7))
    if af: d.text((W/2, 1495), "qual deles está na sua rotina?", font=pf(400, False, 50), fill=OFF + (af,), anchor="ms")
    return im.convert("RGB")
if __name__ == "__main__":
    saida, cat, n1, n2, n3, c1, c2, c3 = sys.argv[1:9]
    lg = Image.open(A/"logo"/"medicinal-palavra-off-white.png").convert("RGBA"); lg = lg.resize((170, round(lg.height*170/lg.width)))
    with tempfile.TemporaryDirectory() as td:
        for i in range(int(FPS * DUR)):
            quadro(i / FPS, cat, [n1, n2, n3], [c1, c2, c3], lg).save(f"{td}/f{i:04d}.png")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{td}/f%04d.png", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-movflags", "+faststart", saida], check=True)
        quadro(DUR - 0.01, cat, [n1, n2, n3], [c1, c2, c3], lg).save(saida.replace(".mp4", "-capa.jpg"), quality=90)
