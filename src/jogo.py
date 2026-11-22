"""Loop da fábrica: transporte, entrada e regras compartilhadas com os testes."""
from pathlib import Path
import pygame
from src.config import (LARGURA_TELA, ALTURA_TELA, FPS, TITULO_JOGO,
                        CAMINHO_RECORDE, ZONA_Y, ZONA_ALTURA, Y_PARADA_PRODUTO,
                        DURACAO_FEEDBACK, LIMITE_ERROS, NUM_FAIXAS,
                        FASE_JOGANDO, FASE_FEEDBACK, FASE_FIM)
from src.funcoes import (criar_estado, mover_faixa, pode_decidir, avaliar_decisao,
                         aplicar_resultado, avancar_produto, verificar_desfecho)
from src.dados import carregar_recorde, salvar_recorde
from src.desenho import criar_fontes, desenhar_jogo
from src.transporte import avancar_transporte, rect_produto


def atualizar_partida(estado, delta_s, decisao=None):
    """Atualiza somente estado; uma decisão só é aceita com produto parado."""
    if estado["fase"] == FASE_FIM:
        return
    if estado["fase"] == FASE_FEEDBACK:
        estado["frames_feedback"] += max(0, delta_s) * FPS
        if estado["frames_feedback"] + 1e-8 >= DURACAO_FEEDBACK:
            avancar_produto(estado)
            estado["desfecho"] = verificar_desfecho(
                estado["erros"], estado["indice"], len(estado["produtos"]), LIMITE_ERROS)
            if estado["desfecho"]:
                estado["fase"] = FASE_FIM
        return
    # Validar antes de avançar evita aceitar uma tecla apertada no trajeto.
    produto = estado["produtos"][estado["indice"]]
    parado = estado["pos_produto"] >= Y_PARADA_PRODUTO
    if decisao in ("aprovar", "rejeitar") and pode_decidir(
            estado["faixa_inspetor"], produto["faixa"], parado):
        resultado = avaliar_decisao(produto, decisao)
        aplicar_resultado(estado, resultado)
        estado.update(resultado=resultado, fase=FASE_FEEDBACK, frames_feedback=0)
        estado["recorde"] = max(estado["recorde"], estado["pontos"])
    else:
        estado["pos_produto"] = avancar_transporte(estado["pos_produto"], delta_s)


def executar_jogo():
    pygame.init()
    try:
        tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption(TITULO_JOGO)
        relogio = pygame.time.Clock()
        fontes = criar_fontes()
        zona = pygame.Rect(0, ZONA_Y, LARGURA_TELA, ZONA_ALTURA)
        caminho = Path(__file__).resolve().parents[1] / CAMINHO_RECORDE
        recorde_salvo = carregar_recorde(caminho)
        estado = criar_estado(recorde_salvo)
        rodando = True
        while rodando:
            delta_s = relogio.tick(FPS) / 1000
            decisao = None
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        rodando = False
                    elif evento.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        estado["faixa_inspetor"] = mover_faixa(estado["faixa_inspetor"],
                            -1 if evento.key == pygame.K_LEFT else 1, NUM_FAIXAS)
                    elif evento.key in (pygame.K_a, pygame.K_r):
                        decisao = "aprovar" if evento.key == pygame.K_a else "rejeitar"
                    elif evento.key == pygame.K_SPACE and estado["fase"] == FASE_FIM:
                        estado = criar_estado(recorde_salvo)
            if not rodando:
                break
            atualizar_partida(estado, delta_s, decisao)
            if estado["recorde"] > recorde_salvo:
                caminho.parent.mkdir(parents=True, exist_ok=True)
                salvar_recorde(caminho, estado["recorde"])
                recorde_salvo = estado["recorde"]
            estado["controles"] = ("Espaço: nova partida | Esc: sair" if estado["fase"] == FASE_FIM
                                  else "← → faixa | A: aprovar | R: rejeitar")
            desenhar_jogo(tela, fontes, estado, zona, rect_produto(estado))
            pygame.display.flip()
    finally:
        pygame.quit()


if __name__ == "__main__":
    executar_jogo()
