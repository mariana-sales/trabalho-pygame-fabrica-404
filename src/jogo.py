from pathlib import Path
import random
import pygame

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    CINZA,
    CAMINHO_RECORDE,
    MODO_FASES,
    MODO_INFINITO,
    NUM_FAIXAS,
    LIMITE_ERROS,
    FASE_JOGANDO,
    FASE_FEEDBACK,
    FASE_FIM,
    FASE_MENU,
    FASE_CONCLUIDA,
    DURACAO_FEEDBACK,
    ZONA_Y,
    ZONA_ALTURA,
)
from src.funcoes import (
    criar_estado,
    criar_estado_menu,
    iniciar_modo,
    configurar_fase,
    gerar_produto_infinito,
    parametros_dificuldade,
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
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if estado["fase"] == FASE_MENU:
                if pygame.Rect(230, 310, 340, 58).collidepoint(evento.pos):
                    iniciar_modo(estado, MODO_FASES)
                elif pygame.Rect(230, 382, 340, 58).collidepoint(evento.pos):
                    iniciar_modo(estado, MODO_INFINITO)
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return False
            if estado["fase"] == FASE_MENU:
                if evento.key in (pygame.K_1, pygame.K_KP1):
                    iniciar_modo(estado, MODO_FASES)
                elif evento.key in (pygame.K_2, pygame.K_KP2):
                    iniciar_modo(estado, MODO_INFINITO)
                continue
            if estado["fase"] == FASE_CONCLUIDA:
                if evento.key == pygame.K_RETURN:
                    configurar_fase(estado, estado["fase_numero"] + 1)
                elif evento.key == pygame.K_m:
                    estado["fase"] = FASE_MENU
                continue
            if estado["fase"] == FASE_FIM:
                if evento.key == pygame.K_RETURN:
                    iniciar_modo(estado, estado.get("modo", MODO_FASES))
                elif evento.key == pygame.K_m:
                    estado["fase"] = FASE_MENU
                continue
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


def atualizar(estado, recorde_caminho, zona, delta_s=1 / FPS):
    """Move com delta time; feedback conta de DURACAO_FEEDBACK até zero."""
    if estado["fase"] == FASE_JOGANDO:
        estado["pos_produto"] = avancar_transporte(
            estado["pos_produto"], delta_s, estado.get("multiplicador_velocidade", 1.0))
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
            estado["produtos_concluidos"] = estado.get("produtos_concluidos", 0) + 1
            if estado["erros"] >= LIMITE_ERROS:
                estado["desfecho"] = "derrota"
                estado["fase"] = FASE_FIM
                if estado["pontos"] > estado["recorde"]:
                    Path(recorde_caminho).parent.mkdir(parents=True, exist_ok=True)
                    salvar_recorde(recorde_caminho, estado["pontos"])
                    estado["recorde"] = estado["pontos"]
                return

            if estado.get("modo") == MODO_INFINITO:
                estado["proximo_aumento"] -= 1
                if estado["proximo_aumento"] <= 0:
                    estado["nivel_dificuldade"] += 1
                    tempo, velocidade = parametros_dificuldade(estado["nivel_dificuldade"])
                    estado["tempo_decisao_base"] = tempo
                    estado["multiplicador_velocidade"] = velocidade
                    estado["proximo_aumento"] = random.randint(5, 8)
                if estado["indice"] + 1 >= len(estado["produtos"]):
                    estado["produtos"].append(gerar_produto_infinito())
                avancar_produto(estado)
            elif concluidos >= len(estado["produtos"]):
                estado["fase"] = FASE_CONCLUIDA
                if estado["pontos"] > estado["recorde"]:
                    Path(recorde_caminho).parent.mkdir(parents=True, exist_ok=True)
                    salvar_recorde(recorde_caminho, estado["pontos"])
                    estado["recorde"] = estado["pontos"]
            else:
                avancar_produto(estado)


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
        estado = criar_estado_menu(carregar_recorde(caminho))
        while True:
            delta_s = relogio.tick(FPS) / 1000
            if not processar_eventos(estado, zona):
                break
            atualizar(estado, caminho, zona, delta_s)
            if estado["fase"] == FASE_MENU:
                estado["controles"] = "1: Fases | 2: Infinito | Esc: sair"
            elif estado["fase"] == FASE_CONCLUIDA:
                estado["controles"] = "Enter: próxima fase | M: menu | Esc: sair"
            elif estado["fase"] == FASE_FIM:
                estado["controles"] = "Enter: jogar novamente | M: menu | Esc: sair"
            else:
                estado["controles"] = "← → faixa | A: aprovar | R: rejeitar | Esc: sair"
            tela.fill(CINZA)
            desenhar_jogo(tela, fontes, estado, zona, rect_do_produto(estado))
            pygame.display.flip()
    finally:
        pygame.quit()


if __name__ == "__main__":
    executar_jogo()
