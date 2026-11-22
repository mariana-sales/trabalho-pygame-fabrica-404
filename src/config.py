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
FAIXAS_X = (230, 310, 390)      # centro horizontal de cada faixa
ZONA_Y = 480
ZONA_ALTURA = 250
Y_INICIO_ESTEIRA = 0
LARGURA_PRODUTO = 60
ALTURA_PRODUTO = 50
Y_INSPETOR = 740
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