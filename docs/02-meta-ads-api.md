# 14 — Meta Ads pela API de Marketing (caminho B)

Objetivo: criar campanhas, impulsionar posts e fazer **dark posts** (anúncios que não aparecem no perfil) pelo n8n, sem ferramenta de terceiros.

O token do Instagram (`docs/01-acesso-instagram.md`) **não serve** para isso: ele usa o login do Instagram, que não tem endpoints de anúncio. Anúncio exige a **API de Marketing**, com login do Facebook e token de **usuário do sistema**.

**Situação em 23/10/2026:** ✅ acesso validado (teste abaixo). Forma de pagamento ativa na conta de anúncios (confirmado pelo Ricardo).

```mermaid
flowchart LR
  BM[Business Manager<br/>Medicinal Farmácia E Manipulação] --> CA[Conta de anúncios<br/>act_...]
  BM --> P[Página do Facebook]
  P --- IG[@medicinalnaweb]
  BM --> APP[APP_clienteDM<br/>+ caso de uso Anúncios]
  BM --> SU[Usuário do sistema<br/>n8n-ads]
  CA --> SU
  P --> SU
  IG --> SU
  APP --> SU
  SU -->|token sem validade| N8N[Credencial n8n<br/>Site Medicinal - Meta Ads token]
  N8N -->|graph.facebook.com| CA
```

## Passo a passo (admin do Business Manager)

### 1. Conta de anúncios
- [x] business.facebook.com → **Configurações → Contas → Contas de anúncios**: confirmar que a conta da Medicinal está ali (ou criar uma).
- [x] Moeda **BRL**, fuso **America/Sao_Paulo**. Esses dois campos não mudam depois.
- [x] **Forma de pagamento** ativa (Cobrança e pagamentos). Sem ela, a API cria os anúncios, mas eles não rodam.

### 2. Página e Instagram
- [x] Página do Facebook da Medicinal em **Contas → Páginas**.
- [x] Instagram @medicinalnaweb ligado à Página (Página → Configurações → Contas vinculadas → Instagram).
- [x] @medicinalnaweb em **Contas → Contas do Instagram**, com a **conta de anúncios** marcada em "Ativos conectados". Conferido em 23/10/2026: Página "Medicinal Farmácia e Manipulação" e as duas contas "MEDICINAL Farmácia e Manipulação" conectadas.

### 3. App
- [x] developers.facebook.com → `APP_clienteDM`: em 23/10/2026 foram adicionadas `ads_management`, `ads_read`, `business_management`, `instagram_basic`, `pages_show_list` e `pages_read_engagement` no caso de uso da API do Instagram, e `pages_manage_ads` por um caso de uso de anúncios/Páginas (não aparece na lista da API do Instagram).
- [ ] O acesso padrão basta, porque só vamos mexer em contas da própria Medicinal. Não é preciso passar pela análise do app.

### 4. Usuário do sistema
- [ ] **Configurações → Usuários → Usuários do sistema → Adicionar**: nome `n8n-ads`, função **Administrador**.
- [ ] **Atribuir ativos**:
  - Conta de anúncios: **Gerenciar campanhas** (ou controle total)
  - Página: **Criar anúncios** e **Ver desempenho** (ou controle total)
  - Conta do Instagram: controle total
  - App `APP_clienteDM`: controle total
- [ ] **Gerar token**: app `APP_clienteDM`, validade **Nunca** e estas permissões:

| Permissão | Para quê |
|---|---|
| `ads_management` | criar e editar campanhas, conjuntos e anúncios |
| `ads_read` | ler campanhas e resultados |
| `business_management` | acessar os ativos do Business Manager |
| `pages_show_list` | listar a Página |
| `pages_read_engagement` | ler posts da Página |
| `pages_manage_ads` | anunciar em nome da Página (dark post) |
| `instagram_basic` | usar a conta do Instagram nos anúncios |

### 5. Credencial no n8n
- [ ] Tipo **Query Auth**, nome do parâmetro `access_token`, nome da credencial `Site Medicinal - Meta Ads (token)`.
- [ ] O token começa com **`EAA`**. Colar direto no n8n, nunca em chat, e-mail ou repositório.

## O que vem para este doc (não é segredo)

| Item | Valor |
|---|---|
| ID da conta de anúncios (`act_...`) | `act_707010962823594` (MEDICINAL Farmácia e Manipulação; 1.356 anúncios, vários em rascunho, em 23/10/2026) |
| ID da Página do Facebook | `551028704983998` (Medicinal Farmácia e Manipulação, ligada ao @medicinalnaweb `17841401675469982`) |
| ID do Business Manager | `706932469498110` (Medicinal Farmácia E Manipulação) |
| Outras contas de anúncios no BM | `ContaAnuncioAgencia02` (2801702060204971) e uma segunda "MEDICINAL Farmácia e Manipulação" (1499162510740083). Usar só a `act_707010962823594` |
| Usuário do sistema | `n8n-ads` (`122104724457514359`), função **Funcionário**: o BM não verificado só permite 1 admin de sistema, e a vaga já está ocupada |
| ID da credencial no n8n | `DoGhzs4iWUtxnXSp` (`Site Medicinal - Meta Ads (token)`, Query Auth) |

## Teste de acesso (somente leitura)

Workflow `Site Medicinal - Teste de acesso Meta Ads (inativo)`, gatilho manual, base `https://graph.facebook.com/v25.0`:

| # | Chamada | Confirma |
|---|---|---|
| 1 | `/me?fields=id,name` | o token do usuário do sistema funciona |
| 2 | `/me/adaccounts?fields=id,name,account_status,currency,timezone_name` | a conta de anúncios está atribuída, ativa e em BRL |
| 3 | `/me/accounts?fields=id,name,instagram_business_account` | a Página está atribuída e ligada ao @medicinalnaweb |
| 4 | `/act_{id}/campaigns?fields=id,name,status,objective&limit=5` | leitura de campanhas |

Dados de pagamento (`funding_source_details`) **não** são lidos.

Workflow `Site Medicinal - Teste de acesso Meta Ads (inativo)` (`0tsI5zGXKXckm9LN`).

**1ª execução (23/10/2026, nº 111835): ✅ tudo ok.**

| Passo | Resultado |
|---|---|
| Usuário do sistema | `n8n-ads` |
| Permissões concedidas | `ads_management`, `ads_read`, `business_management`, `instagram_basic`, `pages_show_list`, `pages_read_engagement`, `pages_manage_ads` (todas as 7) |
| Contas de anúncios visíveis | só `act_707010962823594`, ativa (`account_status=1`), BRL, America/Sao_Paulo |
| Página | `551028704983998`, ligada ao @medicinalnaweb |
| Token nas respostas | não (nenhuma resposta trouxe `paging.next` com `access_token`) |

Os usuários do sistema já existentes (`Conversions API System User`, `USERS_contatoCliente`) não foram alterados.

## Como cada tipo de anúncio sai pela API

| Tipo | Como | Observação |
|---|---|---|
| **Impulsionar post do Instagram** | criativo com `source_instagram_media_id` = ID do post | usa o post como está |
| **Dark post** | criativo com `object_story_spec` (`page_id` + `instagram_user_id` + imagem/texto/link) | roda no feed e nos stories, não aparece no perfil |
| **Campanha** | campanha → conjunto (público, orçamento, datas, posicionamentos) → anúncio | objetivo `OUTCOME_*` |

## Regras de operação

- Tudo é criado com `status=PAUSED`. Só ativar com **OK explícito** (regra 6), porque ativar gera gasto imediato.
- Cada criação traz um resumo para aprovação: objetivo, público, orçamento diário/total, datas, posicionamentos e prévia da arte.
- **Políticas da Meta para saúde:** nada de medicamento sob prescrição, promessa de cura ou de resultado, nem "antes e depois". Público com segmentação limitada em temas de saúde. Manipulados e suplementos: texto revisado pelo farmacêutico antes de ativar.
- LGPD: públicos personalizados a partir de listas de clientes só com base legal definida. Por enquanto, usar só segmentação geográfica/demográfica e públicos de engajamento do próprio perfil.
