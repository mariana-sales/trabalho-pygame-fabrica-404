# CONTRATO DE DADOS (consulte antes de usar uma chave)
#
# produto: nome, faixa (0 a 2) 0 é a esteira da esquerda e 2 é a esteira
#          da direita, defeitos (lista), recomendacao_ia ("aprovar" ou "rejeitar")
#
# resultado: decisao ("aprovar", "rejeitar" ou None), resposta_correta,
#            jogador_acertou, ia_acertou, ia_corrigida
#
# estado:    fase, produtos, indice, pos_produto, faixa_inspetor, pontos, erros,
#            ia_errou, ia_corrigida, resultado, frames_feedback, desfecho, recorde

import random

from src.config import (
    DEFEITOS, FASE_JOGANDO, NOMES_PRODUTOS, NUM_FAIXAS, PONTOS_POR_ACERTO,
    QTD_DEFEITUOSOS, QTD_ERROS_IA, TOTAL_PRODUTOS, Y_INICIO_ESTEIRA,
)

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
    return random.sample(range(total), quantidade)


def sortear_defeitos():
    """Devolve uma lista de 1 a 3 códigos de defeito diferentes."""
    quantidade = random.randint(1, min(3, len(DEFEITOS)))
    return random.sample(list(DEFEITOS), quantidade)


def inverter_recomendacao(recomendacao):
    """Troca 'aprovar' por 'rejeitar' e vice-versa."""
    if recomendacao == "aprovar":
        return "rejeitar"
    return "aprovar"


def gerar_produtos(total, qtd_defeituosos, qtd_erros_ia):
    """Monta a lista de produtos da partida."""
    posicoes_defeituosas = sortear_indices(total, qtd_defeituosos)
    posicoes_ia_erra = sortear_indices(total, qtd_erros_ia)

    produtos = []
    for i in range(total):
        if i in posicoes_defeituosas:
            defeitos = sortear_defeitos()
        else:
            defeitos = []

        produto = {
            "nome": random.choice(NOMES_PRODUTOS),
            "faixa": random.randint(0, NUM_FAIXAS - 1),
            "defeitos": defeitos,
            "recomendacao_ia": None,
        }

        correta = resposta_correta(produto)
        if i in posicoes_ia_erra:
            produto["recomendacao_ia"] = inverter_recomendacao(correta)
        else:
            produto["recomendacao_ia"] = correta

        produtos.append(produto)
    return produtos


def resposta_correta(produto):
    """Sem defeitos: 'aprovar'. Com defeito: 'rejeitar'."""
    if produto["defeitos"]:
        return "rejeitar"
    return "aprovar"


def ia_acertou(produto):
    """True se a recomendação da IA é a resposta correta."""
    return produto["recomendacao_ia"] == resposta_correta(produto)


def criar_estado(recorde):
    """Estado de uma partida nova."""
    return {
        "fase": FASE_JOGANDO,
        "produtos": gerar_produtos(TOTAL_PRODUTOS, QTD_DEFEITUOSOS, QTD_ERROS_IA),
        "indice": 0,
        "pos_produto": Y_INICIO_ESTEIRA,
        "faixa_inspetor": NUM_FAIXAS // 2,
        "pontos": 0,
        "erros": 0,
        "ia_errou": 0,
        "ia_corrigida": 0,
        "resultado": None,
        "frames_feedback": 0,
        "desfecho": None,
        "recorde": recorde,
    }


def mover_faixa(faixa_atual, direcao, num_faixas):
    """Move a faixa em -1 (esquerda) ou +1 (direita), sem sair de 0..num_faixas-1."""
    nova_faixa = faixa_atual + direcao
    return limitar_valor(nova_faixa, 0, num_faixas - 1)


def pode_decidir(faixa_inspetor, faixa_produto, produto_na_zona):
    """True se o inspetor está na esteira do produto e o produto está na zona de inspeção."""
    return faixa_inspetor == faixa_produto and produto_na_zona


def produto_passou_da_zona(pos_produto, fim_da_zona):
    """True se o produto já passou do fim da zona de inspeção."""
    return pos_produto > fim_da_zona


def mover_produto(pos_produto, velocidade, pos_limite):
    """Avança o produto pela esteira sem ultrapassar pos_limite."""
    return min(pos_produto + velocidade, pos_limite)


def avaliar_decisao(produto, decisao):
    """Compara a decisão (ou None) com a resposta correta e devolve o resultado."""
    correta = resposta_correta(produto)
    jogador_acertou = decisao == correta
    ia_certa = ia_acertou(produto)

    return {
        "decisao": decisao,
        "resposta_correta": correta,
        "jogador_acertou": jogador_acertou,
        "ia_acertou": ia_certa,
        "ia_corrigida": (not ia_certa) and jogador_acertou,
    }


def aplicar_resultado(estado, resultado):
    """Atualiza pontos, erros, ia_errou e ia_corrigida no estado."""
    if resultado["jogador_acertou"]:
        estado["pontos"] = calcular_pontos(estado["pontos"], PONTOS_POR_ACERTO)
    else:
        estado["erros"] += 1

    if not resultado["ia_acertou"]:
        estado["ia_errou"] += 1

    if resultado["ia_corrigida"]:
        estado["ia_corrigida"] += 1


def avancar_produto(estado):
    """Passa para o próximo produto e volta a fase para 'jogando'."""
    estado["indice"] += 1
    estado["pos_produto"] = Y_INICIO_ESTEIRA
    estado["fase"] = FASE_JOGANDO
    estado["resultado"] = None
    estado["frames_feedback"] = 0


def partida_perdida(erros, limite_erros):
    """True se os erros chegaram ao limite."""
    return erros >= limite_erros


def partida_vencida(erros, concluidos, total, limite_erros):
    """True se todos os produtos foram concluídos com erros abaixo do limite."""
    return concluidos >= total and erros < limite_erros


def verificar_desfecho(erros, concluidos, total, limite_erros):
    """Devolve None, 'vitoria' ou 'derrota' (a derrota tem prioridade)."""
    if partida_perdida(erros, limite_erros):
        return "derrota"
    if partida_vencida(erros, concluidos, total, limite_erros):
        return "vitoria"
    return None


def texto_feedback(produto, resultado):
    """Devolve a lista de linhas de texto do feedback."""
    linhas = []

    if resultado["decisao"] is None:
        linhas.append("Tempo esgotado: o produto passou sem decisão.")
    elif resultado["jogador_acertou"]:
        linhas.append("Você acertou!")
    else:
        linhas.append("Você errou.")

    if resultado["ia_acertou"]:
        linhas.append("A IA acertou.")
    else:
        linhas.append("A IA errou.")

    if produto["defeitos"]:
        nomes = [DEFEITOS[codigo] for codigo in produto["defeitos"]]
        linhas.append("Defeitos: " + ", ".join(nomes))
    else:
        linhas.append("Sem defeitos.")

    return linhas
