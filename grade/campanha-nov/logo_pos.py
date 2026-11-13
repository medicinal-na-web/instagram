"""Posição do logo oficial (padrão de 13/11/2026): a posição VARIA entre as artes.
Candidatos: superior esquerdo, superior direito, inferior esquerdo, inferior direito e inferior centro, sempre a 60 px da borda.
Escolhe o canto mais calmo (menor variação de luz, ou seja, sem texto, produto ou reflexo), desconsiderando
a posição usada na arte anterior. Chamar DEPOIS de escrever o texto, para o texto contar como área ocupada.
"""
from PIL import ImageStat
CANDIDATOS = ("se", "sd", "ie", "id", "ic")
def caixa(pos, W, H, w, h, m=60):
    return {"se": (m, m), "sd": (W - m - w, m), "ie": (m, H - m - h), "id": (W - m - w, H - m - h), "ic": ((W - w) // 2, H - m - h)}[pos]
def escolhe(img, w, h, evitar=None, ordem=CANDIDATOS, claro=True):
    """claro=True: logo branco (penaliza fundo claro, onde ele some); False: logo escuro (penaliza fundo escuro)."""
    W, H = img.size; melhor = None
    for pos in ordem:
        if pos == evitar: continue
        x, y = caixa(pos, W, H, w, h); reg = img.convert("L").crop((x - 20, y - 20, x + w + 20, y + h + 20))
        st = ImageStat.Stat(reg); media = st.mean[0]
        s = st.stddev[0] + (max(0, media - 165) * 1.5 if claro else max(0, 120 - media) * 1.5)
        if melhor is None or s < melhor[0]: melhor = (s, pos)
    return melhor[1]
def aplica(img, lg, evitar=None, ordem=CANDIDATOS, claro=True):
    """Cola o logo (RGBA) no canto mais calmo e devolve a posição usada."""
    pos = escolhe(img, lg.width, lg.height, evitar, ordem, claro); img.alpha_composite(lg, caixa(pos, img.width, img.height, lg.width, lg.height)); return pos
