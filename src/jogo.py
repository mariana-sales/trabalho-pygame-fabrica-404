import pygame

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    CINZA,
    CAMINHO_RECORDE,
    NUM_FAIXAS,
    TOTAL_PRODUTOS,
    LIMITE_ERROS,
    FASE_JOGANDO,
    FASE_FEEDBACK,
    FASE_FIM,
    DURACAO_FEEDBACK,
    FAIXAS_X,
    ZONA_Y,
    ZONA_ALTURA,
    LARGURA_PRODUTO,
    ALTURA_PRODUTO,
    VELOCIDADE_ESTEIRA,
)
from src.funcoes import (
    criar_estado,
    mover_faixa,
    mover_produto,
    verificar_colisao,
    pode_decidir,
    avaliar_decisao,
    aplicar_resultado,
    avancar_produto,
    verificar_desfecho,
)

from src.funcoes import criar_estado, mover_faixa, mover_produto
from src.desenho import criar_fontes, desenhar_jogo
from src.dados import carregar_recorde


def rect_do_produto(estado):
    """Monta o retângulo do produto atual a partir da posição no estado."""
    produto = estado["produtos"][estado["indice"]]
    retangulo = pygame.Rect(0, 0, LARGURA_PRODUTO, ALTURA_PRODUTO)
    retangulo.centerx = FAIXAS_X[produto["faixa"]]
    retangulo.y = int(estado["pos_produto"])
    return retangulo


def tentar_decidir(estado, decisao, zona):
    """Aprova ou rejeita o produto atual, se o jogador puder decidir agora."""
    if estado["fase"] != FASE_JOGANDO:
        return

    produto = estado["produtos"][estado["indice"]]
    produto_na_zona = verificar_colisao(rect_do_produto(estado), zona)

    if pode_decidir(estado["faixa_inspetor"], produto["faixa"], produto_na_zona):
        resultado = avaliar_decisao(produto, decisao)
        finalizar_produto(estado, resultado)


def finalizar_produto(estado, resultado):
    """Registra o resultado da decisão e entra na fase de feedback."""
    aplicar_resultado(estado, resultado)
    estado["resultado"] = resultado
    estado["fase"] = FASE_FEEDBACK
    estado["frames_feedback"] = DURACAO_FEEDBACK


def processar_eventos(estado, zona):
    """Trata os eventos da janela e do teclado. Devolve False para fechar o jogo."""
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return False
            if estado["fase"] == FASE_JOGANDO:
                if evento.key == pygame.K_LEFT:
                    estado["faixa_inspetor"] = mover_faixa(estado["faixa_inspetor"], -1, NUM_FAIXAS)
                if evento.key == pygame.K_RIGHT:
                    estado["faixa_inspetor"] = mover_faixa(estado["faixa_inspetor"], 1, NUM_FAIXAS)
            if evento.key == pygame.K_a:
                tentar_decidir(estado, "aprovar", zona)
            if evento.key == pygame.K_r:
                tentar_decidir(estado, "rejeitar", zona)
    return True


def atualizar(estado, recorde_caminho, zona):
    """Atualiza o estado a cada quadro: move o produto ou conta a pausa do feedback."""
    if estado["fase"] == FASE_JOGANDO:
        pos_parada = ZONA_Y + ZONA_ALTURA - ALTURA_PRODUTO
        estado["pos_produto"] = mover_produto(
            estado["pos_produto"], VELOCIDADE_ESTEIRA, pos_parada
        )

    elif estado["fase"] == FASE_FEEDBACK:
        estado["frames_feedback"] -= 1
        if estado["frames_feedback"] <= 0:
            concluidos = estado["indice"] + 1
            desfecho = verificar_desfecho(
                estado["erros"], concluidos, TOTAL_PRODUTOS, LIMITE_ERROS
            )
            if desfecho is None:
                avancar_produto(estado)
            else:
                estado["desfecho"] = desfecho
                estado["fase"] = FASE_FIM


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
        atualizar(estado, CAMINHO_RECORDE, zona)
        
        tela.fill(CINZA)
        desenhar_jogo(tela, fontes, estado, zona, rect_do_produto(estado))
        pygame.display.flip()

    pygame.quit()