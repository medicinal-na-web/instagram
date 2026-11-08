# 11 — Ferramentas de geração de imagem e vídeo (avaliação de 08/11/2026)

Pergunta do Ricardo: estamos usando as melhores ferramentas para gerar as imagens e vídeos, ou existe plataforma que atenda melhor?

## Resposta curta

1. **A ferramenta não é o gargalo.** O Runway que já usamos funciona como **hub**: dá acesso, pela mesma conta e pelo mesmo conector, aos modelos que as comparações de 2026 colocam no topo. Para imagem: Nano Banana 2.1 e Pro (Google), GPT Image 2 e 2.5, Seedream 5, Ideogram 4.5 e Recraft. Para vídeo: Veo 3.1, Seedance 2 e 2.5, Kling 4 e O3, Gen-4.5 e Gemini Omni. Trocar de plataforma não traria modelo melhor.
2. **Nenhum modelo garante a embalagem fiel.** Num teste com produto real em 3 cenas e 5 modelos, nenhuma das 13 imagens foi aprovada como foto factual do produto. O caminho seguro é o do `10-insercao-de-produto.md`: embalagem vinda de foto real, cena gerada, verificação automática.
3. **O que falta não é gerador, é reiluminação que preserve o produto.** Para isso vale testar o **IC-Light**, um modelo aberto que reilumina o produto para a luz da cena sem redesenhar o rótulo. Ele roda em ComfyUI ou em Spaces do Hugging Face, e já temos o conector do Hugging Face.
4. **Custo:** o modelo padrão do Runway (Nano Banana Pro) custou 20 créditos por imagem. Para a cena (sem produto), dá para usar um modelo mais barato e reservar o caro para a peça final.

## Comparação por tarefa

| Tarefa | Melhor opção hoje | Onde | Observação |
|---|---|---|---|
| **Cena sem produto** (cozinha, bancada, textura) | Nano Banana Pro / 2.1, Seedream 5 Pro | Runway (já temos) | Nano Banana Pro deu cenas muito realistas no teste de 08/11 |
| **Produto real em cena** | Nenhum modelo sozinho. Usar foto real + `insere_foto` + verificação | nosso pipeline | No teste externo, Nano Banana 2 foi o que mais preservou o produto, e GPT Image 2 o que melhor preservou o texto. Mesmo assim, nenhum foi aprovado como foto factual |
| **Reiluminar o produto para a cena** | IC-Light v2 | ComfyUI (RunComfy) ou Space do Hugging Face | Preserva detalhes e texto do rótulo segundo tutoriais; testar com o Peptistrong |
| **Fundo e sombra em lote** (catálogo, site) | Photoroom API Plus (US$ 100/mês, 1.000 imagens), Claid, Pebblely | externo | Não está confirmado que preservam os pixels do produto: testar antes |
| **Texto e tipografia na arte** | nosso gerador (fontes do padrão) | `grade/teste-padrao-2025/monta.py` | Nunca gerar texto de arte nem de rótulo por IA |
| **Vídeo curto a partir de uma imagem aprovada** | Veo 3.1 (até 3 referências), Seedance 2.5 (referência de produto), Kling O3 | Runway (já temos) | Movimento sutil (luz, vapor, mão). Rejeitar qualquer clipe em que a embalagem mude |
| **Editar vídeo real** (trocar fundo, luz) | Aleph 2.0 (`edit_video`) | Runway (plano pago) | Bom para reels gravados na loja |
| **Anúncio de produto em vídeo** | `generate_product_marketing_video` | Runway | Testar só com foto real do produto |
| **Embalagem em qualquer ângulo** | Modelo 3D (Blender, gratuito) com a arte-final do rótulo | local | Pendência 8 do `CONTEXTO.md` |

## Vídeo: regra para produto

Produto em vídeo é o caso mais difícil, porque rótulo, logo e formato "derretem" entre os quadros. Regras:

- Gerar o vídeo **a partir de uma imagem já aprovada** (image-to-video), com movimento pequeno.
- Preferir vídeo **sem o produto** (ambiente, textura, mão, vapor) e colocar o produto em quadro fixo ou em corte.
- Aplicar `verifica_fidelidade` em quadros do vídeo (1 por segundo). Se qualquer quadro ficar abaixo de 0,90, o clipe é reprovado.
- Reels com gente da Medicinal continuam sendo o formato que mais funcionou em 2025. IA é complemento.

## Plano de teste proposto (antes de mudar qualquer coisa)

Mesmo briefing (Peptistrong na bancada, luz da janela), usando as fotos reais do procedimento 10:

| Teste | Ferramenta | Mede |
|---|---|---|
| 1 | Cena no Runway (Nano Banana 2.1, mais barato) + `insere_foto` | fidelidade, escala, ângulo, tempo, custo |
| 2 | Igual ao 1 + reiluminação com IC-Light | ganho de realismo sem perder fidelidade |
| 3 | Photoroom (fundo + sombra por IA) | fidelidade e realismo de ferramenta pronta |
| 4 | Vídeo de 5 s a partir da melhor imagem (Veo 3.1 × Seedance 2.5) | fidelidade quadro a quadro |

Custo estimado no Runway: cerca de 100 a 150 créditos (imagens a 20 e vídeos bem mais). Saldo atual: 20.

## Fontes

- [Masonry: Best AI Model for Product Photography (30 tests)](https://masonry.so/blog/best-ai-image-model-for-product-photography)
- [Masonry: AI product photography tools by workflow](https://masonry.so/blog/ai-product-photography-tools)
- [Claid: AI product photo tools 2026](https://claid.ai/blog/article/ai-product-photo-tools)
- [Rangy: Best AI for product photography](https://rangy.ai/blog/best-ai-for-product-photography/)
- [ocdevel: AI video generation in 2026](https://ocdevel.com/mlg/mla-26)
- [OpenCreator: AI video models comparison 2026](https://opencreator.io/blog/ai-video-models-comparison-2026)
- [Morphed: AI video generators for e-commerce](https://morphed.app/blog/ai-video-generator-for-ecommerce)
- [diyai: image-to-video tested](https://diyai.io/ai-tools/video-generation/best-ai-image-to-video-generators/)
- [ComfyUI Wiki: IC-Light](https://comfyui-wiki.com/en/models/ic-light)
- [RunComfy: IC-Light workflow](https://www.runcomfy.com/comfyui-workflows/comfyui-ic-light-image-relighting-tool)
- [G2: Photoroom API pricing](https://www.g2.com/products/photoroom-api/pricing)

As comparações são em boa parte de blogs de fornecedores. Servem como lista de candidatos, não como veredito. O teste com os nossos produtos decide.
