# Testes e integração — Fábrica 404

## Executar

```powershell
.venv\Scripts\python.exe main.py
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m src.previa
```

Jogo: setas esquerda/direita mudam de faixa; A aprova, R rejeita, Esc sai.
Espaço reinicia na tela final. A prévia permanece independente, usa exemplos
fictícios e não grava recorde; Espaço alterna suas cenas.

## Validação

88 testes aprovados, sem xfail. Os oito contratos anteriormente pendentes agora
têm implementação em src/funcoes.py; os testes mantêm suas expectativas.

- test_logica.py: sorteio de 10 produtos, 5 defeituosos e 4 erros da IA;
  avaliação, pontuação, contadores, avanço, vitória e derrota.
- test_dados.py: leitura e gravação em arquivos temporários.
- test_desenho.py: estado/Rects intactos, visibilidade do produto, modelos,
  portas e luzes, faixa ativa, feedback, animação e resoluções.
- test_transporte.py: velocidade independente de FPS, escala contínua,
  parada, porta aberta durante travessia, área de inspeção estática, bloqueio
  de decisões prematuras ou na faixa errada, partidas completas e abertura/saída
  do loop real sem escrever no arquivo de recorde.

Testes gráficos usam SDL dummy, sem janela. Quadros do percurso do jogo em
800 × 600 foram renderizados e inspecionados em output/transporte-revisado/.
Isso não substitui a avaliação manual da sensação dos controles.

## Estado e desenho

src/jogo.py recebe entrada e atualiza o estado usando as regras compartilhadas.
src/transporte.py calcula posição e Rect em coordenadas lógicas 800 × 600.
A velocidade de 1,7 px/quadro foi convertida para 102 px/s, equivalente a 60 FPS.
O produto nasce em y=250 dentro do vão e para em y=374; sua escala cresce
uniformemente de 65% a 100%. Quadros longos não ultrapassam a parada.

O plano da porta fica em y=366. Ela permanece aberta até o topo do produto
passar por esse plano e fecha enquanto a inspeção está ocupada. A luz usa
ciano para aberta e âmbar para fechada. Após o feedback, o próximo produto
começa no vão da parede. As bases das portas ficam fora da superfície móvel.

O trecho anterior à porta tem segmentos animados. A plataforma de inspeção e
seus roletes ficam estáticos. O feedback congela também o trecho móvel.

A camada de desenho não muda estado, posição ou recorde. O parâmetro opcional
tempo_ms controla só a animação visual. O HUD e a ficha mostram os dados recebidos,
sem títulos de abertura durante a partida. O fundo recebe revestimentos
geométricos para ajustar os três vãos, preservando os PNGs e sua transparência.

O produto aguarda a decisão na inspeção, conforme o pedido atual. Não existe
prazo novo no loop; o contrato avaliar_decisao(produto, None) continua testado
para futura integração de tempo esgotado. As regras de sorteio, pontuação e
limite de erros já implementadas foram preservadas.
