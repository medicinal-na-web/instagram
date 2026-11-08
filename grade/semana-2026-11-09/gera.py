# Versão 1 das artes (temas por produto, sem foto). Uso: python3 gera.py pecas.json <saida>
import json, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE=os.path.dirname(os.path.abspath(__file__))
BASE=os.path.join(HERE,'..')
F=os.path.join(BASE,'assets','fonts')+'/'
OUT=sys.argv[2]; os.makedirs(OUT,exist_ok=True)
spec=json.load(open(sys.argv[1]))
def font(w,s): return ImageFont.truetype(F+{'b':'poppins-latin-700-normal.woff','m':'poppins-latin-500-normal.woff','r':'poppins-latin-400-normal.woff','s':'pacifico-latin-400-normal.woff'}[w],s)
TEMAS={
 'peptistrong':dict(bg=(18,18,18),bg2=(40,36,20),fg=(255,255,255),ac=(244,194,27),mut=(205,200,185)),
 'maxsolve':dict(bg=(255,244,228),bg2=(250,214,170),fg=(60,32,10),ac=(214,108,20),mut=(120,80,50)),
 'peptipump':dict(bg=(38,28,26),bg2=(110,44,28),fg=(255,240,230),ac=(240,120,70),mut=(225,200,190)),
 'medicinal':dict(bg=(253,236,241),bg2=(246,196,210),fg=(70,18,36),ac=(201,38,79),mut=(120,60,80)),
}
# recorte do Peptistrong (fundo branco -> transparente)
pp=Image.open(os.path.join(BASE,'assets','peptistrong.jpg')).convert('RGBA')
rgb=pp.convert('RGB')
for c in [(0,0),(rgb.width-1,0),(0,rgb.height-1),(rgb.width-1,rgb.height-1)]:
  ImageDraw.floodfill(rgb,c,(255,0,255),thresh=28)
a=Image.new('L',rgb.size,255);pa=a.load();pr=rgb.load()
for y in range(rgb.height):
  for x in range(rgb.width):
    if pr[x,y]==(255,0,255): pa[x,y]=0
pp.putalpha(a.filter(ImageFilter.GaussianBlur(1)))
pp=pp.crop(pp.getbbox())
def wrap(d,txt,f,maxw):
  out=[]
  for par in txt.split('\n'):
    ws=par.split(' ');cur=''
    for w in ws:
      t=(cur+' '+w).strip()
      if d.textlength(t,font=f)<=maxw: cur=t
      else:
        if cur: out.append(cur)
        cur=w
    out.append(cur)
  return out
def grad(W,H,c1,c2):
  im=Image.new('RGB',(W,H));d=ImageDraw.Draw(im)
  for y in range(H):
    t=y/H; d.line([(0,y),(W,y)],fill=tuple(int(c1[i]+(c2[i]-c1[i])*t) for i in range(3)))
  return im
def peca(p):
  W,H=(1080,1920) if p['canal']=='story' else (1080,1350)
  T=TEMAS[p['tema']]
  im=grad(W,H,T['bg'],T['bg2']).convert('RGBA'); d=ImageDraw.Draw(im)
  deco=Image.new('RGBA',(W,H),(0,0,0,0)); dd=ImageDraw.Draw(deco)
  ac=T['ac']
  dd.ellipse([W-420,-260,W+260,420],fill=ac+(55,)); dd.ellipse([-300,H-380,380,H+300],fill=ac+(40,))
  im=Image.alpha_composite(im,deco); d=ImageDraw.Draw(im)
  top=250 if p['canal']=='story' else 110
  M=90
  # marca
  d.text((M,top-70),'medicinal',font=font('b',40),fill=T['fg']); d.text((M+212,top-58),'FARMÁCIA E MANIPULAÇÃO',font=font('m',17),fill=T['mut'])
  y=top+20
  if p.get('kicker'):
    f=font('b',30); tw=d.textlength(p['kicker'].upper(),font=f)
    d.rounded_rectangle([M,y,M+tw+40,y+56],radius=28,fill=ac); d.text((M+20,y+8),p['kicker'].upper(),font=f,fill=T['bg'] if p['tema']!='maxsolve' else (255,255,255))
    y+=90
  fh=font('b',p.get('hsize',96 if p['canal']=='story' else 70))
  for ln in wrap(d,p['titulo'],fh,W-2*M):
    d.text((M,y),ln,font=fh,fill=T['fg']); y+=int(fh.size*1.15)
  y+=24
  img_area=None
  if p.get('produto')=='peptistrong':
    ph=int(H*(0.40 if p['canal']=='story' else 0.36))
    prod=pp.copy(); r=ph/prod.height; prod=prod.resize((int(prod.width*r),ph),Image.LANCZOS)
    img_area=prod
  fb=font('r',p.get('bsize',52 if p['canal']=='story' else 40))
  if p.get('itens'):
    for it in p['itens']:
      lines=wrap(d,it,fb,W-2*M-60)
      d.ellipse([M,y+18,M+22,y+40],fill=ac)
      for ln in lines:
        d.text((M+50,y),ln,font=fb,fill=T['fg']); y+=int(fb.size*1.3)
      y+=14
  if p.get('texto'):
    for ln in wrap(d,p['texto'],fb,W-2*M):
      d.text((M,y),ln,font=fb,fill=T['fg']); y+=int(fb.size*1.32)
  if img_area is not None:
    px0=(W-img_area.width)//2 if not p.get('itens') else W-img_area.width-40
    py0=max(y+20,H-img_area.height-(330 if p['canal']=='story' else 170))
    sh=Image.new('RGBA',(W,H),(0,0,0,0));ImageDraw.Draw(sh).ellipse([px0+30,py0+img_area.height-40,px0+img_area.width-30,py0+img_area.height+20],fill=(0,0,0,110))
    im=Image.alpha_composite(im,sh.filter(ImageFilter.GaussianBlur(18)));im.alpha_composite(img_area,(px0,py0));d=ImageDraw.Draw(im)
  # rodapé
  fy=H-(300 if p['canal']=='story' else 120)
  if p.get('cta'):
    f=font('b',36); tw=d.textlength(p['cta'],font=f)
    d.rounded_rectangle([M,fy-12,M+tw+50,fy+56],radius=34,fill=T['fg']); d.text((M+25,fy-2),p['cta'],font=f,fill=T['bg'])
  if p.get('nota'):
    d.text((M,fy+(80 if p.get('cta') else 0)),p['nota'],font=font('r',24),fill=T['mut'])
  if p.get('slide'):
    d.text((W-M-90,fy+4),p['slide'],font=font('m',30),fill=T['mut'])
  return im.convert('RGB')
for p in spec:
  peca(p).save(os.path.join(OUT,p['arquivo']),quality=90)
  print(p['arquivo'])
