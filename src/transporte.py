"""Transporte em coordenadas lógicas; não desenha nem avalia decisões."""
import pygame
from src.funcoes import mover_produto
from src.config import (FAIXAS_X, Y_INICIO_ESTEIRA, Y_PARADA_PRODUTO,
                        VELOCIDADE_TRANSPORTE, LARGURA_PRODUTO, ALTURA_PRODUTO)


def avancar_transporte(posicao, delta_s):
    """Não ultrapassa a parada, mesmo num quadro longo."""
    return mover_produto(posicao, VELOCIDADE_TRANSPORTE * max(0, delta_s), Y_PARADA_PRODUTO)


def rect_produto(estado):
    if not 0 <= estado["indice"] < len(estado["produtos"]):
        return None
    produto = estado["produtos"][estado["indice"]]
    y = estado["pos_produto"]
    progresso = max(0, min(1, (y-Y_INICIO_ESTEIRA)/(Y_PARADA_PRODUTO-Y_INICIO_ESTEIRA)))
    escala = 0.65 + 0.35 * progresso
    rect = pygame.Rect(0, round(y), round(LARGURA_PRODUTO*escala), round(ALTURA_PRODUTO*escala))
    rect.centerx = FAIXAS_X[produto["faixa"]]
    return rect
