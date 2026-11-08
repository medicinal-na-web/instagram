# 09 — Padrão visual e de conteúdo do feed (base: 2º semestre de 2025)

Proposta de 08/11/2026 para discussão. Baseada nos 68 posts de 15/06 a 31/12/2025, o período de melhor engajamento medido (`07-fase-2025.md`). **Rascunho**: vale depois do OK do Ricardo.

## 1. Princípios

1. **Imagem com cara de foto real.** Por decisão de 08/11/2026, as imagens podem ser geradas por IA enquanto não há sessão de fotos nem rosto da marca, seguindo as regras da seção 11. Nada de banco de imagens com marca d'água (houve "Unsplash" visível em 2025).
2. **Uma ideia por arte.** Uma frase, uma pergunta ou um nome. O resto vai na legenda ou no carrossel.
3. **O texto fica direto na foto.** Sem faixa, sem caixa, sem etiqueta colorida, sem molde fixo.
4. **Tons quentes e luz natural.** O feed tem cara de editorial de revista, não de anúncio.
5. **Gente aparece.** O objetivo é ter pessoa em metade dos posts. Até existir um rosto da marca, mãos, recortes de corpo e ambientes fazem esse papel (seção 11).

## 2. Paleta

Duas camadas: o **marinho é a cor da marca** (âncora, igual em todo post que leva cor sólida) e os **tons quentes são os da fotografia** (extraídos das imagens publicadas no 2º semestre de 2025).

| Nome | Hex | Uso |
|---|---|---|
| **Marinho** | `#102140` | cor da marca: logo sobre fundo claro, rótulos, números, fundo do carrossel de texto |
| **Marinho 2** | `#1c345e` | apoio: linhas, segundo plano em fundo marinho |
| Off-white | `#eee7da` | fundo de carrossel de texto, respiro |
| Areia | `#e0be97` | fundo claro, luz |
| Caramelo | `#bf9162` | destaque quente |
| Café com leite | `#896c57` | fundo médio |
| Terracota | `#794332` | destaque forte, poucas vezes |
| Marrom | `#483932` | fundo escuro |
| Quase preto | `#281612` | fundo escuro, texto sobre claro |
| Cinza quente | `#bdb5a9` | fundo neutro de produto |

Regras do marinho:

- Aparece em **cerca de 1 post a cada 4** (modelos E e F), mais o logo e os rótulos quando o fundo é claro.
- Combinações: **marinho + off-white** (texto) e **marinho + caramelo** (destaque, ex.: palavra em itálico). Evitar marinho ao lado de terracota.
- **Nunca** como faixa, barra ou etiqueta sobre foto (o molde das artes de 09–15/11/2026). Sobre foto, o texto é branco.

Texto: **branco** sobre foto; **marinho** sobre off-white. A cor da embalagem do produto (amarelo do Peptistrong, rosa do Derma Fusion) entra pela foto, não por blocos de cor.

## 3. Tipografia: quatro fontes, no máximo duas por arte

Identificadas comparando os textos dos posts de 2025 com as candidatas. Todas gratuitas (Google Fonts, licença OFL), também no Canva. Arquivos em `grade/assets/fonts/`.

| Voz | Fonte | Quando | Como |
|---|---|---|---|
| **Frase** | **Playfair Display** Regular | frase de marca, carrossel de texto | minúscula, espaçamento entre letras levemente negativo (−2% a −3%); **palavra-chave em Playfair Display Bold Italic**, maior ("a raiz do crescimento ***Saudável***") |
| **Título de reels** | **Playfair Display Italic** + **Archivo Black** | capa de reels | itálico leve no começo ("3 Motivos para tomar") e a palavra principal enorme em Archivo Black ("creatina") |
| **Rótulo** | **Poppins Bold** | nome de série, nome de ativo, número | CAIXA ALTA com espaçamento largo ("RADAR MAGISTRAL", "BASTIDORES DE VISITAÇÃO") |
| **Pergunta** | **IBM Plex Mono** | pergunta-gancho, nota de apoio | sublinhada, pequena, acima do rótulo ("Por que o Peptistrong…") |

Logo `medicinal` pequeno no canto superior (branco sobre foto, marinho sobre off-white).

### Logotipo

O "medicinal" das artes é **sempre o logotipo oficial**, nunca texto digitado em outra fonte. Arquivos em `grade/assets/logo/`:
- `medicinal-logo-oficial.svg` / `.png`: logo completo do site (símbolo + "medicinal" + "FARMÁCIA E MANIPULAÇÃO"), cores originais `#0F62AC` e `#98B7E0`.
- `medicinal-palavra-branco.png` (sobre foto), `-marinho.png` (sobre off-white), `-off-white.png` (sobre marinho), `-azul-oficial.png`: a palavra "medicinal" **recortada do próprio logo**, desenho idêntico.
- Tamanho nas artes 1080×1350: 170 px de largura, a 60 px da borda, no canto superior.
- Proibido redesenhar, distorcer, trocar a fonte ou aplicar efeitos na marca.

## 4. Composição

- **Formato:** 1080×1350 (4:5) no feed; capa de reels 1080×1920 com o título dentro da área central 1080×1350 (é o que aparece na grade).
- Texto **centralizado**, no terço superior ou no meio; nunca encostado na borda (margem de 60 px).
- Foto escurecida de leve (10% a 30%) quando o texto é branco.
- Close e macro: cápsula entre os dedos, pó na colher, textura do creme, mão segurando a embalagem.

## 5. Modelos de arte

| Modelo | O que é | Exemplo de 2025 |
|---|---|---|
| **A · Frase de marca** | frase curta em serifa com palavra em itálico sobre foto macro do produto | "antes de cada fórmula que chega até você, existe um *médico*…" |
| **B · Série / rótulo** | nome da série + nome do ativo em caixa alta espaçada sobre textura da matéria-prima | "RADAR MAGISTRAL · VENOLIN" |
| **C · Pergunta-gancho** | pergunta em mono sublinhada + tema em caixa alta | "Por que o Peptistrong está sendo chamado de revolução na PRESERVAÇÃO MUSCULAR?" |
| **D · Capa de reels com pessoa** | pessoa real no ambiente + título curto | "3 *Motivos* para tomar CREATINA", "Pílula do treino" |
| **E · Número (marinho)** | fundo marinho, dado grande em off-white, complemento em itálico caramelo | "ENTRE 30 E 80 ANOS, VOCÊ PODE PERDER ATÉ 40% *de massa muscular*" (com fonte na legenda) |
| **F · Carrossel de texto** | fundo off-white, texto marinho em serifa, numeração e linha fina; nota em mono | "Peptistrong não substitui a proteína da sua dieta. *Ele complementa.*" |
| **G · Bastidor sem arte** | vídeo ou foto crua, só um rótulo curto | "BASTIDORES DE VISITAÇÃO" |

## 6. Séries fixas

| Série | Formato | Frequência sugerida |
|---|---|---|
| **Especialista convidado** (nutri, derma, médica): "hype ou realidade", "3 motivos" | reels | 1 por semana |
| **Bastidores** (manipulação, visitação médica, degustação, equipe) | reels | 1 por semana |
| **Radar Magistral** (ativo novo, macro da matéria-prima) | reels curto ou carrossel | quinzenal |
| **Pergunta-gancho / número** com "comente X" para receber material | carrossel | 1 por semana |
| **Humor de balcão / POV** | reels | quinzenal |
| **Evento e parceiros** | carrossel de fotos reais | quando houver |

Ritmo: **4 posts por semana**, cerca de 60% reels.

## 7. Grade (como o perfil aparece)

Alternar na sequência de 3 em 3: **pessoa · produto/macro · texto sobre textura ou marinho**. Os quadrados marinhos dão o ritmo da grade: espalhados, nunca dois juntos. Evitar dois posts de texto lado a lado e mais de dois ativos seguidos (o erro de jul–ago/2026).

## 8. Legenda

- **Gancho na 1ª linha** (pergunta ou frase curta).
- 2 ou 3 parágrafos curtos; cerca de **400 caracteres**.
- **CTA "Comente PALAVRA"** para receber material (PDF, explicação); foi o que mais gerou comentário.
- Emoji: no máximo 1 ou 2.
- Hashtags: 3 a 6 no fim, separadas por linhas com "-".
- Marcar o parceiro (@) quando aparecer.
- Nada de preço nem promessa de resultado; dose e uso "com orientação profissional".

## 9. Antes de aprovar (checklist)

- [ ] A foto é real e da Medicinal (ou do parceiro, com autorização)?
- [ ] Quem aparece assinou autorização de uso de imagem?
- [ ] Uma ideia só? No máximo duas vozes de texto?
- [ ] Sem faixa, caixa ou etiqueta?
- [ ] Copy sem alegação de cura, efeito garantido, comparação com medicamento ou antes e depois?
- [ ] Suplemento ou manipulado: revisado pela farmacêutica?
- [ ] Na grade, combina com os dois posts vizinhos?

## 10. Não fazer

- Faixa marinha fixa sobre a foto ou etiqueta marinha (molde das artes de 09–15/11/2026).
- Molde igual para todos os posts (as artes de 09–15/11/2026 e os "Conheça [ativo]" de 2026).
- Imagem gerada por IA ou de banco com pessoas que não são da Medicinal.
- Bloco de cor sólida com texto longo.
- Alegações que apareceram em 2025 e não passam hoje: "treino em cápsula, simula os efeitos do exercício", "reduz gordura abdominal", "resultados reais na composição corporal".

## 11. Imagens com IA (decisão de 08/11/2026)

Enquanto não há sessão de fotos nem rosto da marca, as imagens podem ser geradas por IA (Runway). O que fez as artes de 09–15/11 parecerem IA foi o conjunto: molde fixo, faixa, cenas genéricas de banco e repetição. As regras abaixo atacam cada um desses pontos.

**O que gerar (funciona bem e passa por foto):**
- Macro e textura: cápsula entre os dedos, pó na colher, creme espalhado na pele, gotas, matéria-prima (fava, lentilha, café, flores).
- Mãos em ação: segurando o copo, abrindo o pote, pesando na balança, luva na bancada.
- Ambientes sem rosto: bancada de manipulação, consultório bege com luz de janela, cozinha clara, academia em penumbra.
- Corpo em recorte: ombro, braço treinando, costas, silhueta contra a janela.

**Como pedir (estilo do prompt):** luz natural lateral, tons quentes (areia, caramelo, café), profundidade de campo curta, grão de filme leve, enquadramento imperfeito, objetos de uso real. Evitar estúdio branco, simetria perfeita, sorriso de banco de imagem, pele de plástico, cenas cheias.

**Produto sempre real:** a embalagem nunca é gerada (a IA erra rótulo e logo). Usar a foto real do produto recortada e montada na cena gerada, ou deixar o produto fora da imagem.

**Rosto de IA, só com estas condições:**
- Pessoa de IA pode aparecer como **modelo de estilo de vida** (alguém tomando o shake, treinando), nunca como **farmacêutica, médica, nutricionista, cliente ou "equipe da Medicinal"**. Pessoa inventada dando orientação de saúde ou depoimento é enganoso (regra 4 e publicidade de saúde).
- Marcar o post com o rótulo **"Informações de IA"** do Instagram, que a Meta exige para imagem realista gerada por IA.
- Rosto recorrente gerado por IA (um "personagem" fixo) fica **fora** até o Ricardo decidir.

**Na grade:** imagem de IA não pode ocupar mais de 2 quadrados seguidos sem um post de texto (modelos E e F) ou um conteúdo real (evento, bastidor) no meio.

**Custo:** 20 créditos do Runway por imagem ou edição (modelo padrão). Saldo em 08/11: 20. Vídeo gasta bem mais.

## 12. Produto inserido em cena: naturalidade extrema (regra fixa)

Pedido do Ricardo em 08/11/2026, depois do primeiro teste (lata de Peptistrong "colada" na cozinha). **Vale para toda arte que coloca a embalagem real dentro de outra imagem.** Se não ficar indistinguível de uma foto, a arte não sai.

**O procedimento obrigatório, passo a passo e com critérios de aprovação, está em `10-insercao-de-produto.md`.** O resumo abaixo não substitui o procedimento.

Checklist obrigatório:

1. **Escala e proporção:** medir contra um objeto vizinho na mesma profundidade (copo, tigela, mão). A lata de Peptistrong 300 g é **mais baixa que um copo alto e mais ou menos da mesma largura**; largura ≈ 0,77 da altura (medido em foto real). **Não usar a proporção do mockup 3D** (`assets/peptistrong.jpg`), que é mais alto e fino que a lata de verdade.
2. **Perspectiva:** a câmera da cena define o ângulo. Se a boca do copo aparece como elipse, a tampa e a base da embalagem também aparecem como elipse, na mesma proporção. Mockup de frente em cena vista de cima não serve.
3. **Luz:** mesma direção, cor e dureza da luz da cena. Lado da janela mais claro, lado oposto na sombra, brilho fino na superfície. Se a cena tem manchas de luz (sombra de folhas), elas passam por cima do produto.
4. **Sombras:** sombra de contato escura onde a embalagem toca a superfície e sombra projetada para o lado oposto à luz, com a mesma suavidade das sombras dos outros objetos.
5. **Integração:** mesma nitidez/desfoque do plano onde está, mesmo grão, borda sem halo branco, leve reflexo da cor do ambiente na embalagem.
6. **Rótulo intacto:** nome, logo, textos e cores iguais aos da embalagem oficial. Conferir letra por letra se passar por IA.
7. **Posição com sentido:** a embalagem fica onde alguém a deixaria (ao lado do copo, perto da mão), de preferência parcialmente encoberta por outro objeto ou com outro objeto à frente.

Como fazer, em ordem de preferência:

1. **Foto real** da embalagem tirada no mesmo tipo de luz da cena (celular, luz de janela). É o melhor resultado e não custa nada.
2. **Montagem + harmonização + rótulo original**: montar com `grade/insere_produto.py` (`insere`: escala, perspectiva em elipse, tampa, luz, sombras, grão), harmonizar no Runway e depois `recoloca_rotulo` (a IA acerta luz e sombra mas **estraga o texto do rótulo**; a função devolve o rótulo original com a luz da IA). Exemplo em `grade/teste-padrao-2025/LEIA-ME.md`.
3. Gerar a cena **já com espaço e luz pensados** para o produto (superfície plana, objeto de escala ao lado, luz lateral definida).

A imagem 3D do fabricante (`grade/assets/peptistrong.jpg`) é o pior ponto de partida: é render, não foto. Pedir à loja fotos de celular das embalagens principais (Peptistrong, PeptiPump, Keranat, Maxsolve) em luz de janela.

## 13. Linha editorial: temas que provocam

Pedido do Ricardo em 08/11/2026: **polemizar os temas.** O gancho tem que mexer com a pessoa, contrariar o senso comum ou apontar algo que ela não percebeu.

**Temas foco:**

| Tema | Peso | Exemplos de gancho |
|---|---|---|
| **Queda de cabelo** | **foco principal** | "Seu cabelo não está caindo à toa." · "Shampoo não resolve o que começa por dentro." · "Queda de cabelo depois do verão: normal ou sinal?" |
| **Perda de massa magra** | alto | "Você está perdendo músculo e nem percebe." · "Depois dos 30, o músculo vai embora em silêncio." · "Emagrecer rápido pode estar custando o seu músculo." |
| **Magnésio** | **alto (topo)** | "Cansaço que nem o café resolve?" · "Nem todo magnésio é igual: a forma muda tudo." · "Câimbra à noite, sono leve, foco curto: já olhou o seu magnésio?" (sempre fechando com "investigue com seu médico" / "fale com a farmacêutica") |
| **Falta de zinco** | médio | "O mineral que quase ninguém lembra e que o cabelo, a pele e a imunidade cobram." · "Unha fraca, cabelo caindo, feridas que demoram: já ouviu falar de zinco?" |
| **Visão** | médio | "Tela o dia inteiro: o que seus olhos estão pagando?" |

**Formatos que polemizam bem (de 2025):** "hype ou realidade?", "mito ou verdade", "o que ninguém te conta sobre…", comparação (Whey x Peptistrong), número grande (modelo E), pergunta-gancho (modelo C).

**Limites (regra 4, sem exceção):**

- Polemizar o **tema**, nunca prometer o **resultado**. "Seu cabelo não está caindo à toa" pode; "Keranat acaba com a queda" não.
- Sem assustar com doença nem induzir autodiagnóstico: o fechamento leva a pessoa para **orientação profissional** ("investigue com seu médico", "fale com a farmacêutica").
- Dado sempre com fonte na legenda.
- Sem atacar concorrente, medicamento ou profissão (o "Canetinha x Akkermat" de 2024 não se repete).
- **Minoxidil** e qualquer medicamento sob prescrição: só como tema educativo, nunca como oferta.
- Visão: sem prometer melhora da vista; falar de cuidado, hábito e acompanhamento oftalmológico.
- Suplemento ou manipulado citado: revisão farmacêutica antes de aprovar.
