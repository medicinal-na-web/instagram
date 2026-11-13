"""Gerador único no PADRÃO OFICIAL (doc 09, seção 0, aprovado em 13/11/2026).
- Toda arte é foto, sem filtro de cor; só um escurecimento leve onde fica o texto branco.
- Texto branco centralizado em área calma. A frase usa Playfair e a palavra entre *asteriscos* vira
  uma linha só dela, em Bold Italic, 1,6x maior.
- No máximo 2 fontes: Playfair + (rótulo Poppins OU linha mono sublinhada).
- Story: sem logo, texto entre 14% e 80% da altura. Feed: logo pequeno em posição variável (logo_pos.py).
Uso:
  python3 -I padrao.py <story|feed> <foto> <saida.jpg> "<frase com *chave*>" [--rotulo X | --mono "linha"] [--y 0.55] [--ancora 0.5]
"""
import argparse, re, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
G = Path(__file__).resolve().parent.parent; A = G / "assets"
sys.path.insert(0, str(G / "campanha-nov")); import logo_pos
BR = (255, 255, 255)
def pf(t, it=False, peso=400):
    f = ImageFont.truetype(str(A/"fonts"/("PlayfairDisplay-Italic.ttf" if it else "PlayfairDisplay.ttf")), t); f.set_variation_by_axes([peso]); return f
def minus(t): return re.sub(r"(^|[.!?…]\s+)(\*?)([A-ZÀ-Ý])(?=[a-zà-ÿ]|\s)", lambda m: m.group(1) + m.group(2) + m.group(3).lower(), t)
def larg(t, f): return sum(f.getlength(c) for c in t) - 0.025 * f.size * max(len(t) - 1, 0)
def quebra(t, f, maxw):
    ls, at = [], ""
    for p in t.split():
        n = (at + " " + p).strip()
        if at and larg(n, f) > maxw: ls.append(at); at = p
        else: at = n
    ls = ls + ([at] if at else [])
    if len(ls) < 2: return ls
    # reequilibra: mesmo número de linhas, larguras parecidas
    ps = t.split(); n = len(ls); alvo = larg(t, f) / n; out, cur = [], []
    for i, p in enumerate(ps):
        cur.append(p)
        if len(out) < n - 1 and larg(" ".join(cur), f) >= alvo * 0.92 and len(ps) - i - 1 >= (n - 1 - len(out)):
            out.append(" ".join(cur)); cur = []
    if cur: out.append(" ".join(cur))
    return out if all(larg(l, f) <= maxw for l in out) else ls
def blocos(frase, tam, W):
    """frase com *chave* -> linhas [(texto, fonte)]: antes (normal), chave (grande, linha própria), depois (normal)."""
    frase = minus(" ".join(frase.split())); m = re.search(r"\*([^*]+)\*", frase)
    normal, grande = pf(tam), pf(round(tam * 1.6), True, 700); maxw = W - 200; out = []
    if m:
        chave, depois = m.group(1).strip(), frase[m.end():]
        pont = re.match(r"^[.,!?…:;]+", depois)
        if pont: chave += pont.group(0); depois = depois[pont.end():]
        antes = frase[:m.start()].strip()
        if antes and len(antes.split()) == 1 and len(antes) <= 3: chave = antes + " " + chave; antes = ""  # artigo solto vai junto da palavra-chave
        partes = [(antes, normal), (chave, grande), (depois.strip(), normal)]
    else: partes = [(frase, normal)]
    for t, f in partes:
        if not t: continue
        for l in quebra(t, f, maxw):
            while larg(l, f) > maxw and f.size > 40: f = pf(f.size - 4, f is grande, 700 if f is grande else 400)
            out.append((l, f))
    return out
def cobre(im, W, H, ancora):
    r = max(W/im.width, H/im.height); im = im.resize((round(im.width*r), round(im.height*r)), Image.LANCZOS)
    x = (im.width - W)//2; y = round((im.height - H) * ancora); return im.crop((x, y, x+W, y+H))
def arte(canal, foto, saida, frase, rotulo="", mono="", yfrac=None, ancora=0.5, tam=None, evitar_logo=None):
    W, H = 1080, (1920 if canal == "story" else 1350)
    img = cobre(Image.open(foto).convert("RGB"), W, H, ancora)
    tam = tam or (76 if canal == "story" else 70)
    linhas = blocos(frase, tam, W); alt = sum(f.size * 1.18 for _, f in linhas) + (110 if (rotulo or mono) else 0)
    if yfrac is None:  # procura a faixa mais calma (pouca variação e sem fundo muito claro para texto branco)
        from PIL import ImageStat
        cand = [i / 100 for i in (range(26, 76, 4) if canal == "story" else range(22, 80, 4))]; cinza = img.convert("L"); melhor = None
        for c in cand:
            a0 = max(0, int(H * c - alt / 2)); reg = cinza.crop((140, a0, W - 140, min(H, int(a0 + alt))))
            st = ImageStat.Stat(reg); sc = st.stddev[0] + max(0, st.mean[0] - 215) * 0.3 + abs(c - 0.5) * 8
            if melhor is None or sc < melhor[0]: melhor = (sc, c)
        yfrac = melhor[1]
    y0 = H * yfrac - alt / 2
    if canal == "story": y0 = min(max(y0, 0.16 * H), 0.80 * H - alt)
    # escurecimento leve só na faixa do texto (degradê suave, sem borda)
    from PIL import ImageStat
    media = ImageStat.Stat(img.convert("L").crop((140, int(max(0, y0)), W - 140, int(min(H, y0 + alt))))).mean[0]
    forca = 0.30 + 0.28 * max(0, (media - 150) / 105)  # fundo claro pede um pouco mais de sombra para o branco
    ov = Image.new("L", (W, H), 0); d = ImageDraw.Draw(ov); c0, c1 = y0 - 220, y0 + alt + 220
    for y in range(H):
        t = 0 if y < c0 or y > c1 else (1 - abs((y - (c0 + c1) / 2) / ((c1 - c0) / 2))) ** 0.8
        d.line([(0, y), (W, y)], fill=round(255 * forca * t))
    img = Image.composite(Image.new("RGB", (W, H), (18, 14, 12)), img, ov).convert("RGBA"); d = ImageDraw.Draw(img)
    y = y0
    for t, f in linhas:
        y += f.size; x = (W - larg(t, f)) / 2
        for ch in t: d.text((x, y), ch, font=f, fill=BR, anchor="ls"); x += f.getlength(ch) - 0.025 * f.size
        y += f.size * 0.18
    if rotulo:
        f = ImageFont.truetype(str(A/"fonts"/"Poppins-Bold.ttf"), 46 if canal == "story" else 40); tr = 14; t = rotulo.upper()
        w = sum(f.getlength(c) for c in t) + tr * (len(t) - 1); x = (W - w) / 2
        for ch in t: d.text((x, y + 70), ch, font=f, fill=BR, anchor="ls"); x += f.getlength(ch) + tr
    elif mono:
        f = ImageFont.truetype(str(A/"fonts"/"IBMPlexMono-Regular.ttf"), 40 if canal == "story" else 38); w = f.getlength(mono)
        d.text(((W - w) / 2, y + 70), mono, font=f, fill=BR, anchor="ls"); d.line([((W - w) / 2, y + 82), ((W + w) / 2, y + 82)], fill=BR, width=2)
    pos = None
    if canal == "feed":
        lg = Image.open(A/"logo"/"medicinal-palavra-branco.png").convert("RGBA"); lg = lg.resize((160, round(lg.height*160/lg.width)), Image.LANCZOS)
        pos = logo_pos.aplica(img, lg, evitar_logo)
    img.convert("RGB").save(saida, "JPEG", quality=92); return pos
if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("canal"); a.add_argument("foto"); a.add_argument("saida"); a.add_argument("frase")
    a.add_argument("--rotulo", default=""); a.add_argument("--mono", default=""); a.add_argument("--y", type=float); a.add_argument("--ancora", type=float, default=0.5)
    a.add_argument("--evitar-logo", default=None)
    o = a.parse_args(); print(arte(o.canal, o.foto, o.saida, o.frase, o.rotulo, o.mono, o.y, o.ancora, evitar_logo=o.evitar_logo))
