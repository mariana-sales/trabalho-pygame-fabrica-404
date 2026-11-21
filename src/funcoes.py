# CONTRATO DE DADOS (consulte antes de usar uma chave)
# produto:   nome, faixa (0 a 2), defeitos (lista), recomendacao_ia ("aprovar" ou "rejeitar")
# resultado: decisao ("aprovar", "rejeitar" ou None), resposta_correta,
#            jogador_acertou, ia_acertou, ia_corrigida
# estado:    fase, produtos, indice, x_produto, faixa_inspetor, pontos, erros,
#            ia_errou, ia_corrigida, resultado, frames_feedback, desfecho, recorde

def calcular_pontos(pontos_atual, pontos_ganhos):
    """Soma os pontos ganhos à pontuação atual."""
    return pontos_atual + pontos_ganhos


def tomar_dano(vida_atual, dano):
    """Reduz a vida atual com base no dano recebido."""
    return vida_atual - dano


def jogador_perdeu(vidas):
    """Indica se o jogador ficou sem vidas."""
    return vidas <= 0


def limitar_valor(valor, minimo, maximo):
    """Mantém um valor dentro do intervalo [minimo, maximo]."""
    if valor < minimo:
        return minimo
    if valor > maximo:
        return maximo
    return valor


def verificar_colisao(retangulo_1, retangulo_2):
    """Verifica sobreposição entre dois retângulos do Pygame."""
    return retangulo_1.colliderect(retangulo_2)



def sortear_indices(total, quantidade):
    """Devolve 'quantidade' posições diferentes entre 0 e total-1."""
    return list(range(quantidade))


def sortear_defeitos():
    """Devolve uma lista de 1 a 3 códigos de defeito diferentes."""
    return []


def inverter_recomendacao(recomendacao):
    """Troca 'aprovar' por 'rejeitar' e vice-versa."""
    return recomendacao


def gerar_produtos(total, qtd_defeituosos, qtd_erros_ia):
    """Monta a lista de produtos da partida."""
    return []


def resposta_correta(produto):
    """Sem defeitos: 'aprovar'. Com defeito: 'rejeitar'."""
    return "aprovar"


def ia_acertou(produto):
    """True se a recomendação da IA é a resposta correta."""
    return True


def criar_estado(recorde):
    """Estado de uma partida nova (provisório: um produto fixo)."""
    produto = {"nome": "Caixa", "faixa": 1, "defeitos": [], "recomendacao_ia": "aprovar"}
    return {
        "fase": "jogando", "produtos": [produto], "indice": 0, "x_produto": 0,
        "faixa_inspetor": 1, "pontos": 0, "erros": 0, "ia_errou": 0,
        "ia_corrigida": 0, "resultado": None, "frames_feedback": 0,
        "desfecho": None, "recorde": recorde,
    }


def mover_faixa(faixa_atual, direcao, num_faixas):
    """Move a faixa em -1 ou +1, sem sair de 0..num_faixas-1."""
    return faixa_atual


def pode_decidir(faixa_inspetor, faixa_produto, produto_na_zona):
    """True se o inspetor está na faixa do produto e o produto está na zona."""
    return False


def produto_passou_da_zona(x_produto, fim_da_zona):
    """True se o produto já saiu da zona de inspeção."""
    return False


def avaliar_decisao(produto, decisao):
    """Compara a decisão (ou None) com a resposta correta e devolve o resultado."""
    return {"decisao": decisao, "resposta_correta": "aprovar", "jogador_acertou": False,
            "ia_acertou": False, "ia_corrigida": False}


def aplicar_resultado(estado, resultado):
    """Atualiza pontos, erros, ia_errou e ia_corrigida no estado."""
    pass


def avancar_produto(estado):
    """Passa para o próximo produto e volta a fase para 'jogando'."""
    pass


def partida_perdida(erros, limite_erros):
    """True se os erros chegaram ao limite."""
    return False


def partida_vencida(erros, concluidos, total, limite_erros):
    """True se todos os produtos foram concluídos com erros abaixo do limite."""
    return False


def verificar_desfecho(erros, concluidos, total, limite_erros):
    """Devolve None, 'vitoria' ou 'derrota' (a derrota tem prioridade)."""
    return None


def texto_feedback(produto, resultado):
    """Devolve a lista de linhas de texto do feedback."""
    return []