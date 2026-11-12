# Compõe a grade de 13 a 30/11/2026: 4 stories/dia (09:00, 12:30, 16:00, 20:00) + 4 feeds/semana (18:00).
# Entrada: ids dos temas decididos na aba Temas (ig_tema). Saída: slots.json (data, hora, canal, tema_id).
import json, datetime as dt
FEED = {"2026-11-13":"T001","2026-11-15":"T011","2026-11-16":"T029","2026-11-18":"T012","2026-11-20":"T047",
        "2026-11-22":"T071","2026-11-23":"T062","2026-11-25":"T042","2026-11-27":"T085","2026-11-29":"T069","2026-11-30":"T110"}
CAL = {"2026-11-14":["T052","T053","T054"],"2026-11-15":["T055","T056"],"2026-11-17":["T044","T045"],"2026-11-18":["T046"],
       "2026-11-19":["T047","T051"],"2026-11-20":["T050"],"2026-11-21":["T049","T061"],"2026-11-24":["T063"],
       "2026-11-25":["T064"],"2026-11-26":["T065"],"2026-11-28":["T067"]}
# filas intercaladas por grupo (magnésio espalhado)
TOPO = ["T003","T013","T023","T031","T004","T036","T040","T014","T009","T027","T016","T005","T037","T019","T028","T032",
        "T007","T041","T015","T030","T008","T043","T020","T033","T022","T039","T017"]
MEIO = ["T072","T083","T085x","T093","T076","T087","T079","T091","T077","T089","T084","T094","T078","T090","T092"]
MEIO = [m for m in MEIO if not m.endswith("x")]
BASE = ["T104","T097","T109","T113","T117","T106","T101","T124","T111","T118","T108","T126","T100"]
HORAS = ["09:00","12:30","16:00","20:00"]
BASE.append("T114")
fila=[]; ti=mi=bi=0
padrao=["T","M","T","B"]; i=0
while ti<len(TOPO) or mi<len(MEIO) or bi<len(BASE):
    p=padrao[i%4]; i+=1
    if p=="T" and ti<len(TOPO): fila.append(TOPO[ti]); ti+=1
    elif p=="M" and mi<len(MEIO): fila.append(MEIO[mi]); mi+=1
    elif p=="B" and bi<len(BASE): fila.append(BASE[bi]); bi+=1
d0 = dt.date(2026,11,13); slots=[]; fi=0
for k in range(18):
    d = (d0+dt.timedelta(k)).isoformat()
    dia = list(CAL.get(d, []))
    while len(dia) < 4: dia.append(fila[fi]); fi+=1
    for h,t in zip(HORAS, dia): slots.append({"data":d,"hora":h,"canal":"story","tema_id":t})
    if d in FEED: slots.append({"data":d,"hora":"18:00","canal":"feed","tema_id":FEED[d]})
json.dump(slots, open("slots.json","w"), ensure_ascii=False, indent=1)
st=[x for x in slots if x["canal"]=="story"]
print(len(st), len(slots)-len(st), "fila usada", fi, "de", len(fila))
ids=[x["tema_id"] for x in st]; print("repetidos", sorted({i for i in ids if ids.count(i)>1}))
