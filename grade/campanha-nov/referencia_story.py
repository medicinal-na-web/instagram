"""Story 1 do Dia Dermo: foto do produto de referência em destaque e ofuscada.
Leva desfoque leve no produto inteiro e desfoque forte na marca.
O fundo cinza do packshot é normalizado para branco e multiplicado sobre a cor da marca.
Leva frase em Playfair e rótulo em Poppins. Story sem logo.
Uso: python3 -I referencia_story.py <foto> <saida.jpg> "<frase>" "<RÓTULO>" "<recorte x0,y0,x1,y1 px>" "<marca x0,y0,x1,y1 px>" [areia|offwhite]
"""
import sys
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, str(Path(__file__).resolve().parent))
from modelos import frase_linhas, desenha_frase, espacado, COR, A
cx = lambda s: tuple(int(v) for v in s.split(","))
def story(foto, saida, frase, rotulo, recorte, marca, fundo="areia"):
    W, H = 1080, 1920; base = Image.new("RGB", (W, H), COR[fundo])
    src = Image.open(foto).convert("RGB"); bg = src.getpixel((5, 5))
    src = Image.merge("RGB", [c.point(lambda v, b=b: min(255, round(v * 255 / max(b, 1) * 1.05))) for c, b in zip(src.split(), bg)])
    m = cx(marca); src.paste(src.crop(m).filter(ImageFilter.GaussianBlur(10)), m[:2])   # marca ilegível
    p = src.crop(cx(recorte)).filter(ImageFilter.GaussianBlur(1.6))                     # ofuscado no todo
    alt = 1020; p = p.resize((round(p.width * alt / p.height), alt), Image.LANCZOS)
    x, y = (W - p.width) // 2, 130
    reg = base.crop((x, y, x + p.width, y + p.height)); base.paste(ImageChops.multiply(reg, p), (x, y))
    d = ImageDraw.Draw(base); tam = 70; linhas = frase_linhas(frase, tam, W - 200)
    yf = desenha_frase(d, W, 1190, linhas, tam, COR["marinho"], COR["cafe"] if fundo == "areia" else COR["caramelo"])
    d.line([(W/2 - 40, yf + 30), (W/2 + 40, yf + 30)], fill=COR["marinho"], width=2)
    espacado(d, W/2, yf + 100, rotulo.upper(), ImageFont.truetype(str(A/"fonts"/"Poppins-Bold.ttf"), 30), COR["marinho"], 9)
    assert yf + 100 < 1536, "texto abaixo da área segura"
    base.save(saida, "JPEG", quality=92)
if __name__ == "__main__":
    a = sys.argv[1:] + ["areia"]; story(*a[:7])
