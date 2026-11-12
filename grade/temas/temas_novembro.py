# Base de temas para a triagem da campanha de novembro/2026 (aba Temas da Grade no portal).
# Campos: grupo, camada, tema, gancho, sugestao (stories|feed|ambos), produto_id (VTEX) ou None, saude (livre|revisao|educativo), data_ref
# Regras: feed não leva produto do site (decisão do Ricardo, 12/11); produto só em stories, com link.
# saude: "revisao" = precisa da revisão farmacêutica antes de aprovar; "educativo" = tema de medicamento sob prescrição, sem link e sem oferta.
import json, sys
T = []
def t(grupo, camada, tema, gancho, sug="ambos", prod=None, saude="livre", data=None):
    T.append(dict(grupo=grupo, camada=camada, tema=tema, gancho=gancho, sugestao=sug, produto_id=prod, saude=saude, data_ref=data))

# ---------- TOPO: magnésio ----------
G="Topo · Magnésio"
t(G,"topo","Magnésio e sono","Dormir 8 horas e acordar cansado: o problema pode não ser o tempo de sono.","ambos",1165)
t(G,"topo","Tipos de magnésio: por que não é tudo igual","Quelato, treonato, glicinato, inositol: o nome depois de 'magnésio' muda tudo.","feed")
t(G,"topo","Magnésio treonato e foco","O magnésio que é estudado por chegar ao cérebro.","stories",1216,"revisao")
t(G,"topo","Magnésio e cãibras","Cãibra de madrugada não é só falta de banana.","stories",1149)
t(G,"topo","Café, estresse e magnésio","Quem toma muito café e vive no estresse gasta mais magnésio do que imagina.","ambos",1149)
t(G,"topo","Magnésio inositol","Magnésio + inositol: a dupla que aparece cada vez mais nas fórmulas femininas.","stories",100295,"revisao")
t(G,"topo","Sinais de magnésio baixo","Pálpebra tremendo, cãibra, irritação: o corpo dá recados.","stories",None)
t(G,"topo","Alimentos ricos em magnésio","Cacau, castanhas, folhas verdes: o prato também conta.","feed")
t(G,"topo","Magnésio no treino","Treina pesado e não recupera? O mineral esquecido do pós-treino.","stories",1165)
t(G,"topo","Mito: magnésio engorda?","Não. Mas o mito circula por um motivo curioso.","stories")

# ---------- TOPO: queda de cabelo ----------
G="Topo · Queda de cabelo"
t(G,"topo","Queda sazonal de cabelo","Seu cabelo cai mais em certas épocas do ano. Isso tem nome.","ambos")
t(G,"topo","Keranat: o que é","O ativo de origem vegetal que virou queridinho de quem cuida do fio por dentro.","ambos",28003,"revisao")
t(G,"topo","Biotina: quando faz sentido","Biotina não é milagre, mas tem hora certa para entrar.","stories",1073,"revisao")
t(G,"topo","Zinco e cabelo","Falta de zinco também aparece no ralo do banheiro.","stories",1076,"revisao")
t(G,"topo","Ferro e queda de cabelo","Queda difusa em mulheres: o ferro precisa ser investigado.","feed",None,"revisao")
t(G,"topo","Estresse e queda (eflúvio)","O cabelo cai 2 a 3 meses depois do estresse. Por isso ninguém liga uma coisa à outra.","ambos")
t(G,"topo","Minoxidil: o que é e por que exige prescrição","Minoxidil não é cosmético de prateleira. Entenda.","feed",None,"educativo")
t(G,"topo","Couro cabeludo: a pele que você esquece","Cuidar do fio sem cuidar do couro cabeludo é começar pelo fim.","ambos")
t(G,"topo","Pill Food: o que tem dentro","Vitaminas e aminoácidos para o fio: leia a composição antes de escolher.","stories",7006,"revisao")
t(G,"topo","Cabelo e proteína","Dieta pobre em proteína cobra a conta no cabelo.","feed")
t(G,"topo","Queda pós-parto","É comum, assusta e costuma passar. Mas merece acompanhamento.","feed",None,"revisao")
t(G,"topo","Cabelo, cloro e sol","Verão chegando: piscina e sol também envelhecem o fio.","stories")

# ---------- TOPO: massa magra ----------
G="Topo · Massa magra"
t(G,"topo","Perda de massa magra depois dos 40","A partir dos 30, perdemos músculo todo ano. Silenciosamente.","ambos")
t(G,"topo","Peptistrong: peptídeos de colágeno para músculo","Nem todo colágeno é para pele.","ambos",50003,"revisao")
t(G,"topo","Dieta restritiva e músculo","Emagrecer perdendo músculo é trocar um problema por outro.","feed")
t(G,"topo","Proteína no café da manhã","O café da manhã brasileiro quase não tem proteína.","stories",50003)
t(G,"topo","HMB/KIC e preservação muscular","O que a ciência diz sobre preservar músculo em fases de restrição.","stories",1213,"revisao")
t(G,"topo","Sarcopenia","A palavra difícil que define quem perde força ao envelhecer.","feed",None,"revisao")
t(G,"topo","Creatina não é só para atleta","Idosos, mulheres, cérebro: a creatina saiu da academia.","stories")
t(G,"topo","Músculo e glicemia","Músculo é o maior consumidor de glicose do corpo.","feed")

# ---------- TOPO: zinco e visão ----------
G="Topo · Zinco"
t(G,"topo","Falta de zinco: sinais","Unha com manchas brancas, paladar estranho, feridas que demoram a fechar.","ambos",1076,"revisao")
t(G,"topo","Zinco e imunidade","Mineral pequeno, papel enorme na defesa do corpo.","stories",1076)
t(G,"topo","Zinco e pele oleosa","A relação entre zinco e acne que pouca gente conhece.","stories",1076,"revisao")
t(G,"topo","Zinco em excesso também faz mal","Mais não é melhor: o equilíbrio com o cobre.","feed",None,"revisao")
G="Topo · Visão"
t(G,"topo","Telas e cansaço visual","8 horas de tela por dia e o olho pede socorro.","ambos")
t(G,"topo","Luteína e zeaxantina","Os pigmentos que funcionam como filtro natural da retina.","feed",None,"revisao")
t(G,"topo","Astaxantina e olhos","O carotenoide que dá a cor rosa ao salmão também é estudado para a visão.","stories",1117,"revisao")
t(G,"topo","Olho seco e ômega 3","Olho seco no ar-condicionado: a gordura certa importa.","stories",6000,"revisao")
t(G,"topo","Regra 20-20-20","A cada 20 minutos, 20 segundos olhando a 20 pés. Simples e esquecida.","stories")

# ---------- TOPO: GHK-Cu e longevidade ----------
G="Topo · GHK-Cu e tendências"
t(G,"topo","GHK-Cu: o peptídeo de cobre","O ativo que domina os laboratórios de skincare e já chegou à manipulação.","ambos",None,"revisao")
t(G,"topo","GHK-Cu: sérum de marca x manipulado","O mesmo ativo, em concentração personalizada.","feed",None,"revisao")
t(G,"topo","NAD+ e longevidade","Por que todo mundo fala de NAD+ agora.","ambos",1141,"revisao")
t(G,"topo","Resveratrol","O composto da uva que virou símbolo de longevidade.","stories",1083,"revisao")

# ---------- CALENDÁRIO DE NOVEMBRO ----------
G="Calendário · Novembro Azul"
t(G,"calendario","Novembro Azul: homem também se cuida","Ir ao médico não é sinal de fraqueza.","ambos",None,"livre","2026-11-17")
t(G,"calendario","Próstata: o que todo homem precisa saber","Exame não é tabu.","feed",None,"revisao","2026-11-17")
t(G,"calendario","Saw palmetto","A planta mais estudada na saúde masculina.","stories",100301,"revisao","2026-11-18")
t(G,"calendario","Testosterona baixa: sinais","Cansaço, libido baixa, perda de músculo: investigue.","feed",None,"revisao","2026-11-19")
t(G,"calendario","Zinco e saúde masculina","O mineral que aparece em todo protocolo masculino.","stories",1076,"revisao","2026-11-18")
t(G,"calendario","Homem, sono e estresse","Homem também tem insônia e ansiedade.","stories",None,"livre","2026-11-21")
t(G,"calendario","Licopeno","O pigmento do tomate e a saúde masculina.","stories",1171,"revisao","2026-11-20")
t(G,"calendario","Maca peruana","A raiz andina da energia e da disposição.","stories",1103,"revisao","2026-11-19")
G="Calendário · Dia Mundial do Diabetes (14/11)"
t(G,"calendario","Dia Mundial do Diabetes","Diabetes tipo 2 pode ser silencioso por anos.","ambos",None,"livre","2026-11-14")
t(G,"calendario","Canela e glicemia: mito ou verdade","O que a ciência sabe sobre a canela.","stories",1059,"revisao","2026-11-14")
t(G,"calendario","Fibras e o pico de glicose","A ordem dos alimentos no prato muda o pico de açúcar.","feed",None,"livre","2026-11-14")
t(G,"calendario","Picolinato de cromo","O mineral associado à vontade de doce.","stories",1031,"revisao","2026-11-15")
t(G,"calendario","Berberina","A berberina na mira da ciência.","stories",1065,"revisao","2026-11-15")
t(G,"calendario","Diabetes e cuidado com os pés","Um cuidado diário que evita grandes problemas.","stories",None,"livre","2026-11-14")
G="Calendário · Consciência Negra (20/11)"
t(G,"calendario","Cabelo crespo e cacheado: cuidados","Cada curvatura pede um cuidado.","ambos",None,"livre","2026-11-20")
t(G,"calendario","Pele negra e vitamina D","Mais melanina, mais necessidade de sol para produzir vitamina D.","feed",None,"revisao","2026-11-20")
t(G,"calendario","Pele negra também precisa de protetor solar","Mito: pele negra não queima.","stories",None,"livre","2026-11-20")
t(G,"calendario","Manchas e hiperpigmentação","Manchas na pele negra pedem ativos certos.","stories",None,"revisao","2026-11-21")
G="Calendário · Verão chegando"
t(G,"calendario","Protetor solar oral (Polypodium)","Fotoproteção por dentro complementa, não substitui o protetor.","ambos",1084,"revisao","2026-11-23")
t(G,"calendario","Hidratação no calor","Sede já é sinal de desidratação.","stories",None,"livre","2026-11-24")
t(G,"calendario","Inchaço no calor","Pernas inchadas no verão: circulação pede atenção.","stories",1022,"revisao","2026-11-25")
t(G,"calendario","Pele e antioxidantes no verão","Sol, poluição e radicais livres.","stories",1117,"revisao","2026-11-26")
t(G,"calendario","Corpo de verão sem terrorismo","Pressa para o verão é a pior conselheira.","feed",None,"livre","2026-11-27")
t(G,"calendario","Probióticos e viagem","Intestino em viagem: preparar antes.","stories",5008,"revisao","2026-11-28")
G="Calendário · Fim de ano"
t(G,"calendario","Estresse de fim de ano","Dezembro começa em novembro no corpo.","ambos",1087,"revisao","2026-11-29")
t(G,"calendario","Adaptógenos: ashwagandha e rhodiola","Plantas que ajudam o corpo a lidar com o estresse.","stories",1086,"revisao","2026-11-29")
t(G,"calendario","Digestão nas festas","Prepare o fígado para dezembro.","stories",1147,"revisao","2026-11-30")

# ---------- MEIO: receitas, varejo, institucional, tendências ----------
G="Meio · Receitas"
t(G,"meio","Receita: Piña Colada proteica","Sobremesa de verão com Peptistrong.","ambos",50003)
t(G,"meio","Receita: café proteico gelado","O café gelado que vira lanche.","ambos",50003)
t(G,"meio","Receita: mousse de cacau proteica","Doce de fim de tarde com proteína.","ambos",50003)
t(G,"meio","Receita: smoothie verde com spirulina","Verde, gelado e cheio de nutrientes.","stories",1048)
t(G,"meio","Receita: overnight oats com colágeno","Café da manhã que fica pronto enquanto você dorme.","stories",1150)
t(G,"meio","Receita: chá gelado de hibisco","Refresco de verão sem açúcar.","stories",1017)
t(G,"meio","Receita: golden milk (cúrcuma e gengibre)","A bebida dourada da noite.","stories",1010)
G="Meio · Varejo e lançamentos"
t(G,"meio","Moccacino: o que é","Bebida pronta da nossa linha.","stories",28001)
t(G,"meio","Clonapure","Conheça o Clonapure.","stories",28002,"revisao")
t(G,"meio","Ômega 3: como escolher","EPA, DHA e a concentração que importa.","ambos",6007,"revisao")
t(G,"meio","Óleos em cápsula: linhaça, borage, coco","Cada óleo tem uma indicação.","stories",6003)
t(G,"meio","Tinturas: o que são","Extratos de plantas em gotas.","stories",9023)
t(G,"meio","Probióticos: cada cepa uma função","Não existe 'o' probiótico.","ambos",5006,"revisao")
t(G,"meio","Akkermansia: a bactéria da vez","A bactéria que virou estrela das pesquisas do intestino.","ambos",5022,"revisao")
G="Meio · Institucional"
t(G,"meio","ISO 9001: o que muda para você","Certificação de qualidade na prática da manipulação.","ambos")
t(G,"meio","Como nasce uma fórmula manipulada","Da receita à cápsula: bastidores.","feed")
t(G,"meio","Controle de qualidade na manipulação","Cada lote conferido.","stories")
t(G,"meio","Fale com a farmacêutica","Dúvida sobre suplemento? Pergunte antes de comprar.","stories")
t(G,"meio","Entrega e retirada","Como pedir pelo site e pelo WhatsApp.","stories")
t(G,"meio","Manipulado x industrializado","Dose personalizada: o que significa.","feed")
G="Meio · Tendências e luxo"
t(G,"meio","Cosmético coreano e manipulação","Ativos da K-beauty que a manipulação já faz.","ambos",None,"revisao")
t(G,"meio","Sérum de luxo: o que tem dentro","Pagar pela marca ou pelo ativo?","feed",None,"revisao")
t(G,"meio","Colágeno: tipos I, II e peptídeos","Colágeno não é tudo igual.","ambos",1069,"revisao")
t(G,"meio","Ácido hialurônico oral","Hidratação de dentro para fora.","stories",1072,"revisao")
t(G,"meio","Glutationa","O antioxidante mestre do corpo.","stories",1159,"revisao")
t(G,"meio","Beleza de dentro para fora","Nutricosméticos: o que tem evidência.","feed",None,"revisao")

# ---------- BASE: bem-estar geral ----------
G="Base · Sono e mente"
t(G,"base","Melatonina vegetal","A melatonina de origem vegetal.","stories",1203,"revisao")
t(G,"base","Higiene do sono","Rotina antes de deitar vale mais que qualquer cápsula.","feed")
t(G,"base","Ansiedade e respiração","Exercício de 1 minuto para baixar a ansiedade.","stories")
t(G,"base","Passiflora e melissa","Chás e plantas calmantes tradicionais.","stories",1091,"revisao")
t(G,"base","L-teanina","O aminoácido do chá verde e a calma com foco.","stories",1040,"revisao")
t(G,"base","Memória e foco","Esquecimento no dia a dia: quando se preocupar.","feed",None,"revisao")
t(G,"base","Bacopa monnieri","A planta ayurvédica estudada para memória.","stories",1173,"revisao")
G="Base · Intestino e digestão"
t(G,"base","Intestino preso","Fibra sem água não resolve.","stories",1043)
t(G,"base","Eixo intestino-cérebro","O intestino conversa com o cérebro.","feed")
t(G,"base","Intolerância à lactose","Lactase em cápsula: para quem serve.","stories",1130)
t(G,"base","Fígado gordo","O fígado também engorda.","feed",None,"revisao")
t(G,"base","Boldo e alcachofra","Clássicos da digestão.","stories",1053)
G="Base · Imunidade"
t(G,"base","Vitamina C","Quanto é suficiente?","stories",1120)
t(G,"base","Imunidade e sono","Quem dorme mal adoece mais.","stories")
t(G,"base","Própolis","O antibiótico das abelhas? Entenda.","stories",9007,"revisao")
t(G,"base","Epicor e beta-glucana","Ativos de imunidade da nova geração.","stories",1115,"revisao")
G="Base · Articulações e mobilidade"
t(G,"base","Dor no joelho e colágeno tipo II","O colágeno das articulações.","stories",1069,"revisao")
t(G,"base","Movimento é remédio","Articulação parada enferruja.","feed")
t(G,"base","Boswellia","Planta tradicional para articulações.","stories",1116,"revisao")
G="Base · Energia e metabolismo"
t(G,"base","Cansaço constante","Cansaço não é normal. Investigue.","feed",None,"revisao")
t(G,"base","Vitamina B12 e vegetarianos","Quem não come carne precisa olhar para a B12.","stories",1162,"revisao")
t(G,"base","Coenzima Q10","A energia das células.","stories",1082,"revisao")
t(G,"base","Termogênicos: o que esperar","Termogênico não emagrece sozinho.","feed",None,"revisao")
t(G,"base","Chá verde e matcha","Cafeína com calma.","stories",1041)
t(G,"base","Retenção de líquido","Inchaço não é gordura.","stories",1021,"revisao")
G="Base · Saúde da mulher"
t(G,"base","Menopausa e calorões","A transição que ninguém explica direito.","feed",None,"revisao")
t(G,"base","TPM","Sintomas que não precisam ser normais.","stories",1088,"revisao")
t(G,"base","Ferro e cansaço feminino","Menstruação intensa e ferro baixo.","stories",1161,"revisao")
t(G,"base","Libido feminina","Tema pouco falado, muito comum.","stories",1152,"revisao")
G="Base · Pele e unhas"
t(G,"base","Unhas fracas","A unha mostra a nutrição.","stories",1210,"revisao")
t(G,"base","Celulite","Celulite tem graus e não é falta de cuidado.","stories",1035,"revisao")
t(G,"base","Pele seca no ar-condicionado","Hidratação por fora e por dentro.","stories",1072)
t(G,"base","Acne adulta","Espinha depois dos 25: por quê?","feed",None,"revisao")
G="Base · Coração"
t(G,"base","Colesterol e ômega 3","Gordura boa contra gordura ruim.","stories",6000,"revisao")
t(G,"base","Pressão e sal escondido","O sal que você não vê.","feed")
t(G,"base","Circulação e varizes","Pernas pesadas no fim do dia.","stories",1022,"revisao")

json.dump(T, sys.stdout, ensure_ascii=False)
