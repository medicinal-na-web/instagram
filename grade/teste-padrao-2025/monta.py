# Monta 4 artes de teste do padrão (09-padrao-visual.md) sobre imagens de IA + produto real.
import sys,os
from PIL import Image,ImageDraw,ImageFont,ImageEnhance,ImageFilter,ImageChops
D=os.path.dirname(os.path.abspath(__file__)); R='/home/user/instagram/grade/assets/'
F=R+'fonts/'
NAVY='#102140'; OFF='#eee7da'; CAR='#bf9162'
def V(n,s,var=None):
  f=ImageFont.truetype(F+n,s)
  if var: f.set_variation_by_name(var)
  return f
serif=lambda s: V('PlayfairDisplay.ttf',s,'Regular'); ital=lambda s: V('PlayfairDisplay-Italic.ttf',s,'Bold Italic')
caps=lambda s: V('Poppins-Bold.ttf',s); mono=lambda s: V('IBMPlexMono-Regular.ttf',s); black=lambda s: V('ArchivoBlack.ttf',s)
def bg(f,dark=0.8,fy=0.5):
  im=Image.open(f).convert('RGB'); w,h=im.size; t=1080/1350
  if w/h>t: nw=int(h*t); im=im.crop(((w-nw)//2,0,(w-nw)//2+nw,h))
  else: nh=int(w/t); y0=int((h-nh)*fy); im=im.crop((0,y0,w,y0+nh))
  return ImageEnhance.Brightness(im.resize((1080,1350),Image.LANCZOS)).enhance(dark)
def grad(im,top=True,a=110):
  g=Image.new('L',(1,1350)); 
  for y in range(1350): g.putpixel((0,y),int(a*max(0,(1-y/700))) if top else int(a*max(0,(y-650)/700)))
  g=g.resize((1080,1350)); im.paste(Image.new('RGB',(1080,1350),(20,14,10)),(0,0),g); return im
def ctext(d,y,t,f,sp=0,fill='white'):
  ws=[d.textlength(c,font=f) for c in t]; w=sum(ws)+sp*(len(t)-1); x=(1080-w)/2
  for c,cw in zip(t,ws): d.text((x,y),c,font=f,fill=fill); x+=cw+sp
def logo(d,right=False,fill='white'):
  # Logotipo oficial: a palavra "medicinal" recortada do logo do site (assets/logo), nunca texto digitado.
  cor={'white':'branco','#ffffff':'branco',NAVY:'marinho',OFF:'off-white'}.get(fill,'branco')
  wm=Image.open(R+'logo/medicinal-palavra-%s.png'%cor); L=170; wm=wm.resize((L,int(wm.height*L/wm.width)),Image.LANCZOS)
  x=1080-60-L if right else 60
  d._image.paste(wm,(x,54),wm)
def grain(im,amt=10):
  n=Image.effect_noise((1080,1350),amt).convert('RGB'); return ImageChops.overlay(im,ImageEnhance.Brightness(n).enhance(1.0)) if False else Image.blend(im,ImageChops.add(im,n,2,-128),0.25)
def cutout(path):
  p=Image.open(path).convert('RGB'); g=p.convert('L')
  m=g.point(lambda v:255 if v>238 else 0)  # candidatos a fundo
  W,H=m.size
  for xy in [(0,0),(W-1,0),(0,H-1),(W-1,H-1),(W//2,0),(W//2,H-1),(0,H//2),(W-1,H//2)]:
    if m.getpixel(xy)==255: ImageDraw.floodfill(m,xy,128)
  m=m.point(lambda v:0 if v==128 else 255).filter(ImageFilter.GaussianBlur(1.0))
  bb=m.getbbox(); p=p.crop(bb); m=m.crop(bb); out=p.convert('RGBA'); out.putalpha(m); return out
cap,lent,plank,kitchen=sys.argv[1:5] if len(sys.argv)>4 else [os.path.join(D,"ia",n+".jpg") for n in ("capsula","lentilha","prancha","cozinha")]
arts=[]
# A frase de marca
im=grad(bg(cap,0.92,0.6),True,120); d=ImageDraw.Draw(im); logo(d)
ctext(d,200,'por trás de cada fórmula',serif(72),sp=-3); ctext(d,285,'existe um',serif(72),sp=-3); ctext(d,358,'farmacêutico.',ital(108),sp=-3)
d.text((60,1250),'(que confere tudo antes de chegar até você)',font=V('Poppins-Bold.ttf',22),fill='white'); arts.append(('A-frase',im))
# B radar
im=bg(lent,0.7); d=ImageDraw.Draw(im)
ctext(d,610,'RADAR MAGISTRAL',caps(50),sp=13); ctext(d,680,'PEPTIPUMP',caps(50),sp=13); arts.append(('B-radar',im))
# C pergunta
im=grad(bg(plank,0.85,0.5),True,140); d=ImageDraw.Draw(im); logo(d,True)
for i,t in enumerate(['Por que a massa muscular','merece atenção depois dos 40?']):
  f=mono(38); w=d.textlength(t,font=f); x=(1080-w)/2; y=170+i*56; d.text((x,y),t,font=f,fill='white'); d.line((x,y+48,x+w,y+48),fill='white',width=2)
ctext(d,300,'PRESERVAÇÃO',caps(66),sp=9); ctext(d,380,'MUSCULAR',caps(66),sp=9); arts.append(('C-pergunta',im))
# D produto real na cena: ia/v5/cena_com_lata.jpg = cena sob medida + foto real da lata (IC-Light) + insere_foto; validação em ia/v5/v5_validacao.md
im=grad(bg(os.path.join(D,'ia','v5','cena_com_lata.jpg'),0.98,0.25),True,130); d=ImageDraw.Draw(im); logo(d)
ctext(d,150,'a rotina de quem',serif(72),sp=-3); ctext(d,232,'cuida do',serif(72),sp=-3); ctext(d,305,'músculo.',ital(108),sp=-3); arts.append(('D-produto',im))
# E numero marinho
im=Image.new('RGB',(1080,1350),NAVY); d=ImageDraw.Draw(im); logo(d,fill=OFF)
ctext(d,330,'DEPOIS DOS 30,',caps(42),sp=8,fill=OFF); ctext(d,392,'A MASSA MUSCULAR',caps(42),sp=8,fill=OFF)
ctext(d,480,'3-8%',black(250),fill=OFF); ctext(d,790,'a menos',ital(104),sp=-2,fill=CAR); ctext(d,895,'por década.',ital(104),sp=-2,fill=CAR)
d.text((60,1250),'Fonte na legenda.',font=mono(26),fill=OFF); arts.append(('E-numero',im))
for n,a in arts: a.save(os.path.join(D,n+'.jpg'),quality=92)
# grade 3 colunas como no perfil
order=['A-frase','B-radar','E-numero','C-pergunta','D-produto']
S=360;H=480; W=Image.new('RGB',(S*3+8,(H+4)*2),'white')
for i,n in enumerate(order):
  a=Image.open(os.path.join(D,n+'.jpg')).resize((S,H)); W.paste(a,((i%3)*(S+4),(i//3)*(H+4)))
W.save(os.path.join(D,'grade-teste.jpg'),quality=90)
B=Image.new('RGB',(5*545+10,690),'#f6f2ec')
for i,(n,a) in enumerate(arts): B.paste(a.resize((540,675)),(5+i*545,8))
B.save(os.path.join(D,'artes-teste.jpg'),quality=90)
print('ok')
