"""Escurece só o vermelho vivo (gota de suco) para ficar no tom bordô dos gomos.
Máscara: matiz vermelho, saturação alta e brilho acima do tom da polpa. Uso: python3 -I escurece_gota.py <entrada.png> <saida.png> [fator]"""
import sys
import numpy as np
from PIL import Image, ImageFilter
def processa(im, fator=0.68):
    hsv = np.asarray(im.convert("HSV")).astype(np.float32) / 255.0
    h, s, v = hsv[..., 0] * 360, hsv[..., 1], hsv[..., 2]
    vermelho = (h >= 340) | (h <= 6)
    m = vermelho & (s > 0.72) & (v > 0.60)
    mask = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))
    mk = np.asarray(mask).astype(np.float32) / 255.0
    rgb = np.asarray(im.convert("RGB")).astype(np.float32)
    alvo = rgb * fator; alvo[..., 2] *= 1.04  # leve puxada para o bordô
    out = rgb * (1 - mk[..., None]) + alvo * mk[..., None]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
if __name__ == "__main__":
    f = float(sys.argv[3]) if len(sys.argv) > 3 else 0.68
    processa(Image.open(sys.argv[1]), f).save(sys.argv[2])
