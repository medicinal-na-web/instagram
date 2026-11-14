"""Story automático "POST NOVO NO FEED" (sem logo, padrão oficial): post em destaque sobre a própria foto desfocada.
Uso: python3 -I story_post_novo.py <arte_feed.jpg> <saida.jpg>"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
A = Path(__file__).resolve().parent.parent / "assets" / "fonts"; W, H = 1080, 1920
def cobre(im, w, h):
    r = max(w/im.width, h/im.height); im = im.resize((round(im.width*r), round(im.height*r)), Image.LANCZOS); x = (im.width-w)//2; y = (im.height-h)//2; return im.crop((x, y, x+w, y+h))
src = Image.open(sys.argv[1]).convert("RGB")
bg = ImageEnhance.Brightness(cobre(src, W+160, H+160).filter(ImageFilter.GaussianBlur(38))).enhance(0.55).crop((80, 80, 80+W, 80+H)).convert("RGBA")
cw, ch = 840, 1050; cx, cy = (W-cw)//2, 470
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([cx, cy+24, cx+cw, cy+ch+24], 28, fill=(0, 0, 0, 115)); bg.alpha_composite(sh.filter(ImageFilter.GaussianBlur(30)))
card = src.resize((cw, ch), Image.LANCZOS).convert("RGBA"); m = Image.new("L", (cw, ch), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, cw, ch], 28, fill=255); bg.paste(card, (cx, cy), m)
d = ImageDraw.Draw(bg); f = ImageFont.truetype(str(A/"Poppins-Bold.ttf"), 44); t = "POST NOVO NO FEED"; tr = 10
w = sum(f.getlength(c) for c in t) + tr*(len(t)-1); x = (W-w)/2
for c in t: d.text((x, 400), c, font=f, fill="white", anchor="ls"); x += f.getlength(c) + tr
fm = ImageFont.truetype(str(A/"IBMPlexMono-Regular.ttf"), 36); t2 = "toque no perfil @medicinalnaweb"; w2 = fm.getlength(t2)
d.text(((W-w2)/2, cy+ch+110), t2, font=fm, fill="white", anchor="ls"); d.line([((W-w2)/2, cy+ch+122), ((W+w2)/2, cy+ch+122)], fill="white", width=2)
bg.convert("RGB").save(sys.argv[2], "JPEG", quality=92)
