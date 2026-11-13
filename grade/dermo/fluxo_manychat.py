"""Gera o roteiro (para o Claude no navegador) do fluxo do ManyChat de UM Dermo-day, a partir de fluxos/<data>-<ativo>.json.
Regras fixas: nunca citar "farmacêutica"; respostas ficam só no ManyChat (LGPD); fluxo criado PAUSADO; um fluxo por Dermo-day.
Uso: python3 -I fluxo_manychat.py fluxos/2026-11-25-retinal.json > roteiro.txt
"""
import json, sys
f = json.load(open(sys.argv[1])); b = lambda xs: " · ".join(f"[{x}]" for x in xs)
print(f"""TAREFA: criar no ManyChat (Instagram @medicinalnaweb) o fluxo do DERMO-DAY de {f['data']} ({f['ativo']}).
Nome da automação: "{f['nome_fluxo']}". Um fluxo por Dermo-day: NÃO edite os fluxos de outras datas.

REGRAS
- Não apagar nem alterar outras automações. Não abrir nem copiar conversas de clientes.
- Nunca escrever "farmacêutica" ou "farmacêutico" nas mensagens.
- Se pedir pagamento/upgrade, PARE e me avise.
- Criar PAUSADO. Ao final, mande prints de cada etapa do fluxo.

GATILHO
- Instagram > Keyword: mensagem CONTÉM "dermo" (resposta de story, comentário no post do feed via "Post or Reel Comments" e direct).
- No gatilho de comentário: responder publicamente "Te chamei no direct ✨" e abrir o direct.
- Ativação: este fluxo fica LIGADO de {f['data']} (quarta) até a terça seguinte; o fluxo do Dermo-day anterior é PAUSADO no mesmo momento.

CAMPOS (criar se não existirem; tipo Text): dermo_retinoide, dermo_pele, dermo_objetivo, dermo_gestacao, dermo_textura, dermo_rotina.
TAGS: {", ".join(f['tags'])}.

FLUXO (Send Message com botões de resposta rápida; cada botão salva no campo indicado)
1. "{f['boas_vindas']}"
   "{f['convite']}"  Botões: [Bora!] · [Só quero saber o preço]
   - [Só quero saber o preço] -> "{f['msg_preco']}" -> segue para a pergunta 2.
2. "{f['pergunta_retinoide']}"  {b(f['opcoes_retinoide'])}  -> dermo_retinoide
   - [{f['opcoes_retinoide'][2]}] -> "{f['msg_receita']}" -> tag dermo-receita -> ir para HANDOFF.
3. "{f['pergunta_pele']}"  {b(f['opcoes_pele'])}  -> dermo_pele
   - [Sensível] -> "{f['msg_sensivel']}" -> segue.
4. "{f['pergunta_objetivo']}"  {b(f['opcoes_objetivo'])}  -> dermo_objetivo
5. "{f['pergunta_gestacao']}"  {b(f['opcoes_gestacao'])}  -> dermo_gestacao
   - [Sim] -> "{f['msg_gestacao']}" -> tag dermo-alternativa -> ir para HANDOFF.
6. "{f['pergunta_textura']}"  {b(f['opcoes_textura'])}  -> dermo_textura
7. "{f['pergunta_rotina']}"  {b(f['opcoes_rotina'])}  -> dermo_rotina
8. "{f['resumo']}"
   "{f['pergunta_final']}"  {b(f['opcoes_final'])}
   - [{f['opcoes_final'][0]}] -> "{f['msg_quero']}" -> HANDOFF.
   - [{f['opcoes_final'][1]}] -> "{f['msg_duvida']}" -> aguardar texto livre -> HANDOFF.

HANDOFF: adicionar as tags; abrir a conversa para Live Chat (atendimento humano) e notificar a equipe.
FORA DO HORÁRIO (antes das 8h ou depois das 18h, e domingo): após o HANDOFF enviar "{f['fora_horario']}".
LEMBRETE: se a pessoa parar no meio, depois de 23 h (dentro da janela de 24 h do Instagram) enviar UMA vez: "{f['lembrete_23h']}" com o botão [Continuar], que retoma da pergunta em que parou.

TESTE: usar o Preview do ManyChat percorrendo os 4 caminhos: completo, preço, receita e gestante. Deixar PAUSADO e me mandar prints.""")
