# Instagram @medicinalnaweb

Projeto do Instagram da Medicinal (Maringá/PR): grade de conteúdo, artes, acessos à Meta e rotinas de publicação. Separado do site (`site-medicinalnaweb`), que trata de VTEX, FastStore e portais.

## Conteúdo

- [`CONTEXTO.md`](CONTEXTO.md): **leia primeiro**. Estado atual, IDs e próximos passos.
- [`docs/01-acesso-instagram.md`](docs/01-acesso-instagram.md): API do Instagram com login do Instagram (publicação, cota, insights). Validado.
- [`docs/02-meta-ads-api.md`](docs/02-meta-ads-api.md): API de Marketing da Meta (campanhas, impulsionamento e dark posts). Acesso validado.
- [`docs/03-grade-instagram.md`](docs/03-grade-instagram.md): a Grade @medicinalnaweb, regras de publicação e a semana 09–15/11.
- [`docs/04-peptistrong-black-friday.md`](docs/04-peptistrong-black-friday.md): Peptistrong diário (pauta de 02 a 30/11), padrões da Black Friday e o que a copy não pode dizer.
- [`docs/05-historico.md`](docs/05-historico.md): linha do tempo do chat do Instagram (22/10 a 08/11) e de onde veio cada arquivo.
- [`docs/06-fase-2024.md`](docs/06-fase-2024.md): o que fazia os posts de 2024 funcionarem e o que não copiar.
- [`docs/07-fase-2025.md`](docs/07-fase-2025.md): 2025 e a comparação com 2024.
- [`docs/08-feed-2026.md`](docs/08-feed-2026.md): o feed de 2026, as fases do ano e o diagnóstico.
- [`docs/09-padrao-visual.md`](docs/09-padrao-visual.md): **padrão visual e de conteúdo do feed** (paleta, fontes, modelos, séries, legenda, checklist). Rascunho para aprovação.
- [`docs/10-insercao-de-produto.md`](docs/10-insercao-de-produto.md): **procedimento obrigatório** para colocar embalagem real em cena de IA (medidas, fotos, cena sob medida, verificações automáticas).
- [`docs/11-ferramentas-imagem-video.md`](docs/11-ferramentas-imagem-video.md): avaliação das ferramentas de imagem e vídeo e plano de teste.
- [`docs/12-fontes-e-temas.md`](docs/12-fontes-e-temas.md): **fontes de informação e temas para conteúdo** (documento vivo, atualizar sempre).
- [`grade/`](grade/): código da grade (`grade-instagram.html`) e os geradores das artes (`semana-2026-11-09/`: `gera.py` v1 por produto, `gera2.py` v2 azul-marinho com fotos).

## Regras que valem sempre

1. **Nada vai ao ar sem OK explícito** do Ricardo. Campanha e anúncio nascem pausados.
2. **Sem segredos no repositório**: tokens e chaves ficam nas credenciais do n8n.
3. **LGPD**: sem dados de clientes, sem comentários ou directs de pessoas nos workflows.
4. **Sem alegação de cura ou efeito**, sem antes e depois, sem medicamento sob prescrição como oferta. Suplementos e manipulados com revisão farmacêutica antes de aprovar.
5. Os nomes dos workflows no n8n começam com `Site Medicinal - `.
