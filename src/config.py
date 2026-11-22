# Configurações centrais do jogo (tela, cores e caminhos de arquivos).
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60

TITULO_JOGO = "Fábrica 404 — Controle de Qualidade"

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (212,212,212)

CAMINHO_RECORDE = "data/recorde.txt"
CAMINHO_SPRITES = "assets/imagens/spritesheet.bmp"


# --- Regras ---  (Mariana)
NUM_FAIXAS = 3
TOTAL_PRODUTOS = 10
QTD_DEFEITUOSOS = 5
QTD_ERROS_IA = 4
LIMITE_ERROS = 3
PONTOS_POR_ACERTO = 10

FASE_JOGANDO = "jogando"
FASE_FEEDBACK = "feedback"
FASE_FIM = "fim"

NOMES_PRODUTOS = ["Caixa", "Pacote", "Garrafa", "Lata", "Frasco"]

DEFEITOS = {
    "embalagem_danificada": "Embalagem amassada",
    "etiqueta_incompleta": "Etiqueta incompleta",
    "codigo_ilegivel": "Código ilegível",
}

# --- Layout e cores ---  (Kauan)
# Valores provisórios: o Kauan ajusta pela arte.
FAIXAS_X = (242, 400, 558)      # eixos retos alinhados ao fundo que preenche 800 × 600
PORTAS_X = FAIXAS_X
Y_BASE_PORTAS = 414            # pés em y≈387, imediatamente antes da zona (390)
Y_FIM_ESTEIRA = 452
ZONA_Y = 390
ZONA_ALTURA = 30
Y_INICIO_ESTEIRA = 282
LARGURA_PRODUTO = 46
ALTURA_PRODUTO = 42
Y_INSPETOR = 568
ALTURA_INSPETOR = 132
VELOCIDADE_ESTEIRA = 1.7        # pixels por quadro
DURACAO_FEEDBACK = 120          # quadros (2 s a 60 FPS)

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (212, 212, 212)
# Novas cores (Kauan define; estes são valores de partida)
COR_ESTEIRA = (71, 85, 105)
COR_ZONA = (245, 166, 35)
COR_INSPETOR = (234, 88, 12)
COR_PRODUTO = (217, 174, 114)
COR_ACERTO = (22, 163, 74)
COR_ERRO = (220, 38, 38)
