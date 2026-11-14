"""Dermo-day no PADRÃO OFICIAL (doc 09, seção 0): carrossel do feed (6 lâminas) + 4 stories, tudo com padrao.arte().
- Toda arte é foto real, sem filtro de cor; só escurecimento leve na faixa do texto.
- Produto de referência: recortado da foto do fabricante, marca desfocada, leve desfoque geral, pousado
  (multiplicação + sombra suave) sobre uma foto real de bancada vazia.
Uso: python3 -I render_oficial.py <conteudo_oficial.json> <pasta_saida>
"""
import json, sys
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFilter
G = Path(__file__).resolve().parent.parent; sys.path.insert(0, str(G / "padrao"))
from padrao import arte

def produto_na_bancada(c, saida, W, H, alt_frac=0.50, base_frac=0.90):
    fundo = Image.open(c["fundo_bancada"]).convert("RGB")
    r = max(W / fundo.width, H / fundo.height); fundo = fundo.resize((round(fundo.width * r), round(fundo.height * r)), Image.LANCZOS)
    x0 = (fundo.width - W) // 2; y0 = (fundo.height - H) // 2; fundo = fundo.crop((x0, y0, x0 + W, y0 + H))
    src = Image.open(c["foto_referencia"]).convert("RGB"); bg = src.getpixel((5, 5))
    src = Image.merge("RGB", [ch.point(lambda v, b=b: min(255, round(v * 255 / max(b, 1)))) for ch, b in zip(src.split(), bg)])  # fundo do fabricante -> branco
    m = tuple(c["marca"]); src.paste(src.crop(m).filter(ImageFilter.GaussianBlur(10)), m[:2])  # marca ilegível
    p = src.crop(tuple(c["recorte"])).filter(ImageFilter.GaussianBlur(1.4))  # ofuscado, mas em destaque
    alt = round(H * alt_frac); p = p.resize((round(p.width * alt / p.height), alt), Image.LANCZOS)
    x = (W - p.width) // 2 + round(W * 0.05); y = round(H * base_frac) - alt
    # sombra de contato suave sob o produto
    sh = Image.new("L", (W, H), 0); ImageDraw.Draw(sh).ellipse([x + p.width * 0.30, y + alt - 30, x + p.width * 0.80, y + alt + 20], fill=120)
    fundo = Image.composite(Image.new("RGB", (W, H), (60, 52, 46)), fundo, sh.filter(ImageFilter.GaussianBlur(24)))
    reg = fundo.crop((x, y, x + p.width, y + alt)); mask = Image.new("L", p.size, 0)
    ImageDraw.Draw(mask).rectangle([30, 30, p.width - 30, alt - 30], fill=255); mask = mask.filter(ImageFilter.GaussianBlur(24))
    fundo.paste(Image.composite(ImageChops.multiply(reg, p), reg, mask), (x, y)); fundo.save(saida, quality=95); return saida

if __name__ == "__main__":
    c = json.load(open(sys.argv[1])); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True); s = c["slug"]
    capa_feed = produto_na_bancada(c, str(out / "_capa_feed.jpg"), 1080, 1350)
    capa_story = produto_na_bancada(c, str(out / "_capa_story.jpg"), 1080, 1920, alt_frac=0.42, base_frac=0.86)
    pos = None
    for i, L in enumerate(c["feed"], 1):
        foto = capa_feed if L["foto"] == "CAPA" else L["foto"]
        pos = arte("feed", foto, str(out / f"{s}-feed-{i}.jpg"), L["frase"], mono=L.get("mono", ""), yfrac=L.get("y"),
                   ancora=L.get("ancora", 0.5), evitar_logo=pos)
    for i, L in enumerate(c["stories"], 1):
        foto = capa_story if L["foto"] == "CAPA" else L["foto"]
        arte("story", foto, str(out / f"{s}-story-{i}.jpg"), L["frase"], mono=L.get("mono", ""), yfrac=L.get("y"), ancora=L.get("ancora", 0.5))
    print("ok")
