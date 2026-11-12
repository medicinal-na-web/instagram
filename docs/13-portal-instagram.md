# 13 — Instagram no PortalSiteMedicinal

Desde 12/11/2026 a Grade do @medicinalnaweb é aberta pelo **PortalSiteMedicinal**: https://www.portalsite.medicinalnaweb.com.br. Na tela inicial ficam três opções: **Campanhas**, **Novos produtos** e **Instagram**.

```mermaid
flowchart LR
  U[Equipe] -->|login por código no e-mail| P[PortalSiteMedicinal<br/>brasa_loader_sm]
  P -->|opção Instagram| I[App da Grade<br/>brasa_loader_ig em iframe]
  I -->|ig_grade_carregar / ig_post_salvar| DB[(Supabase formulaCerta<br/>ig_post, ig_estrategia, ig_acesso)]
  I -->|textos| IA[Edge Function ig-ia<br/>Claude]
  I -->|imagem e vídeo| RW[Edge Function ig-runway]
  RW --> ST[(Storage ig-grade)]
  N[n8n: Site Medicinal - Grade IG - Publicar (portal)<br/>ativo, a cada 10 min] -->|ig_pub_reservar / concluir / falhar| DB
  N --> IG[Instagram]
```

## Como funciona
- **Mesmo login do portal.** O app da Grade roda dentro de um iframe e usa a sessão do portal (`window.smTokenIG`). Não pede um segundo código. O papel na Grade vem da tabela `ig_acesso`: `admin` e `editor` editam e só o `admin` aprova. O Ricardo é admin.
- **Base de dados:** a migração para o Supabase já tinha sido feita entre 07 e 09/11/2026 por outra conversa (tabelas `ig_*`, 19 posts publicados, estratégia, mídias em `ig-grade/grade/espelho/`).
- **IA de texto** (`ig-ia`, Claude) e **Runway** (`ig-runway`) rodam no servidor e as chaves ficam nos segredos do Supabase. Status em 12/11: as duas chaves estão configuradas.
- **Publicação:** é feita pelo workflow n8n `bj72gS6IgLvoQh7C` (ativo), que a cada 10 min publica 1 bloco Aprovado com data e hora vencidas. Vídeo e reels continuam à mão.

## Publicação de 12/11/2026
- Portal `brasa_loader_sm`: md5 `d246a704…` → `68b68f34da04c86ca8c182b0e3ec1126` (card Instagram, seção `tabInstagram`, funções `igAbre`, `smTokenIG` e `smSairIG`). Backup em `_brasa_parts_sm_bkp_20261112_ig`.
- App `brasa_loader_ig`: md5 `44f3dde6…` → `86328330652f055784070b91cd65d802` (modo embutido `EMBED`). Backup em `_brasa_parts_ig_bkp_20261112_ig`.
- Stage `_sm_stage` ids 21 e 22. A função temporária de stage foi removida.
- Cópias publicadas: `portal/portalsitemedicinal-publicado-20261112.html` e `portal/app-instagram-publicado-20261112.html`.

## Virar post do feed (12/11/2026)
- Em qualquer story criado na Grade (inclusive um já publicado), o editor mostra o botão **✦ Virar post do feed**. Ele não aparece nos stories automáticos "POST NOVO NO FEED".
- Fluxo:
  1. A IA (`ig-ia`, ação `post_completo`, canal feed) recebe o texto do story e escreve título, frase de marca, legenda completa (gancho, 2–3 parágrafos, orientação profissional) e hashtags. A instrução tem até 500 caracteres.
  2. O Runway gera uma foto nova em 4:5. A descrição da foto pede frases afirmativas e o terço superior liso, para a frase.
  3. `arteComFrase` monta a arte 1080×1350 (Playfair, palavra-chave em itálico, logo oficial branco).
  4. O post é salvo como **Rascunho** para amanhã às 18:00. Ao aprovar, a regra cria o story "POST NOVO NO FEED".
- Publicação: `brasa_loader_ig` md5 `86328330…` → `5e4c85b6f5385ddf8af3a023b6fe686f`. Backup em `_brasa_parts_ig_bkp_20261112_vf`; stage `_sm_stage` id 23.
- Primeiro story publicado pelo portal: "Magnésio e o ritual do sono" (12/11, 13:21, n8n).

## O que fica do artefato
- O artefato https://claude.ai/artifact/Ayp1jCcyffTqZth63yXdtX fica como histórico. O trabalho novo é feito no portal.
- A rotina "pedidos de imagem e vídeo (Runway)" (`trig_01BXAxUbfjXqbQ7Le6Ha8tjd`) foi **desativada** em 12/11: o portal chama o Runway direto.
- A rotina "publicação de blocos aprovados" (`trig_01ActqDM3WKFbTmso9xCSwbm`) só lê o artefato. Ela pode ser desativada pelo Ricardo em claude.ai/code → Agendados.

## Aba Temas: triagem da campanha de novembro (12/11/2026)
- Tabela `ig_tema` (RLS, sem acesso direto). Funções `ig_temas_listar()` e `ig_tema_decidir(p_id, p)` (admin/editor). Só o admin marca `revisado`.
- Carga inicial: 132 temas (topo 43, calendário 27, meio 26, base 36), 75 com produto do site e link `https://www.medicinalnaweb.com.br/<link_id>/p`. Fonte: `grade/temas/temas_novembro.py` (gera `temas_novembro.json`).
- Decisões do Ricardo (12/11):
  - link de produto só nos stories (adesivo de link); feed sem produto do site;
  - Black November fica separada, no fluxo de Campanhas;
  - a campanha começa em 13/11;
  - o Ricardo (farmacêutico) faz a revisão.
- Na triagem, cada tema recebe Stories / Feed / Os dois / Descartar, prioridade ★, Usar link / Sem link e "revisado" (para temas com `saude` = `revisao`). Temas `educativo` (medicamento sob prescrição) não mostram link.
- Próximo passo: o compositor monta de 13 a 30/11 (4 stories por dia, 4 posts no feed por semana) com os temas decididos e revisados e grava os blocos em Rascunho na Grade.
- Publicação: `brasa_loader_ig` md5 `5e4c85b6…` → `1b65c4cbd300445d7a9033e5128721bb`. Backup em `_brasa_parts_ig_bkp_20261112_tm`; stage id 24.

## Campanha de novembro na Grade (12/11/2026)
- Composição: `grade/campanha-nov/compoe.py` gera `slots.json` com 72 stories (09:00, 12:30, 16:00 e 20:00) e 11 posts no feed (18:00). Calendário nas datas: 14/11 diabetes, 17–21/11 Novembro Azul e Consciência Negra, 23–28/11 verão, 29–30/11 fim de ano. Nenhum tema se repete.
- Redação: 3 agentes seguindo `BRIEFING.md` → `stories_13a21.json`, `stories_22a30.json` e `feeds.json`.
- Gravação: 83 blocos em `ig_post` com `campanha = 'nov-2026'`, todos em **Rascunho** e sem imagem. 37 stories levam `link_url`.
- Colunas novas em `ig_post`:
  - `link_url`: só stories. `ig_post_salvar` aceita só links do site e recusa link no feed. **`ig_pub_reservar` não publica blocos com link** (a API não coloca adesivo de link): esses stories saem à mão.
  - `campanha`;
  - `frase_arte`: frase da arte do feed.
- App (`brasa_loader_ig` md5 `525733c805f3851c072a417031357f83`, backup `_brasa_parts_ig_bkp_20261112_v4`):
  - **✦ Gerar artes da campanha**, na aba Stories: gera em lote, um bloco por vez, foto no Runway + frase + logo;
  - **✦ Gerar arte** no editor de cada bloco;
  - campo e selo "🔗 à mão" nos stories com link.
- Arte no padrão do doc 09 (ajustada a pedido do Ricardo, "respeitar ao máximo a regra de cor e fonte"):
  - Playfair Display Regular (400), com a palavra-chave em Bold Italic (700), 18% maior;
  - espaçamento de −2,5%, minúscula no início de frase (siglas e nomes ficam como estão);
  - texto branco sobre a foto, escurecimento total entre 10% e 30%;
  - logo oficial branco de 170 px, a 60 px da borda;
  - margem lateral de 90 px.
- Para revisar antes de aprovar:
  - stories de canela (T053), cromo (T055) e berberina (T056) no Dia do Diabetes;
  - Clonapure (T079), com texto neutro;
  - Keranat (T012) no feed;
  - ISO 9001 (T085): confirmar que a Medicinal é certificada;
  - fontes citadas nas legendas (NIH, AAD, ISSN, Endocrine Society, SBD etc.), que vieram da memória do redator e não foram conferidas;
  - CTAs "Comente PALAVRA", que prometem enviar um material que ainda precisa existir.

## Três formatos na grade (12/11/2026)
1. **Posts padrão**: artes estáticas nos modelos A (foto), E (marinho), F (off-white) e C (pergunta); compositores `grade/campanha-nov/arte.py` e `modelos.py`.
2. **Ativos animados**: 2 por semana. Vídeo de 5 s gerado no Runway (seedance-2.5, 9:16, cerca de 150 créditos) com frase, rótulo e logo; compositor `grade/ativos-animados/ativo_animado.py`; lista em `grade/ativos-animados/LISTA.md`. Conceitos sem efeito no corpo: Morosil → laranja moro; Elibria → brasa suave. Logo de marca de terceiro só com autorização do detentor.
3. **Pódio da manipulação**: nos fins de semana. No sábado, o vídeo animado (`grade/podio/podio_video.py`); no domingo, o campeão com link. Dados do workflow `Fw0EFRJ9uwxCyaOF` (réplica, agregado, 90 dias), nota proporcional (1º = 10,0), sem fármacos.
- Vídeos ficam em `ig-grade/grade/video/`, enviados pelo workflow novo `Site Medicinal - Grade IG - URL de upload de vídeo (inativo)` (`7msLgE4lhBLmvTCd`). O bucket `sitemedicinal-banners` só aceita imagem de até 2 MB.
- Vídeo é publicado à mão (a publicação automática só faz imagem).
- Grade: pódios em 14, 21 e 28/11 às 11:00; campeões com link em 15, 22 e 29/11 às 11:00; ativo animado do magnésio treonato em 17/11 às 11:00. Esses blocos são extras: o dia fica com 5 stories.

## Link por direct (ManyChat) · 12/11/2026

A API do Instagram não coloca adesivo de link no story, e o app da Meta (APP_clienteDM) só tem acesso padrão a `instagram_business_manage_messages`. Por isso o link vai por **direct via ManyChat**.

```mermaid
flowchart LR
  S[Story aprovado<br/>"responda CAFÉ e receba o link"] --> R[Pessoa responde o story]
  R --> M[ManyChat: gatilho Story Reply]
  M -->|POST rpc/ig_link_por_palavra| DB[(Supabase ig_post<br/>palavra_chave + link_dm)]
  DB -->|encontrado + link| M
  M -->|direct com botão Ver no site| R
```

- **Palavra-chave sem acento nem caractere especial** (pedido do Ricardo, 12/11): CAFE, MAGNESIO, COLAGENO, SALMAO, PROPOLIS, HIALURONICO. A função também aceita com acento.
- **Banco:** colunas `palavra_chave` e `link_dm` em `ig_post`. A função `ig_link_por_palavra(p_texto)` ignora acento e caixa e só devolve link de bloco **aprovado ou publicado**. Resposta: `{encontrado, palavra, link, produto}`. Não grava nada da pessoa (LGPD).
- **ManyChat:** automação "Site Medicinal - Link por palavra (story)". Gatilho Story Reply, External Request (POST com a chave pública anon do portal, corpo `{"p_texto": "{{last_input_text}}"}`), campos `link_produto` e `link_ok`, condição `link_ok = true` → direct com o link. Sem palavra conhecida, não responde (a equipe atende).
- Configuração feita pelo Claude no navegador do Ricardo, a partir do roteiro preparado nesta conversa (o roteiro tem a chave pública e fica fora do repositório). Automação criada pausada; o Ricardo liga depois do teste.
- **Story sem logo** (12/11): o cabeçalho do Instagram já mostra @medicinalnaweb. `arte.py`, `modelos.py`, `ativo_animado.py` e `podio_video.py` só põem logo no feed.
- **Link sempre na página do produto, com UTM** (decisão do Ricardo, 12/11): o direct leva à página do produto, para a pessoa ler o contexto do item. Desde 12/11, `ig_link_por_palavra` devolve o link com `utm_source=instagram&utm_medium=dm&utm_campaign=story-AAAA-MM&utm_content=<palavra>`. Isso mede as vendas por story e permite, no futuro, uma promoção na VTEX restrita a essa UTM (fluxo de Campanhas, criada pausada, só com OK do Ricardo). Como o desconto da VTEX aparece no carrinho, o direct precisará avisar isso quando houver promoção.
