"""Reproduz a prévia de 800 x 600 a partir dos PNGs e layout.json."""
from pathlib import Path
import json
import pygame

root = Path(__file__).resolve().parent
layout = json.loads((root / 'layout.json').read_text(encoding='utf-8'))
tela = pygame.Surface(layout['tamanho'])
tela.fill(layout['fundo'])
for camada in layout['camadas']:
    arte = pygame.image.load(str(root / camada['arquivo']))
    tela.blit(arte, (camada['x'], camada['y']))
pygame.image.save(tela, str(root / 'preview' / 'cena_800x600.png'))
