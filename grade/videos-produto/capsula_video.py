"""Formato 4 - "Cápsula por dentro": macro da cápsula abrindo (Runway) + texto no PADRÃO OFICIAL (doc 09, seção 0).
Texto branco, Playfair, palavra-chave em linha própria Bold Italic 1,6x; story sem logo; sem filtro de cor,
só escurecimento suave atrás do texto. O texto entra com fade depois que o pó cai; o último quadro segura
alguns segundos para leitura.
Uso: python3 -I capsula_video.py <entrada.mp4> <saida.mp4> "<frase com *chave*>" [--mono "comente X"] [--y 0.2] [--entra 2.6] [--segura 2.5]
"""
import argparse, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
G = Path(__file__).resolve().parent.parent; sys.path.insert(0, str(G / "padrao"))
from padrao import blocos, larg, A, BR

def overlay(frase, saida_png, mono="", yfrac=0.2, tam=76):
    W, H = 1080, 1920
    linhas = blocos(frase, tam, W); alt = sum(f.size * 1.18 for _, f in linhas) + (110 if mono else 0)
    y0 = min(max(H * yfrac - alt / 2, 0.14 * H), 0.80 * H - alt)  # área segura do story: 14% a 80%
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c0, c1 = y0 - 240, y0 + alt + 240
    for y in range(H):  # degradê suave atrás do texto, sem faixa
        t = 0 if y < c0 or y > c1 else (1 - abs((y - (c0 + c1) / 2) / ((c1 - c0) / 2))) ** 0.8
        d.line([(0, y), (W, y)], fill=(18, 14, 12, round(255 * 0.40 * t)))
    y = y0
    for t, f in linhas:
        y += f.size; x = (W - larg(t, f)) / 2
        for ch in t: d.text((x, y), ch, font=f, fill=BR, anchor="ls"); x += f.getlength(ch) - 0.025 * f.size
        y += f.size * 0.18
    if mono:
        f = ImageFont.truetype(str(A / "fonts" / "IBMPlexMono-Regular.ttf"), 40); w = f.getlength(mono)
        d.text(((W - w) / 2, y + 70), mono, font=f, fill=BR, anchor="ls"); d.line([((W - w) / 2, y + 82), ((W + w) / 2, y + 82)], fill=BR, width=2)
    im.save(saida_png)

if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("entrada"); a.add_argument("saida"); a.add_argument("frase")
    a.add_argument("--mono", default=""); a.add_argument("--y", type=float, default=0.2)
    a.add_argument("--tam", type=int, default=76); a.add_argument("--desce", type=float, default=0, help="amplia o vídeo e ancora no topo, descendo o objeto (ex.: 0.08)")
    a.add_argument("--entra", type=float, default=2.6); a.add_argument("--segura", type=float, default=2.5)
    o = a.parse_args()
    with tempfile.TemporaryDirectory() as td:
        ov = f"{td}/ov.png"; overlay(o.frase, ov, o.mono, o.y, o.tam); k = 1 + o.desce
        fc = (f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,scale=iw*{k}:-2,crop=1080:1920:(iw-1080)/2:0,tpad=stop_mode=clone:stop_duration={o.segura}[v];"
              f"[1:v]format=rgba,fade=t=in:st={o.entra}:d=0.7:alpha=1[o];[v][o]overlay=0:0:shortest=1")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", o.entrada, "-loop", "1", "-i", ov, "-filter_complex", fc,
                        "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-r", "30", "-movflags", "+faststart", o.saida], check=True)
