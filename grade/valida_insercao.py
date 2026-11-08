"""Validação de produto inserido em cena (procedimento: docs/10-insercao-de-produto.md, seção 7c).

Uso:
    python3 valida_insercao.py ficha_insercao.json
Saída: relatório no terminal + <saida>_validacao.md + <saida>_inspecao.jpg. Código de saída 1 se reprovar.

A ficha de inserção (JSON) registra as MEDIDAS feitas na cena e no produto. Nada é estimado pelo script:
o que não foi medido fica como "não medido" e reprova.
"""
import json, sys, os, math
import numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from insere_produto import (verifica_fidelidade, verifica_mascara, verifica_contato, verifica_halo,
                            folha_inspecao)

LIMITES = {
    'escala_tol': 0.03,          # ±3% da altura real
    'proporcao_tol': 0.02,       # ±2% da proporção real
    'angulo_tol': 0.03,          # diferença máxima da razão das elipses
    'fidelidade_min': 0.90,
    'contato_min': 0.30,
    'halo_max': 18,
    'luz_margem': 0.04,          # lado da janela pelo menos 4% mais claro
    'grao_faixa': (0.6, 1.6),    # grão do produto / grão da cena
    'nitidez_faixa': (0.5, 2.0), # nitidez da borda do produto / nitidez de objeto vizinho na mesma profundidade
    'preto_max_dif': 25,         # preto do produto não pode estar mais claro que o preto da cena + 25
}


def _L(im): return np.asarray(im.convert('L')).astype(float)


def _detalhe(im):
    g = im.convert('L'); return _L(g) - _L(g.filter(ImageFilter.GaussianBlur(1.5)))


def valida(f):
    r = []  # (grupo, item, ok, valor, limite)
    arte = Image.open(f['arte']).convert('RGB'); cena = Image.open(f['cena']).convert('RGB')
    rc = Image.open(f['recorte']).convert('RGBA')
    cx = tuple(f['colocacao']['caixa'])                     # onde o recorte (inteiro) ficou na arte
    x0, y0, x1, y1 = cx
    corpo_x0, corpo_x1 = f['colocacao']['corpo_x']            # laterais do corpo na arte
    base_y = f['colocacao']['base_y']                         # ponto mais baixo da base na arte
    prod = f['produto']; med = f['cena_medidas']

    # 1. ESCALA
    pxcm = med['ref_altura_px'] / med['ref_altura_cm']
    alt_real = prod.get('altura_cm')
    alt_px = y1 - y0
    if alt_real:
        esperado = alt_real * pxcm; d = alt_px / esperado - 1
        r.append(('Geometria', 'Escala (altura)', abs(d) <= LIMITES['escala_tol'], f'{alt_px}px × esperado {esperado:.0f}px ({d:+.1%})', '±3%'))
    else:
        r.append(('Geometria', 'Escala (altura)', False, 'altura do produto NÃO MEDIDA com régua', 'ficha do produto'))
    # 2. PROPORÇÃO
    larg_corpo = corpo_x1 - corpo_x0; prop = larg_corpo / alt_px
    prop_ref = prod.get('proporcao_corpo_altura')
    d = prop / prop_ref - 1
    r.append(('Geometria', 'Proporção (largura/altura)', abs(d) <= LIMITES['proporcao_tol'], f'{prop:.3f} × {prop_ref:.3f} ({d:+.1%})', '±2%'))
    # 3. ÂNGULO
    da = abs(med['elipse_cena'] - prod['elipse_foto'])
    r.append(('Geometria', 'Ângulo da câmera (elipses)', da <= LIMITES['angulo_tol'], f"cena {med['elipse_cena']:.2f} × foto {prod['elipse_foto']:.2f} (dif. {da:.2f})", '≤ 0,03'))

    # 4. FIDELIDADE
    ok, c = verifica_fidelidade(arte, rc, cx, LIMITES['fidelidade_min'])
    r.append(('Embalagem', 'Fidelidade do rótulo/forma', ok, f'{c}', '≥ 0,90'))
    # 5. RECORTE
    ok, det = verifica_mascara(rc.resize((x1 - x0, y1 - y0)))
    r.append(('Bordas', 'Recorte em uma peça, sem ilhas', bool(ok), f"{det['pecas']} peça(s), {det['ilhas_maiores_que_20px']} ilha(s), borda semitransp. {det['borda_semitransparente']}", '1 peça, borda ≤ 0,06'))
    # 6. HALO
    ok, h = verifica_halo(arte, rc, cx, LIMITES['halo_max'])
    r.append(('Bordas', 'Halo claro na borda', bool(ok), f'{h}', '≤ 18'))
    # 7. NITIDEZ da borda × objeto vizinho
    def nit(box):
        g = arte.crop(tuple(int(v) for v in box)).convert('L'); return float(np.var(_L(g.filter(ImageFilter.FIND_EDGES))))
    n_prod = nit((corpo_x0 - 6, y0 + (y1 - y0) * 0.3, corpo_x0 + 6, y0 + (y1 - y0) * 0.7))
    n_viz = nit(tuple(med['vizinho_borda_caixa']))
    q = n_prod / max(n_viz, 1e-6)
    a, b = LIMITES['nitidez_faixa']
    r.append(('Bordas', 'Nitidez da borda × objeto vizinho', a <= q <= b, f'{q:.2f}', f'{a}–{b}'))

    # 8. CONTATO
    ok, pts = verifica_contato(arte, cena, base_y, corpo_x0, corpo_x1, prod['base_arco'] * (y1 - y0), LIMITES['contato_min'])
    r.append(('Contato', 'Sombra de contato em toda a pegada (7 pontos)', bool(ok), f'mín. {min(pts):.2f} ' + str([round(float(p), 2) for p in pts]), '≥ 0,30 em todos'))
    # 9. SOMBRA PROJETADA do lado oposto à luz
    lado = med['luz_lado']                                   # 'esquerda' ou 'direita'
    oposto_x = (corpo_x0 - larg_corpo * 0.6, corpo_x0) if lado == 'direita' else (corpo_x1, corpo_x1 + larg_corpo * 0.6)
    A, C = _L(arte), _L(cena)
    ys = slice(int(base_y) - 2, int(base_y) + 14)
    xs = slice(int(oposto_x[0]), int(oposto_x[1]))
    esc = 1 - A[ys, xs].mean() / max(C[ys, xs].mean(), 1)
    r.append(('Contato', 'Sombra projetada do lado oposto à luz', esc >= 0.08, f'escurece {esc:.0%}', '≥ 8%'))

    # 10. LUZ: lado da janela mais claro no produto
    m = np.asarray(rc.resize((x1 - x0, y1 - y0)).split()[3]) > 200
    P = A[y0:y1, x0:x1]
    meio = (corpo_x0 + corpo_x1) // 2 - x0
    esq = P[:, :meio][m[:, :meio]].mean(); dir_ = P[:, meio:][m[:, meio:]].mean()
    claro = dir_ / esq - 1 if lado == 'direita' else esq / dir_ - 1
    r.append(('Luz', f'Lado da janela ({lado}) mais claro no produto', claro >= LIMITES['luz_margem'], f'{claro:+.1%}', '≥ +4%'))
    # 11. PRETOS
    p_prod = np.percentile(P[m], 2); p_cena = np.percentile(C, 2)
    r.append(('Luz', 'Pretos do produto × pretos da cena', p_prod <= p_cena + LIMITES['preto_max_dif'], f'produto {p_prod:.0f} × cena {p_cena:.0f}', 'produto ≤ cena + 25'))
    # 12. GRÃO: medido só em áreas LISAS (sem letras, bordas ou desenho), no produto e na cena
    def grao(im_l, mascara=None):
        g = Image.fromarray(np.clip(im_l, 0, 255).astype(np.uint8))
        det = _L(g) - _L(g.filter(ImageFilter.GaussianBlur(1.2)))
        estrutura = _L(g.filter(ImageFilter.GaussianBlur(2)).filter(ImageFilter.FIND_EDGES))
        ok = estrutura <= np.percentile(estrutura if mascara is None else estrutura[mascara], 30)
        if mascara is not None: ok &= mascara
        v = det[ok]
        return float(1.4826 * np.median(np.abs(v - np.median(v)))) if v.size > 50 else float('nan')
    m_int = np.asarray(rc.resize((x1 - x0, y1 - y0)).split()[3].filter(ImageFilter.MinFilter(9))) > 200
    g_prod = grao(A[y0:y1, x0:x1], m_int)
    g_cena = grao(C[max(0, y0 - 120):max(1, y0 - 10), x0:x1])
    q = g_prod / max(g_cena, 1e-6); a, b = LIMITES['grao_faixa']
    r.append(('Acabamento', 'Grão do produto × grão da cena (áreas lisas)', a <= q <= b, f'{q:.2f} (produto {g_prod:.2f} × cena {g_cena:.2f})', f'{a}–{b}'))

    # Itens só visuais (obrigatórios na folha de inspeção)
    visuais = ['Tampa/topo: forma real, sem linha solta, sem moldura nos cantos, sem ruído',
               'Acessórios (alça etc.): vãos abertos, sem fundo da foto original grudado',
               'Base: sem degrau nos cantos, sem superfície clara entre borda e sombra',
               'Sem emenda de cor no produto',
               'Sombra do produto coerente com as sombras da cena (direção, comprimento, dureza)',
               'No tamanho do feed: passa por foto']
    return r, visuais


def relatorio(f, r, visuais):
    aprov = all(x[2] for x in r)
    linhas = [f"# Validação de inserção: {f.get('nome', '')}", '',
              f"**Resultado automático: {'APROVADO' if aprov else 'REPROVADO'}**" + ('' if aprov else ' (corrigir os itens ❌ antes da revisão humana)'), '',
              '| Grupo | Verificação | Resultado | Valor | Limite |', '|---|---|---|---|---|']
    for g, i, ok, v, lim in r:
        linhas.append(f"| {g} | {i} | {'✅' if ok else '❌'} | {v} | {lim} |")
    linhas += ['', '## Revisão visual obrigatória (folha de inspeção)', '']
    linhas += [f'- [ ] {v}' for v in visuais]
    linhas += ['', '- [ ] Aprovação do Ricardo']
    return aprov, '\n'.join(linhas)


if __name__ == '__main__':
    fp = sys.argv[1]; f = json.load(open(fp)); base_dir = os.path.dirname(os.path.abspath(fp))
    for k in ('arte', 'cena', 'recorte'): f[k] = os.path.join(base_dir, f[k])
    r, vis = valida(f)
    aprov, md = relatorio(f, r, vis)
    saida = os.path.join(base_dir, f.get('saida', 'insercao'))
    open(saida + '_validacao.md', 'w').write(md)
    folha_inspecao(Image.open(f['arte']).convert('RGB'), tuple(f['colocacao']['caixa']), saida + '_inspecao.jpg',
                   verificacoes=[(i, ok, v) for g, i, ok, v, lim in r])
    print(md)
    sys.exit(0 if aprov else 1)
