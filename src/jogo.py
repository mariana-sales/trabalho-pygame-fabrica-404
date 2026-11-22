import pygame

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    CINZA,
    CAMINHO_RECORDE,
    NUM_FAIXAS,
    FAIXAS_X,
    ZONA_Y,
    ZONA_ALTURA,
    LARGURA_PRODUTO,
    ALTURA_PRODUTO,
)
from src.funcoes import criar_estado, mover_faixa
from src.desenho import criar_fontes, desenhar_jogo
from src.dados import carregar_recorde


def rect_do_produto(estado):
    """Monta o retângulo do produto atual a partir da posição no estado."""
    produto = estado["produtos"][estado["indice"]]
    retangulo = pygame.Rect(0, 0, LARGURA_PRODUTO, ALTURA_PRODUTO)
    retangulo.centerx = FAIXAS_X[produto["faixa"]]
    retangulo.y = int(estado["pos_produto"])
    return retangulo


def processar_eventos(estado, zona):
    """Trata os eventos da janela e do teclado. Devolve False para fechar o jogo."""
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return False
            if evento.key == pygame.K_LEFT:
                estado["faixa_inspetor"] = mover_faixa(estado["faixa_inspetor"], -1, NUM_FAIXAS)
            if evento.key == pygame.K_RIGHT:
                estado["faixa_inspetor"] = mover_faixa(estado["faixa_inspetor"], 1, NUM_FAIXAS)
    return True

def executar_jogo():
    """Executa o loop principal do jogo."""
    pygame.init()

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)
    relogio = pygame.time.Clock()

    fontes = criar_fontes()
    zona = pygame.Rect(
        FAIXAS_X[0] - LARGURA_PRODUTO // 2,
        ZONA_Y,
        FAIXAS_X[-1] - FAIXAS_X[0] + LARGURA_PRODUTO,
        ZONA_ALTURA,
    )
    estado = criar_estado(carregar_recorde(CAMINHO_RECORDE))

    rodando = True
    while rodando:
        relogio.tick(FPS)
        rodando = processar_eventos(estado, zona)

        tela.fill(CINZA)
        desenhar_jogo(tela, fontes, estado, zona, rect_do_produto(estado))
        pygame.display.flip()

    pygame.quit()