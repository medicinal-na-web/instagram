"""Modelos de arte sem foto do padrão (doc 09, seção 5), para variar os stories do dia.
E: fundo marinho #102140, rótulo Poppins caixa alta off-white, frase Playfair off-white, palavra-chave Bold Italic caramelo.
F: fundo off-white #eee7da, rótulo e frase em marinho, palavra-chave Bold Italic marinho.
C: fundo areia #e0be97, pergunta IBM Plex Mono sublinhada (marinho) + resposta Playfair marinho, palavra-chave caramelo escuro (café).
Logo: palavra oficial (off-white sobre marinho; marinho sobre claro), 170 px a 60 px da borda.
Uso: python3 -I modelos.py <E|F|C> <story|feed> <saida.jpg> "<frase>" "<ROTULO>" ["<pergunta?>"]
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, str(Path(__file__).resolve().parent))
from arte import fonte, minus, larg, A
COR = {"marinho": (16, 33, 64), "offwhite": (238, 231, 218), "areia": (224, 190, 151), "caramelo": (191, 145, 98), "cafe": (137, 108, 87), "marinho2": (28, 52, 94)}
def espacado(d, cx, y, txt, f, cor, track):
    w = sum(f.getlength(c) for c in txt) + track * (len(txt) - 1); x = cx - w / 2
    for c in txt: d.text((x, y), c, font=f, fill=cor, anchor="ls"); x += f.getlength(c) + track
    return w
def frase_linhas(frase, tam, maxw):
    pal = [{"t": w.replace("*", ""), "k": "*" in w} for w in minus(" ".join(frase.split())).split(" ") if w]
    linhas, atual, lw = [], [], 0
    for p in pal:
        f = fonte(p["k"], tam); p["w"] = larg(p["t"], f, tam); esp = f.getlength(" ")
        if atual and lw + p["w"] > maxw: linhas.append(atual); atual, lw = [], 0
        atual.append(p); lw += p["w"] + esp
    if atual: linhas.append(atual)
    if len(linhas) > 1 and len(linhas[-1]) == 1 and len(linhas[-2]) > 2: linhas[-1].insert(0, linhas[-2].pop())
    return linhas
def desenha_frase(d, W, y, linhas, tam, cor, cor_k):
    alt = tam * 1.3
    for ps in linhas:
        w = sum(p["w"] for p in ps) + sum(fonte(p["k"], tam).getlength(" ") for p in ps[:-1]); x = (W - w) / 2
        for p in ps:
            f = fonte(p["k"], tam)
            for c in p["t"]: d.text((x, y + tam), c, font=f, fill=cor_k if p["k"] else cor, anchor="ls"); x += f.getlength(c) - 0.025 * tam
            x += f.getlength(" ")
        y += alt
    return y
def modelo(m, canal, saida, frase, rotulo="", pergunta=""):
    W, H = 1080, (1920 if canal == "story" else 1350)
    fundo, texto, kw, logo = {"E": ("marinho", "offwhite", "caramelo", "off-white"), "F": ("offwhite", "marinho", "marinho", "marinho"),
                              "C": ("areia", "marinho", "marinho2", "marinho")}[m]
    img = Image.new("RGB", (W, H), COR[fundo]); d = ImageDraw.Draw(img)
    tam = 84 if canal == "story" else 70; maxw = W - 200
    linhas = frase_linhas(frase, tam, maxw); alt_frase = len(linhas) * tam * 1.3
    pop = ImageFont.truetype(str(A / "fonts" / "Poppins-Bold.ttf"), 30); mono = ImageFont.truetype(str(A / "fonts" / "IBMPlexMono-Regular.ttf"), 40)
    bloco = alt_frase + (110 if rotulo else 0) + (130 if pergunta else 0)
    y = (H - bloco) / 2 + (40 if canal == "story" else 20)
    if pergunta:
        w = mono.getlength(pergunta); x = (W - w) / 2
        d.text((x, y + 40), pergunta, font=mono, fill=COR[texto], anchor="ls"); d.line([(x, y + 52), (x + w, y + 52)], fill=COR[texto], width=2)
        y += 130
    y = desenha_frase(d, W, y, linhas, tam, COR[texto], COR[kw])
    if rotulo:
        y += 40; d.line([(W / 2 - 40, y), (W / 2 + 40, y)], fill=COR["caramelo"] if m == "E" else COR[texto], width=2)
        espacado(d, W / 2, y + 70, rotulo.upper(), pop, COR[texto], 9)
    lg = Image.open(A / "logo" / f"medicinal-palavra-{logo}.png").convert("RGBA"); lg = lg.resize((170, round(lg.height * 170 / lg.width)), Image.LANCZOS)
    img = img.convert("RGBA"); img.alpha_composite(lg, (60, 290 if canal == "story" else 60)); img.convert("RGB").save(saida, "JPEG", quality=92)
if __name__ == "__main__":
    a = sys.argv[1:] + ["", ""]
    modelo(a[0], a[1], a[2], a[3], a[4], a[5])
