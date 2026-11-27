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

Em Fábrica 404, uma fábrica usa inteligência artificial para classificar produtos, mas o sistema comete erros. O jogador controla um inspetor que se move entre as três faixas de uma esteira. Produtos chegam em sequência e podem estar ativos ao mesmo tempo em faixas diferentes. Cada um avança pela esteira com características que indicam se está adequado ou defeituoso. A IA recomenda aprovar ou rejeitar, e essa recomendação pode estar errada.

O jogador precisa acompanhar as três faixas, mover o inspetor até a faixa de cada produto e decidir quando ele tocar a zona de inspeção. Cada produto tem seu próprio prazo: deixar um produto passar sem inspeção conta como erro. O resultado aparece em uma mensagem curta sem pausar as outras esteiras.

## Modos de jogo

- **Fases:** começa com 10 produtos. A quantidade passa para 15 nas fases 2 e 3, 20 nas fases 4 e 5, e aumenta em mais 5 a cada duas fases. A dificuldade aumenta nas fases 3, 5, 7 e assim por diante, reduzindo o tempo de decisão e acelerando a esteira.
- **Infinito:** não tem quantidade final. A velocidade e a pressão do tempo aumentam em intervalos variáveis, sem indicar ao jogador exatamente quando ocorrerá o próximo aumento.

## Loja de inspetores

No menu, use `3`, `L` ou clique em **Loja de inspetores**. Navegue com as
setas e pressione `Enter` para comprar e equipar, ou equipar um item já comprado.
`Esc` ou `M` volta ao menu. A loja mostra preço, saldo e os estados bloqueado,
comprado e equipado. O Original é gratuito; Petróleo custa 100, Violeta 200
e Aço 300 pontos. As variações só trocam a paleta do uniforme, preservando
cabelo vermelho, capacete, faixas de segurança e silhueta; não dão vantagens.

Cada acerto credita 10 pontos ao **saldo de compras**, salvo imediatamente e
acumulado entre partidas. Comprar não reduz a pontuação da partida nem o recorde.
O arquivo `data/inspetores.json` guarda saldo, compras e aparência equipada;
reiniciar a partida ou o aplicativo mantém a seleção. Arquivo ausente ou inválido
inicia com saldo zero e o Original disponível. Se a gravação falhar, o jogo avisa:
ganhos ficam em memória e compras não são confirmadas até poder salvar.

## Objetivo do jogador

Conferir as características de cada produto em vez de seguir cegamente a recomendação da IA. No modo Fases, concluir cada fase libera a próxima; nos dois modos, a partida termina ao cometer o 3º erro.

## Regras do jogo

- Produtos chegam em intervalos regulares e podem ocupar as três faixas simultaneamente; cada faixa tem no máximo um produto ativo para manter os objetos legíveis.
- O inspetor inspeciona o produto da faixa em que está. O painel mostra as características, a recomendação da IA e o prazo do produto na zona; barras sobre os produtos indicam o tempo restante.
- A IA recomenda aprovar ou rejeitar cada produto e pode errar. Na primeira fase, são 10 produtos, 5 defeituosos e 4 recomendações incorretas.
- O jogador move o inspetor até a faixa do produto e pode decidir assim que ele colide com a zona de inspeção. Nesse ponto ele já atravessou completamente a porta. Os prazos continuam correndo nas outras faixas enquanto o jogador decide.
- Se o produto tiver qualquer defeito, a resposta correta é rejeitar; sem defeitos, é aprovar. Cada acerto vale +10 pontos; cada erro aumenta em 1 o contador de erros.
- Quando uma inspeção termina, o produto sai do jogo e uma mensagem breve informa o resultado; o transporte e os prazos dos outros produtos não são interrompidos.
- Na derrota, o jogo explica a falha que atingiu o limite de erros (detalhes abaixo).

## Motivo da derrota

A tela final conserva pontos, recorde, erros e estatísticas da IA e identifica
o produto e a faixa da **falha que causou o terceiro erro**. Uma decisão errada
mostra a escolha feita, a resposta correta e os defeitos (ou a ausência deles).
Uma expiração informa se faltou chegar à faixa ou decidir depois da chegada.
O prazo de decisão continua correndo mesmo se o inspetor sair dessa faixa.

O registro é copiado no momento da falha e o jogo encerra imediatamente: outros
produtos ou eventos no mesmo quadro não substituem a causa pela seleção da tela.
Se vários prazos expirarem juntos, eles são processados na ordem dos produtos
ativos, até a falha que atinge o limite. O texto usa quebra de linha em um painel
separado das estatísticas. `Enter` reinicia e `M` volta ao menu.

## Controles

- Na tela inicial, `1` ou clique: modo Fases; `2` ou clique: modo Infinito; `3`/`L` ou clique: loja.
- Setas esquerda e direita: mudar de faixa
- A: aprovar o produto
- R: rejeitar o produto
- ESC: sair do jogo
- Enter na tela final: jogar novamente no mesmo modo.
- Enter entre fases: iniciar a próxima fase.
- M: voltar ao menu.

O feedback de cada inspeção é breve e não bloqueia as setas, as decisões ou o movimento dos produtos. Os controles ficam bloqueados apenas nas telas de menu e resultado final.
O recorde é salvo ao terminar a partida, apenas se superar o valor anterior.
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

## Integração das regras, telas e recorde

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
O loop usa a arquitetura da Mariana: eventos, decisão, finalização e atualização.
Os produtos avançam em paralelo com prazos independentes; o painel mostra o
item na faixa do inspetor e barras indicam os prazos ativos. O feedback não
interrompe a partida. `transporte.py` adapta `mover_produto()` ao delta time e
calcula o retângulo de cada sprite com escala gradual.
O texto de feedback vem das regras e o desenho acrescenta o destaque de correção
ou divergência da IA. Contrato: [tests/README.md](tests/README.md).

Validação histórica da integração anterior: **108 testes passaram**, sem falhas esperadas. Inclui
transporte a 30/60/144 FPS, portas, plataforma estática, decisões, vitória,
derrota, reinício com Enter, persistência do recorde e ciclo completo pelo loop
com eventos de teclado e SDL sem janela. Quadros do percurso real
conferidos visualmente em 800 × 600; testes de desenho cobrem outras resoluções.
As mudanças da loja e da explicação de derrota receberam apenas verificação sintática e `git diff --check`;
testes automatizados e validação jogando ficam para execução manual pelo autor.

Artes: `assets/imagens/fabrica404/` contém o pacote fornecido pelo usuário
(portas B, zonas B e inspetor A) e o fundo derivado da referência aprovada.
As esteiras frontais e produtos estão em `assets/imagens/fabrica404_v2/`.
A origem e os prompts do fundo estão em `assets/imagens/fabrica404/README-fundo.md`.
Autoria/licença das referências não informadas no material fornecido.
Imagens da integração: `output/integracao-final/`. As outras pastas de prévias
preservam revisões anteriores.
