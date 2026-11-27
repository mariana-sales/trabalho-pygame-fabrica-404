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
    CAMINHO_PERFIL,
    PONTOS_POR_ACERTO,
    FASE_LOJA,
    MODO_FASES,
    MODO_INFINITO,
    NUM_FAIXAS,
    LIMITE_ERROS,
    FASE_JOGANDO,
    FASE_FIM,
    FASE_MENU,
    FASE_CONCLUIDA,
    DURACAO_MENSAGEM_RESULTADO,
    ZONA_Y,
    ZONA_ALTURA,
)
from src.funcoes import (
    criar_estado_menu,
    iniciar_modo,
    configurar_fase,
    gerar_produto_infinito,
    liberar_proximo_produto,
    parametros_dificuldade,
    mover_faixa,
    verificar_colisao,
    pode_decidir,
    avaliar_decisao,
    aplicar_resultado,
)

from src.desenho import criar_fontes, desenhar_jogo
from src.dados import carregar_recorde, salvar_recorde
from src.loja import (INSPETORES, carregar_perfil, abrir_loja, comprar_ou_equipar,
                      creditar_acerto, persistir_carteira)
from src.transporte import avancar_transporte, rect_produto, rect_produto_ativo


def criar_zona():
    """Zona lógica larga o suficiente para as três marcações de inspeção."""
    return pygame.Rect(0, ZONA_Y, LARGURA_TELA, ZONA_ALTURA)


def rect_do_produto(estado):
    """Monta o retângulo do produto atual a partir da posição no estado."""
    return rect_produto(estado)


def tentar_decidir(estado, decisao, zona):
    """Decide sobre o produto na faixa do inspetor, se ele estiver na zona."""
    if estado["fase"] != FASE_JOGANDO:
        return
    for ativo in estado.get("produtos_ativos", []):
        produto = ativo["produto"]
        produto_na_zona = verificar_colisao(rect_produto_ativo(ativo), zona)
        if pode_decidir(estado["faixa_inspetor"], produto["faixa"], produto_na_zona):
            finalizar_produto(estado, ativo, avaliar_decisao(produto, decisao))
            return


def finalizar_produto(estado, ativo, resultado):
    """Registra o resultado individual sem interromper os demais produtos."""
    produto = ativo["produto"]
    aplicar_resultado(estado, resultado)
    if resultado["jogador_acertou"]:
        creditar_acerto(estado, PONTOS_POR_ACERTO)
    estado["resultado"] = resultado
    estado["produto_feedback"] = produto
    estado["feedback_mensagem"] = (
        "Tempo esgotado: produto não inspecionado" if resultado["decisao"] is None
        else "Inspeção correta" if resultado["jogador_acertou"]
        else "Inspeção incorreta"
    )
    estado["feedback_temporizador"] = DURACAO_MENSAGEM_RESULTADO
    estado["produtos_ativos"].remove(ativo)
    estado["produtos_concluidos"] = estado.get("produtos_concluidos", 0) + 1
    estado["indice"] = estado["produtos_concluidos"]
    estado["produtos_concluidos_delta"] = estado.get("produtos_concluidos_delta", 0) + 1


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
                elif pygame.Rect(230, 454, 340, 58).collidepoint(evento.pos):
                    abrir_loja(estado)
        if evento.type == pygame.KEYDOWN:
            if estado["fase"] == FASE_LOJA:
                if evento.key in (pygame.K_ESCAPE, pygame.K_m):
                    estado["fase"] = FASE_MENU
                elif evento.key in (pygame.K_LEFT, pygame.K_UP):
                    estado["loja_selecao"] = (estado["loja_selecao"] - 1) % len(INSPETORES)
                elif evento.key in (pygame.K_RIGHT, pygame.K_DOWN):
                    estado["loja_selecao"] = (estado["loja_selecao"] + 1) % len(INSPETORES)
                elif evento.key == pygame.K_RETURN:
                    comprar_ou_equipar(estado)
                continue
            if evento.key == pygame.K_ESCAPE:
                return False
            if estado["fase"] == FASE_MENU:
                if evento.key in (pygame.K_1, pygame.K_KP1):
                    iniciar_modo(estado, MODO_FASES)
                elif evento.key in (pygame.K_2, pygame.K_KP2):
                    iniciar_modo(estado, MODO_INFINITO)
                elif evento.key in (pygame.K_3, pygame.K_KP3, pygame.K_l):
                    abrir_loja(estado)
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
    """Atualiza cada esteira e o prazo individual de cada produto ativo."""
    delta_s = max(0, delta_s)
    estado["feedback_temporizador"] = max(
        0, estado.get("feedback_temporizador", 0) - delta_s)
    if estado["feedback_temporizador"] <= 0:
        estado["feedback_mensagem"] = None

    if estado["fase"] != FASE_JOGANDO:
        return

    velocidade = estado.get("multiplicador_velocidade", 1.0)
    for ativo in list(estado.get("produtos_ativos", [])):
        ativo["pos_y"] = avancar_transporte(ativo["pos_y"], delta_s, velocidade)
        if not verificar_colisao(rect_produto_ativo(ativo), zona):
            continue

        na_faixa = estado["faixa_inspetor"] == ativo["produto"]["faixa"]
        if not ativo["chegou"] and na_faixa:
            ativo["chegou"] = True
        if ativo["chegou"]:
            ativo["tempo_decisao"] -= delta_s
            esgotou = ativo["tempo_decisao"] <= 1e-8
        else:
            ativo["tempo_chegada"] -= delta_s
            esgotou = ativo["tempo_chegada"] <= 1e-8

        if esgotou:
            finalizar_produto(estado, ativo,
                              avaliar_decisao(ativo["produto"], None))
        if estado["erros"] >= LIMITE_ERROS:
            estado["desfecho"] = "derrota"
            estado["fase"] = FASE_FIM
            break

    if estado["erros"] >= LIMITE_ERROS:
        estado["desfecho"] = "derrota"
        estado["fase"] = FASE_FIM

    if estado["fase"] == FASE_FIM:
        if estado["pontos"] > estado["recorde"]:
            Path(recorde_caminho).parent.mkdir(parents=True, exist_ok=True)
            salvar_recorde(recorde_caminho, estado["pontos"])
            estado["recorde"] = estado["pontos"]
        return

    if estado.get("modo") == MODO_INFINITO:
        concluidos = estado.pop("produtos_concluidos_delta", 0)
        estado["proximo_aumento"] -= concluidos
        if estado["proximo_aumento"] <= 0:
            estado["nivel_dificuldade"] += 1
            tempo, velocidade = parametros_dificuldade(estado["nivel_dificuldade"])
            estado["tempo_decisao_base"] = tempo
            estado["multiplicador_velocidade"] = velocidade
            estado["proximo_aumento"] = random.randint(5, 8)
        if (estado["proximo_produto"] >= len(estado["produtos"])
                and not estado.get("produto_infinito_enfileirado")):
            estado["produtos"].append(gerar_produto_infinito())
            estado["produto_infinito_enfileirado"] = True

    estado["tempo_ate_proximo_produto"] = max(
        0, estado.get("tempo_ate_proximo_produto", 0) - delta_s)
    if estado["tempo_ate_proximo_produto"] <= 0:
        if not liberar_proximo_produto(estado):
            estado["tempo_ate_proximo_produto"] = 0.2

    terminou_fila = estado.get("proximo_produto", 0) >= len(estado["produtos"])
    if (estado.get("modo") == MODO_FASES and terminou_fila
            and not estado.get("produtos_ativos")):
        estado["fase"] = FASE_CONCLUIDA
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
        estado = criar_estado_menu(carregar_recorde(caminho))
        estado["caminho_perfil"] = Path(__file__).resolve().parents[1] / CAMINHO_PERFIL
        estado["perfil"] = carregar_perfil(estado["caminho_perfil"])
        while True:
            delta_s = relogio.tick(FPS) / 1000
            if not processar_eventos(estado, zona):
                persistir_carteira(estado)
                break
            atualizar(estado, caminho, zona, delta_s)
            if estado["fase"] == FASE_MENU:
                estado["controles"] = "1: Fases | 2: Infinito | 3: Loja | Esc: sair"
            elif estado["fase"] == FASE_LOJA:
                estado["controles"] = "Setas: escolher | Enter: comprar/equipar | Esc ou M: voltar"
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
