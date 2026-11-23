# Fábrica 404 — sprites selecionados em alta qualidade

Arquivos PNG individuais dos modelos selecionados: porta B, esteira A, zona B e inspetor A. Os sprites foram separados do material visual escolhido e mantêm a paleta futurista grafite/aço/ciano com amarelo de segurança.

## Arquivos e dimensões nativas

| Arquivo | Dimensões PNG | Fundo/canal |
|---|---:|---|
| `esteira_a_central.png` | 442 × 377 px | transparência alfa |
| `esteira_a_direita.png` | 593 × 377 px | transparência alfa |
| `esteira_a_esquerda.png` | 593 × 377 px | transparência alfa |
| `inspetor_a.png` | 670 × 1295 px | transparência alfa |
| `porta_b_aberta_central.png` | 512 × 512 px | transparência alfa |
| `porta_b_aberta_direita.png` | 512 × 512 px | transparência alfa |
| `porta_b_aberta_esquerda.png` | 512 × 512 px | transparência alfa |
| `porta_b_fechada_central.png` | 512 × 512 px | transparência alfa |
| `porta_b_fechada_direita.png` | 512 × 512 px | transparência alfa |
| `porta_b_fechada_esquerda.png` | 512 × 512 px | transparência alfa |
| `zona_inspecao_b_central.png` | 724 × 303 px | transparência alfa |
| `zona_inspecao_b_direita.png` | 699 × 342 px | transparência alfa |
| `zona_inspecao_b_esquerda.png` | 700 × 342 px | transparência alfa |

## Escala no Pygame

As dimensões PNG são a resolução nativa entregue, não um tamanho obrigatório de `blit`. Foram mantidos os canvases originais das seis portas para que cada par aberto/fechado use exatamente o mesmo tamanho e ponto de encaixe. Para uma cena de 800 × 600, carregue cada sprite em `pygame.image.load(...).convert_alpha()` e ajuste para o retângulo da respectiva faixa. Use `pygame.transform.scale` para manter pixels nítidos ao reduzir/expandir pixel art; os PNGs originais permanecem intactos.

## Encaixe e alinhamento

- As portas estão organizadas por perspectiva: esquerda, central e direita. Em cada perspectiva, os arquivos aberta/fechada têm o mesmo canvas de 512 × 512 px; suportes e referência de base permanecem na mesma posição ao alternar o estado.
- Esteiras e zonas foram recortadas individualmente das três perspectivas, preservando o alfa e a proporção de cada recorte.
- As zonas têm centro transparente para manter visível o objeto inspecionado.
- O inspetor é um PNG isolado, de costas, com cabelo vermelho, capacete amarelo, uniforme e prancheta.

## Ordem recomendada de camadas

1. Fundo da fábrica.
2. Esteiras (esquerda, central, direita).
3. Zona de inspeção sobre cada esteira.
4. Produtos e portas de controle, posicionados de acordo com a lógica do jogo (a porta deve permanecer atrás do produto parado).
5. Inspetor.
6. Interface e mensagens do Pygame.

## Prévia

`preview/cena_referencia_800x600.png` mostra a composição escolhida do cenário em 800 × 600 px. A prévia serve como referência visual da câmera e da posição dos elementos; os assets em `assets/` continuam separados para integração por camadas.
