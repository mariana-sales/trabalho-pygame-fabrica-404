"""Camada visual: apresenta o estado recebido, sem alterar regras ou transições."""
from functools import lru_cache
from math import ceil, cos, sin
from pathlib import Path

import pygame

from src.config import (FAIXAS_X, Y_INSPETOR, DEFEITOS, LIMITE_ERROS,
                        FASE_FIM, FASE_FEEDBACK, FASE_JOGANDO, PORTAS_X,
                        Y_BASE_PORTAS, Y_FIM_ESTEIRA, Y_INICIO_ESTEIRA,
                        ALTURA_INSPETOR)

ARTES = Path(__file__).resolve().parents[1] / "assets" / "imagens"
FUNDO = (13, 25, 36)
PAINEL = (15, 29, 41)
TEXTO = (231, 242, 248)
SUAVE = (163, 185, 200)
CIANO = (62, 216, 226)
AMARELO = (255, 199, 75)
VERDE = (102, 226, 153)
VERMELHO = (255, 132, 129)
SPRITES_PRODUTOS = {
    "Caixa": "produto_caixa.png", "Pacote": "produto_caixa.png",
    "Garrafa": "produto_garrafa.png", "Frasco": "produto_garrafa.png",
    "Lata": "produto_lata.png", "Peça mecânica": "produto_peca_mecanica.png",
}


def criar_fontes():
    return {"titulo": pygame.font.SysFont("segoeui", 24, bold=True),
            "normal": pygame.font.SysFont("segoeui", 17),
            "pequena": pygame.font.SysFont("segoeui", 14),
            "rotulo": pygame.font.SysFont("segoeui", 12),
            "numero": pygame.font.SysFont("segoeui", 22, bold=True)}


@lru_cache(maxsize=48)
def _arte(nome, tamanho=None):
    pasta = "fabrica404_v2" if nome.startswith(("produto_", "esteira_")) and not nome.startswith("esteira_a_") else "fabrica404"
    caminho = ARTES / pasta / nome
    if not caminho.is_file():
        return None
    original = pygame.image.load(str(caminho))
    if pygame.display.get_surface() is not None:
        original = original.convert_alpha()
    if tamanho is None:
        return original
    escala = min(1, tamanho[0] / original.get_width(), tamanho[1] / original.get_height())
    return pygame.transform.scale(original, (max(1, round(original.get_width()*escala)),
                                              max(1, round(original.get_height()*escala))))


def _cobrir(imagem, tamanho, ancorar_base=False):
    """Escala uniforme e recorte central; nunca deixa margens vazias."""
    escala = max(tamanho[0]/imagem.get_width(), tamanho[1]/imagem.get_height())
    ampliada = pygame.transform.scale(imagem, (ceil(imagem.get_width()*escala),
                                               ceil(imagem.get_height()*escala)))
    recorte = pygame.Rect(0, 0, *tamanho)
    recorte.center = ampliada.get_rect().center
    if ancorar_base:
        recorte.bottom = ampliada.get_height()
    return ampliada.subsurface(recorte).copy()


@lru_cache(maxsize=4)
def _fundo_pronto(raiz):
    original = _arte("fundo_fabrica.png")
    if original is None:
        return None
    fundo = _cobrir(original, (800, 600))
    # Escurecer apenas a camada distante mantém personagens e máquinas nítidos.
    sombra = pygame.Surface((800, 600), pygame.SRCALPHA)
    sombra.fill((5, 15, 25, 48))
    pygame.draw.rect(sombra, (5, 15, 25, 78), (0, 0, 800, 280))
    fundo.blit(sombra, (0, 0))
    return fundo


def _texto(tela, fonte, texto, pos, cor=TEXTO):
    tela.blit(fonte.render(str(texto), True, cor), pos)


def _linhas(tela, fonte, texto, x, y, largura, cor=TEXTO):
    linha = ""
    for palavra in str(texto).split():
        candidata = (linha + " " + palavra).strip()
        if fonte.size(candidata)[0] > largura and linha:
            _texto(tela, fonte, linha, (x, y), cor)
            y += fonte.get_linesize()
            linha = palavra
        else:
            linha = candidata
    if linha:
        _texto(tela, fonte, linha, (x, y), cor)
        y += fonte.get_linesize()
    return y


def _cartao(tela, rect, alfa=220):
    rect = pygame.Rect(rect)
    camada = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(camada, (*PAINEL, alfa), camada.get_rect(), border_radius=6)
    pygame.draw.rect(camada, (73, 106, 121, 150), camada.get_rect(), 1, border_radius=6)
    tela.blit(camada, rect)


@lru_cache(maxsize=12)
def _zona_em_perspectiva(tamanho, faixa):
    base = _arte("zona_inspecao_b_central.png", tamanho)
    if base is None:
        return None
    largura, altura = base.get_size()
    projetada = pygame.Surface((largura, altura), pygame.SRCALPHA)
    for y in range(altura):
        margem = round(10 * (1-y/max(1, altura-1)))
        linha = pygame.transform.scale(base.subsurface((0, y, largura, 1)), (largura-margem, 1))
        projetada.blit(linha, (margem//2, y))
    return projetada


def desenhar_fundo(tela):
    fundo = _fundo_pronto(str(ARTES))
    if fundo is not None:
        tela.blit(fundo, (0, 0))
    else:
        # Provisório: usado apenas quando o PNG não estiver instalado.
        tela.fill(FUNDO)
        pygame.draw.rect(tela, (23, 38, 50), (0, 0, 800, 280))
        for x in FAIXAS_X:
            pygame.draw.rect(tela, FUNDO, (x-40, 190, 80, 90))


def desenhar_esteiras(tela, faixa_ativa=None, tempo_ms=0, em_movimento=True):
    arte = _arte("esteira_central.png", (150, Y_FIM_ESTEIRA-Y_INICIO_ESTEIRA))
    fase = (tempo_ms / 110) % 16 if em_movimento else 0
    angulo = tempo_ms / 700 if em_movimento else 0
    for faixa, x in enumerate(FAIXAS_X):
        # Pequeno trecho de ligação entra na saída da parede, atrás do sprite.
        topo_ligacao = Y_INICIO_ESTEIRA-16
        pygame.draw.polygon(tela, (39, 47, 58), [(x-24, topo_ligacao), (x+24, topo_ligacao),
                                               (x+30, Y_INICIO_ESTEIRA+12), (x-30, Y_INICIO_ESTEIRA+12)])
        for sinal in (-1, 1):
            pygame.draw.line(tela, (72, 86, 101), (x+sinal*24, topo_ligacao),
                             (x+sinal*30, Y_INICIO_ESTEIRA+12), 2)
        if arte is not None:
            tela.blit(arte, arte.get_rect(midbottom=(x, Y_FIM_ESTEIRA)))
        else:
            pygame.draw.rect(tela, (43, 48, 60), (x-65, Y_INICIO_ESTEIRA, 130, Y_FIM_ESTEIRA-Y_INICIO_ESTEIRA))
        # Segmentos discretos avançam só no tampo; os sprites não são deformados.
        topo, fim = Y_INICIO_ESTEIRA+12, Y_FIM_ESTEIRA-44
        for y in range(topo, fim, 16):
            pos_y = int(y+fase)
            if pos_y >= fim:
                continue
            largura = round(24 + 32*(pos_y-topo)/(fim-topo))
            pygame.draw.line(tela, (65, 75, 88), (x-largura, pos_y), (x+largura, pos_y))
        for dx in (-37, -12, 12, 37):
            centro = (x+dx, Y_FIM_ESTEIRA-24)
            ponta = (centro[0]+round(cos(angulo)*3), centro[1]+round(sin(angulo)*3))
            pygame.draw.line(tela, (117, 132, 146), centro, ponta)
        if faixa == faixa_ativa:
            camada = pygame.Surface((800, 600), pygame.SRCALPHA)
            for sinal in (-1, 1):
                pygame.draw.line(camada, (*CIANO, 145),
                                 (x+sinal*28, topo), (x+sinal*61, fim), 2)
            tela.blit(camada, (0, 0))


def desenhar_portas(tela, portas=None):
    portas = portas if portas is not None else ("aberta",)*3
    for faixa, x in enumerate(PORTAS_X):
        porta = _arte(f"porta_b_{portas[faixa]}_central.png", (120, 120))
        if porta is not None:
            tela.blit(porta, porta.get_rect(midbottom=(x, Y_BASE_PORTAS)))
        else:
            pygame.draw.rect(tela, CIANO, (x-43, Y_BASE_PORTAS-80, 86, 55), 2)
        # Ciano = livre; âmbar = ocupada, usando o mesmo estado do sprite.
        cor = CIANO if portas[faixa] == "aberta" else AMARELO
        pygame.draw.rect(tela, (9, 19, 27), (x-11, Y_BASE_PORTAS-93, 22, 9), border_radius=2)
        pygame.draw.rect(tela, cor, (x-8, Y_BASE_PORTAS-90, 16, 3))


def zona_da_faixa(zona, faixa):
    return pygame.Rect(FAIXAS_X[faixa]-40, zona.y, 80, zona.height).clip(zona)


def estados_portas_inspecao(produto, rect_produto, zona):
    portas = ["aberta"] * len(FAIXAS_X)
    if produto is not None and rect_produto is not None:
        faixa = produto["faixa"]
        if rect_produto.colliderect(zona_da_faixa(zona, faixa)):
            portas[faixa] = "fechada"
    return tuple(portas)


def desenhar_zonas(tela, zona):
    for faixa in range(len(FAIXAS_X)):
        trecho = zona_da_faixa(zona, faixa)
        if trecho.width and trecho.height:
            marca = _zona_em_perspectiva(trecho.size, faixa)
            if marca is not None:
                tela.blit(marca, marca.get_rect(center=trecho.center))
            else:
                pygame.draw.rect(tela, CIANO, trecho, 2)


def desenhar_cenario(tela, zona, portas=None, faixa_ativa=None, tempo_ms=0, em_movimento=True):
    desenhar_fundo(tela)
    desenhar_esteiras(tela, faixa_ativa, tempo_ms, em_movimento)
    desenhar_portas(tela, portas)
    desenhar_zonas(tela, zona)


def desenhar_inspetor(tela, faixa_inspetor):
    x = FAIXAS_X[faixa_inspetor]
    arte = _arte("inspetor_a.png", (76, ALTURA_INSPETOR))
    if arte is not None:
        tela.blit(arte, arte.get_rect(midbottom=(x, Y_INSPETOR)))
    else:
        pygame.draw.rect(tela, CIANO, (x-12, Y_INSPETOR-38, 24, 36), border_radius=4)
        pygame.draw.circle(tela, AMARELO, (x, Y_INSPETOR-48), 12)


def desenhar_produto(tela, rect_produto, produto=None):
    nome = produto["nome"] if produto is not None else "Caixa"
    arte = _arte(SPRITES_PRODUTOS.get(nome, "produto_caixa.png"), rect_produto.size)
    if arte is not None:
        tela.blit(arte, arte.get_rect(midbottom=rect_produto.midbottom))
    else:
        pygame.draw.rect(tela, (199, 151, 92), rect_produto, border_radius=3)


def desenhar_painel(tela, fontes, produto):
    _cartao(tela, (12, 70, 776, 94), 211)
    for x in (188, 540):
        pygame.draw.line(tela, (49, 77, 94), (x, 82), (x, 152))
    _texto(tela, fontes["rotulo"], "EM INSPEÇÃO", (24, 80), SUAVE)
    _linhas(tela, fontes["normal"], produto["nome"], 24, 104, 150)
    _texto(tela, fontes["rotulo"], "CARACTERÍSTICAS DO PRODUTO", (202, 80), SUAVE)
    y = 98
    for defeito in produto["defeitos"]:
        y = _linhas(tela, fontes["pequena"], DEFEITOS.get(defeito, defeito), 202, y, 320, AMARELO)
    if not produto["defeitos"]:
        _texto(tela, fontes["normal"], "Sem defeitos", (202, y), VERDE)
    _texto(tela, fontes["rotulo"], "RECOMENDAÇÃO DA IA", (554, 80), SUAVE)
    _texto(tela, fontes["numero"], produto["recomendacao_ia"].upper(), (554, 99), CIANO)
    _texto(tela, fontes["pequena"], "Compare com as características.", (554, 137), SUAVE)


def desenhar_hud(tela, fontes, estado):
    _cartao(tela, (0, 0, 800, 62), 237)
    _texto(tela, fontes["titulo"], "FÁBRICA 404", (16, 4))
    _texto(tela, fontes["rotulo"], "CONTROLE DE QUALIDADE", (17, 35), CIANO)
    total = len(estado["produtos"])
    progresso = min(estado["indice"]+1, total)
    dados = [("PONTOS", estado["pontos"]), ("ERROS", f'{estado["erros"]} / {LIMITE_ERROS}'),
             ("PRODUTO", f'{progresso} / {total}'), ("RECORDE", estado["recorde"])]
    for i, (rotulo, valor) in enumerate(dados):
        x = 270+i*130
        pygame.draw.line(tela, (49, 77, 94), (x-14, 12), (x-14, 49))
        _texto(tela, fontes["rotulo"], rotulo, (x, 7), SUAVE)
        _texto(tela, fontes["numero"], valor, (x, 25))


def linhas_feedback(produto, resultado):
    if resultado["decisao"] is None:
        titulo = "Tempo esgotado"
    else:
        titulo = "Acerto" if resultado["jogador_acertou"] else "Erro"
        if resultado["ia_corrigida"]:
            titulo += " · Você corrigiu a IA"
        elif resultado["decisao"] != produto["recomendacao_ia"]:
            titulo += " · Divergência da IA"
    ia = "A IA acertou" if resultado["ia_acertou"] else "A IA errou"
    return [titulo, ia, f'Resposta correta: {resultado["resposta_correta"]}']


def desenhar_feedback(tela, fontes, linhas):
    # Mensagem imediata abaixo da ficha, sem cobrir portas, objeto ou inspetor.
    _cartao(tela, (12, 172, 776, 68), 237)
    cor = VERDE if linhas and linhas[0].startswith("Acerto") else AMARELO
    for i, linha in enumerate(linhas[:3]):
        _texto(tela, fontes["normal"] if i == 0 else fontes["pequena"], linha,
               (24, 177+i*20), cor if i == 0 else TEXTO)


def desenhar_tela_fim(tela, fontes, estado):
    _cartao(tela, (130, 100, 540, 430), 237)
    venceu = estado["desfecho"] == "vitoria"
    _texto(tela, fontes["titulo"], "VITÓRIA · TURNO CONCLUÍDO" if venceu else "DERROTA · LIMITE DE ERROS",
           (154, 122), VERDE if venceu else VERMELHO)
    for y, nome, valor in [(190, "Pontuação final", estado["pontos"]),
                            (245, "Erros cometidos", estado["erros"]),
                            (300, "Recorde", estado["recorde"]),
                            (355, "Recomendações erradas da IA", estado["ia_errou"]),
                            (410, "Vezes que você corrigiu a IA", estado["ia_corrigida"])]:
        _texto(tela, fontes["normal"], nome, (154, y))
        _texto(tela, fontes["numero"], valor, (606, y-3), CIANO)
    _texto(tela, fontes["pequena"], "Supervisão humana faz a diferença.", (154, 486), SUAVE)


def desenhar_rodape(tela, fontes, estado, portas):
    _cartao(tela, (0, 574, 800, 26), 228)
    texto = "Inspeção ocupada · porta fechada" if "fechada" in portas else "Inspeção livre · portas abertas"
    _texto(tela, fontes["pequena"], texto, (12, 577), AMARELO if "fechada" in portas else CIANO)
    controles = estado.get("controles", "Ciano: livre · Âmbar: ocupada")
    _texto(tela, fontes["pequena"], controles, (460, 577), SUAVE)


def _desenhar_quadro(tela, interface, fontes, estado, zona, rect_produto, tempo_ms):
    if estado["fase"] == FASE_FIM:
        desenhar_fundo(tela)
        desenhar_hud(interface, fontes, estado)
        desenhar_tela_fim(interface, fontes, estado)
        return
    produto = None
    if 0 <= estado["indice"] < len(estado["produtos"]):
        produto = estado["produtos"][estado["indice"]]
    portas = estados_portas_inspecao(produto, rect_produto, zona)
    faixa = produto["faixa"] if produto is not None and rect_produto is not None else None
    desenhar_cenario(tela, zona, portas, faixa, tempo_ms, estado["fase"] == FASE_JOGANDO)
    if produto is not None:
        if rect_produto is not None:
            if portas[produto["faixa"]] == "fechada":
                pygame.draw.rect(tela, (49, 129, 140), rect_produto.inflate(6, 6), 1, border_radius=3)
            desenhar_produto(tela, rect_produto, produto)
    desenhar_inspetor(tela, estado["faixa_inspetor"])
    # UI por último: mesma organização em todas as resoluções.
    desenhar_hud(interface, fontes, estado)
    if produto is not None:
        desenhar_painel(interface, fontes, produto)
    desenhar_rodape(interface, fontes, estado, portas)
    if estado["fase"] == FASE_FEEDBACK and estado["resultado"] is not None and produto is not None:
        desenhar_feedback(interface, fontes, linhas_feedback(produto, estado["resultado"]))


def desenhar_jogo(tela, fontes, estado, zona, rect_produto, tempo_ms=None):
    """Estado/Rects usam 800×600. Tempo opcional controla somente animação visual."""
    tempo_ms = pygame.time.get_ticks() if tempo_ms is None else tempo_ms
    if tela.get_size() == (800, 600):
        _desenhar_quadro(tela, tela, fontes, estado, zona, rect_produto, tempo_ms)
        return
    cena = pygame.Surface((800, 600))
    interface = pygame.Surface((800, 600), pygame.SRCALPHA)
    _desenhar_quadro(cena, interface, fontes, estado, zona, rect_produto, tempo_ms)
    # Preservar o primeiro plano ao recortar uma janela larga: não cortar os pés.
    tela.blit(_cobrir(cena, tela.get_size(), ancorar_base=True), (0, 0))
    # A cena pode ser recortada; a interface inteira permanece visível.
    escala = min(tela.get_width()/800, tela.get_height()/600)
    def colocar_area(area, ancora, posicao):
        trecho = interface.subsurface(area)
        trecho = pygame.transform.scale(trecho, (round(trecho.get_width()*escala),
                                                 round(trecho.get_height()*escala)))
        tela.blit(trecho, trecho.get_rect(**{ancora: posicao}))

    if estado["fase"] == FASE_FIM:
        colocar_area((0, 0, 800, 62), "midtop", (tela.get_width()//2, 0))
        colocar_area((130, 100, 540, 430), "center", tela.get_rect().center)
    else:
        colocar_area((0, 0, 800, 240), "midtop", (tela.get_width()//2, 0))
        colocar_area((0, 574, 800, 26), "midbottom", (tela.get_width()//2, tela.get_height()))
