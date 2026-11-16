"""Novembro Azul · carrossel "os números" (feed 4:5) no PADRÃO OFICIAL (doc 09, seção 0).
Foto real com a fita azul em toda lâmina, sem filtro; escurecimento suave só atrás do texto e do gráfico.
Fontes: Playfair (frases, palavra-chave Bold Italic 1,6x) + Poppins (números, anos, fonte). Logo pequeno em posição variável.
Dados: casos novos estimados (INCA) e óbitos (SIM/DATASUS, CID C61, dados finais até 2024). Ver grade/temas/prostata-dados-oficiais.md.
Uso: python3 -I carrossel_numeros.py <pasta_saida>
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageStat
G = Path(__file__).resolve().parent.parent; A = G / "assets"
sys.path.insert(0, str(G / "padrao")); sys.path.insert(0, str(G / "campanha-nov"))
from padrao import arte, blocos, larg
import logo_pos
W, H = 1080, 1350; BR = (255, 255, 255)
FOTO = G / "fotos-padrao" / "fita-linho.png"
POP = lambda t: ImageFont.truetype(str(A / "fonts" / "Poppins-Bold.ttf"), t)
POPR = lambda t: ImageFont.truetype(str(A / "fonts" / "Poppins-Bold.ttf"), t)

def base(ancora=0.15):
    im = Image.open(FOTO).convert("RGB"); r = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x = (im.width - W) // 2; y = round((im.height - H) * ancora); im = im.crop((x, y, x + W, y + H))
    media = ImageStat.Stat(im.convert("L").crop((80, 100, W - 80, 1000))).mean[0]
    forca = 0.34 + 0.28 * max(0, (media - 150) / 105)
    ov = Image.new("L", (W, H), 0); d = ImageDraw.Draw(ov)
    for y in range(H):
        t = 0 if y < 20 or y > 1080 else min(1, (y - 20) / 160, (1080 - y) / 180)
        d.line([(0, y), (W, y)], fill=round(255 * forca * t))
    return Image.composite(Image.new("RGB", (W, H), (18, 14, 12)), im, ov).convert("RGBA")

def titulo(d, frase, y, tam=58):
    for t, f in blocos(frase, tam, W):
        y += f.size; x = (W - larg(t, f)) / 2
        for ch in t: d.text((x, y), ch, font=f, fill=BR, anchor="ls"); x += f.getlength(ch) - 0.025 * f.size
        y += f.size * 0.18
    return y

def fonte(d, txt, y):
    f = POP(24); tr = 5; t = txt.upper(); w = sum(f.getlength(c) for c in t) + tr * (len(t) - 1); x = (W - w) / 2
    for c in t: d.text((x, y), c, font=f, fill=BR + (220,), anchor="ls"); x += f.getlength(c) + tr

def barras(d, rotulos, valores, topo, base_y, destaque_ult=True, rotulo_valor=None, larg_max=200):
    n = len(valores); area = W - 200; passo = area / n; lb = min(larg_max, passo * 0.62); vmax = max(valores)
    for i, (r, v) in enumerate(zip(rotulos, valores)):
        cx = 100 + passo * (i + 0.5); h = (base_y - topo) * v / vmax; ult = i == n - 1
        a = 235 if (ult and destaque_ult) else 150
        d.rounded_rectangle([cx - lb / 2, base_y - h, cx + lb / 2, base_y], 10, fill=BR + (a,))
        if rotulo_valor is None or i in rotulo_valor:
            fv = POP(40 if n <= 4 else 30); d.text((cx, base_y - h - 18), f"{v:,}".replace(",", "."), font=fv, fill=BR, anchor="ms")
        d.text((cx, base_y + 44), r, font=POP(30 if n <= 4 else 24), fill=BR, anchor="ms")

def logo(img, evitar):
    lg = Image.open(A / "logo" / "medicinal-palavra-branco.png").convert("RGBA"); lg = lg.resize((150, round(lg.height * 150 / lg.width)), Image.LANCZOS)
    return logo_pos.aplica(img, lg, evitar, ordem=("id", "ie"))  # gráficos: só cantos de baixo (nunca sobre o título nem sobre a fita)

def camada(img):
    c = Image.new("RGBA", img.size, (0, 0, 0, 0)); return c, ImageDraw.Draw(c)

def grafico_casos(saida, evitar):
    img = base(); c, d = camada(img)
    y = titulo(d, "casos novos estimados por ano: *+18%*", 70)
    barras(d, ["2020–2022", "2023–2025", "2026–2028"], [65840, 71730, 77920], y + 140, 930)
    fonte(d, "fonte: INCA · estimativas por triênio", 1035)
    img = Image.alpha_composite(img, c); return logo(img, evitar), img

def grafico_obitos(saida, evitar):
    img = base(); c, d = camada(img)
    y = titulo(d, "mortes por câncer de próstata: *+23% em 10 anos*", 70, 54)
    anos = list(range(2015, 2025)); vals = [14484, 14926, 15391, 15576, 15983, 15841, 16301, 16429, 17258, 17826]
    barras(d, [str(a)[2:] if a not in (2015, 2024) else str(a) for a in anos], vals, y + 140, 930, rotulo_valor={0, 9}, larg_max=70)
    fonte(d, "fonte: SIM/Ministério da Saúde · dados finais", 1035)
    img = Image.alpha_composite(img, c); return logo(img, evitar), img

if __name__ == "__main__":
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True); F = str(FOTO)
    pos = arte("feed", F, str(out / "na-carrossel-1.jpg"), "os números do *Novembro Azul*", yfrac=0.3)
    pos, im = grafico_casos(None, pos); im.convert("RGB").save(out / "na-carrossel-2.jpg", quality=92)
    pos, im = grafico_obitos(None, pos); im.convert("RGB").save(out / "na-carrossel-3.jpg", quality=92)
    pos = arte("feed", F, str(out / "na-carrossel-4.jpg"), "esses números podem ser *diferentes*.", mono="informação muda hábitos", yfrac=0.3, evitar_logo=pos)
    arte("feed", F, str(out / "na-carrossel-5.jpg"), "nós não vamos deixar de *conscientizar*.", mono="converse com seu médico", yfrac=0.3, evitar_logo=pos)
    print("ok")
