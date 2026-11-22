# Testes e integração visual — Fábrica 404

## Executar

```powershell
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m src.previa
.venv\Scripts\python.exe -m src.previa --tamanho 1280x720
.venv\Scripts\python.exe -m src.previa --salvar output/previa-integrada
```

A prévia usa exemplos explícitos, não grava recorde e aceita redimensionamento.
Espaço alterna exemplos; Esc fecha. A exportação usa tempo visual zero e SDL
sem janela para produzir imagens reproduzíveis.

## Contratos e pendências

`src/jogo.py` ainda é o template com gemas e vidas. A main integrada em `d102ae6`
implementa movimento, inspeção, sorteios, produtos e recomendações; avaliação,
resultados, avanço e desfechos ainda são esboços. Os oito testes `pendente`
usam `xfail(strict=True)`: retire a marca quando a regra for implementada.
Para expor as pendências: `python -m pytest tests/test_logica.py --runxfail -q`.
Nenhuma dessas regras foi alterada para implementar o visual.

- `test_logica.py`: regras acordadas, incluindo 10 produtos, 5 defeituosos e
  4 recomendações erradas, movimento, decisões, contadores e fim da partida.
- `test_dados.py`: leitura e gravação apenas em arquivos temporários.
- `test_desenho.py`: estado e Rects intactos, produtos visíveis, ocupação das
  portas, animação determinística, faixa ativa, luzes, feedback e resoluções.

Fronteiras: produto passa da zona quando `pos_produto > fim_da_zona`.
Rects apenas encostando não colidem. Avanço deve voltar a `Y_INICIO_ESTEIRA`.
`ia_errou` conta recomendações já avaliadas.

## Interface de desenho

Após criar o display, chame `criar_fontes()` uma vez. O contrato continua:

```python
desenhar_jogo(tela, fontes, estado, zona, rect_produto)
```

Estado e Rects usam coordenadas lógicas 800 × 600, inclusive com janela maior.
Use as constantes de `src/config.py`; uma zona pode ser
`pygame.Rect(0, ZONA_Y, 800, ZONA_ALTURA)`. O parâmetro opcional `tempo_ms`
controla somente o movimento visual; sem ele, usa o relógio do Pygame.
A fase de feedback congela a animação. O desenho nunca movimenta o produto,
calcula pontos, salva recorde ou muda a fase.

A faixa ativa é a do produto atual, independentemente da posição da personagem.
Sem produto visível, nenhuma faixa é destacada. As portas usam a ocupação do
Rect na zona da respectiva faixa, inclusive durante feedback: ciano/aberta
quando livre; âmbar/fechada quando ocupada. A antiga chave `estado['portas']`
não é mais usada por `desenhar_jogo`; não há bloqueio físico novo.

O loop deve atualizar recorde e resultados antes de desenhar. Pode fornecer
`estado['controles']` com as teclas que de fato implementa.

## Composição atual

Fundo em `assets/imagens/fabrica404/fundo_fabrica.png`; portas B, zonas B e
inspetor A preservados. Esteiras frontais e produtos usam PNGs de `fabrica404_v2`.
Pacote usa a caixa; Frasco usa a garrafa; o catálogo de sorteio não foi alterado.

A cena preenche a janela por escala uniforme e recorte, sem deformação. O recorte
preserva a base para manter a personagem visível em janelas largas. A interface
é composta separadamente: permanece inteira, com HUD no topo e rodapé na base.
O fundo distante recebe uma sombra; os sprites mantêm contraste e canal alfa.
Não há suavização ao escalar pixel art.

A inspeção usa painel translúcido fixo; resultado tem no máximo três linhas;
vitória/derrota usam a mesma fábrica e paleta. Imagens de referência da revisão:
`output/previa-integrada/`. O fallback geométrico só aparece se faltar um PNG.
