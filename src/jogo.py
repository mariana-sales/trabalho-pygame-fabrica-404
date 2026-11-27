from pathlib import Path
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
    ZONA_Y,
    ZONA_ALTURA,
)
from src.funcoes import (
    criar_estado,
    mover_faixa,
    verificar_colisao,
    pode_decidir,
    avaliar_decisao,
    aplicar_resultado,
    avancar_produto,
    verificar_desfecho,
    contar_prazo_chegada,
    contar_prazo_decisao
)

from src.desenho import criar_fontes, desenhar_jogo
from src.dados import carregar_recorde, salvar_recorde
from src.transporte import avancar_transporte, rect_produto


def criar_zona():
    """Zona lógica larga o suficiente para as três marcações de inspeção."""
    return pygame.Rect(0, ZONA_Y, LARGURA_TELA, ZONA_ALTURA)


def rect_do_produto(estado):
    """Monta o retângulo do produto atual a partir da posição no estado."""
    return rect_produto(estado)


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
            if evento.key == pygame.K_RETURN and estado["fase"] == FASE_FIM:
                novo = criar_estado(estado["recorde"])
                estado.clear()
                estado.update(novo)
    return True


def atualizar(estado, recorde_caminho, zona, delta_s=1 / FPS):
    """Move com delta time; feedback conta de DURACAO_FEEDBACK até zero."""
    if estado["fase"] == FASE_JOGANDO:
        estado["pos_produto"] = avancar_transporte(estado["pos_produto"], delta_s)
        if verificar_colisao(rect_do_produto(estado), zona):
            produto = estado["produtos"][estado["indice"]]

            if estado["chegou"]:
                esgotou = contar_prazo_decisao(estado, delta_s)
            else:
                na_faixa = estado["faixa_inspetor"] == produto["faixa"]
                esgotou = contar_prazo_chegada(estado, na_faixa, delta_s)

            if esgotou:
                finalizar_produto(estado, avaliar_decisao(produto, None))

    elif estado["fase"] == FASE_FEEDBACK:
        estado["frames_feedback"] = max(0, estado["frames_feedback"] - max(0, delta_s) * FPS)
        if estado["frames_feedback"] <= 1e-8:
            estado["frames_feedback"] = 0
            concluidos = estado["indice"] + 1
            desfecho = verificar_desfecho(
                estado["erros"], concluidos, TOTAL_PRODUTOS, LIMITE_ERROS
            )
            if desfecho is None:
                avancar_produto(estado)
            else:
                estado["desfecho"] = desfecho
                estado["fase"] = FASE_FIM
                if estado["pontos"] > estado["recorde"]:
                    Path(recorde_caminho).parent.mkdir(parents=True, exist_ok=True)
                    salvar_recorde(recorde_caminho, estado["pontos"])
                    estado["recorde"] = estado["pontos"]


def executar_jogo():
    """Executa o loop principal do jogo."""
    pygame.init()
    try:
        tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption(TITULO_JOGO)
        relogio = pygame.time.Clock()
        fontes = criar_fontes()
        zona = criar_zona()
        caminho = Path(__file__).resolve().parents[1] / CAMINHO_RECORDE
        estado = criar_estado(carregar_recorde(caminho))
        while True:
            delta_s = relogio.tick(FPS) / 1000
            if not processar_eventos(estado, zona):
                break
            atualizar(estado, caminho, zona, delta_s)
            estado["controles"] = ("Enter: nova partida | Esc: sair" if estado["fase"] == FASE_FIM
                                  else "← → faixa | A: aprovar | R: rejeitar")
            tela.fill(CINZA)
            desenhar_jogo(tela, fontes, estado, zona, rect_do_produto(estado))
            pygame.display.flip()
    finally:
        pygame.quit()


if __name__ == "__main__":
    executar_jogo()
