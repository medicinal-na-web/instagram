"""Marca Medicinal nas artes: SEMPRE a partir do logo oficial do site (assets/logo/medicinal-logo-oficial.svg).

Nunca digitar "medicinal" em fonte: usar estas funções.
  palavra(cor, largura)          -> só a palavra "medicinal" recortada do logo
  logo(tipo, cor, largura)       -> tipo 'completo' (símbolo + palavra + "FARMÁCIA E MANIPULAÇÃO")
                                     ou 'sem-simbolo' (palavra + "FARMÁCIA E MANIPULAÇÃO")
  cor: 'branco' (sobre foto/marinho), 'marinho' (sobre claro), 'off-white', 'original' (azuis do site)
"""
import os
from PIL import Image

PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'logo')


def _abre(nome, largura):
    im = Image.open(os.path.join(PASTA, nome)).convert('RGBA')
    return im.resize((int(largura), int(im.height * largura / im.width)), Image.LANCZOS)


def palavra(cor='branco', largura=170):
    cor = 'azul-oficial' if cor == 'original' else cor
    return _abre(f'medicinal-palavra-{cor}.png', largura)


def logo(tipo='sem-simbolo', cor='branco', largura=260):
    return _abre(f'medicinal-logo-{tipo}-{cor}.png', largura)


def aplica(img, marca, xy):
    """Cola a marca (RGBA) na arte, na posição (x, y) do canto superior esquerdo."""
    img.paste(marca, (int(xy[0]), int(xy[1])), marca)
    return img
