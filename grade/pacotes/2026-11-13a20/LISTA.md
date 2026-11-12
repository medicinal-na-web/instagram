# Pacote 13 a 20/11/2026 · stories com palavra-chave (ManyChat)

**Mudou em 12/11/2026:** não há mais adesivo de link nem agendamento à mão no Business Suite para as imagens.
- A arte pede "responda PALAVRA e receba o link". Quem responde o story recebe o link por direct pelo **ManyChat**, que consulta `ig_link_por_palavra` no Supabase (só responde para blocos aprovados ou publicados).
- **Palavra-chave sempre sem acento nem caractere especial** (ex.: CAFE, MAGNESIO), para facilitar a digitação. A busca também aceita com acento.
- **Story sem logo** (decisão do Ricardo, 12/11): o Instagram já mostra a foto e @medicinalnaweb no topo. Feed continua com logo. Texto acima da barra de resposta.
- **Imagens** saem pela automação da Grade quando o Ricardo aprova o bloco. **Vídeos** ainda são agendados à mão (a automação publica só imagem).
- Artes e vídeos: arquivos desta pasta (prefixo `nov2026-v4-` no Supabase). Para refazer: `python3 -I render.py <pasta com fotos1420 e vídeos do Runway>`.
- Configuração do ManyChat: `docs/13-portal-instagram.md`, seção "Link por direct (ManyChat)".

| Data | Hora | Tipo | Story | Palavra-chave |
|---|---|---|---|---|
| 13/11 | 09:00 | imagem | Magnésio treonato | TREONATO ⛔ em espera (Anvisa) |
| 13/11 | 12:30 | imagem | Café proteico | CAFE ✅ aprovado |
| 13/11 | 16:00 | imagem | Biotina | BIOTINA |
| 13/11 | 20:00 | imagem | Psyllium | FIBRA |
| 14/11 | 11:00 | vídeo | Pódio · nutracêuticos | — |
| 14/11 | 12:30 | imagem | Canela | CANELA |
| 15/11 | 09:00 | imagem | Picolinato de cromo | CROMO |
| 15/11 | 11:00 | imagem | Campeã do pódio · B12 | B12 |
| 15/11 | 12:30 | imagem | Berberina | BERBERINA |
| 15/11 | 16:00 | imagem | Probióticos por cepa | PROBIOTICO |
| 16/11 | 12:30 | imagem | Cãibra e magnésio | MAGNESIO |
| 16/11 | 16:00 | imagem | Colágeno tipo II | COLAGENO |
| 17/11 | 11:00 | vídeo | Ativo animado · treonato | ⛔ em espera (Anvisa) |
| 17/11 | 16:00 | imagem | Vitamina C (modelo F) | ACEROLA |
| 18/11 | 09:00 | imagem | Saw palmetto | PALMETTO |
| 18/11 | 12:30 | imagem | Hibisco gelado | HIBISCO |
| 18/11 | 16:00 | imagem | Zinco e cabelo | ZINCO |
| 19/11 | 11:00 | vídeo | Ativo animado · Morosil | MOROSIL |
| 19/11 | 12:30 | imagem | Maca peruana | MACA |
| 20/11 | 09:00 | imagem | Licopeno | LICOPENO |
| 20/11 | 12:30 | imagem | KIC | KIC |
| 20/11 | 16:00 | imagem | Vitamina B12 | B12 |

`painel-pacote.jpg`: folha de contato com as faixas de área segura em vermelho.
