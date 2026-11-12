"""Re-renderiza os stories do pacote 13–20/11 (story sem logo, decisão de 12/11/2026).
Uso: python3 -I render.py <pasta_scratch_com_fotos1420_e_videos_runway>"""
import json, shutil, subprocess, sys
from pathlib import Path
S = sys.argv[1]; G = Path(__file__).resolve().parents[2]; P = Path(__file__).resolve().parent
CN, AA, PD = G/"campanha-nov", G/"ativos-animados", G/"podio"
run = lambda *a: subprocess.run(["python3", "-I", *map(str, a)], check=True, cwd=CN)
c = lambda k: f"responda {k} e receba o link"
D13 = CN/"dia13"; F = f"{S}/fotos1420"
A = {(a["data"], a["hora"]): a for a in json.load(open(CN/"stories_14a30_v2.json"))}
nome = lambda d, h, t: P/f"{d[8:]}-11_{h.replace(':', 'h')}_{t}.jpg"
run("arte.py", D13/"fotos/s1230v2.png", "story", P/"13-11_12h30_cafe-proteico.jpg", "seu café da tarde pode virar *lanche*.", "", c("CAFE"))
run("modelos.py", "C", "story", P/"13-11_16h00_biotina.jpg", "depende do *motivo* da queda.", "BIOTINA", "biotina segura a queda de cabelo?", c("BIOTINA"))
run("arte.py", D13/"fotos/s2000v2.png", "story", P/"13-11_20h00_psyllium.jpg", "fibra sem *água* não funciona.", "", c("FIBRA"))
run("modelos.py", "E", "story", D13/"13-0900-story-E-magnesio-treonato.jpg", "nem todo magnésio chega ao *cérebro*.", "MAGNÉSIO TREONATO")
for (d, h), (t, f, y, k) in {("2026-11-14", "12:30"): ("canela", "canela", "", "CANELA"), ("2026-11-15", "09:00"): ("cromo", "cromo", "", "CROMO"),
        ("2026-11-16", "12:30"): ("caibra-magnesio", "caibra", "", "MAGNESIO"), ("2026-11-18", "12:30"): ("hibisco", "hibisco", "0.70", "HIBISCO"),
        ("2026-11-19", "12:30"): ("maca", "maca", "", "MACA"), ("2026-11-20", "09:00"): ("licopeno", "licopeno", "", "LICOPENO")}.items():
    run("arte.py", f"{F}/{f}.png", "story", nome(d, h, t), A[(d, h)]["legenda"], y, c(k))
run("modelos.py", "F", "story", P/"17-11_16h00_vitamina-c.jpg", "vitamina C: mais nem sempre é *melhor*.", "VITAMINA C", "", c("ACEROLA"))
for d, h, t, k in [("2026-11-15", "12:30", "berberina", "BERBERINA"), ("2026-11-15", "16:00", "probioticos", "PROBIOTICO"), ("2026-11-16", "16:00", "colageno", "COLAGENO"),
                   ("2026-11-18", "09:00", "saw-palmetto", "PALMETTO"), ("2026-11-18", "16:00", "zinco-cabelo", "ZINCO"), ("2026-11-20", "12:30", "kic", "KIC"), ("2026-11-20", "16:00", "vitamina-b12", "B12")]:
    a = A[(d, h)]; run("modelos.py", a["modelo"], "story", nome(d, h, t), a["legenda"], a.get("rotulo", ""), "", c(k))
run("modelos.py", "F", "story", P/"15-11_11h00_campea-podio-b12.jpg", "a campeã do pódio tem nome: vitamina *B12*.", "PÓDIO · NUTRACÊUTICOS", "", c("B12"))
for v, saida, fr, rot, k in [("morosil2", "morosil", "a laranja que *sangra* vermelho tem nome: moro.", "MOROSIL", "MOROSIL"),
                             ("elibria-runway", "elibria", "o *calor* que começa por dentro.", "ELIBRIA", ""),
                             ("treonato-runway", "magnesio-treonato", "o magnésio que chega ao *cérebro*.", "MAGNÉSIO TREONATO", "")]:
    run(AA/"ativo_animado.py", f"{S}/{v}.mp4", AA/f"ativo-animado-{saida}.mp4", fr, rot, c(k) if k else "")
shutil.copy(AA/"ativo-animado-morosil.mp4", P/"19-11_11h00_ativo-animado-morosil.mp4")
for s, cat, n, q in [("podio-nutraceuticos", "Nutracêuticos", ["vitamina B12", "vitamina D3", "metilfolato"], ["10,0", "9,5", "7,4"]),
                     ("podio-cabelo", "Cabelo", ["biotina", "cistina e cisteína", "auxina tricógena"], ["10,0", "3,1", "1,8"]),
                     ("podio-pele-beleza", "Pele e beleza", ["niacinamida", "Clonapure", "ácido hialurônico"], ["10,0", "6,4", "5,5"])]:
    subprocess.run(["python3", "-I", "podio_video.py", f"{s}.mp4", cat, *n, *q], check=True, cwd=PD)
shutil.copy(PD/"podio-nutraceuticos.mp4", P/"14-11_11h00_podio-nutraceuticos.mp4")
print("ok")
