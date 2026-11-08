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
- [`grade/`](grade/): código da grade (`grade-instagram.html`) e os geradores das artes (`semana-2026-11-09/`: `gera.py` v1 por produto, `gera2.py` v2 azul-marinho com fotos).

## Regras que valem sempre

1. **Nada vai ao ar sem OK explícito** do Ricardo. Campanha e anúncio nascem pausados.
2. **Sem segredos no repositório**: tokens e chaves ficam nas credenciais do n8n.
3. **LGPD**: sem dados de clientes, sem comentários ou directs de pessoas nos workflows.
4. **Sem alegação de cura ou efeito**, sem antes e depois, sem medicamento sob prescrição como oferta. Suplementos e manipulados com revisão farmacêutica antes de aprovar.
5. Os nomes dos workflows no n8n começam com `Site Medicinal - `.
