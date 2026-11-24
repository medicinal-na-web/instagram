"""Slide de dados do estudo do Morosil (feed 4:5) no padrão oficial: foto real com escurecimento suave,
título Playfair com palavra-chave em linha própria, números em Poppins, fonte do estudo em mono.
Dados: Briskey et al. (folder Galena), 98 adultos com sobrepeso, 12 semanas, 400 mg/dia, com restrição calórica.
Uso aprovado pelo Ricardo (farmacêutico responsável) em 24/11/2026.
Uso: python3 -I slide_dados.py <foto> <saida.jpg>"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageStat
G = Path(__file__).resolve().parents[2]; A = G / "assets"
sys.path.insert(0, str(G / "padrao")); sys.path.insert(0, str(G / "campanha-nov"))
from padrao import blocos, larg
import logo_pos
W, H = 1080, 1350; BR = (255, 255, 255)
POP = lambda t: ImageFont.truetype(str(A / "fonts" / "Poppins-Bold.ttf"), t)
MONO = lambda t: ImageFont.truetype(str(A / "fonts" / "IBMPlexMono-Regular.ttf"), t)

def base(foto):
    im = Image.open(foto).convert("RGB"); r = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x = (im.width - W) // 2; y = (im.height - H) // 2; im = im.crop((x, y, x + W, y + H))
    media = ImageStat.Stat(im.convert("L").crop((80, 80, W - 80, 1150))).mean[0]
    forca = 0.50 + 0.25 * max(0, (media - 140) / 115)
    ov = Image.new("L", (W, H), 0); d = ImageDraw.Draw(ov)
    for yy in range(H):
        t = 0 if yy < 10 or yy > 1180 else min(1, (yy - 10) / 120, (1180 - yy) / 160)
        d.line([(0, yy), (W, yy)], fill=round(255 * forca * t))
    return Image.composite(Image.new("RGB", (W, H), (18, 14, 12)), im, ov).convert("RGBA")

if __name__ == "__main__":
    foto, saida = sys.argv[1:3]
    img = base(foto); c = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    y = 70
    for t, f in blocos("o que o estudo *mostrou*", 60, W):
        y += f.size; x = (W - larg(t, f)) / 2
        for ch in t: d.text((x, y), ch, font=f, fill=BR, anchor="ls"); x += f.getlength(ch) - 0.025 * f.size
        y += f.size * 0.18
    linhas = [("−4,2%", "peso corporal"), ("−3,9 cm", "cintura"), ("−3,4 cm", "quadril"),
              ("−14,4%", "gordura visceral"), ("mantida", "massa magra")]
    y += 70
    for num, rot in linhas:
        fn = POP(64); fr = MONO(34)
        d.text((W / 2 - 30, y), num, font=fn, fill=BR, anchor="rs")
        d.text((W / 2 + 10, y), rot, font=fr, fill=BR + (235,), anchor="ls")
        y += 118
    f = MONO(24)
    for i, t in enumerate(["Briskey et al. · 98 adultos com sobrepeso", "12 semanas · 400 mg/dia · com restrição calórica"]):
        d.text((W / 2, 1120 + i * 36), t, font=f, fill=BR + (215,), anchor="ms")
    img = Image.alpha_composite(img, c)
    lg = Image.open(A / "logo" / "medicinal-palavra-branco.png").convert("RGBA"); lg = lg.resize((150, round(lg.height * 150 / lg.width)), Image.LANCZOS)
    logo_pos.aplica(img, lg, None, ordem=("id", "ie"))
    img.convert("RGB").save(saida, quality=92)
