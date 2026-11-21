"""Formato "Receita em cenas": vídeo de 3 a 5 cenas (Runway multishot) + um passo escrito por cena, no PADRÃO OFICIAL
(doc 09, seção 0): texto branco Playfair, palavra-chave em linha própria Bold Italic 1,6x, máx. 12 palavras por passo,
story/reels sem logo, texto entre 14% e 80% da altura, escurecimento suave só atrás do texto.
Cada passo entra e sai com fade; o último quadro segura alguns segundos para leitura.
Uso: python3 -I receita_video.py <entrada.mp4> <saida.mp4> --passo "0:3.7|abacaxi, coco e *proteína.*" --passo "3.7:7.5|bata com *gelo.*|mono opcional" [--y 0.22] [--segura 2.5]
"""
import argparse, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image
G = Path(__file__).resolve().parent
sys.path.insert(0, str(G))
from capsula_video import overlay

FADE = 0.4

def alfa(t, t0, t1):
    if t < t0 or t > t1: return 0.0
    return max(0.0, min(1.0, (t - t0) / FADE, (t1 - t) / FADE))

if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("entrada"); a.add_argument("saida")
    a.add_argument("--passo", action="append", required=True); a.add_argument("--y", type=float, default=0.22)
    a.add_argument("--tam", type=int, default=76); a.add_argument("--segura", type=float, default=2.5)
    o = a.parse_args(); fps = 30
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", o.entrada], capture_output=True, text=True).stdout)
    total = dur + o.segura
    passos = []
    for p in o.passo:
        tempo, *resto = p.split("|"); t0, t1 = (float(x) for x in tempo.split(":"))
        passos.append((t0, total + 1 if t1 >= dur - 0.05 else t1, resto[0], resto[1] if len(resto) > 1 else ""))
    with tempfile.TemporaryDirectory() as td:
        base = {}
        for i, (t0, t1, frase, mono) in enumerate(passos):
            overlay(frase, f"{td}/p{i}.png", mono, o.y, o.tam); base[i] = Image.open(f"{td}/p{i}.png").convert("RGBA")
        vazio = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); cache = {}
        for k in range(int(total * fps) + 1):
            t = k / fps; im = vazio
            for i, (t0, t1, _, _) in enumerate(passos):
                al = round(alfa(t, t0, t1), 2)
                if al > 0:
                    chave = (i, al)
                    if chave not in cache:
                        c = base[i].copy(); c.putalpha(c.getchannel("A").point(lambda v, al=al: round(v * al))); cache[chave] = c
                    im = Image.alpha_composite(im, cache[chave])
            im.save(f"{td}/q{k:05d}.png")
        fc = (f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,tpad=stop_mode=clone:stop_duration={o.segura},fps={fps}[v];"
              f"[1:v]format=rgba[o];[v][o]overlay=0:0:shortest=1")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", o.entrada, "-framerate", str(fps), "-i", f"{td}/q%05d.png", "-filter_complex", fc,
                        "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-r", "30", "-movflags", "+faststart", o.saida], check=True)
