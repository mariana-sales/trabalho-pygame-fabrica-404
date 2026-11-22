"""Prévia visual independente; dados fictícios, sem regras ou persistência.

python -m src.previa --salvar pasta  # imagens de todas as telas, sem janela
python -m src.previa                # Espaço alterna exemplos; Esc sai
python -m src.previa --tamanho 1280x720  # janela redimensionável
"""
import argparse
import os
from pathlib import Path


def exemplos():
    from src.config import ZONA_Y, ZONA_ALTURA, ALTURA_PRODUTO
    produto = dict(nome="Caixa", faixa=1,
                   defeitos=["embalagem_danificada", "etiqueta_incompleta", "codigo_ilegivel"],
                   recomendacao_ia="aprovar")
    estado = dict(fase="jogando", produtos=[produto.copy() for _ in range(10)],
                  indice=5, pos_produto=ZONA_Y+ZONA_ALTURA-ALTURA_PRODUTO-4,
                  faixa_inspetor=1, pontos=40, erros=1,
                  ia_errou=3, ia_corrigida=2, resultado=None, frames_feedback=0,
                  desfecho=None, recorde=80,
                  controles="PRÉVIA · Espaço: alternar | Esc: sair")
    yield "inspecao", estado.copy()
    for nome in ("Garrafa", "Lata", "Pacote", "Frasco"):
        yield nome, dict(estado, produtos=[dict(produto, nome=nome) for _ in range(10)])
    yield "antes_inspecao", dict(estado, pos_produto=ZONA_Y-ALTURA_PRODUTO)
    yield "apos_inspecao", dict(estado, pos_produto=ZONA_Y+ZONA_ALTURA)
    for nome, decisao, jogador, ia in [("correcao", "rejeitar", True, False),
                                      ("erro", "aprovar", False, False),
                                      ("ia_acertou", "rejeitar", True, True),
                                      ("tempo", None, False, False)]:
        exemplo = dict(estado, fase="feedback", resultado=dict(
            decisao=decisao, resposta_correta="rejeitar", jogador_acertou=jogador,
            ia_acertou=ia, ia_corrigida=jogador and not ia))
        if ia:
            exemplo["produtos"] = [dict(produto, recomendacao_ia="rejeitar") for _ in range(10)]
        yield nome, exemplo
    yield "vitoria", dict(estado, fase="fim", desfecho="vitoria", indice=10,
                          pontos=80, erros=2, ia_errou=4, ia_corrigida=3)
    yield "derrota", dict(estado, fase="fim", desfecho="derrota", erros=3)


def tamanho_janela(valor):
    try:
        largura, altura = (int(parte) for parte in valor.lower().split("x"))
        if largura <= 0 or altura <= 0:
            raise ValueError
        return largura, altura
    except ValueError as erro:
        raise argparse.ArgumentTypeError("Use LARGURAxALTURA, por exemplo 800x600.") from erro


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--salvar", type=Path)
    parser.add_argument("--tamanho", type=tamanho_janela, default=(800, 600))
    args = parser.parse_args()
    if args.salvar:
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        os.environ["SDL_AUDIODRIVER"] = "dummy"
    import pygame
    from src.config import (LARGURA_TELA, FAIXAS_X, ZONA_Y, ZONA_ALTURA,
                            LARGURA_PRODUTO, ALTURA_PRODUTO)
    from src.desenho import criar_fontes, desenhar_jogo
    pygame.init()
    try:
        flags = 0 if args.salvar else pygame.RESIZABLE
        tela = pygame.display.set_mode(args.tamanho, flags)
        pygame.display.set_caption("Fábrica 404 — PRÉVIA VISUAL (dados fictícios)")
        fontes = criar_fontes()
        zona = pygame.Rect(0, ZONA_Y, LARGURA_TELA, ZONA_ALTURA)
        cenas = list(exemplos())

        def renderizar(estado, tempo_ms=None):
            rect = None
            if 0 <= estado["indice"] < len(estado["produtos"]):
                produto = estado["produtos"][estado["indice"]]
                rect = pygame.Rect(0, estado["pos_produto"], LARGURA_PRODUTO, ALTURA_PRODUTO)
                rect.centerx = FAIXAS_X[produto["faixa"]]
            desenhar_jogo(tela, fontes, estado, zona, rect, tempo_ms=tempo_ms)

        if args.salvar:
            args.salvar.mkdir(parents=True, exist_ok=True)
            for nome, estado in cenas:
                renderizar(estado, tempo_ms=0)
                pygame.image.save(tela, str(args.salvar / f"{nome}.png"))
            return
        indice = 0
        rodando = True
        relogio = pygame.time.Clock()
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                elif evento.type == pygame.VIDEORESIZE:
                    tela = pygame.display.set_mode(evento.size, flags)
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        rodando = False
                    elif evento.key == pygame.K_SPACE:
                        indice = (indice + 1) % len(cenas)
            renderizar(cenas[indice][1])
            pygame.display.flip()
            relogio.tick(30)
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
