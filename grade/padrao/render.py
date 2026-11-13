"""Renderiza o manifesto no padrão oficial. Itens sem foto ficam listados em pendentes.txt (aguardando Runway)."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import padrao
M = json.load(open(Path(__file__).parent/"manifesto.json")); out = Path(__file__).parent.parent/"pacotes/padrao-oficial"; out.mkdir(parents=True, exist_ok=True)
feito, pend, ult = [], [], None
for m in sorted(M, key=lambda x: (x["data"], x["hora"])):
    nome = f'{m["data"][8:]}-11_{m["hora"].replace(":","h")}_{m["canal"]}.jpg'
    if not m.get("foto"): pend.append(f'{m["data"]} {m["hora"]} {m["canal"]}: {m["foto_pedido"][:90]}'); continue
    pos = padrao.arte(m["canal"], m["foto"], str(out/nome), m["frase"], m.get("rotulo",""), m.get("mono",""), m.get("y"), m.get("ancora",0.5), evitar_logo=ult)
    if m["canal"] == "feed": ult = pos
    feito.append(nome)
(out/"pendentes.txt").write_text("\n".join(pend)); print(len(feito), "renderizados;", len(pend), "pendentes de foto")
