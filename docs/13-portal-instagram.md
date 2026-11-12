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
