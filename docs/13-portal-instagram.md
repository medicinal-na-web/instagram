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
- **1 produto com link por dia** (Ricardo, 12/11): só o story do produto do dia tem palavra-chave e chamada; os demais saem como conteúdo. **Pódio sempre no sábado** (vídeo 11:00 + campeã com link 12:30). **Palavras breves** (CAFE, VITC, SAW, ALCA, HIALU, PASSI). Tabela em `grade/pacotes/2026-11-13a20/LISTA.md`.

## Aprovar × Publicar agora (12/11/2026)
- Pedido do Ricardo: o antigo "Aprovar e publicar agora" trocava a data e a hora do bloco para o momento do clique e ignorava o agendamento.
- Agora há dois botões (só admin):
  - **Aprovar (no horário agendado):** mantém data e hora. Recusa horário que já passou.
  - **Publicar agora:** pede confirmação ("sem esperar o horário agendado"). Depois aprova com a data e a hora do clique, e o bloco sai na próxima rodada (até 10 min).
- Os dois exigem o checklist "Antes de aprovar".
- Incidente que motivou: em 12/11 às 18:33, o story do treonato (em espera por causa da Anvisa) foi aprovado pelo botão antigo com a data de hoje. O Claude voltou o bloco para Rascunho em 13/11 09:00 antes da rodada de publicação.
- `brasa_loader_ig` md5 `525733c8…` → `9ae3956ed5a0fd8f3dc55b875287f027`; backup em `_brasa_parts_ig_bkp_20261112_v5`; stage id 26.

## Temas de dermocosméticos (12/11/2026)
- Pedido do Ricardo: faltavam temas de dermocosméticos. Grupo novo **Topo · Dermocosméticos**, T133 a T150 (18 temas), na aba Temas para triagem.
- Assuntos: niacinamida, vitamina C tópica, hialurônico tópico × oral, protetor com cor, reaplicação, retinol × tretinoína (educativo), manchas, ceramidas, ureia, pantenol, bakuchiol, peptídeos, ordem dos produtos, ácidos e sol, antioxidante + protetor, sérum sob medida, pele oleosa, protetor labial.
- O site não tem dermocosmético tópico à venda (busca de 12/11). Por isso os temas não têm link: são conteúdo ou chamada para a manipulação.

## Formatos de dia (Ricardo, 12/11/2026)
- **Dia de um produto só:** o dia tem apenas 2 stories sobre o mesmo produto.
  - 11:00: vídeo "ativo animado", sem chamada.
  - 12:30: story com a foto real do produto (packshot do site) e a chamada "responda PALAVRA e receba o link".
  - Gerador: `grade/campanha-nov/produto_story.py`. Ele multiplica o packshot de fundo branco sobre a cor da marca, sem recorte, e assim a sombra original fica natural.
  - Datas: **19/11 Morosil** e **26/11 Keranat** (`keranat-150mg-60caps`).
  - Os stories que ocupavam esses dias viraram **Ideia** em 01/12 e 02/12.
- **Dia Dermo (quarta-feira, um por semana):**
  - Escolhe-se um dermocosmético comercial em alta e explora-se o ativo destaque dele. O fechamento diz que esse ativo pode entrar no cosmético manipulado.
  - O dia tem só essa sequência de 4 stories: gancho, ativo, cuidados e chamada.
  - Simulação em **25/11**: o "retinal shot" coreano, em 4 stories (12:30, 12:40, 12:50, 13:00):
    1. Gancho, com foto de ampola sem marca (Runway): "todo mundo quer o *retinal shot* coreano. o que tem dentro?"
    2. O ativo (modelo E): "*retinal*: uma forma de vitamina A, um passo mais perto da forma ativa do que o retinol."
    3. Cuidados (modelo C): "retinal é para qualquer um? à noite, com protetor de dia. gestante e lactante *não* usam."
    4. Chamada, com foto da bancada de manipulação (Runway, frasco âmbar com rótulo em branco): "agora no *seu* manipulado.", com "responda DERMO e monte o seu".
  - Sem marca nem embalagem de terceiros na arte.
  - O site não tem o produto. A palavra DERMO não tem link: quem responde é atendido pela equipe no direct.
  - Revisão farmacêutica obrigatória, porque retinal é retinoide e há a questão da concentração e da regra de cosmético.
  - Os stories que ocupavam 25/11 viraram Ideia em 03/12.
  - Arquivos em `grade/pacotes/dia-dermo/`.
- Story 1 do Dia Dermo (pedido do Ricardo, 12/11): **foto do produto de referência em destaque, ofuscada**.
  - É a foto de loja do produto: desfoque leve no todo e desfoque forte na marca. O fundo cinza vira a cor da marca.
  - Gerador: `grade/campanha-nov/referencia_story.py`.
  - A foto de terceiro não vai para o repositório (`.gitignore`) e fica só na pasta local e no Storage.

## Automação DERMO no ManyChat (Dermo-day, 13/11/2026)
- **Banco:**
  - tabela `ig_dermo` com o ativo da semana: data, ativo, referência, resumo, cuidados, `gestante_ok`, texturas e `aprovado`. Tem RLS e não guarda dados de clientes;
  - RPC `ig_dermo_atual()`, que o anon pode chamar. Ela devolve o Dermo-day aprovado mais recente dos últimos 7 dias; sem nenhum, devolve `{"encontrado": false}`;
  - carga de 25/11: retinal, `gestante_ok=false`, `aprovado=false`. Fica aprovado quando o Ricardo aprovar o Dermo-day.
- **Fluxo no ManyChat** (automação "Site Medicinal - Dermo-day (DERMO)", criada pausada pelo Claude no navegador, com roteiro fora do repo):
  - Disparo: a palavra DERMO, em resposta ao story ou no direct.
  - Depois do disparo: busca do ativo da semana e boas-vindas personalizadas.
  - 4 perguntas com botões: tipo de pele, objetivo, uso atual de ácido ou retinoide, gestante ou amamentando.
  - Gestante ou amamentando, com ativo contraindicado: mensagem de alternativa segura, sem a pergunta de textura.
  - Senão: pergunta de textura.
  - Fechamento: os cuidados do ativo, a tag `dermo-lead` e a passagem para atendimento humano, que manda a fórmula e o orçamento.
- **LGPD:** as respostas da pessoa ficam só no ManyChat e no atendimento. Nada volta para o Supabase, o n8n ou o repositório.

## Dermo-day na linguagem visual de 2025 (13/11/2026)
- Pedido do Ricardo:
  - "ainda com cara de IA, compare com 2025";
  - nunca citar "farmacêutica" nas chamadas;
  - chamada no tom de "comente DERMO e conheça o retinal feito para você".
- Diferenças achadas na comparação com a grade de 2025 (68 posts em `scratchpad/g25`):
  1. Em 2025, **toda arte é foto**: produto real, mão, textura. Não havia fundo de cor chapada. Os modelos E, F e C em fundo sólido eram o que dava cara de molde.
  2. **Tons apagados:** taupe, cinza quente, café com leite, com pouca saturação. As fotos do Runway saíam douradas e saturadas.
  3. **Palavra-chave em Playfair Bold Italic branca, bem maior e numa linha só dela** ("*Resultado*", "*médico…*"), não em caramelo.
  4. Rótulo em Poppins espaçado ou linha mono sublinhada, sempre branco sobre foto.
- Carrossel refeito (`grade/dermo/carrossel.py`):
  - todas as lâminas com foto, tratadas com `apagado()`;
  - linhas da frase separadas por `|`, e a linha-chave sai 1,75× maior;
  - duas fontes por lâmina;
  - logo branco pequeno.
- Fotos: 3 são da própria Medicinal em 2025 (textura de sérum, creme na pele, topo do frasco), a do produto de referência é ofuscada e a da bancada vem do Runway.

## Fluxo do ManyChat por Dermo-day (13/11/2026)
- Pedido do Ricardo: um fluxo de atendimento bem elaborado **para cada Dermo-day**.
- **Fonte:** `grade/dermo/fluxos/<data>-<ativo>.json` guarda os textos, perguntas, botões, avisos de contraindicação e tags do ativo da semana.
- **Roteiro:** `python3 -I grade/dermo/fluxo_manychat.py <json>` gera o texto para o Claude no navegador criar a automação "Site Medicinal - Dermo-day <data> (<ativo>)".
- **Gatilho:** DERMO em resposta ao story, comentário no carrossel (resposta pública "Te chamei no direct ✨") ou direct.
- **Caminhos do fluxo:**
  - completo: 6 perguntas (uso de retinoide, pele, objetivo, gestação, textura, rotina), depois um resumo personalizado, "Quer receber a sugestão com o orçamento?" e atendimento humano;
  - preço: explica que o valor depende da fórmula e segue para as perguntas;
  - receita médica: oferece manipular a receita e pede a foto dela;
  - gestante, amamentando ou tentando engravidar: diz que o ativo não é indicado e oferece alternativa segura.
- **Complementos:** lembrete único depois de 23 h, aviso fora do horário e tags (`dermo-lead`, `dermo-<data>`, `dermo-<ativo>`).
- **Ativação:** cada fluxo fica ligado da quarta até a terça seguinte, e o da semana anterior é pausado. Todo fluxo é criado pausado.
- **Regras:** nunca citar "farmacêutica"; as respostas ficam só no ManyChat (LGPD).
- O fluxo genérico anterior (`ig_dermo_atual`) fica como reserva.

## Correção do link por direct (13/11/2026)
- **Sintoma:** o story do café saiu às 12:31, mas quem respondeu "CAFE" não recebeu nada.
- **O que os logs mostram:** o ManyChat chamou `ig_link_por_palavra` às 13:21 e 13:22 e recebeu HTTP 200. A falha é do lado do ManyChat: ou a variável do texto chegou vazia, ou houve problema no mapeamento da resposta ou na condição.
- **Ajustes no banco:**
  - texto vazio ou variável não preenchida (`{{...}}`) recebe o produto do dia publicado nas últimas 24 h; texto sem palavra conhecida continua sem resposta;
  - a resposta passou a trazer `ok` ("sim" ou "nao", em texto) e `mensagem` (frase pronta com o link), o que evita problemas de booleano e de variável em botão;
  - tabela `ig_link_log` para diagnóstico. Guarda só o horário, se encontrou, o modo, o tamanho do texto, se veio variável não preenchida e a palavra encontrada; nunca o texto da pessoa.
- **No ManyChat:** usar `ok` em texto na condição e mandar `{{link_msg}}` como mensagem. O roteiro de correção foi entregue ao Ricardo.
- **Validado em 13/11/2026 às 13:54:** resposta "CAFE" ao story do café, feita de outra conta. O banco encontrou a palavra e o direct chegou com o link. O fluxo de link por palavra está em produção.

## Uma automação só para todas as palavras (13/11/2026)
- Pergunta do Ricardo: "a cada palavra, uma automação? não seria tudo em uma?" A resposta é **uma automação só**.
- **"Site Medicinal - Palavras (links e materiais)"** atende resposta a story, comentário em qualquer post e direct. Ela chama `ig_link_por_palavra`, que decide o que devolver:
  1. **material** (tabela `ig_material`: palavra, mensagem, ativo, validade). Por exemplo, SONO devolve a lista de alimentos com magnésio;
  2. **link do produto do dia** (`ig_post.palavra_chave`).
- A resposta traz `ok` ("sim"/"nao"), `tipo` (material ou link) e `mensagem` pronta. O ManyChat só envia `{{link_msg}}`.
- Palavra nova, seja de link ou de material, se cadastra no banco, sem mexer no ManyChat.
- O **Dermo-day** continua com automação própria, porque é uma conversa com perguntas, não uma resposta única.

## Rotina de vídeos (13/11/2026)

Workflow n8n `fQhO15C8QjrbBRIG` "Site Medicinal - Grade IG - Publicar vídeo", a cada 10 minutos. O publicador de imagens (`bj72gS6IgLvoQh7C`) não foi alterado; a separação é feita no banco:

- `ig_pub_reservar` agora ignora `formato in ('video','reels')`.
- `ig_pub_reservar_video(p_limite)` (só service_role) reserva 1 bloco de vídeo **Aprovado**, vencido, sem erro, sem `link_url`; feed exige o story "POST NOVO NO FEED".

Fluxo: reservar → valida 1 MP4 no armazenamento da Grade → cria container (story = `STORIES`; feed/reels = `REELS` com legenda e `share_to_feed`) → espera 45 s e confere `status_code`; se não estiver `FINISHED`, espera mais 90 s → publica (`media_publish`) → `ig_pub_concluir` com id e permalink. Erro em qualquer etapa vai para `ig_pub_falhar` (aparece no portal).

Travas: execução manual só cria o container e não publica; título começando com `TESTE` nunca é publicado.

## Formato 4 "Cápsula por dentro" (14/11/2026)

- Vídeo macro da cápsula abrindo; a frase se escreve letra a letra (10 letras/s, com esmaecer) desde 0,3 s. Gerador: `grade/videos-produto/capsula_video.py`.
- Custo: 428 créditos Runway (foto 20 + animação 6 s em 1080p 408), cerca de R$ 25; em 720p, cerca de R$ 11.
- Agendado em 15/11 às 14:00: story de vídeo (aprovado) ligado ao reels do feed (aprovado pelo Ricardo), com a legenda sobre suplementação personalizada.
