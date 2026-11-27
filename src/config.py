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
TEMPO_CHEGADA = 2.0 
TEMPO_DECISAO = 4.0   

FASE_JOGANDO = "jogando"
FASE_FEEDBACK = "feedback"
FASE_FIM = "fim"
FASE_MENU = "menu"
FASE_CONCLUIDA = "fase_concluida"

MODO_FASES = "fases"
MODO_INFINITO = "infinito"

# Progressão: 10, 15, 15, 20, 20... e dificuldade maior nas fases 3, 5, 7...
TEMPO_DECISAO_MINIMO = 1.6
REDUCAO_TEMPO_POR_DIFICULDADE = 0.35
ACRESCIMO_VELOCIDADE_POR_DIFICULDADE = 0.18
INTERVALO_DIFICULDADE_INFINITO_MIN = 5
INTERVALO_DIFICULDADE_INFINITO_MAX = 8

NOMES_PRODUTOS = ["Caixa", "Pacote", "Garrafa", "Lata", "Frasco"]

DEFEITOS = {
    "embalagem_danificada": "Embalagem amassada",
    "etiqueta_incompleta": "Etiqueta incompleta",
    "codigo_ilegivel": "Código ilegível",
}

# --- Layout e cores ---  (Kauan)
# Coordenadas lógicas do cenário aprovado em 800 × 600.
FAIXAS_X = (242, 400, 558)      # eixos retos alinhados ao fundo que preenche 800 × 600
PORTAS_X = FAIXAS_X
Y_FIM_ESTEIRA = 452
ZONA_Y = 390
ZONA_ALTURA = 30
Y_INICIO_ESTEIRA = 250         # produto surge dentro do vão escuro
LARGURA_PRODUTO = 46
ALTURA_PRODUTO = 42
Y_INSPETOR = 568
ALTURA_INSPETOR = 132
VELOCIDADE_ESTEIRA = 1.7        # pixels por quadro
DURACAO_FEEDBACK = 120          # quadros (2 s a 60 FPS)

# Novas cores (Kauan define; estes são valores de partida)
COR_ESTEIRA = (71, 85, 105)
COR_ZONA = (245, 166, 35)
COR_INSPETOR = (234, 88, 12)
COR_PRODUTO = (217, 174, 114)
COR_ACERTO = (22, 163, 74)
COR_ERRO = (220, 38, 38)

# Transporte: coordenadas lógicas e velocidade equivalente a 1,7 px/frame a 60 FPS.
# Até um produto no tamanho máximo já passou inteiro antes de tocar a zona.
Y_PASSAGEM_PORTA = ZONA_Y - ALTURA_PRODUTO
Y_BASE_PORTAS = Y_PASSAGEM_PORTA + 34  # margem transparente do canvas de 150 px
Y_PARADA_PRODUTO = ZONA_Y + ZONA_ALTURA - ALTURA_PRODUTO
VELOCIDADE_TRANSPORTE = VELOCIDADE_ESTEIRA * FPS
