"""Story do produto do dia: foto real do produto (packshot do site, fundo branco removido) sobre fundo da marca,
frase Playfair (palavra-chave Bold Italic), rótulo Poppins e chamada "responda PALAVRA e receba o link".
Story sem logo (o Instagram já mostra @medicinalnaweb). Texto acima da barra de resposta (y < 1536).
Uso: python3 -I produto_story.py <foto_site> <saida.jpg> "<frase>" "<RÓTULO>" "<PALAVRA>" [offwhite|areia] [tolerância do branco, padrão 18; suba se a sombra do packshot ficar]
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, str(Path(__file__).resolve().parent))
from modelos import frase_linhas, desenha_frase, espacado, COR, A
def recorta(foto, tol=18):
    im = Image.open(foto).convert("RGB"); W, H = im.size
    m = Image.new("L", (W, H), 0); px = im.load(); mp = m.load(); pilha = [(0, 0), (W-1, 0), (0, H-1), (W-1, H-1)]
    branco = lambda p: min(p) >= 255 - tol
    while pilha:  # preenche a partir das bordas só o branco conectado ao fundo
        x, y = pilha.pop()
        if x < 0 or y < 0 or x >= W or y >= H or mp[x, y] or not branco(px[x, y]): continue
        mp[x, y] = 255; pilha += [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    alpha = m.point(lambda v: 255 - v).filter(ImageFilter.GaussianBlur(1.2))
    rgba = im.convert("RGBA"); rgba.putalpha(alpha); return rgba.crop(alpha.getbbox())
def story(foto, saida, frase, rotulo, palavra, fundo="offwhite", tol=18):
    W, H = 1080, 1920; img = Image.new("RGB", (W, H), COR[fundo]).convert("RGBA")
    # multiplicação: o branco do packshot vira a cor do fundo e a sombra original fica natural (sem recorte)
    src = Image.open(foto).convert("RGB")
    bb = Image.eval(src.convert("L"), lambda v: 255 if v < 255 - tol else 0).getbbox()
    pad = 40; q = src.crop(bb); p = Image.new("RGB", (q.width + 2 * pad, q.height + 3 * pad), (255, 255, 255)); p.paste(q, (pad, pad))
    alt = 720; p = p.resize((round(p.width * alt / p.height), alt), Image.LANCZOS)
    if p.width > 760: p = p.resize((760, round(p.height * 760 / p.width)), Image.LANCZOS)
    x, y = (W - p.width) // 2, 1040 - p.height
    base = img.convert("RGB"); reg = base.crop((x, y, x + p.width, y + p.height))
    from PIL import ImageChops
    base.paste(ImageChops.multiply(reg, p), (x, y)); img = base.convert("RGBA")
    d = ImageDraw.Draw(img); tam = 74; linhas = frase_linhas(frase, tam, W - 200)
    yf = desenha_frase(d, W, 1090, linhas, tam, COR["marinho"], COR["caramelo"] if fundo == "offwhite" else COR["cafe"])
    d.line([(W/2 - 40, yf + 30), (W/2 + 40, yf + 30)], fill=COR["marinho"], width=2)  # rótulo removido: no máximo 2 fontes
    fm = ImageFont.truetype(str(A/"fonts"/"IBMPlexMono-Regular.ttf"), 36); cta = f"responda {palavra} e receba o link"
    yc = yf + 110; wc = fm.getlength(cta); xc = (W - wc) / 2
    d.text((xc, yc), cta, font=fm, fill=COR["marinho"], anchor="ls"); d.line([(xc, yc + 10), (xc + wc, yc + 10)], fill=COR["marinho"], width=2)
    assert yc + 12 < 1536, "chamada abaixo da área segura"
    img.convert("RGB").save(saida, "JPEG", quality=92)
if __name__ == "__main__":
    a = sys.argv[1:] + ["offwhite", "18"][len(sys.argv) - 6:]; story(a[0], a[1], a[2], a[3], a[4], a[5], int(a[6]))
