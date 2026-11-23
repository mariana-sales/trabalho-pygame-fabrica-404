"""Percurso contínuo e integração com as regras reais, sem gravar recorde."""
import copy
import pygame
import pytest
from src.config import (Y_INICIO_ESTEIRA, Y_PARADA_PRODUTO, Y_PASSAGEM_PORTA,
                        FAIXAS_X, ZONA_Y, ZONA_ALTURA)
from src.funcoes import criar_estado, resposta_correta
from src.jogo import atualizar, tentar_decidir, criar_zona, rect_do_produto
from src.transporte import avancar_transporte, rect_produto
from src.desenho import estados_portas_inspecao, desenhar_esteiras


@pytest.mark.parametrize("fps", [30, 60, 144])
def test_velocidade_independe_do_fps_e_para_sem_ultrapassar(fps):
    y = Y_INICIO_ESTEIRA
    for _ in range(fps // 2):
        y = avancar_transporte(y, 1/fps)
    assert y == pytest.approx(Y_INICIO_ESTEIRA + 51)
    assert avancar_transporte(y, 10) == Y_PARADA_PRODUTO
    assert avancar_transporte(Y_PARADA_PRODUTO, 10) == Y_PARADA_PRODUTO


@pytest.mark.parametrize("faixa", range(3))
def test_trajeto_porta_e_escala_continuos(faixa, tmp_path):
    estado = criar_estado(0)
    estado["produtos"][0]["faixa"] = faixa
    zona = pygame.Rect(0, ZONA_Y, 800, ZONA_ALTURA)
    anterior = rect_produto(estado)
    assert anterior.top == Y_INICIO_ESTEIRA
    for _ in range(90):
        atualizar(estado, tmp_path / "recorde.txt", zona, 1/60)
        rect = rect_produto(estado)
        assert rect.centerx == FAIXAS_X[faixa]
        assert 0 <= rect.top-anterior.top <= 2
        assert 0 <= rect.width-anterior.width <= 1
        porta = estados_portas_inspecao(estado["produtos"][0], rect, zona)[faixa]
        if rect.colliderect(zona):
            assert rect.top >= Y_PASSAGEM_PORTA
            assert porta == "fechada"
        else:
            assert porta == "aberta"
        assert rect == rect_do_produto(estado)
        anterior = rect
    assert rect.top == Y_PARADA_PRODUTO
    assert rect.bottom <= zona.bottom


def test_entrada_prematura_ou_faixa_errada_nao_decide(tmp_path):
    estado = criar_estado(0)
    estado["faixa_inspetor"] = estado["produtos"][0]["faixa"]
    zona = criar_zona()
    tentar_decidir(estado, "aprovar", zona)
    assert estado["fase"] == "jogando"
    atualizar(estado, tmp_path / "recorde.txt", zona, 2)
    estado["faixa_inspetor"] = (estado["faixa_inspetor"] + 1) % 3
    tentar_decidir(estado, "aprovar", zona)
    assert estado["resultado"] is None
    assert estado["pontos"] == estado["erros"] == 0


@pytest.mark.parametrize("acertar,desfecho,total", [(True, "vitoria", 10), (False, "derrota", 3)])
def test_partida_completa_sem_repetir_decisoes(acertar, desfecho, total, tmp_path):
    estado = criar_estado(0)
    zona = criar_zona()
    caminho = tmp_path / "dados" / "recorde.txt"
    for i in range(total):
        assert estado["indice"] == i
        assert estado["pos_produto"] == Y_INICIO_ESTEIRA
        produto = estado["produtos"][i]
        estado["faixa_inspetor"] = produto["faixa"]
        atualizar(estado, caminho, zona, 2)
        decisao = resposta_correta(produto)
        if not acertar:
            decisao = "aprovar" if decisao == "rejeitar" else "rejeitar"
        tentar_decidir(estado, decisao, zona)
        assert estado["fase"] == "feedback"
        pontos, erros = estado["pontos"], estado["erros"]
        tentar_decidir(estado, decisao, zona)
        atualizar(estado, caminho, zona, 0.5)
        assert (estado["pontos"], estado["erros"]) == (pontos, erros)
        atualizar(estado, caminho, zona, 1.5)
    assert estado["fase"] == "fim"
    assert estado["desfecho"] == desfecho
    assert estado["pontos"] == (100 if acertar else 0)
    assert estado["indice"] == total - 1
    assert rect_do_produto(estado) is not None
    if acertar:
        assert estado["ia_errou"] == estado["ia_corrigida"] == 4
        assert caminho.read_text() == "100"
    antes = copy.deepcopy(estado)
    tentar_decidir(estado, "aprovar", zona)
    atualizar(estado, caminho, zona, 100)
    assert estado == antes


def test_plataforma_inspecao_imovel_com_transporte_ativo():
    quadros = []
    for tempo in (0, 140):
        tela = pygame.Surface((800, 600))
        desenhar_esteiras(tela, 1, tempo, True)
        quadros.append(tela)
    area = pygame.Rect(0, Y_PASSAGEM_PORTA, 800, 100)
    assert pygame.image.tobytes(quadros[0].subsurface(area), "RGB") == pygame.image.tobytes(
        quadros[1].subsurface(area), "RGB")


def test_loop_abre_desenha_e_sai_sem_gravar(monkeypatch):
    from src import jogo
    chamadas = []
    eventos = iter([[], [pygame.event.Event(pygame.QUIT)]])
    monkeypatch.setattr(jogo.pygame.event, "get", lambda: next(eventos))
    monkeypatch.setattr(jogo, "carregar_recorde", lambda _: 0)
    monkeypatch.setattr(jogo, "salvar_recorde", lambda *args: pytest.fail("Não houve decisão"))
    desenhar = jogo.desenhar_jogo
    def observar(*args, **kwargs):
        chamadas.append(args[2]["pos_produto"])
        return desenhar(*args, **kwargs)
    monkeypatch.setattr(jogo, "desenhar_jogo", observar)
    jogo.executar_jogo()
    assert len(chamadas) == 1
    assert Y_INICIO_ESTEIRA <= chamadas[0] < Y_PARADA_PRODUTO
