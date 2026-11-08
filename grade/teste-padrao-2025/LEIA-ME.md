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

**Resultado:** nenhuma das versões de D passou no padrão do Ricardo. As lições viraram o procedimento `docs/10-insercao-de-produto.md`. `ia/cozinha_final.jpg` hoje é a versão 4 (foto real da lata, sem IA na embalagem, fidelidade 0,937), ainda reprovada por ângulo e luz incompatíveis com a cena.

## Versão 5 (08/11/2026): procedimento completo com a foto real

`D-produto-v5.jpg`, a partir de `ia/v5/`:
1. Cena gerada sob medida (`ia/v5/cena.jpg`): câmera baixa, luz quente pela direita, copo de ~14 cm como referência, centro vazio.
2. Lata: foto real de 03/09/2025 (tampa e alça verdadeiras), reiluminada pelo IC-Light com luz da direita, só o mapa de luz (`ia/v5/lata_real_luz_direita.png`).
3. Inserção sem deformar (`insere_foto`), sombra para a esquerda igual à da tigela.

| Verificação | Resultado | Situação |
|---|---|---|
| Fidelidade do rótulo | 0,957 (mín. 0,90) | ✅ |
| Proporção largura/altura | 0,668 × 0,665 da foto | ✅ |
| Luz | lado claro à direita, igual à janela | ✅ |
| Escala | 29,7 px/cm pelo copo; lata com **12 cm estimados** | ⚠️ falta medir com régua |
| Ângulo | elipse da cena ≈ 0,10–0,16 × foto da lata ≈ 0,05 | ❌ tampa aparece "chapada" |

**Não aprovada** pelo ângulo. Uma 2ª cena pedindo câmera rente à bancada (`ia/v6/`) saiu pior: a IA voltou a olhar de cima e gerou sombras incoerentes.

**Aprendizado:** os geradores de imagem fazem a câmera **levemente de cima** (elipse ≈ 0,10–0,16) e resistem ao ângulo rente. A foto do produto mais útil é a de **~30° de cima**; a frontal serve pouco. Priorizar essa foto na sessão de fotos (`docs/10`, seção 2).
