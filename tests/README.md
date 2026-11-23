# Testes e integração — Fábrica 404

## Executar

```powershell
.venv\Scripts\python.exe main.py
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m src.previa
```

Jogo: setas esquerda/direita mudam de faixa; A aprova, R rejeita, Esc sai.
Enter reinicia na tela final. Setas e decisões ficam bloqueadas no feedback e
no fim. Na prévia independente, Espaço alterna exemplos; ela não grava recorde.

## Resultado da integração

108 testes aprovados, sem xfail. A integração usa as regras e a arquitetura da
Mariana, incluindo A9, e preserva as telas, o layout e a persistência robusta do
Kauan. O trabalho foi validado numa cópia isolada antes do commit de merge.

- test_logica.py: movimento, sorteio 10/5/4, decisões, timeout no contrato,
  pontuação, contadores, limpeza ao avançar, desfechos e texto de feedback.
- test_dados.py: arquivo ausente/inválido e leitura/gravação em pasta temporária.
- test_desenho.py: imutabilidade de estado/Rects, sprites visíveis, portas/luzes,
  destaque da faixa, feedback, animação e diferentes resoluções.
- test_transporte.py: velocidade a 30/60/144 FPS, escala gradual, parada,
  portas, decisões, vitória/derrota e saída do loop.
- test_integracao.py: decisão na primeira colisão com porta já fechada,
  marcações laterais inteiras, feedback regressivo de dois segundos,
  bloqueio de controles, Enter preservando o dicionário e o recorde,
  derrota no décimo produto, persistência após nova sessão e pontuação menor,
  textos dentro do painel e ciclo completo pelo loop com teclas simuladas.

O teste do loop executa vitória, Enter, uma nova partida com derrota e saída,
usando o desenho real, tempo acelerado e recorde temporário. SDL dummy permite
executar sem janela. Quadros de chegada, inspeção, feedback, vitória, reinício
e derrota foram conferidos em 800 × 600, em output/integracao-final/.
A avaliação humana da sensação dos controles continua sendo parte do polimento.

## Contratos consolidados

- criar_estado usa FASE_JOGANDO, NUM_FAIXAS // 2 e o gerador da Mariana.
- aplicar_resultado usa calcular_pontos e os contadores acordados.
- avancar_produto limpa resultado e frames_feedback e volta a FASE_JOGANDO.
- texto_feedback é a fonte das três mensagens. O desenho acrescenta à primeira
  o destaque de correção/divergência da IA, sem recalcular o resultado.
- processar_eventos, tentar_decidir, finalizar_produto e atualizar permanecem
  como a arquitetura do loop. atualizar aceita delta_s opcional (1/FPS por padrão).
- frames_feedback começa em 120 e diminui conforme delta_s * FPS, até zero.
- O desfecho é verificado antes de avançar: o índice final permanece válido.
- Enter em fim reinicia com clear/update, preservando a identidade do estado.
- O recorde é salvo apenas ao fim se a pontuação superar o valor carregado.
  O caminho parte da raiz do projeto; a pasta é criada se necessário.
- pygame.quit é garantido por try/finally.

## Transporte, portas e zona

A decisão continua baseada em colisão, conforme o plano de integração.
Para não aceitar decisão enquanto o produto atravessa a porta, o plano da porta
foi posicionado em y=348, antes do primeiro contato possível de um produto de
altura máxima com a zona. A zona visual/lógica vai de y=390 a y=420, cobre toda
a largura da tela e preserva as três marcações de 80 px.

O produto surge em y=250 e para em y=378 (borda inferior em 420). Sua escala
cresce de 65% a 100%. transporte.avancar_transporte delega a mover_produto,
convertendo delta time em deslocamento a 102 px/s. jogo.rect_do_produto delega
a transporte.rect_produto, compartilhando o Rect entre desenho e colisão.
Não há duas atualizações de movimento por quadro.

A porta fica aberta durante a travessia e fecha enquanto a zona está ocupada.
A área dianteira e seus roletes permanecem imóveis; apenas o trecho anterior
à porta anima. O feedback congela também esse trecho.

## Pendências preservadas

Não foi criado um prazo automático de inspeção. O contrato de decisão `None` e seu feedback estão testados, mas não são disparados automaticamente pelo loop.
