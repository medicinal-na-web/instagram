# Teste do padrão visual com imagens de IA (08/11/2026)

Aplicação do `docs/09-padrao-visual.md` sobre 4 imagens geradas no Runway (pasta `ia/`) e a foto real da lata de Peptistrong (`../assets/peptistrong.jpg`, nunca gerada).

| Arte | Modelo do padrão | Imagem |
|---|---|---|
| `A-frase.jpg` | A · Frase de marca | IA: cápsula entre os dedos |
| `B-radar.jpg` | B · Série Radar Magistral (PeptiPump) | IA: lentilha saindo do saco de linho |
| `C-pergunta.jpg` | C · Pergunta-gancho | IA: mulher em prancha, sem rosto |
| `D-produto.jpg` | A · Frase + produto real montado na cena | IA: bancada de cozinha + lata real (ver abaixo) |
| `E-numero.jpg` | E · Número em marinho | sem imagem |
| `grade-teste.jpg` | como as 5 ficam na grade do perfil | |

Gerar de novo: `python3 monta.py` (usa as fontes de `../assets/fonts/`).

**Status:** teste, não aprovado. Nada disso foi para a grade nem para o Instagram.

Pendências antes de usar de verdade:
- O dado "3–8% a menos por década depois dos 30" precisa de fonte citada na legenda e revisão farmacêutica.
- Posts com pessoa realista de IA (C) levam o rótulo "Informações de IA" no Instagram.
- Custo: 20 créditos do Runway por imagem ou harmonização. Saldo após o teste: **20**.

## Como a lata entrou na cena (D)

1ª versão reprovada pelo Ricardo: lata "colada", grande demais, sem perspectiva. Processo que passou:

1. `ia/cozinha.jpg`: cena gerada.
2. `ia/cozinha_com_produto.jpg`: montagem com `../insere_produto.py` (`insere`), com a **proporção da lata real** (largura ≈ 0,77 da altura, medida nas fotos reais de 2025; o mockup 3D é mais alto e fino), altura menor que a do copo, mais ao fundo, tampa e base em elipse, luz e sombras.
3. `ia/cozinha_harmonizada.jpg`: harmonização no Runway (luz, tampa, sombra, reflexos). **A IA estragou o texto do rótulo** ("TEENOUÓSICA", "COCOOLAIS").
4. `ia/cozinha_final.jpg`: `recoloca_rotulo` devolve o rótulo original iluminado pela luz da IA. Texto conferido.
