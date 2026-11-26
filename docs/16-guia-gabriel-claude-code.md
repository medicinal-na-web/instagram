# Guia do Gabriel no Claude Code · 26/11/2026

Para quê: produzir as peças que a plataforma (Grade) não faz sozinha, com o Claude seguindo as regras do projeto. Exemplos: arte no padrão a partir de foto real, slide de dados, texto sobre vídeo, legenda a partir de PDF de fornecedor.
O Code **produz**. **Publicar** continua sendo pela Grade: o Gabriel sobe o arquivo no bloco, confere o checklist e aprova (`15-guia-operador-plataforma.md`).

## Parte 1 · O que o Ricardo faz antes (uma vez)
1. **Conta Claude do Gabriel:** convidar mkt@atendimentomedicinal.net para a organização no claude.ai, num plano que inclua o Claude Code.
2. **GitHub:**
   - o Gabriel cria uma conta no GitHub;
   - o Ricardo o adiciona como colaborador do repositório `medicinal-na-web/instagram` (Settings → Collaborators) com permissão **Write**.
3. **Proteger a branch principal (a trava das regras):**
   - em Settings → Branches → Add rule para `main`;
   - marcar "Require a pull request before merging" e "Require approvals";
   - assim, mudança em regra (`CLAUDE.md`, `docs/`, scripts de padrão) só entra com aprovação do Ricardo.
4. **Runway:** decidir se o Gabriel usa a conta da Medicinal (créditos compartilhados) ou uma conta própria.

## Parte 2 · Primeiro acesso do Gabriel (uma vez)
1. Entrar em **claude.ai** com o e-mail mkt@ e abrir **Code** (claude.ai/code).
2. **Conectar o GitHub:** em https://claude.ai/connect-github, entrar com a conta GitHub dele e autorizar.
3. **Conectores:** em Configurações → Conectores, ligar **somente**:
   - **Runway**, para gerar imagem;
   - **Google Drive** (opcional), para buscar fotos de produto.
4. **Não ligar** Supabase, n8n, Gmail nem outros. O Claude só alcança o que estiver conectado: é isso que impede mexer em banco, workflows, site e acessos.

## Parte 3 · Cada sessão de trabalho
1. **Nova sessão** no Code → escolher o repositório **medicinal-na-web/instagram** → ambiente padrão.
2. **Primeira mensagem** (copiar e colar):
   > Sou o Gabriel, operador do Instagram. Leia o CLAUDE.md, o CONTEXTO.md, o docs/09-padrao-visual.md e o docs/15-guia-operador-plataforma.md. Hoje vou preparar as peças de [data]. Não use Supabase nem n8n; as peças eu subo pela Grade.
3. **Pedir as peças**, uma por vez, com a ideia, a data, o canal (feed ou story) e o material. Exemplos:
   - "Feed de sexta 28/11, tema bastidores: arte no padrão com esta foto real [anexar] e a frase 'a fórmula nasce na *bancada.*'. Faça também o story do post."
   - "Leia este PDF do fornecedor [anexar] e proponha 3 frases e uma legenda sem promessa de resultado."
   - "Ponha o texto no padrão sobre este vídeo [anexar], passo 1: … passo 2: …"
4. **Conferir:** o Claude mostra a imagem. Pedir ajustes até ficar no padrão (checklist do guia 15).
5. **Baixar a peça:** pedir "me envie o arquivo final".
6. **Na Grade:** abrir o bloco (Rascunho) → **Enviar arquivo** → frase, legenda, palavra-chave e link → checklist → **Aprovar**.
7. **Fechar a sessão:** pedir "faça commit e push na branch desta sessão". Não pedir merge na `main`: isso é com o Ricardo.

## O que NÃO pedir ao Claude
- Mexer em banco, n8n, site, VTEX, acessos ou na publicação automática.
- Mudar regra ou padrão visual (`CLAUDE.md`, `docs/09`, scripts de `grade/padrao/`). Sugestão de mudança vai para o Ricardo.
- Usar dados, fotos, comentários ou directs de clientes (LGPD).
- Gerar embalagem de produto com IA ou mockup. Produto aparece só com foto real.
- Promessa de efeito ou cura, antes e depois, medicamento de receita como oferta, e "farmacêutica" em chamada.

## Quando chamar o Ricardo
- Dúvida de saúde, produto, preço ou promoção.
- Produto inserido em cena e vídeo de receita com personagem: o Ricardo revisa antes de aprovar.
- O Claude disser que algo está fora do padrão ou contra uma regra, e você achar que precisa ser feito mesmo assim.
- Qualquer erro de acesso (GitHub, Runway).

## Limites atuais
- **Vídeo e reels:** saem à mão no Instagram. A rotina automática publica só imagem.
- **Runway:** a geração de vídeo está indisponível enquanto a conta estiver no plano gratuito.
