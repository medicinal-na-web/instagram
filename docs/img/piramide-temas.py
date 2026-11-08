"""Gera docs/img/piramide-temas.png (rodar na raiz do repositório)."""
import sys; sys.path.insert(0,'grade')
from PIL import Image, ImageDraw, ImageFont
import marca
F='grade/assets/fonts/'
def V(n,s,v=None):
    f=ImageFont.truetype(F+n,s)
    if v: f.set_variation_by_name(v)
    return f
serif=V('PlayfairDisplay.ttf',64,'Regular'); ital=V('PlayfairDisplay-Italic.ttf',32,'Bold Italic')
caps=lambda s: V('Poppins-Bold.ttf',s); mono=V('IBMPlexMono-Regular.ttf',24); fi=V('Poppins-Bold.ttf',22)
NAVY=(16,33,64); NAVY2=(28,52,94); OFF=(238,231,218); CAR=(191,145,98); AREIA=(224,190,151); QP=(40,22,18)
W,H=1600,1500
im=Image.new('RGB',(W,H),OFF); d=ImageDraw.Draw(im)
marca.aplica(im,marca.logo('sem-simbolo','marinho',260),(70,60))
d.text((70,150),'Pirâmide de temas',font=serif,fill=NAVY)
d.text((72,235),'@medicinalnaweb · do mais importante (topo) ao geral (base)',font=mono,fill=NAVY2)
cx=800; top=320; base=1390
def hw(yy): return 290+(yy-top)/(base-top)*470
camadas=[('TOPO','prioridade máxima · ~45% do feed',NAVY,OFF,CAR,['Ativos foco: Peptistrong · Keranat · GHK-Cu · Magnésio','Temas que polemizam: queda de cabelo (foco),','perda de massa magra, zinco, visão','Lançamentos da linha']),
         ('MEIO','reforço da marca · ~35% do feed',NAVY2,OFF,CAR,['Receitas com produtos da linha','Produtos de varejo da linha','Vídeos institucionais (manipulação, equipe, ISO)','Tendências magistrais · "O ativo por trás de…"']),
         ('BASE','temas gerais · ~20% do feed',AREIA,QP,NAVY,['Datas e sazonalidade · eventos e parceiros','Bem-estar geral · perguntas do balcão','Inspiração de luxo · bastidores do dia a dia','Avisos e institucional da loja'])]
y=top
for (nome,sub,cor,tc,sc,itens),h in zip(camadas,(345,345,360)):
    y0,y1=y,y+h
    d.polygon([(cx-hw(y0),y0),(cx+hw(y0),y0),(cx+hw(y1),y1),(cx-hw(y1),y1)],fill=cor)
    f=caps(32); w=d.textlength(nome,font=f); d.text((cx-w/2,y0+26),nome,font=f,fill=tc)
    w=d.textlength(sub,font=ital); d.text((cx-w/2,y0+70),sub,font=ital,fill=sc)
    for i,it in enumerate(itens):
        w=d.textlength(it,font=fi); d.text((cx-w/2,y0+135+i*38),it,font=fi,fill=tc)
    y=y1+8
d.text((70,H-60),'Rascunho para aprovação. Fonte: docs/12-fontes-e-temas.md',font=mono,fill=NAVY2)
im.save('docs/img/piramide-temas.png')
