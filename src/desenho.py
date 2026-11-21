def criar_fontes():
    """Cria as fontes uma vez (depois do pygame.init). Devolve um dicionário."""
    return {}

def desenhar_jogo(tela, fontes, estado, zona, rect_produto):
    """Escolhe o que desenhar conforme estado['fase']."""
    pass

def desenhar_cenario(tela, zona):
    """Fundo, esteira, três faixas e zona de inspeção."""
    pass

def desenhar_inspetor(tela, faixa_inspetor):
    pass

def desenhar_produto(tela, rect_produto):
    pass

def desenhar_painel(tela, fontes, produto):
    """Nome, defeitos e 'IA recomenda: ...'."""
    pass

def desenhar_hud(tela, fontes, estado):
    """Pontos, erros x/3, produto n/10 e recorde."""
    pass

def desenhar_feedback(tela, fontes, linhas):
    pass

def desenhar_tela_fim(tela, fontes, estado):
    pass