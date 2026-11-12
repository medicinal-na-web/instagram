"""Ativo animado: vídeo curto (Runway) + frase e rótulo no padrão do doc 09, saída 1080x1920 MP4.
Texto off-white (Playfair Regular; palavra-chave Bold Italic caramelo), rótulo Poppins caixa alta, logo off-white.
A frase entra com fade aos 0,8 s, no terço inferior.
Uso: python3 -I ativo_animado.py <video_entrada> <saida.mp4> "<frase com *chave*>" "<RÓTULO>" """
import subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "campanha-nov"))
from modelos import frase_linhas, desenha_frase, espacado, COR, A
from PIL import ImageFont
def overlay(frase, rotulo, saida_png):
    W, H = 1080, 1920; im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for y in range(int(H * 0.5), H):  # degradê suave (sem faixa), até 35% no rodapé
        d.line([(0, y), (W, y)], fill=(0, 0, 0, round(255 * 0.35 * ((y - H * 0.5) / (H * 0.5)) ** 1.4)))
    tam = 80; linhas = frase_linhas(frase, tam, W - 200); y = H * 0.70
    yf = desenha_frase(d, W, y, linhas, tam, COR["offwhite"] + (255,), COR["caramelo"] + (255,))
    if rotulo:
        d.line([(W/2 - 40, yf + 30), (W/2 + 40, yf + 30)], fill=COR["caramelo"] + (255,), width=2)
        espacado(d, W/2, yf + 100, rotulo.upper(), ImageFont.truetype(str(A/"fonts"/"Poppins-Bold.ttf"), 30), COR["offwhite"] + (255,), 9)
    lg = Image.open(A/"logo"/"medicinal-palavra-off-white.png").convert("RGBA"); lg = lg.resize((170, round(lg.height*170/lg.width)))
    im.alpha_composite(lg, (60, 60)); im.save(saida_png)
if __name__ == "__main__":
    vin, vout, frase, rot = sys.argv[1:5]
    with tempfile.TemporaryDirectory() as td:
        ov = f"{td}/ov.png"; overlay(frase, rot, ov)
        fc = ("[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
              "null[v];"
              "[1:v]format=rgba,fade=t=in:st=0.8:d=0.6:alpha=1[o];[v][o]overlay=0:0")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vin, "-loop", "1", "-i", ov, "-filter_complex", fc,
                        "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-c:a", "aac", "-movflags", "+faststart", vout], check=True)
