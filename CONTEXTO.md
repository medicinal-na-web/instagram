# Contexto para novas sessões

Este arquivo resume a conversa de 22/10 a 08/11/2026 que levou ao projeto. Leia com o `README.md`.

## Ativos e IDs (não são segredos)

| Item | Valor |
|---|---|
| Conta do Instagram | @medicinalnaweb, ID `17841401675469982`, conta BUSINESS |
| Página do Facebook | Medicinal Farmácia e Manipulação, ID `551028704983998` |
| Business Manager | Medicinal Farmácia E Manipulação, ID `706932469498110` |
| Conta de anúncios | `act_707010962823594` (BRL, America/Sao_Paulo, ativa, pagamento ativo) |
| App da Meta | `APP_clienteDM` (`898730696565732`), usado pelos dois acessos |
| App do Instagram | `APP_clienteDM-IG` (`957953860481209`) |
| Usuário do sistema (ads) | `n8n-ads` (`122104724457514359`), função Funcionário |
| Grade (Artifact) | https://claude.ai/artifact/Ayp1jCcyffTqZth63yXdtX (privada) |

**Credenciais no n8n** (o token fica só lá): `Site Medicinal - Instagram (token)` (`ZTNV44evExPBBMNC`, Query Auth, token do Instagram, vence em ~60 dias, renovação pendente) e `Site Medicinal - Meta Ads (token)` (`DoGhzs4iWUtxnXSp`, Query Auth, token sem validade).

## Workflows no n8n (todos desativados, gatilho manual ou webhook)

| Nome | ID | Função |
|---|---|---|
| Teste de acesso Instagram | `UKhPnwvSom56JWEq` | Só leitura |
| Teste de acesso Meta Ads | `0tsI5zGXKXckm9LN` | Só leitura |
| Publicar story Instagram | `sNa5QuakTZd3gjYM` | Usado no story de Outubro Rosa |
| Espelho do feed Instagram (leitura) | `7I7FHnyRbsaWaTvD` | Lê as últimas mídias |
| Instagram mídias do feed (sub) | `9xmnZPrHM0uLq924` | Sem histórico (a paginação traz o token) |
| Grade IG - URL de upload | `YUm9MkLzNIpC0BAz` | Webhook `sitemedicinal-grade-ig-upload`, URL assinada |
| Grade IG - Publicar | `JzeSG0EOQRW58NmI` | Webhook `sitemedicinal-grade-ig-publicar` |
| Instagram posts desde 2024 (leitura) | `JKs2B6e46nDNjr51` | Gatilho manual, lê os posts de 2024 em diante pelo sub abaixo |
| Instagram posts desde 2024 (sub, sem histórico) | `70pLth4t9PibQL7d` | Paginação com token descartada, sem histórico |

## Estado em 08/11/2026

- **Instagram:** publicação e insights validados. Story de Outubro Rosa publicado em 22/10.
- **Meta Ads:** acesso validado. Nada anunciado ainda.
- **Grade:** 18 posts espelhados (publicados) e 24 blocos da semana 09–15/11 em **Rascunho**, com fotos do Runway e identidade azul-marinho.
- **Publicação automática:** rotina `grade-publicacao` (de hora em hora, 8h–22h) publica blocos **Aprovado** com data/hora vencidos. **Está sem o conector n8n**: precisa ser adicionado em claude.ai → Rotinas, senão não publica nada.
- **Vídeo:** botão "Gerar vídeo no Runway" no editor. Ainda não foi testado. Saldo do Runway: **20 créditos** em 08/11 (imagem ou edição custa 20; vídeo gasta bem mais). Precisa recarregar para produzir a semana.
- **Canva:** créditos de IA acabaram em 07/11. O botão "Gerar imagem no Canva" falha até renovar.

## Pendências

1. Adicionar o conector n8n à rotina de publicação.
2. Renovar o token do Instagram antes de ~21/12/2026.
3. Gerar o primeiro vídeo de teste (aprovação direta do Ricardo na grade).
4. Bucket público próprio no Supabase para as artes (hoje dependem de links temporários).
5. App da Meta: URL de exclusão de dados, categoria, ícone, reautorização de 2 fatores e um segundo administrador.
6. Revisão farmacêutica da semana 09–15/11 antes de aprovar, principalmente Maxsolve e PeptiPump.
7. Migrar a grade para o PortalSiteMedicinal quando o endereço voltar.
8. **A entregar (decisão do Ricardo em avaliação):** base de imagem dos produtos para inserção em cena (`docs/10-insercao-de-produto.md`). Opção A: 6 fotos reais por produto (3 ângulos × luz dos dois lados) + medidas com régua. Opção B: modelo 3D por produto (medidas + arte-final do rótulo em PDF/AI da gráfica), que gera qualquer ângulo e luz. Opção C: as duas (fotos já; 3D do Peptistrong em paralelo). Começar pelo Peptistrong.
9. Avaliar ferramentas de geração de imagem e vídeo de produto (comparação em `docs/11-ferramentas-imagem-video.md`).

## Material de campanha

- **Peptistrong diário** (02 a 30/11) e as regras de copy do Peptistrong estão em `docs/04-peptistrong-black-friday.md`. Ainda é rascunho para aprovação.
- Histórico completo do chat do Instagram: `docs/05-historico.md`.
- Fase de 2024: `docs/06-fase-2024.md`. 2025 e comparação: `docs/07-fase-2025.md` (o 2º semestre de 2025 é o melhor período medido). Feed de 2026: `docs/08-feed-2026.md` (perfil quase parado desde setembro; jul–ago virou catálogo de ativos).

- **Padrão visual proposto** (base 2º semestre de 2025 + marinho `#102140`): `docs/09-padrao-visual.md`. Fontes gratuitas em `grade/assets/fonts/` (Playfair Display, Poppins, IBM Plex Mono, Archivo Black).
- **Decisão de 08/11:** sem rosto da marca e sem sessão de fotos por ora, as imagens serão geradas por IA, com as regras da seção 11 do padrão. Automação "comente PALAVRA" (ManyChat) fica para depois.
- **Teste do padrão com IA** (5 artes): `grade/teste-padrao-2025/`. Ricardo aprovou a direção. A arte com produto (D) **não passou**: virou o procedimento `docs/10-insercao-de-produto.md`. Para a 1ª arte com produto: medidas com régua e 6 fotos do Peptistrong (3 ângulos × luz dos dois lados).
- **Linha editorial (08/11):** polemizar os temas; **queda de cabelo é o foco**, depois perda de massa magra, falta de zinco e visão (seção 13 do padrão, com os limites de saúde).

## Decisões tomadas

- Acesso por **duas APIs**: login do Instagram para publicar e ler; login do Facebook para anúncios.
- Usuário do sistema **Funcionário** (BM não verificado só permite 1 administrador de sistema).
- **Ninguém é publicado sem aprovação.** A rotina só publica blocos marcados como Aprovado.
- Grade como **Artifact** enquanto o portal não está no ar.
