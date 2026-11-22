"""Empacota as artes geradas e monta a cena usando somente os PNGs separados."""
from pathlib import Path
import json
import zipfile
import pygame

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'sprites'
OUT.mkdir(exist_ok=True)


def load(name):
    return pygame.image.load(str(ROOT / 'originais' / (name + '.png')))


def fit(image, size):
    scale = min(size[0] / image.get_width(), size[1] / image.get_height())
    return pygame.transform.scale(image, (round(image.get_width()*scale), round(image.get_height()*scale)))


def save(name, image):
    # Exportação pixel art: alfa binário elimina resíduos quase invisíveis
    # (alfa 1/255) no centro vazado, sem suavizar nem redesenhar as cores.
    for y in range(image.get_height()):
        for x in range(image.get_width()):
            color = image.get_at((x, y))
            color.a = 255 if color.a >= 128 else 0
            image.set_at((x, y), color)
    pygame.image.save(image, str(OUT / (name + '.png')))


sizes = {}
for name, limit in [('esteira_esquerda', (190, 185)), ('esteira_central', (190, 185)),
                    ('esteira_direita', (190, 185)), ('inspetor', (48, 92)),
                    ('produto_caixa', (42, 36)), ('produto_garrafa', (22, 44)),
                    ('produto_lata', (26, 36)), ('produto_peca_mecanica', (36, 32)),
                    ('zona_inspecao_esquerda', (94, 24)), ('zona_inspecao_central', (94, 24)),
                    ('zona_inspecao_direita', (94, 24))]:
    im = load(name)
    # Remover apenas margens: a arte e o alfa gerado permanecem intactos.
    im = fit(im.subsurface(im.get_bounding_rect(min_alpha=200)), limit)
    canvas = pygame.Surface((im.get_width()+4, im.get_height()+4), pygame.SRCALPHA)
    canvas.blit(im, (2, 2))
    save(name, canvas)

for side in ('esquerda', 'central', 'direita'):
    opened = load('porta_aberta_' + side)
    closed = load('porta_fechada_' + side)
    # Recorte e transformação comuns ao par, mantendo um único referencial.
    crop = opened.get_bounding_rect(min_alpha=200).union(closed.get_bounding_rect(min_alpha=200))
    opened = fit(opened.subsurface(crop), (100, 108))
    closed = pygame.transform.scale(closed.subsurface(crop), opened.get_size())
    # Montagem: o mesmo suporte aberto nos dois estados; só muda o vão.
    # As folhas vêm da geração fechada, sem redesenhar a moldura.
    result = opened.copy()
    w, h = result.get_size()
    for y in range(round(h * .28), round(h * .98)):
        for x in range(round(w * .16), round(w * .84)):
            if opened.get_at((x, y)).a < 128:
                result.set_at((x, y), closed.get_at((x, y)))
    for state, im in [('aberta', opened), ('fechada', result)]:
        canvas = pygame.Surface((104, 112), pygame.SRCALPHA)
        canvas.blit(im, ((104-w)//2, 112-h-2))
        save(f'porta_{state}_{side}', canvas)


def sprite(name):
    return pygame.image.load(str(OUT / (name + '.png')))


scene = pygame.Surface((800, 600))
scene.fill((13, 25, 36))
layout = []

def place(name, position, anchor='midbottom'):
    im = sprite(name)
    rect = im.get_rect(**{anchor: position})
    scene.blit(im, rect)
    layout.append({'arquivo': 'sprites/' + name + '.png', 'x': rect.x, 'y': rect.y})

# Retaguardas convergem suavemente, pontas dianteiras permanecem separadas.
for side, front, rear in [('esquerda', 240, 286), ('central', 400, 400), ('direita', 560, 532)]:
    place('porta_aberta_' + side, (rear, 280))
    place('esteira_' + side, (front, 455))
    place('zona_inspecao_' + side, (front, 400), 'center')
place('produto_caixa', (400, 402))
place('inspetor', (400, 556))
pygame.image.save(scene, str(ROOT / 'preview' / 'cena_800x600.png'))
(ROOT / 'layout.json').write_text(json.dumps({'tamanho': [800, 600], 'fundo': [13, 25, 36], 'camadas': layout}, indent=2), encoding='utf-8')

# Prancha técnica separada, nunca embutida em nenhum sprite.
board = pygame.Surface((1000, 800))
board.fill((29, 43, 57))
for index, p in enumerate(sorted(OUT.glob('*.png'))):
    im = pygame.image.load(str(p))
    x, y = (index % 5)*200+100, (index // 5)*200+100
    board.blit(im, im.get_rect(center=(x,y)))
pygame.image.save(board, str(ROOT / 'preview' / 'todos_os_sprites.png'))

rows = []
for p in sorted(OUT.glob('*.png')):
    im = pygame.image.load(str(p))
    w, h = im.get_size()
    assert im.get_flags() & pygame.SRCALPHA
    assert im.get_at((0,0)).a == 0
    if p.stem.startswith('zona_'):
        assert im.get_at((w//2,h//2)).a == 0, p.name
    rows.append(f'| `{p.name}` | {w} × {h} |')

text = '''# Fábrica 404 — sprites refeitos, versão 2

Pacote de 17 sprites PNG RGBA separados, gerados com a ferramenta de imagem
integrada a partir da referência visual fornecida. Perspectiva frontal levemente
elevada; esteiras convergentes; grafite/aço/ciano; inspetor de costas.

## Dimensões dos arquivos prontos para o jogo

| Arquivo em `sprites/` | Dimensões em pixels |
|---|---|
''' + '\n'.join(rows) + '''

## Prévia e encaixe

- `preview/cena_800x600.png`: composição de 800 × 600 feita com os PNGs de
  `sprites/`, fundo azul-marinho, sem interface; área superior livre.
- `preview/todos_os_sprites.png`: prancha técnica de 800 × 600 para inspeção.
- `layout.json`: posições exatas e ordem das camadas da prévia.
- Cada par de portas usa canvas de 104 × 112 e o mesmo ponto de encaixe:
  centro inferior. A moldura aberta é compartilhada nos dois estados; apenas
  as folhas do vão mudam. Não recorte os estados separadamente.
- As zonas são camadas independentes com centro transparente. Posicione sobre
  a superfície da esteira, antes dos produtos; nunca sobre os roletes.
- O inspetor mede menos de 100 pixels de altura na prévia.

## Nitidez, transparência e origem

Os arquivos de `sprites/` já estão na escala da prévia. Use `convert_alpha()`
no Pygame. Para ampliar, use `pygame.transform.scale` em múltiplos inteiros;
não use `smoothscale`. Não use cor-chave: os PNGs possuem alfa real.
As margens foram recortadas e os sprites redimensionados por vizinho mais
próximo. O canal alfa das artes geradas foi preservado.

`originais/` contém as 17 gerações selecionadas em sua resolução de origem.
`geracao.json` registra os prompts usados com a ferramenta integrada (sem API
externa). `montar_pacote.py` reproduz a preparação e a prévia com Pygame.
Os sprites não contêm texto, pontuação ou painéis. A caixa usa somente fita,
a lata é lisa, a garrafa não tem rótulo e a peça mecânica não tem inscrições.

Para refazer a montagem: `python montar_pacote.py` (requer pygame).
'''
(ROOT / 'README.md').write_text(text, encoding='utf-8')
print('17 sprites exportados; alfa e centros das zonas conferidos.')
