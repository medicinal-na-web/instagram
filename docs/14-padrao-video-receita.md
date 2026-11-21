# Padrão dos vídeos de receita

Pedido do Ricardo em 21/11/2026: toda receita em vídeo usa o **mesmo cenário**, a **mesma mão**, os **mesmos ângulos de câmera** e o **passo a passo na tela**, para a série ficar reconhecível. Complementa `09-padrao-visual.md` (seção 0) e `10-insercao-de-produto.md`.

**Status: proposta, aguardando aprovação do Ricardo** (bancada-mestre e ângulos em `grade/receitas/cenario/`).

## 1. Cenário fixo (bancada-mestre)
**Versão atual (21/11/2026, escolha do Ricardo): cozinha moderna, opção 1** (`grade/receitas/cenario-moderno/opcao-1.png`). A bancada de carvalho (`grade/receitas/cenario/`) ficou "retrô" e foi substituída.
- Bancada grossa de **granito claro levigado** (branco e cinza suave, veios discretos, acabamento fosco, borda reta).
- Armários sem puxador em off-white fosco, painel de **madeira clara ripada**, torneira fina de aço escovado.
- **Luz natural de janela vindo da esquerda**, clara e suave. Sempre a mesma direção (combina com a inserção de produto do doc 10).
- Decoração mínima: vaso de cerâmica com um galho verde, liquidificador de vidro ao fundo, desfocado.
- Frente da bancada livre para os ingredientes.
- Sem filtro de cor (doc 09).
- Toda cena de IA usa a **imagem-mestre como referência**, para não mudar de cozinha entre receitas.

## 2. A mão
- Só mãos e antebraços, **nunca rosto**.
- Mesma mão em todas as receitas: unhas curtas e naturais, sem anel, sem esmalte, manga de linho cru dobrada.
- Tom de pele: definir com o Ricardo (pode variar por receita, como na sexta da Consciência Negra, mas dentro de uma receita é sempre a mesma mão).
- Gravação real: autorização de imagem da pessoa cujas mãos aparecem.

## 2b. Personagens que falam (IA)
- Sempre marcadas como **conteúdo gerado por IA**; nunca se apresentam como farmacêutica nem como alguém da equipe.
- **Loira, olhos claros, bronzeada, 40+** (`grade/receitas/personagem/personagem-loira-cozinha-moderna.png`): **avental moderno grafite de alças cruzadas com couro** sobre malha off-white; voz **Clarice** (grave, timbre de 40 anos).
- Pronúncia: escrever "protéica" no texto da fala (sem o acento a voz diz "proteólico"); na tela e na legenda, grafia correta "proteica".
- **Personagem morena** (a criar): voz **Bianca** (médio-grave, aveludada). Indicação do Ricardo, 21/11.
- Amostras em `grade/receitas/vozes/`.

## 3. Ângulos de câmera (sempre estes 4, nesta ordem)
| Plano | Câmera | Uso | Passo na tela |
|---|---|---|---|
| **A · Ingredientes** | de cima (90°), bancada inteira | ingredientes arrumados, a mão entra e organiza | lista curta dos ingredientes |
| **B · Ação** | 45° de frente, fechado nas mãos | mão dosando, cortando, colocando no liquidificador | o passo principal ("1 dose de…", "bata com gelo") |
| **C · Despejo** | lateral, na altura do copo | despejar no copo, câmera lenta | "sirva na hora" ou equivalente |
| **D · Final** | 45° de frente, levemente mais aberto, empurrão lento | copo pronto + **produto real ao lado, à direita** | nome da receita + chamada |

- Vertical 9:16, 4 cenas, cerca de 15 s + 2,5 s parados no final para leitura.
- Plano D é onde o produto aparece com rótulo legível.

## 4. Produto na receita
- Quando a receita divulga um produto (ex.: Peptistrong Piña Colada), a **embalagem real** aparece:
  - em **gravação real** (preferido: mão pegando e dosando, roteiro P1 em `12-fontes-e-temas.md`); ou
  - **inserida no plano D parado** pelo procedimento do doc 10 (IC-Light, sombra de contato, fidelidade ≥ 0,90), com foto real da embalagem do sabor certo.
- **Nunca** embalagem gerada por IA nem lata em movimento feita por IA.
- O produto da receita conta como o **produto com link do dia** (regra de um link por dia).

## 5. Passo a passo na tela
- Script: `grade/videos-produto/receita_video.py` (um passo por cena, entra e sai com fade junto do corte).
- Padrão oficial: branco, Playfair, palavra-chave em linha própria Bold Italic 1,6x, até 12 palavras, sem logo no reels/story, texto entre 14% e 80% da altura (padrão: 20%, sobre a área livre da parede).
- Último passo: nome da receita + "receita completa na legenda" (ou "comente PALAVRA" quando houver automação para a palavra).

## 6. Legenda
- Receita completa com medidas, sem promessa de resultado, "a quantidade de proteína no dia é individual: converse com seu nutricionista". Sem "farmacêutica" na chamada.

## Registro
| Data | O que mudou |
|---|---|
| 21/11/2026 | Proposta criada depois do piloto da piña colada (que saiu sem o produto e foi para rascunho). |
| 21/11/2026 | Cenário trocado pela cozinha moderna com granito (opção 1); personagem loira 40+ com avental grafite e voz Clarice. |
