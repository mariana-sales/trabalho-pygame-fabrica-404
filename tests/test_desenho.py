"""Verificação do contrato de desenho, sem janela nem arquivo real de recorde."""
import copy
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
import pytest
from src import desenho
from src.config import (FAIXAS_X, Y_INSPETOR, ZONA_Y, ZONA_ALTURA,
                        ALTURA_INSPETOR, PORTAS_X, Y_BASE_PORTAS,
                        LARGURA_TELA, ALTURA_TELA, LARGURA_PRODUTO, ALTURA_PRODUTO,
                        Y_INICIO_ESTEIRA, Y_FIM_ESTEIRA, Y_PASSAGEM_PORTA)
from src.previa import exemplos


@pytest.fixture
def superficie():
    pygame.init()
    yield pygame.Surface((LARGURA_TELA, ALTURA_TELA)), desenho.criar_fontes()
    pygame.quit()


def rect_inspecao(faixa=1):
    rect = pygame.Rect(0, ZONA_Y+ZONA_ALTURA-ALTURA_PRODUTO-4,
                       LARGURA_PRODUTO, ALTURA_PRODUTO)
    rect.centerx = FAIXAS_X[faixa]
    return rect


@pytest.mark.parametrize("nome,estado", list(exemplos()))
def test_telas_preservam_estado(superficie, nome, estado):
    tela, fontes = superficie
    antes = copy.deepcopy(estado)
    zona = pygame.Rect(0, ZONA_Y, LARGURA_TELA, ZONA_ALTURA)
    rect = rect_inspecao()
    rect_antes = rect.copy()
    desenho.desenhar_jogo(tela, fontes, estado, zona, rect, tempo_ms=0)
    assert estado == antes
    assert rect == rect_antes
    assert tela.get_bounding_rect().size == (LARGURA_TELA, ALTURA_TELA)


@pytest.mark.parametrize("faixa", range(3))
def test_inspetor_respeita_faixa(superficie, faixa):
    tela, _ = superficie
    tela.fill((0, 0, 0))
    desenho.desenhar_inspetor(tela, faixa)
    for outra in range(3):
        area = tela.subsurface((FAIXAS_X[outra]-40, Y_INSPETOR-ALTURA_INSPETOR,
                                80, ALTURA_INSPETOR))
        pixels = pygame.image.tobytes(area, "RGB")
        assert any(pixels) == (outra == faixa)


def test_produto_respeita_rect(superficie):
    tela, _ = superficie
    tela.fill((0, 0, 0))
    rect = pygame.Rect(60, 300, 60, 50)
    desenho.desenhar_produto(tela, rect)
    assert tela.get_at(rect.center)[:3] != (0, 0, 0)
    assert tela.get_at((125, 325))[:3] == (0, 0, 0)


def test_cenario_sem_artes(superficie, monkeypatch, tmp_path):
    tela, _ = superficie
    monkeypatch.setattr(desenho, "ARTES", tmp_path)
    desenho._arte.cache_clear()
    desenho._zona_em_perspectiva.cache_clear()
    try:
        desenho.desenhar_cenario(tela, pygame.Rect(0, ZONA_Y, LARGURA_TELA, ZONA_ALTURA))
        desenho.desenhar_inspetor(tela, 1)
        assert tela.get_at((FAIXAS_X[1], Y_INSPETOR - 48))[:3] == desenho.AMARELO
    finally:
        desenho._arte.cache_clear()
        desenho._zona_em_perspectiva.cache_clear()


def test_modelos_selecionados_e_encaixe_portas(superficie):
    for x in PORTAS_X:
        aberta = desenho._arte("porta_b_aberta_central.png", (120, 120))
        fechada = desenho._arte("porta_b_fechada_central.png", (120, 120))
        assert aberta is not None and fechada is not None
        assert aberta.get_rect(midbottom=(x, Y_BASE_PORTAS)) == fechada.get_rect(midbottom=(x, Y_BASE_PORTAS))
    assert desenho._arte("esteira_central.png", (150, Y_FIM_ESTEIRA-Y_INICIO_ESTEIRA)) is not None
    assert desenho._arte("inspetor_a.png", (76, ALTURA_INSPETOR)).get_height() == ALTURA_INSPETOR
    for faixa in range(3):
        zona = desenho._zona_em_perspectiva((98, 40), faixa)
        assert zona.get_at((zona.get_width()//2, zona.get_height()//2)).a == 0


@pytest.mark.parametrize("faixa", range(3))
def test_produto_na_inspecao_fica_inteiro_visivel(superficie, faixa):
    tela, fontes = superficie
    _, estado = next(exemplos())
    estado["faixa_inspetor"] = faixa
    produto = estado["produtos"][estado["indice"]]
    produto["faixa"] = faixa
    rect = rect_inspecao(faixa)
    zona = pygame.Rect(0, ZONA_Y, LARGURA_TELA, ZONA_ALTURA)
    desenho.desenhar_jogo(tela, fontes, estado, zona, rect, tempo_ms=0)
    isolado = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
    desenho.desenhar_produto(isolado, rect, produto)
    for y in range(rect.top, rect.bottom):
        for x in range(rect.left, rect.right):
            pixel = isolado.get_at((x, y))
            if pixel.a == 255:
                assert tela.get_at((x, y))[:3] == pixel[:3]


@pytest.mark.parametrize("faixa", range(3))
def test_porta_abre_fecha_e_reabre_conforme_ocupacao(faixa):
    zona = pygame.Rect(0, ZONA_Y, LARGURA_TELA, ZONA_ALTURA)
    produto = {"faixa": faixa}
    rect = pygame.Rect(0, ZONA_Y-ALTURA_PRODUTO, LARGURA_PRODUTO, ALTURA_PRODUTO)
    rect.centerx = FAIXAS_X[faixa]
    abertas = ("aberta",) * 3
    assert desenho.estados_portas_inspecao(produto, rect, zona) == abertas

    rect.y = Y_PASSAGEM_PORTA - 1  # Ainda não passou inteiro pelo plano da porta.
    assert desenho.estados_portas_inspecao(produto, rect, zona) == abertas
    rect.y = ZONA_Y - ALTURA_PRODUTO + 1  # Primeiro contato com a zona: já passou pela porta.
    esperado = list(abertas)
    esperado[faixa] = "fechada"
    assert desenho.estados_portas_inspecao(produto, rect, zona) == tuple(esperado)
    rect.y = ZONA_Y
    assert desenho.estados_portas_inspecao(produto, rect, zona) == tuple(esperado)
    rect.y = zona.bottom  # Borda sem sobreposição: zona livre novamente.
    assert desenho.estados_portas_inspecao(produto, rect, zona) == abertas
    assert desenho.estados_portas_inspecao(produto, None, zona) == abertas
    assert desenho.estados_portas_inspecao(None, rect, zona) == abertas
    rect.topleft = (0, ZONA_Y)  # Mesmo y, mas fora da faixa: não fecha.
    assert desenho.estados_portas_inspecao(produto, rect, zona) == abertas



def test_renderizacao_usa_ocupacao_mesmo_no_feedback(superficie, monkeypatch):
    tela, fontes = superficie
    _, estado = next(exemplos())
    estado["portas"] = ("aberta",) * 3  # Valor antigo não deve manter a zona ocupada aberta.
    zona = pygame.Rect(0, ZONA_Y, LARGURA_TELA, ZONA_ALTURA)
    rect = rect_inspecao()
    chamadas = []
    monkeypatch.setattr(desenho, "desenhar_portas", lambda tela, portas: chamadas.append(portas))
    for fase in ("jogando", "feedback"):
        estado["fase"] = fase
        desenho.desenhar_jogo(tela, fontes, estado, zona, rect)
        assert chamadas[-1] == ("aberta", "fechada", "aberta")
    desenho.desenhar_jogo(tela, fontes, estado, zona, None)
    assert chamadas[-1] == ("aberta",) * 3


@pytest.mark.parametrize("faixa", range(3))
def test_destaque_acompanha_produto_independente_do_inspetor(superficie, monkeypatch, faixa):
    tela, fontes = superficie
    _, estado = next(exemplos())
    estado["produtos"][estado["indice"]]["faixa"] = faixa
    estado["faixa_inspetor"] = (faixa+1) % len(FAIXAS_X)
    zona = pygame.Rect(0, ZONA_Y, LARGURA_TELA, ZONA_ALTURA)
    chamadas = []
    desenhar = desenho.desenhar_esteiras

    def observar(tela, faixa_ativa=None, tempo_ms=0, em_movimento=True):
        chamadas.append(faixa_ativa)
        return desenhar(tela, faixa_ativa, tempo_ms, em_movimento)

    monkeypatch.setattr(desenho, "desenhar_esteiras", observar)
    desenho.desenhar_jogo(tela, fontes, estado, zona, rect_inspecao(faixa), tempo_ms=0)
    assert chamadas[-1] == faixa
    desenho.desenhar_jogo(tela, fontes, estado, zona, None, tempo_ms=0)
    assert chamadas[-1] is None


@pytest.mark.parametrize("faixa", range(3))
def test_luzes_das_portas_indicam_ocupacao_e_liberacao(superficie, faixa):
    tela, fontes = superficie
    _, estado = next(exemplos())
    estado["produtos"][estado["indice"]]["faixa"] = faixa
    zona = pygame.Rect(0, ZONA_Y, LARGURA_TELA, ZONA_ALTURA)
    rect = rect_inspecao(faixa)
    desenho.desenhar_jogo(tela, fontes, estado, zona, rect, tempo_ms=0)
    for outra, x in enumerate(PORTAS_X):
        esperado = desenho.AMARELO if outra == faixa else desenho.CIANO
        assert tela.get_at((x, Y_BASE_PORTAS-112))[:3] == esperado
    rect.top = zona.bottom
    desenho.desenhar_jogo(tela, fontes, estado, zona, rect, tempo_ms=0)
    for x in PORTAS_X:
        assert tela.get_at((x, Y_BASE_PORTAS-112))[:3] == desenho.CIANO


def test_animacao_visual_sem_mudar_partida(superficie):
    tela, fontes = superficie
    _, estado = next(exemplos())
    antes = copy.deepcopy(estado)
    zona = pygame.Rect(0, ZONA_Y, LARGURA_TELA, ZONA_ALTURA)
    rect = rect_inspecao()
    rect_antes = rect.copy()
    desenho.desenhar_jogo(tela, fontes, estado, zona, rect, tempo_ms=0)
    primeiro = pygame.image.tobytes(tela, "RGB")
    desenho.desenhar_jogo(tela, fontes, estado, zona, rect, tempo_ms=140)
    assert pygame.image.tobytes(tela, "RGB") != primeiro
    desenho.desenhar_jogo(tela, fontes, estado, zona, rect, tempo_ms=0)
    assert pygame.image.tobytes(tela, "RGB") == primeiro
    assert estado == antes
    assert rect == rect_antes


def test_esteiras_paradas_nao_animam(superficie):
    tela, _ = superficie
    quadros = []
    for tempo in (0, 140):
        tela.fill((0, 0, 0))
        desenho.desenhar_esteiras(tela, faixa_ativa=1, tempo_ms=tempo, em_movimento=False)
        quadros.append(pygame.image.tobytes(tela, "RGB"))
    assert quadros[0] == quadros[1]


@pytest.mark.parametrize("tamanho", [(800, 600), (1280, 720), (600, 800)])
def test_renderizacao_preenche_janelas_de_proporcoes_distintas(superficie, tamanho):
    _, fontes = superficie
    _, estado = next(exemplos())
    antes = copy.deepcopy(estado)
    zona = pygame.Rect(0, ZONA_Y, LARGURA_TELA, ZONA_ALTURA)
    quadros = []
    for sentinela in ((255, 0, 255), (0, 255, 0)):
        tela = pygame.Surface(tamanho)
        tela.fill(sentinela)
        desenho.desenhar_jogo(tela, fontes, estado, zona, rect_inspecao(), tempo_ms=0)
        quadros.append(pygame.image.tobytes(tela, "RGB"))
    assert quadros[0] == quadros[1]  # Nenhum pixel conserva o quadro anterior.
    assert estado == antes


def test_fundo_chega_as_bordas_sem_margens_lisas(superficie):
    tela, _ = superficie
    desenho.desenhar_fundo(tela)
    for x in (0, tela.get_width()-1):
        cores = {tuple(tela.get_at((x, y))) for y in range(0, tela.get_height(), 30)}
        assert len(cores) > 1


@pytest.mark.parametrize("decisao,jogador,ia,termo", [
    ("rejeitar", True, True, "acert"),
    ("rejeitar", True, False, "acert"),
    ("aprovar", False, True, "err"),
    ("aprovar", False, False, "err"),
    (None, False, False, "tempo"),
])
def test_feedback_curto_reflete_resultado(decisao, jogador, ia, termo):
    produto = dict(nome="Caixa", faixa=1, defeitos=["codigo_ilegivel"],
                   recomendacao_ia="rejeitar" if ia else "aprovar")
    resultado = dict(decisao=decisao, resposta_correta="rejeitar",
                     jogador_acertou=jogador, ia_acertou=ia,
                     ia_corrigida=jogador and not ia)
    antes = copy.deepcopy((produto, resultado))
    linhas = desenho.linhas_feedback(produto, resultado)
    assert 1 <= len(linhas) <= 3
    assert termo in linhas[0].lower()
    texto = " ".join(linhas).lower()
    assert "ia" in texto
    if resultado["ia_corrigida"]:
        assert "corrig" in texto or "diverg" in texto
    if not jogador:
        assert "você corrigiu" not in texto
    assert (produto, resultado) == antes
