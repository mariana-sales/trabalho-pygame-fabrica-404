# Fábrica 404 — Controle de Qualidade

Projeto final da disciplina de Introdução a Algoritmos/Programação, desenvolvido com Python e Pygame.

Um jogo arcade em que o jogador é um inspetor humano que revisa as recomendações de uma inteligência artificial de controle de qualidade, que às vezes erra. Tema: Inteligência Artificial no Cotidiano — Aplicações e Uso Responsável (confiabilidade e supervisão humana).

> Status: em desenvolvimento. A proposta completa está em `docs/proposta.MD`.

## Integrantes do grupo

- Kauan Victor Silva Pereira
- Mariana Sales Oliveira
## Estrutura do projeto

- `main.py`: ponto de entrada da aplicação.
- `src/`: código-fonte principal do jogo (loop, regras, sprites e dados).
- `assets/`: imagens, fontes e sons.
- `data/`: arquivos persistentes (recorde/ranking).
- `tests/`: testes unitários com `pytest`.
- `docs/`: documentação do projeto, incluindo proposta inicial.
## Descrição do jogo

Em Fábrica 404, uma fábrica usa inteligência artificial para classificar produtos, mas o sistema comete erros. O jogador controla um inspetor que se move entre as três faixas de uma esteira. Um produto por vez surge em uma faixa aleatória e avança pela esteira, com características que indicam se está adequado ou defeituoso. A IA recomenda aprovar ou rejeitar, e essa recomendação pode estar errada.

O jogador precisa estar na faixa do produto, conferir suas características e decidir quando ele estiver parado na inspeção. Após cada decisão, o jogo mostra um feedback explicando o resultado.

## Objetivo do jogador

Classificar corretamente os 10 produtos da partida, conferindo as características de cada um em vez de seguir cegamente a recomendação da IA. O jogador vence ao concluir os 10 produtos com no máximo 2 erros e perde ao cometer o 3º erro.

## Regras do jogo

- Um produto por vez surge em uma faixa aleatória e avança pela esteira; suas características aparecem em um painel fixo na tela.
- A IA recomenda aprovar ou rejeitar cada produto e erra em um número fixo de produtos por partida, sorteados a cada partida.
- O jogador move o inspetor até a faixa do produto e decide depois da parada na inspeção.
- Se o produto tiver qualquer defeito, a resposta correta é rejeitar; sem defeitos, é aprovar. Cada acerto vale +10 pontos; cada erro aumenta em 1 o contador de erros.
- Nesta revisão o produto aguarda a decisão parado; não foi introduzido um prazo de inspeção. O contrato de tempo esgotado continua testado, mas não é acionado pelo loop.
- Após cada decisão, o jogo explica se o jogador acertou, se a IA acertou e quais eram os defeitos.
## Controles

- Setas esquerda e direita: mudar de faixa
- A: aprovar o produto
- R: rejeitar o produto
- ESC: sair do jogo
- Espaço na tela final: nova partida
## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/mariana-sales/trabalho-pygame-fabrica-404.git
cd trabalho-pygame-fabrica-404
pip install -r requirements.txt
python main.py
```

## Como executar os testes

```bash
python -m pytest
```

## Recursos externos utilizados

As artes fornecidas para esta entrega estão descritas abaixo, com origem e situação da licença.

## Visual integrado — branch `kauan-tela-e-testes`

A fábrica preenche a janela, sem margens, preservando proporções por escala e
recorte. HUD compacto, painel da IA translúcido, destaque ciano na faixa do
produto, segmentos animados apenas no trecho móvel e luzes das portas por ocupação.
Feedback e telas finais usam os dados recebidos e a mesma identidade visual.

```powershell
.venv\Scripts\python.exe main.py
.venv\Scripts\python.exe -m src.previa
.venv\Scripts\python.exe -m src.previa --tamanho 1280x720
.venv\Scripts\python.exe -m pytest -q
```

Na prévia, Espaço alterna exemplos e Esc sai; a janela pode ser redimensionada.
A prévia usa dados fictícios explícitos e não salva recorde. `main.py` executa
a partida real em 800 × 600. O transporte usa delta time; o produto surge no vão
da parede, passa pela porta e para na zona. A porta fecha após a passagem completa.
As funções antes vazias de avaliação, contadores e desfechos foram completadas
conforme os contratos existentes. Contrato: [tests/README.md](tests/README.md).

Validação desta revisão: **88 testes passaram**, sem falhas esperadas. Inclui
transporte a 30/60/144 FPS, portas, plataforma estática, decisões, vitória,
derrota e abertura/saída do loop com SDL sem janela. Quadros do percurso real
conferidos visualmente em 800 × 600; testes de desenho cobrem outras resoluções.

Artes: `assets/imagens/fabrica404/` contém o pacote fornecido pelo usuário
(portas B, zonas B e inspetor A) e o fundo derivado da referência aprovada.
As esteiras frontais e produtos estão em `assets/imagens/fabrica404_v2/`.
A origem e os prompts do fundo estão em `assets/imagens/fabrica404/README-fundo.md`.
Autoria/licença das referências não informadas no material fornecido.
Imagens desta revisão: `output/transporte-revisado/`.
