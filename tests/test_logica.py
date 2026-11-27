"""Contratos das regras da fábrica, incluindo avaliação e desfechos."""
import random

import pygame
import pytest

from src import funcoes as f
from src.config import DEFEITOS, NOMES_PRODUTOS


def produto(defeitos=(), recomendacao="aprovar"):
    return dict(nome="Caixa", faixa=1, defeitos=list(defeitos), recomendacao_ia=recomendacao)


def test_calcular_pontos():
    assert f.calcular_pontos(10, 5) == 15


@pytest.mark.parametrize("valor,esperado", [(-5, 0), (150, 100), (50, 50), (0, 0), (100, 100)])
def test_limitar_valor(valor, esperado):
    assert f.limitar_valor(valor, 0, 100) == esperado


def test_colisao_zona():
    zona = pygame.Rect(0, 400, 600, 80)
    assert f.verificar_colisao(pygame.Rect(100, 410, 60, 50), zona)
    assert not f.verificar_colisao(pygame.Rect(100, 480, 60, 50), zona)
    assert not f.verificar_colisao(pygame.Rect(100, 300, 60, 50), zona)


def test_mover_inspetor():
    assert [f.mover_faixa(faixa, direcao, 3) for faixa, direcao in
            [(0, -1), (0, 1), (1, -1), (1, 1), (2, 1)]] == [0, 1, 0, 2, 2]


def test_pode_decidir():
    for inspetor in range(3):
        for faixa in range(3):
            for na_zona in (False, True):
                assert f.pode_decidir(inspetor, faixa, na_zona) == (inspetor == faixa and na_zona)


def test_produto_passou_da_zona():
    assert not f.produto_passou_da_zona(479, 480)
    assert not f.produto_passou_da_zona(480, 480)
    assert f.produto_passou_da_zona(481, 480)


def test_indices_unicos_e_validos():
    for quantidade in (0, 4, 10):
        indices = f.sortear_indices(10, quantidade)
        assert len(indices) == len(set(indices)) == quantidade
        assert all(0 <= i < 10 for i in indices)


def test_indices_nao_sao_sempre_fixos():
    anterior = random.getstate()
    try:
        resultados = set()
        for seed in range(20):
            random.seed(seed)
            resultados.add(tuple(sorted(f.sortear_indices(10, 4))))
        assert len(resultados) > 1
    finally:
        random.setstate(anterior)


def test_sortear_defeitos():
    for _ in range(20):
        defeitos = f.sortear_defeitos()
        assert 1 <= len(defeitos) <= 3
        assert len(defeitos) == len(set(defeitos))
        assert set(defeitos) <= set(DEFEITOS)


def test_inverter_recomendacao():
    assert f.inverter_recomendacao("aprovar") == "rejeitar"
    assert f.inverter_recomendacao("rejeitar") == "aprovar"


def test_partida_10_produtos_5_defeituosos_4_erros_ia():
    for _ in range(20):
        produtos = f.gerar_produtos(10, 5, 4)
        assert len(produtos) == 10
        assert sum(bool(p["defeitos"]) for p in produtos) == 5
        # Oráculo independente: não usar ia_acertou para validar o gerador.
        assert sum(p["recomendacao_ia"] != ("rejeitar" if p["defeitos"] else "aprovar")
                   for p in produtos) == 4
        for p in produtos:
            assert p["nome"] in NOMES_PRODUTOS
            assert p["faixa"] in range(3)
            assert p["recomendacao_ia"] in ("aprovar", "rejeitar")
            assert set(p["defeitos"]) <= set(DEFEITOS)


def test_resposta_correta():
    assert f.resposta_correta(produto()) == "aprovar"
    for defeito in DEFEITOS:
        assert f.resposta_correta(produto([defeito])) == "rejeitar"


def test_acerto_da_ia():
    for defeitos in ([], ["codigo_ilegivel"]):
        for recomendacao in ("aprovar", "rejeitar"):
            assert f.ia_acertou(produto(defeitos, recomendacao)) == (
                recomendacao == ("rejeitar" if defeitos else "aprovar"))


def test_criar_estado():
    estado = f.criar_estado(70)
    assert estado["recorde"] == 70
    assert estado["fase"] == "jogando"
    assert estado["indice"] == estado["pontos"] == estado["erros"] == 0
    assert len(estado["produtos"]) == 10
    assert sum(bool(p["defeitos"]) for p in estado["produtos"]) == 5


def test_decisoes_e_tempo_esgotado():
    for defeitos in ([], ["codigo_ilegivel"]):
        correta = "rejeitar" if defeitos else "aprovar"
        for ia in ("aprovar", "rejeitar"):
            for decisao in ("aprovar", "rejeitar", None):
                assert f.avaliar_decisao(produto(defeitos, ia), decisao) == dict(
                    decisao=decisao, resposta_correta=correta,
                    jogador_acertou=decisao == correta, ia_acertou=ia == correta,
                    ia_corrigida=decisao == correta and ia != correta)


def test_pontos_erros_e_contadores():
    for jogador, ia in [(True, True), (True, False), (False, True), (False, False)]:
        estado = f.criar_estado(50)
        estado.update(pontos=20, erros=1, ia_errou=1, ia_corrigida=1)
        resultado = dict(decisao="aprovar", resposta_correta="aprovar",
                         jogador_acertou=jogador, ia_acertou=ia, ia_corrigida=jogador and not ia)
        f.aplicar_resultado(estado, resultado)
        assert estado["pontos"] == (30 if jogador else 20)
        assert estado["erros"] == (1 if jogador else 2)
        assert estado["ia_errou"] == 1 + (not ia)
        assert estado["ia_corrigida"] == 1 + (jogador and not ia)


def test_tempo_esgotado_conta_erro():
    estado = f.criar_estado(0)
    f.aplicar_resultado(estado, f.avaliar_decisao(produto(), None))
    assert estado["erros"] == 1
    assert estado["pontos"] == 0


def test_avancar_produto():
    from src.config import Y_INICIO_ESTEIRA
    estado = f.criar_estado(50)
    estado.update(fase="feedback", pos_produto=450, pontos=20, erros=1,
                  resultado={"decisao": "aprovar"}, frames_feedback=40)
    f.avancar_produto(estado)
    assert estado["indice"] == 1
    assert estado["fase"] == "jogando"
    assert estado["pos_produto"] == Y_INICIO_ESTEIRA
    assert estado["resultado"] is None
    assert estado["frames_feedback"] == 0
    assert (estado["pontos"], estado["erros"], estado["recorde"]) == (20, 1, 50)


def test_derrota():
    assert [f.partida_perdida(n, 3) for n in (0, 2, 3, 4)] == [False, False, True, True]


def test_vitoria():
    assert f.partida_vencida(2, 10, 10, 3)
    assert not f.partida_vencida(2, 9, 10, 3)
    assert not f.partida_vencida(3, 10, 10, 3)


def test_desfecho_e_prioridade_derrota():
    assert f.verificar_desfecho(0, 9, 10, 3) is None
    assert f.verificar_desfecho(2, 10, 10, 3) == "vitoria"
    assert f.verificar_desfecho(3, 10, 10, 3) == "derrota"
    assert f.verificar_desfecho(3, 4, 10, 3) == "derrota"


@pytest.mark.parametrize("pos,vel,limite,esperado", [(100, 0.7, 480, 100.7),
    (479, 2, 480, 480), (480, 2, 480, 480), (100, 0, 480, 100)])
def test_mover_produto(pos, vel, limite, esperado):
    assert f.mover_produto(pos, vel, limite) == pytest.approx(esperado)


def test_texto_feedback_informa_ia_defeitos_e_tempo():
    p = produto(["codigo_ilegivel"], "aprovar")
    linhas = f.texto_feedback(p, f.avaliar_decisao(p, None))
    assert len(linhas) == 3
    assert "Tempo esgotado" in linhas[0]
    assert linhas[1] == "A IA errou."
    assert "Código ilegível" in linhas[2]

def test_prazo_chegada_esgota():
    estado = f.criar_estado(0)
    assert not f.contar_prazo_chegada(estado, False, 1.5)
    assert f.contar_prazo_chegada(estado, False, 0.5)


def test_prazo_chegada_para_ao_chegar():
    estado = f.criar_estado(0)
    assert not f.contar_prazo_chegada(estado, True, 1.0)
    assert estado["chegou"]
    assert not f.contar_prazo_chegada(estado, False, 10)


def test_prazo_chegada_reinicia_no_proximo_produto():
    estado = f.criar_estado(0)
    estado.update(chegou=True, tempo_chegada=0.3)
    f.avancar_produto(estado)
    assert estado["chegou"] is False
    assert estado["tempo_chegada"] == 2.0