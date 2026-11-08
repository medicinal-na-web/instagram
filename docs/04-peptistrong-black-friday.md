# 04 — Peptistrong diário e regras de copy (Black Friday 2026)

Trazido do plano integrado da campanha no repositório `site-medicinalnaweb` (`docs/campanha/plano-black-friday.md`, branch `claude/lucid-lovelace-ikusv2`, commit `f610eeb` de 03/11/2026). Aqui ficam só as partes do Instagram. O plano completo (site, e-mail, UTMs, calendário geral) continua lá.

**Rascunho para aprovação**: nada aqui foi publicado, agendado ou enviado.

## Padrões da campanha que valem para o Instagram

- **Conceito e assinatura** iguais em banner, e-mail e story (mesmo título, mesma cor, mesmo selo de data).
- **UTM padrão**: `utm_campaign=bf2026`, `utm_source` = `site` | `email` | `instagram`, `utm_content` = id da peça (ex.: `em03`, `st-1118`, `pep-d12`).
- **Cupom por canal** (ex.: `BFEMAIL`, `BFINSTA`), se o comercial aprovar, para separar a venda de cada canal no ROAS.
- **Mesmo calendário** para entrada e saída: o banner sai do ar no mesmo dia em que o e-mail e o story dizem que acabou. Isso evita o problema do banner vencido (`docs/06-validacao-troca-banner.md` no repositório `site-medicinalnaweb`).

| Fase | Datas | Stories |
|---|---|---|
| Aquecimento | 03/11 – 15/11 | só Peptistrong diário |
| Esquenta | 16/11 – 26/11 | contagem regressiva diária |
| Black Friday | 27/11 – 30/11 | oferta do dia, últimas horas |
| Saída | 01/12 | agradecimento |

## 1. Peptistrong diário no Instagram

Uma postagem de feed por dia e ao menos um story por dia, de 02/11 a 30/11. Pilares fixos por dia da semana, para facilitar produção em lote:

| Dia | Pilar | Formato |
|---|---|---|
| Seg | **Ciência simples**: o que são peptídeos bioativos, de onde vem (fava), dose de 2,4 g | carrossel |
| Ter | **Receita**: shake, mingau, smoothie com Chocolate Belga ou Piña Colada | reels |
| Qua | **Para quem é**: treino, 40+, rotina corrida, volta aos treinos | carrossel |
| Qui | **Mito ou verdade** sobre proteína e músculo | carrossel / enquete no story |
| Sex | **Bastidores**: manipulação, qualidade, equipe farmacêutica | reels |
| Sáb | **Rotina**: como encaixar o Peptistrong no dia | foto / reels |
| Dom | **Pergunte ao farmacêutico**: caixa de perguntas, respostas na segunda | story |

Pauta das 4 semanas:

| Semana | Seg | Ter | Qua | Qui | Sex | Sáb | Dom |
|---|---|---|---|---|---|---|---|
| 02–08/11 | O que é Peptistrong | Shake de Chocolate Belga | Para quem treina | "Só whey constrói músculo?" | Como é feito | Antes ou depois do treino? | Caixa de perguntas |
| 09–15/11 | Fava: proteína vegetal | Smoothie Piña Colada | Músculo depois dos 40 | "Proteína engorda?" | Controle de qualidade | Rotina de quem trabalha cedo | Respostas |
| 16–22/11 | Dose de 2,4 g: por que tão pouco | Mingau proteico | Volta aos treinos | "Vegetal é fraco?" | Equipe farmacêutica | Peptistrong na viagem | Caixa de perguntas |
| 23–29/11 | Resumo: 4 semanas de ciência | Receita da Black Friday | Presente para quem treina | "Vale a pena estocar?" | **Black Friday**: oferta | **Black Friday**: últimas unidades/sabores | **Black Friday**: último dia amanhã |
| 30/11 | Cyber Monday: últimas horas | | | | | | |

Produção e publicação:

- **Lote semanal**: as 7 artes e legendas da semana ficam prontas e aprovadas até a quinta anterior.
- **Templates fixos** no Canva (feed 1080×1350, story 1080×1920) com a identidade da campanha. A partir de 23/11 o selo da Black Friday entra nas peças do Peptistrong.
- **Publicação**: feed e reels podem ser agendados pela API do Instagram (n8n) ou pelo Meta Business Suite. Story com **link, enquete, caixa de perguntas ou contagem regressiva** é manual: a API não suporta esses recursos.

## 2. Regulatório: o que a copy do Peptistrong não pode dizer

A descrição atual do produto no site usa números e indicações do fabricante do ingrediente. Em publicidade de suplemento (ANVISA, CONAR e política da Meta), alguns deles são arriscados. **Validar com o farmacêutico/regulatório antes da primeira postagem.**

| Evitar na campanha | Motivo | Alternativa |
|---|---|---|
| "Previne sarcopenia", "para pacientes acamados, bariátricos, pós-cirúrgicos" | Alegação terapêutica / público clínico | "Contribui para a rotina de quem cuida da massa muscular", com orientação profissional |
| "400% mais síntese proteica", "4x mais potente que whey" | Comparativo com dado de estudo do fornecedor, sem contexto | Citar o estudo com fonte, se o regulatório liberar; senão, "ingrediente com estudos clínicos" |
| "Reduz inflamação em 60%" | Alegação de efeito fisiológico | Não usar |
| Antes e depois, corpo "transformado" | Política da Meta e CONAR | Rotina, receita, bastidores |

Depoimentos de clientes só com **autorização por escrito** e sem dado de saúde (LGPD).

Achado de passagem: o nome do sabor está como **"Pinã Colada"** no cadastro da VTEX (SKU 50004); o correto é "Piña Colada".

## 3. Workflow previsto no n8n

| Workflow | O que faz | Depende de |
|---|---|---|
| `Site Medicinal - Instagram: Peptistrong diário (inativo)` | Agenda feed e reels aprovados pela API do Instagram | Conta Business + app da Meta |

Ainda não criado. Hoje a publicação da grade passa pelos workflows `Grade IG - Publicar` e pela rotina `grade-publicacao` (ver `03-grade-instagram.md`).
