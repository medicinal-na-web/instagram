"""Formato 4 - "Cápsula por dentro": macro da cápsula abrindo (Runway) + texto no PADRÃO OFICIAL (doc 09, seção 0).
Texto branco, Playfair, palavra-chave em linha própria Bold Italic 1,6x; story sem logo; sem filtro de cor,
só escurecimento suave atrás do texto. O texto entra com fade depois que o pó cai; o último quadro segura
alguns segundos para leitura.
Uso: python3 -I capsula_video.py <entrada.mp4> <saida.mp4> "<frase com *chave*>" [--mono "comente X"] [--y 0.2] [--entra 0.3] [--cps 10] [--segura 2.5]
"""
import argparse, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
G = Path(__file__).resolve().parent.parent; sys.path.insert(0, str(G / "padrao"))
from padrao import blocos, larg, A, BR

def overlay(frase, saida_png, mono="", yfrac=0.2, tam=76, n=None, g=1.0):
    """n = quantos caracteres já aparecem (efeito de digitação); g = intensidade do escurecimento (0 a 1)."""
    W, H = 1080, 1920
    linhas = blocos(frase, tam, W); alt = sum(f.size * 1.18 for _, f in linhas) + (110 if mono else 0)
    y0 = min(max(H * yfrac - alt / 2, 0.14 * H), 0.80 * H - alt)  # área segura do story: 14% a 80%
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c0, c1 = y0 - 240, y0 + alt + 240
    for y in range(H):  # degradê suave atrás do texto, sem faixa
        t = 0 if y < c0 or y > c1 else (1 - abs((y - (c0 + c1) / 2) / ((c1 - c0) / 2))) ** 0.8
        d.line([(0, y), (W, y)], fill=(18, 14, 12, round(255 * 0.40 * t * g)))
    camada = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dc = ImageDraw.Draw(camada)
    y = y0; i = 0; vis = float("inf") if n is None else n; FADE = 3.0  # cada letra esmaece ao longo de ~3 letras
    def a_de(i): return 255 if vis == float("inf") else round(255 * max(0.0, min(1.0, (vis - i) / FADE)))
    for t, f in linhas:
        y += f.size; x = (W - larg(t, f)) / 2  # posição final fixa: a frase "se escreve" sem pular
        for ch in t:
            al = a_de(i)
            if al > 0: dc.text((x, y), ch, font=f, fill=BR + (al,), anchor="ls")
            x += f.getlength(ch) - 0.025 * f.size; i += 1
        y += f.size * 0.18
    if mono and a_de(i) > 0:
        f = ImageFont.truetype(str(A / "fonts" / "IBMPlexMono-Regular.ttf"), 40); w = f.getlength(mono); al = a_de(i)
        dc.text(((W - w) / 2, y + 70), mono, font=f, fill=BR + (al,), anchor="ls"); dc.line([((W - w) / 2, y + 82), ((W + w) / 2, y + 82)], fill=BR + (al,), width=2)
    im = Image.alpha_composite(im, camada)
    im.save(saida_png)

if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("entrada"); a.add_argument("saida"); a.add_argument("frase")
    a.add_argument("--mono", default=""); a.add_argument("--y", type=float, default=0.2)
    a.add_argument("--tam", type=int, default=76); a.add_argument("--desce", type=float, default=0, help="amplia o vídeo e ancora no topo, descendo o objeto (ex.: 0.08)")
    a.add_argument("--entra", type=float, default=0.3); a.add_argument("--cps", type=float, default=10, help="letras por segundo"); a.add_argument("--segura", type=float, default=2.5)
    o = a.parse_args()
    with tempfile.TemporaryDirectory() as td:
        k = 1 + o.desce; fps = 30
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", o.entrada], capture_output=True, text=True).stdout) + o.segura
        total = len("".join(t for t, _ in blocos(o.frase, o.tam, 1080))) + len(o.mono); ultimo = None
        for i in range(int(dur * fps) + 1):  # um PNG por quadro; repete o arquivo quando nada muda
            tt = i / fps; n = max(0.0, min(total + 3.0, (tt - o.entra) * o.cps)); g = max(0.0, min(1.0, (tt - o.entra + 0.3) / 0.5))
            chave = (round(n, 2), round(g, 2)); dst = f"{td}/q{i:05d}.png"
            if chave != (ultimo or (None,))[0]: overlay(o.frase, dst, o.mono, o.y, o.tam, n, g); ultimo = (chave, dst)
            else: Path(dst).symlink_to(ultimo[1])
        fc = (f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,scale=iw*{k}:-2,crop=1080:1920:(iw-1080)/2:0,tpad=stop_mode=clone:stop_duration={o.segura},fps={fps}[v];"
              f"[1:v]format=rgba[o];[v][o]overlay=0:0:shortest=1")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", o.entrada, "-framerate", str(fps), "-i", f"{td}/q%05d.png", "-filter_complex", fc,
                        "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-r", "30", "-movflags", "+faststart", o.saida], check=True)
