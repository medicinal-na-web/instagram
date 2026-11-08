# Identidade azul-marinho/branco/cinza com foto: foto em cima, texto embaixo em faixa branca.
import json, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
HERE=os.path.dirname(os.path.abspath(__file__))
BASE=os.path.join(HERE,'..')
F=os.path.join(BASE,'assets','fonts')+'/'
spec=json.load(open(sys.argv[1])); OUT=sys.argv[2]; FOTOS=sys.argv[3] if len(sys.argv)>3 else ''
os.makedirs(OUT,exist_ok=True)
NAVY=(16,33,64); NAVY2=(28,52,94); WHITE=(255,255,255); GRAY=(236,239,243); GRAY2=(120,130,145); INK=(22,30,44)
def font(w,s): return ImageFont.truetype(F+{'b':'poppins-latin-700-normal.woff','m':'poppins-latin-500-normal.woff','r':'poppins-latin-400-normal.woff'}[w],s)
def wrap(d,txt,f,maxw):
  out=[]
  for par in txt.split('\n'):
    cur=''
    for w in par.split(' '):
      t=(cur+' '+w).strip()
      if d.textlength(t,font=f)<=maxw: cur=t
      else:
        if cur: out.append(cur)
        cur=w
    out.append(cur)
  return out
pp=Image.open(os.path.join(BASE,'assets','peptistrong.jpg')).convert('RGB')
def foto(p,W,H):
  f=p.get('foto')
  if f=='peptistrong':
    bg=Image.new('RGB',(W,H),WHITE); prod=pp.copy(); prod.thumbnail((int(W*0.75),int(H*0.92)))
    bg.paste(prod,((W-prod.width)//2,(H-prod.height)//2)); return bg
  path=os.path.join(FOTOS,(f or '')+'.jpg')
  if f and os.path.exists(path): return ImageOps.fit(Image.open(path).convert('RGB'),(W,H),Image.LANCZOS)
  ph=Image.new('RGB',(W,H),NAVY2); d=ImageDraw.Draw(ph)
  for i in range(-H,W,60): d.line([(i,0),(i+H,H)],fill=NAVY,width=18)
  d.text((40,H-70),'[foto: '+(f or 'a definir')+']',font=font('m',30),fill=(170,185,210)); return ph
def peca(p):
  story=p['canal']=='story'; W,H=(1080,1920) if story else (1080,1350)
  im=Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(im)
  fh=int(H*(0.52 if story else 0.50))
  if p.get('so_texto'): fh=0
  if fh: im.paste(foto(p,W,fh),(0,0))
  # faixa da marca
  M=80; top=(230 if story else 0)
  if fh:
    bar=Image.new('RGBA',(W,110),NAVY+(225,)); im.paste(bar,(0,top),bar)
  d=ImageDraw.Draw(im)
  d.text((M,top+28),'medicinal',font=font('b',42),fill=WHITE if fh else NAVY)
  d.text((M+222,top+44),'FARMÁCIA E MANIPULAÇÃO',font=font('m',18),fill=(200,210,225) if fh else GRAY2)
  y=fh+50 if fh else top+170
  if p.get('kicker'):
    f=font('b',28); k=p['kicker'].upper(); tw=d.textlength(k,font=f)
    d.rectangle([M,y,M+tw+36,y+52],fill=NAVY); d.text((M+18,y+8),k,font=f,fill=WHITE); y+=80
  ft=font('b',(80 if story else 62)); 
  for ln in wrap(d,p['titulo'],ft,W-2*M): d.text((M,y),ln,font=ft,fill=NAVY); y+=int(ft.size*1.13)
  y+=18; fb=font('r',(46 if story else 36))
  if p.get('itens'):
    for it in p['itens']:
      d.rectangle([M,y+fb.size//2-4,M+16,y+fb.size//2+12],fill=NAVY2)
      for ln in wrap(d,it,fb,W-2*M-50): d.text((M+40,y),ln,font=fb,fill=INK); y+=int(fb.size*1.28)
      y+=8
  if p.get('texto'):
    for ln in wrap(d,p['texto'],fb,W-2*M): d.text((M,y),ln,font=fb,fill=INK); y+=int(fb.size*1.3)
  # rodapé
  fy=H-(330 if story else 110)
  d.line([(M,fy-24),(W-M,fy-24)],fill=GRAY,width=3)
  x=M
  if p.get('cta'):
    f=font('b',32); tw=d.textlength(p['cta'],font=f); d.rectangle([M,fy-6,M+tw+44,fy+54],fill=NAVY); d.text((M+22,fy+2),p['cta'],font=f,fill=WHITE)
  if p.get('nota'): d.text((M,fy+(70 if p.get('cta') else 0)),p['nota'],font=font('r',22),fill=GRAY2)
  if p.get('slide'): d.text((W-M-70,fy+6),p['slide'],font=font('m',30),fill=GRAY2)
  if y>fy-30: print('AVISO texto longo',p['arquivo'],y,fy)
  return im
for p in spec: peca(p).save(os.path.join(OUT,p['arquivo']),quality=90)
print('ok',len(spec))
