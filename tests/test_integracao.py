"""Contratos entre o loop da Mariana, o layout, as portas e a persistência."""
import copy
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
import pygame
import pytest
from src import jogo, desenho, funcoes
from src.config import (FAIXAS_X, Y_INICIO_ESTEIRA, Y_PARADA_PRODUTO,
                        DURACAO_FEEDBACK, Y_PASSAGEM_PORTA)
from src.dados import carregar_recorde


@pytest.fixture
def eventos(monkeypatch):
    pygame.init()
    fila = []
    monkeypatch.setattr(pygame.event, "get", lambda: list(fila))
    yield fila
    pygame.quit()


@pytest.mark.parametrize("faixa", range(3))
def test_primeira_colisao_permite_decisao_com_porta_ja_fechada(faixa, tmp_path):
    estado = funcoes.criar_estado(0)
    estado["produtos"][0]["faixa"] = estado["faixa_inspetor"] = faixa
    zona = jogo.criar_zona()
    while not jogo.rect_do_produto(estado).colliderect(zona):
        jogo.atualizar(estado, tmp_path / "recorde.txt", zona)
    assert estado["pos_produto"] < Y_PARADA_PRODUTO  # Colisão, não só parada.
    rect = jogo.rect_do_produto(estado)
    assert rect.top >= Y_PASSAGEM_PORTA
    jogo.tentar_decidir(estado, "aprovar", zona)
    assert estado["fase"] == "feedback"
    assert desenho.estados_portas_inspecao(estado["produtos"][0], rect, zona)[faixa] == "fechada"


def test_zona_preserva_largura_das_tres_marcacoes():
    zona = jogo.criar_zona()
    for faixa, x in enumerate(FAIXAS_X):
        rect = desenho.zona_da_faixa(zona, faixa)
        assert rect.width == 80
        assert rect.centerx == x


@pytest.mark.parametrize("fps", [30, 60, 144])
def test_feedback_regressivo_dura_dois_segundos(fps, tmp_path):
    estado = funcoes.criar_estado(0)
    estado["pos_produto"] = Y_PARADA_PRODUTO
    estado["faixa_inspetor"] = estado["produtos"][0]["faixa"]
    zona = jogo.criar_zona()
    jogo.tentar_decidir(estado, "aprovar", zona)
    assert estado["frames_feedback"] == DURACAO_FEEDBACK
    for _ in range(2 * fps - 1):
        jogo.atualizar(estado, tmp_path / "recorde.txt", zona, 1/fps)
    assert estado["fase"] == "feedback"
    jogo.atualizar(estado, tmp_path / "recorde.txt", zona, 1/fps)
    assert estado["fase"] == "jogando"
    assert estado["indice"] == 1
    assert estado["pos_produto"] == Y_INICIO_ESTEIRA
    assert estado["resultado"] is None
    assert estado["frames_feedback"] == 0


@pytest.mark.parametrize("fase", ["feedback", "fim"])
def test_setas_e_decisoes_bloqueadas_fora_da_partida(fase, eventos):
    estado = funcoes.criar_estado(0)
    estado.update(fase=fase, pos_produto=Y_PARADA_PRODUTO)
    antes = copy.deepcopy(estado)
    for tecla in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_r):
        eventos[:] = [pygame.event.Event(pygame.KEYDOWN, key=tecla)]
        assert jogo.processar_eventos(estado, jogo.criar_zona())
        assert estado == antes


def test_enter_reinicia_preservando_recorde_e_identidade_do_estado(eventos):
    estado = funcoes.criar_estado(100)
    estado.update(fase="fim", indice=9, pontos=100, erros=2, desfecho="vitoria")
    identidade = id(estado)
    eventos[:] = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)]
    assert jogo.processar_eventos(estado, jogo.criar_zona())
    assert id(estado) == identidade
    assert estado["recorde"] == 100
    assert estado["pontos"] == estado["erros"] == estado["indice"] == 0
    assert estado["fase"] == "jogando"
    assert len(estado["produtos"]) == 10
    antes = copy.deepcopy(estado)
    jogo.processar_eventos(estado, jogo.criar_zona())
    assert estado == antes  # Enter fora do fim não reinicia.


@pytest.mark.parametrize("tipo,campos", [(pygame.QUIT, {}), (pygame.KEYDOWN, {"key": pygame.K_ESCAPE})])
def test_fecha_em_qualquer_fase(tipo, campos, eventos):
    for fase in ("jogando", "feedback", "fim"):
        estado = funcoes.criar_estado(0)
        estado["fase"] = fase
        eventos[:] = [pygame.event.Event(tipo, **campos)]
        assert not jogo.processar_eventos(estado, jogo.criar_zona())


def test_derrota_no_decimo_e_recorde_persistente(tmp_path, monkeypatch):
    caminho = tmp_path / "nova_pasta" / "recorde.txt"
    estado = funcoes.criar_estado(0)
    estado.update(indice=9, pontos=70, erros=2, pos_produto=Y_PARADA_PRODUTO)
    produto = estado["produtos"][9]
    estado["faixa_inspetor"] = produto["faixa"]
    errada = "aprovar" if produto["defeitos"] else "rejeitar"
    jogo.tentar_decidir(estado, errada, jogo.criar_zona())
    assert not caminho.exists()  # Persistência apenas ao encerrar a partida.
    jogo.atualizar(estado, caminho, jogo.criar_zona(), 2)
    assert estado["desfecho"] == "derrota"
    assert estado["indice"] == 9
    assert estado["recorde"] == carregar_recorde(caminho) == 70
    # Nova sessão, pontuação inferior: manter arquivo e valor anteriores.
    estado = funcoes.criar_estado(carregar_recorde(caminho))
    estado.update(fase="feedback", indice=9, pontos=60, erros=2, frames_feedback=1)
    monkeypatch.setattr(jogo, "salvar_recorde", lambda *args: pytest.fail("Não deve regravar recorde menor"))
    jogo.atualizar(estado, caminho, jogo.criar_zona())
    assert estado["desfecho"] == "vitoria"
    assert estado["recorde"] == carregar_recorde(caminho) == 70


def test_feedback_das_regras_cabe_no_painel(eventos):
    fontes = desenho.criar_fontes()
    produto = dict(nome="Caixa", faixa=1, defeitos=list(funcoes.DEFEITOS), recomendacao_ia="aprovar")
    for decisao in (None, "aprovar", "rejeitar"):
        resultado = funcoes.avaliar_decisao(produto, decisao)
        linhas = desenho.linhas_feedback(produto, resultado)
        assert linhas[1:] == funcoes.texto_feedback(produto, resultado)[1:]
        for i, linha in enumerate(linhas):
            fonte = fontes["normal"] if i == 0 else fontes["pequena"]
            assert fonte.size(linha)[0] <= 744


def test_loop_real_vitoria_enter_derrota_e_recorde(tmp_path, monkeypatch):
    """Percorre executar_jogo com eventos reais de tecla e tempo acelerado."""
    caminho = tmp_path / "sessao" / "recorde.txt"
    monkeypatch.setattr(jogo, "CAMINHO_RECORDE", str(caminho))
    quadros = []
    finais = []
    desenhar = jogo.desenhar_jogo

    class Relogio:
        def tick(self, fps):
            return 1000

    monkeypatch.setattr(jogo.pygame.time, "Clock", Relogio)

    def observar(tela, fontes, estado, zona, rect):
        quadros.append(copy.deepcopy(estado))
        if estado["fase"] == "fim":
            finais.append(estado["desfecho"])
        desenhar(tela, fontes, estado, zona, rect)

    def teclado():
        assert len(quadros) < 200, "O loop não alcançou o fim esperado"
        if not quadros:
            return []
        estado = quadros[-1]
        if estado["fase"] == "fim":
            if len(finais) == 2:
                return [pygame.event.Event(pygame.QUIT)]
            tecla = pygame.K_RETURN
        elif estado["fase"] == "feedback":
            return []
        else:
            produto = estado["produtos"][estado["indice"]]
            diferenca = produto["faixa"] - estado["faixa_inspetor"]
            if diferenca:
                tecla = pygame.K_RIGHT if diferenca > 0 else pygame.K_LEFT
            else:
                decisao = funcoes.resposta_correta(produto)
                if finais:  # Segunda partida: três erros deliberados.
                    decisao = "rejeitar" if decisao == "aprovar" else "aprovar"
                tecla = pygame.K_a if decisao == "aprovar" else pygame.K_r
        return [pygame.event.Event(pygame.KEYDOWN, key=tecla)]

    monkeypatch.setattr(jogo, "desenhar_jogo", observar)
    monkeypatch.setattr(jogo.pygame.event, "get", teclado)
    jogo.executar_jogo()
    assert finais == ["vitoria", "derrota"]
    assert carregar_recorde(caminho) == 100
    assert quadros[-1]["recorde"] == 100
    assert "Enter" in quadros[-1]["controles"]
