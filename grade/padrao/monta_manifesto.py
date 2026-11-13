"""Monta o manifesto de recomposição (stories 14-30/11 e feeds) no padrão oficial.
Cada item: data, hora, canal, frase, rotulo|mono, foto (caminho local) ou foto_pedido (prompt Runway, tons naturais, sem filtro).
Saída: manifesto.json. Dias de formato próprio (19 e 26 = produto só; 25 = Dermo-day) ficam de fora (têm geradores próprios)."""
import json
from pathlib import Path
G = Path(__file__).resolve().parent.parent; S = "/tmp/claude-0/-home-user/41e0b6ad-ad94-5c50-8f1c-d050b9313448/scratchpad"
A = json.load(open(G/"campanha-nov/stories_14a30_v2.json"))
# produto do dia (palavra-chave) por data/hora, conforme o banco em 13/11
PD = {("2026-11-15","11:00"):"CANELA",("2026-11-16","12:30"):"MAGNESIO",("2026-11-17","16:00"):"VITC",("2026-11-18","09:00"):"SAW",
      ("2026-11-20","09:00"):"LICOPENO",("2026-11-22","12:30"):"SALMAO",("2026-11-23","09:00"):"TEANINA",("2026-11-24","12:30"):"FERRO",
      ("2026-11-27","20:00"):"ALCA",("2026-11-29","09:00"):"UNHAS",("2026-11-30","09:00"):"PASSI"}
TROCA = {("2026-11-14","12:30"):("2026-11-15","11:00"),("2026-11-21","12:30"):("2026-11-22","11:00"),("2026-11-28","12:30"):("2026-11-29","11:00")}
FOTO = {"2026-11-14 12:30": f"{S}/fotos1420/canela.png", "2026-11-15 09:00": f"{S}/fotos1420/cromo.png", "2026-11-16 12:30": f"{S}/fotos1420/caibra.png",
        "2026-11-17 16:00": f"{S}/fotos1420/vitc.png", "2026-11-18 12:30": f"{S}/fotos1420/hibisco.png", "2026-11-20 09:00": f"{S}/fotos1420/licopeno.png",
        }
CENAS = json.load(open(Path(__file__).parent/"cenas.json"))
ESTILO = (" Fotografia realista de celular de boa qualidade, luz natural de janela, cores naturais (sem dourado exagerado, sem filtro),"
          " fundo neutro claro, um assunto só, bastante espaço vazio no meio da imagem para texto. Sem pessoas de rosto, sem texto, sem logo, sem embalagem.")
out = []
for a in A:
    d, h = a["data"], a["hora"]
    if d in ("2026-11-19", "2026-11-25", "2026-11-26"): continue
    d2, h2 = TROCA.get((d, h), (d, h)); chave = PD.get((d2, h2), "")
    pergunta = (a.get("pergunta") or "").strip(); frase = (pergunta + " " + a["legenda"]).strip() if pergunta else a["legenda"]
    it = {"data": d2, "hora": h2, "canal": "story", "frase": frase, "tema": a.get("tema_id", "")}
    if chave: it["mono"] = f"responda {chave} e receba o link"
    elif a.get("rotulo"): it["rotulo"] = a["rotulo"]
    f = FOTO.get(f"{d} {h}")
    if f: it["foto"] = f
    else:
        base = CENAS.get(a.get("tema_id", "")) or (a.get("prompt_imagem") or "").split(" Paleta")[0].split(" Manhã")[0].split(" Noite")[0]
        it["foto_pedido"] = base + ESTILO
    out.append(it)
FEEDS = json.load(open(G/"campanha-nov/feeds.json"))
for f in FEEDS:
    if f["data"] in ("2026-11-13",): continue
    out.append({"data": f["data"], "hora": "18:00", "canal": "feed", "frase": f.get("frase_arte") or f["titulo"],
                "foto_pedido": (f.get("prompt_imagem") or f["titulo"]).split(" B")[0] + ESTILO})
json.dump(out, open(Path(__file__).parent/"manifesto.json", "w"), ensure_ascii=False, indent=1)
print(len(out), "itens;", sum(1 for i in out if "foto" in i), "com foto;", sum(1 for i in out if "foto_pedido" in i), "aguardando foto")
