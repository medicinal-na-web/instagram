"""Pousa o packshot do site (fundo branco) sobre uma foto real (multiplicação + sombra de contato), para o padrão oficial.
Uso: python3 -I pousa_produto.py <foto_fundo> <packshot> <saida.jpg> [--alt 0.40] [--base 0.86] [--x 0.42]"""
import argparse
from PIL import Image, ImageChops, ImageDraw, ImageFilter
a = argparse.ArgumentParser(); a.add_argument("fundo"); a.add_argument("pack"); a.add_argument("saida")
a.add_argument("--alt", type=float, default=0.40); a.add_argument("--base", type=float, default=0.86); a.add_argument("--x", type=float, default=0.42)
o = a.parse_args(); W, H = 1080, 1920
f = Image.open(o.fundo).convert("RGB"); r = max(W / f.width, H / f.height); f = f.resize((round(f.width * r), round(f.height * r)), Image.LANCZOS)
f = f.crop(((f.width - W) // 2, (f.height - H) // 2, (f.width - W) // 2 + W, (f.height - H) // 2 + H))
p = Image.open(o.pack).convert("RGB"); bb = ImageChops.difference(p, Image.new("RGB", p.size, (255, 255, 255))).convert("L").point(lambda v: 255 if v > 12 else 0).getbbox()
p = p.crop((max(0, bb[0] - 20), max(0, bb[1] - 20), min(p.width, bb[2] + 20), min(p.height, bb[3] + 20)))
alt = round(H * o.alt); p = p.resize((round(p.width * alt / p.height), alt), Image.LANCZOS)
x = round(W * o.x - p.width / 2); y = round(H * o.base) - alt
sh = Image.new("L", (W, H), 0); ImageDraw.Draw(sh).ellipse([x + p.width * 0.12, y + alt - 34, x + p.width * 0.95, y + alt + 22], fill=130)
f = Image.composite(Image.new("RGB", (W, H), (50, 42, 38)), f, sh.filter(ImageFilter.GaussianBlur(22)))
reg = f.crop((x, y, x + p.width, y + alt)); f.paste(ImageChops.multiply(reg, p), (x, y)); f.save(o.saida, quality=95); print("ok")
