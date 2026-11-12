# Briefing de redação — campanha Instagram @medicinalnaweb, 13 a 30/11/2026

Marca: Medicinal Farmácia e Manipulação (Maringá/PR), farmácia de manipulação com loja em medicinalnaweb.com.br e atendimento por WhatsApp. O farmacêutico responsável (Ricardo) revisa tudo antes de aprovar.

## Tom e linha editorial
- Português do Brasil, tom de editorial de revista (não de anúncio), claro, confiável e acolhedor. Uma ideia por peça.
- **Polemizar o TEMA, nunca prometer o RESULTADO.** O gancho contraria o senso comum ou faz uma pergunta que incomoda.
- Use o "gancho" do tema como ponto de partida, mas reescreva se encontrar um melhor.

## Proibido (sem exceção)
- Alegação de cura, tratamento ou efeito garantido ("emagrece", "acaba com a queda", "cura ansiedade", "aumenta testosterona", "baixa a glicose", "trata").
- Antes e depois.
- Medicamento sob prescrição como oferta (minoxidil só como tema educativo, sem link e sem indicação).
- Comparar com medicamento ou dizer que o manipulado "é igual" a um produto de marca.
- Atacar concorrente, medicamento ou profissão.
- Assustar com doença ou induzir autodiagnóstico.
- Preço. Dose diferente da de uso. Dados de clientes.
- Pessoa de IA apresentada como farmacêutica, médica, nutricionista, cliente ou equipe.
- Temas de saúde fecham levando para orientação profissional ("fale com a farmacêutica", "converse com seu médico ou nutricionista").
- Suplemento é "parte da rotina", "pode ajudar", "é estudado para"; nunca "resolve".

## STORY (canal story, 9:16)
- `titulo`: título interno curto (até 6 palavras).
- `legenda`: o TEXTO que vai escrito na arte do story, no máximo 22 palavras, em 1 ou 2 frases. Marque UMA palavra-chave entre asteriscos (ex.: *magnésio*). Pode terminar com pergunta.
- Se o story tem `link_url`, a última frase convida para o link, sem preço e sem promessa (ex.: "Conheça a fórmula no link."). Sem link, convide para conversar ("Responda este story" ou "Fale com a farmacêutica no WhatsApp").
- `prompt_imagem`: descrição EM PORTUGUÊS (até 55 palavras) de UMA fotografia para gerar no Runway, no padrão visual:
  - fotografia realista, luz natural lateral, tons quentes (areia, caramelo, café, off-white) com algum detalhe azul-marinho;
  - profundidade de campo curta e grão de filme leve;
  - macro, textura, matéria-prima, bancada ou ambiente doméstico;
  - **o terço inferior é uma superfície lisa e desfocada (tecido, madeira, parede), livre para o texto.**
  - Escreva só o que DEVE aparecer, em frases afirmativas. Exemplo: "copo de vidro com gelo e gotas de condensação", e não "sem parecer quente".
  - No máximo uma mão, relaxada, parcialmente fora do quadro, ou nenhuma pessoa.
  - Nada de rosto, embalagem, rótulo, logotipo ou texto na imagem.
- `hashtags`: vazio.

## FEED (canal feed, 4:5)
- `titulo`: até 6 palavras.
- `frase_arte`: a frase que vai escrita sobre a foto, no modelo "frase de marca": até 10 palavras, uma ideia, provoca sem prometer. Marque UMA palavra-chave entre asteriscos.
- `legenda`:
  - gancho na 1ª linha;
  - 2 ou 3 parágrafos curtos, cerca de 400 a 600 caracteres, com uma informação útil e verificável;
  - fechamento com orientação profissional;
  - quando fizer sentido, CTA "Comente PALAVRA" (uma palavra em maiúsculas) para receber material;
  - no máximo 1 emoji;
  - **sem produto do site e sem link** (decisão do Ricardo).
- `hashtags`: 3 a 6, separadas por espaço (ex.: #magnesio #sono #farmaciademanipulacao #maringa).
- `prompt_imagem`: como no story, mas o espaço livre é o **terço superior** (céu, parede ou tecido desfocado), para a frase.
- `link_url`: vazio.

## Saída
Arquivo JSON (lista), um objeto por slot, com as chaves: `data`, `hora`, `canal`, `tema_id`, `titulo`, `legenda`, `hashtags`, `prompt_imagem`, `frase_arte` (só feed; no story repita a `legenda`), `link_url`.
- `link_url` vem do tema: preencha com `produto_url` **somente** se o canal for story e `produto_ok = 'sim'`; caso contrário, "".

## Revisão do Ricardo (12/11/2026, depois das artes de 13/11) — vale para TODOS os stories
- **Texto curto e assertivo**: no máximo 12 palavras, 1 frase (2 no máximo), feita para gerar curiosidade e vontade de tocar no adesivo de link. Afirmação que provoca ou pergunta que incomoda. Ex.: "nem todo magnésio chega ao *cérebro*.", "fibra sem *água* não funciona."
- **Proibido nos stories**: "fale/converse com a farmacêutica", "pergunte à farmacêutica", "conheça no link", "acesse o link", "link na bio", "toque no link". O adesivo de link faz esse papel.
- Continua proibido prometer efeito (curiosidade sim, promessa não).
- **Variar cor e modelo entre os stories do mesmo dia** (não pode parecer o mesmo assunto). Cada story recebe um `modelo`:
  - `A` foto + frase branca (cena varia de paleta: manhã clara e fria com azul-marinho, terracota e barro, noite escura e quente, verde botânico profundo, branco luminoso);
  - `E` fundo **marinho** liso, rótulo Poppins caixa alta off-white + frase Playfair off-white com palavra-chave em itálico **caramelo** (sem foto);
  - `F` fundo **off-white** liso, frase Playfair **marinho** com palavra-chave em itálico, rótulo Poppins marinho (sem foto);
  - `C` pergunta em **IBM Plex Mono sublinhada** + resposta curta em Playfair, sobre fundo **areia** ou **café** liso (sem foto).
  Por dia: no máximo 2 stories com foto (modelo A), e nunca dois modelos iguais seguidos. Marinho (E) no máximo 1 por dia.
- Para `E`, `F` e `C`: `rotulo` (2 a 3 palavras em caixa alta, ex.: "MAGNÉSIO TREONATO") e, no `C`, `pergunta` (até 8 palavras, termina com "?").

## Ajuste de 12/11/2026 (Ricardo)
- 1 produto com link por dia; os outros stories sem chamada.
- Pódio sempre aos sábados, com a campeã (produto do dia) logo depois, às 12:30.
- Palavra-chave breve, sem acento nem caractere especial.
- Story sem logo; feed com logo.
