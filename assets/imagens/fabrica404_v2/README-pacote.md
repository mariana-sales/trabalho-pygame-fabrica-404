# Fábrica 404 — sprites refeitos, versão 2

Pacote de 17 sprites PNG RGBA separados, gerados com a ferramenta de imagem
integrada a partir da referência visual fornecida. Perspectiva frontal levemente
elevada; esteiras convergentes; grafite/aço/ciano; inspetor de costas.

## Dimensões dos arquivos prontos para o jogo

| Arquivo em `sprites/` | Dimensões em pixels |
|---|---|
| `esteira_central.png` | 167 × 189 |
| `esteira_direita.png` | 164 × 189 |
| `esteira_esquerda.png` | 155 × 189 |
| `inspetor.png` | 46 × 96 |
| `porta_aberta_central.png` | 104 × 112 |
| `porta_aberta_direita.png` | 104 × 112 |
| `porta_aberta_esquerda.png` | 104 × 112 |
| `porta_fechada_central.png` | 104 × 112 |
| `porta_fechada_direita.png` | 104 × 112 |
| `porta_fechada_esquerda.png` | 104 × 112 |
| `produto_caixa.png` | 46 × 36 |
| `produto_garrafa.png` | 22 × 48 |
| `produto_lata.png` | 29 × 40 |
| `produto_peca_mecanica.png` | 40 × 36 |
| `zona_inspecao_central.png` | 98 × 16 |
| `zona_inspecao_direita.png` | 98 × 20 |
| `zona_inspecao_esquerda.png` | 98 × 19 |

## Prévia e encaixe

- `preview/cena_800x600.png`: composição de 800 × 600 feita com os PNGs de
  `sprites/`, fundo azul-marinho, sem interface; área superior livre.
- `preview/todos_os_sprites.png`: prancha técnica de 1000 × 800 para inspeção.
- `layout.json`: posições exatas e ordem das camadas da prévia.
- Cada par de portas usa canvas de 104 × 112 e o mesmo ponto de encaixe:
  centro inferior. A moldura aberta é compartilhada nos dois estados; apenas
  as folhas do vão mudam. Não recorte os estados separadamente.
- As zonas são camadas independentes com centro transparente. Posicione sobre
  a superfície da esteira, antes dos produtos; nunca sobre os roletes.
- O inspetor mede menos de 100 pixels de altura na prévia.

## Nitidez, transparência e origem

Os arquivos de `sprites/` já estão na escala da prévia. Use `convert_alpha()`
no Pygame. Para ampliar, use `pygame.transform.scale` em múltiplos inteiros;
não use `smoothscale`. Não use cor-chave: os PNGs possuem alfa real.
As margens foram recortadas e os sprites redimensionados por vizinho mais
próximo. O alfa final foi normalizado para 0/255, eliminando resíduos semitransparentes no centro das zonas e mantendo contornos nítidos.

`prompts.json` registra os prompts usados com a ferramenta de imagem integrada.
`montar_previa.py` reproduz a composição usando exatamente os PNGs separados.
Os sprites não contêm texto, pontuação ou painéis. A caixa usa somente fita,
a lata é lisa, a garrafa não tem rótulo e a peça mecânica não tem inscrições.

Para refazer a prévia: `python montar_previa.py` (requer pygame).

## Conferência

- 17 PNGs RGBA com alfa 0/255; sem fundo embutido.
- Centro das três marcações totalmente transparente.
- Pares de portas: 104 × 112, mesmos suportes e ponto de encaixe.
- Prévia conferida visualmente em tamanho real: três esteiras convergentes,
  marcações ciano, caixa central, personagem pequeno de costas e área superior
  livre para a interface. A imagem é uma recriação, não um recorte do print.