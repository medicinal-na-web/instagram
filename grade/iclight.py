"""Chama o IC-Light privado (huggingface.co/spaces/medicinal/IC-Light) e devolve o produto reiluminado.

Acesso: segredo de rede do ambiente (Bearer, token só de leitura do Space) para huggingface.co e
medicinal-ic-light.hf.space; nenhum token no código. O gradio_client não funciona com este Space
(a rota de info da API quebra no Gradio 4.29), então a chamada usa a fila do Gradio direto (sse_v3).

Uso no procedimento (docs/10-insercao-de-produto.md): NÃO usar a imagem do IC-Light na arte.
Usar só o mapa de luz: aplica_luz(original, reiluminada) devolve a foto original com a luz nova,
preservando rótulo e detalhes. Depois, verifica_fidelidade (>= 0,90).
"""
import json, time, uuid, io
import requests
from PIL import Image, ImageFilter
import numpy as np

BASE = 'https://medicinal-ic-light.hf.space'
LUZES = ('None', 'Left Light', 'Right Light', 'Top Light', 'Bottom Light')


def reilumina(caminho_img, prompt, luz='Left Light', largura=512, altura=640, seed=12345, passos=25, timeout=400):
    assert luz in LUZES
    up = requests.post(BASE + '/upload', files={'files': open(caminho_img, 'rb')}, timeout=60); up.raise_for_status()
    img = {'path': up.json()[0], 'meta': {'_type': 'gradio.FileData'}}
    sh = uuid.uuid4().hex[:11]
    data = [img, prompt, largura, altura, 1, seed, passos, 'best quality',
            'lowres, bad anatomy, bad hands, cropped, worst quality', 2, 1.5, 0.5, 0.9, luz]
    r = requests.post(BASE + '/queue/join', json={'data': data, 'fn_index': 2, 'session_hash': sh,
                                                  'event_data': None, 'trigger_id': None}, timeout=60)
    r.raise_for_status()
    with requests.get(BASE + '/queue/data', params={'session_hash': sh}, stream=True, timeout=timeout) as s:
        for line in s.iter_lines():
            if not line or not line.startswith(b'data:'): continue
            m = json.loads(line[5:])
            if m.get('msg') == 'process_completed':
                out = m['output']
                if 'data' not in out: raise RuntimeError(str(out)[:500])
                fg_url = out['data'][0]['url']; relit_url = out['data'][1][0]['image']['url']
                get = lambda u: Image.open(io.BytesIO(requests.get(u, timeout=60).content)).convert('RGB')
                return get(fg_url), get(relit_url)
    raise TimeoutError('IC-Light não respondeu')


def aplica_luz(original, reiluminada, raio=6, forca=0.6, limites=(0.5, 1.8)):
    """Foto original (alta resolução, rótulo fiel) × razão de luz da versão reiluminada (só baixa frequência).
    forca: 0 = sem mudança, 1 = luz completa do IC-Light (costuma exagerar; 0,5-0,7 é mais natural)."""
    o = original.convert('RGB'); r = reiluminada.convert('RGB')
    # o IC-Light corta ao centro na proporção da saída: cortar o original igual antes de comparar
    ar = r.width / r.height
    if abs(o.width / o.height - ar) > 1e-3:
        if o.width / o.height > ar:
            nw = int(o.height * ar); x0 = (o.width - nw) // 2; o = o.crop((x0, 0, x0 + nw, o.height))
        else:
            nh = int(o.width / ar); y0 = (o.height - nh) // 2; o = o.crop((0, y0, o.width, y0 + nh))
    r = r.resize(o.size, Image.LANCZOS)
    bo = np.asarray(o.filter(ImageFilter.GaussianBlur(raio))).astype(float) + 4
    br = np.asarray(r.filter(ImageFilter.GaussianBlur(raio))).astype(float) + 4
    R = np.clip(br / bo, *limites) ** forca
    return Image.fromarray(np.clip(np.asarray(o).astype(float) * R, 0, 255).astype(np.uint8))
