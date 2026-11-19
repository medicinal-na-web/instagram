"""Variante do ativo_animado.py com o texto no topo (área calma do fundo marinho), para quando o objeto ocupa o centro e o rodapé.
Texto no padrão oficial (doc 09, seção 0): branco, Playfair, palavra-chave em linha própria; fundo marinho aceito pelo Ricardo (16/11/2026). Uso: python3 -I ativo_animado_topo.py <video> <saida.mp4> "<frase *chave*>" "<RÓTULO>" [y=0.13]"""
import subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "padrao"))
from padrao import blocos, larg, A, BR  # padrão oficial: texto branco, palavra-chave em linha própria Bold Italic 1,6x
def overlay(frase, rotulo, saida_png, y0=0.13):
    W, H = 1080, 1920; im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for y in range(0, int(H * 0.42)):  # degradê suave no topo, sem faixa
        d.line([(0, y), (W, y)], fill=(0, 0, 0, round(255 * 0.30 * (1 - y / (H * 0.42)) ** 1.3)))
    y = H * y0
    for t, f in blocos(frase, 74, W):
        y += f.size; x = (W - larg(t, f)) / 2
        for ch in t: d.text((x, y), ch, font=f, fill=BR + (255,), anchor="ls"); x += f.getlength(ch) - 0.025 * f.size
        y += f.size * 0.18
    im.save(saida_png)
if __name__ == "__main__":
    vin, vout, frase, rot = sys.argv[1:5]; y0 = float(sys.argv[5]) if len(sys.argv) > 5 else 0.13
    with tempfile.TemporaryDirectory() as td:
        ov = f"{td}/ov.png"; overlay(frase, rot, ov, y0)
        fc = "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[v];[1:v]format=rgba,fade=t=in:st=0.8:d=0.6:alpha=1,fade=t=out:st=8.3:d=0.7:alpha=1[o];[v][o]overlay=0:0:shortest=1"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vin, "-loop", "1", "-i", ov, "-filter_complex", fc, "-shortest",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-an", "-movflags", "+faststart", vout], check=True)
