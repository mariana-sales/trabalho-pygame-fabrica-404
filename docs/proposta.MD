# Proposta Inicial do Jogo

## 1. Nome do Jogo

**Nome:**

Fábrica 404 — Controle de Qualidade

## 2. Integrantes do grupo

- Nome 1: Kauan Victor Silva Pereira
- Nome 2: Mariana Sales Oliveira

## 3. Tema escolhido

**Tema:**

Confiabilidade de sistemas inteligentes e supervisão humana em processos automatizados.

**Como esse tema se relaciona com o jogo?**

A IA da fábrica recomenda aprovar ou rejeitar cada produto, mas erra em um número fixo de produtos por partida; quem a segue sem conferir acumula erros e perde. O jogador atua como inspetor humano: analisa as características de cada produto e revisa a recomendação. Após cada decisão, o jogo explica o resultado e o motivo, trabalhando confiabilidade, transparência e supervisão humana.

## 4. Tipo de jogo

**Tipo escolhido:**

Arcade de classificação com tomada de decisão: o jogador movimenta um personagem entre faixas de uma esteira e decide sobre cada produto em tempo limitado.

## 5. Descrição geral do jogo

**Descrição:**

A tela mostra uma fábrica em perspectiva, com três esteiras paralelas posicionadas lado a lado, uma área de inspeção, um painel com as características do produto atual e as informações da partida (pontos, erros e progresso). O jogador controla um inspetor que se move horizontalmente entre as três faixas.

Um produto por vez surge em uma faixa aleatória e avança pela esteira. Cada produto tem características que indicam se está adequado ou defeituoso (por exemplo, embalagem amassada, etiqueta incompleta ou código ilegível). A IA simulada recomenda aprovar ou rejeitar, e essa recomendação pode estar errada. O jogador precisa estar na mesma faixa do produto quando ele chegar à área de inspeção, onde ele para e aguarda a decisão do jogador.

Exemplo: o produto 4 chega na faixa 2 com embalagem amassada, etiqueta incompleta e código ilegível, mas a IA recomenda aprovar. A decisão correta é rejeitar.

## 6. Objetivo do jogador

**Objetivo:**

Classificar corretamente os 10 produtos da partida, conferindo as características de cada um em vez de seguir cegamente a recomendação da IA, e terminar com o menor número possível de erros.

## 7. Regras principais

- Regra 1: Um produto por vez surge em uma faixa aleatória e avança pela esteira; suas características aparecem em um painel fixo na tela.
- Regra 2: A IA recomenda aprovar ou rejeitar cada produto e erra em um número fixo de produtos por partida (por exemplo, 4 de 10), sorteados a cada partida.
- Regra 3: O jogador move o inspetor até a faixa do produto e decide (aprovar ou rejeitar) antes que ele saia da área de inspeção.
- Regra 4: Se o produto tiver qualquer defeito, a resposta correta é rejeitar; sem defeitos, é aprovar. Cada acerto vale +10 pontos; cada erro soma 1 erro, e produto que sai sem decisão também conta como erro.
- Regra 5: Após cada decisão, o jogo mostra um feedback explicando se o jogador acertou, se a IA acertou e quais eram os defeitos.

## 8. Condição de vitória

**Condição de vitória:**

Concluir os 10 produtos da partida com no máximo 2 erros.

## 9. Condição de derrota ou encerramento

**Condição de derrota ou encerramento:**

O jogador perde ao cometer o 3º erro. A partida também se encerra quando os 10 produtos são concluídos; nesse caso, com no máximo 2 erros, há vitória. Ao final, uma tela resume o desempenho, incluindo quantas vezes a IA errou e quantas o jogador corrigiu.

## 10. Elementos previstos no jogo

- **Personagem ou elemento principal:** inspetor de qualidade controlado pelo jogador, que se move entre as três faixas da esteira.
- **Obstáculos ou desafios:** produtos que avançam continuamente pela esteira, o tempo limitado para decidir e as recomendações incorretas da IA.
- **Itens ou objetos de interação (se houver):** produtos com características diferentes (embalagens danificadas, etiquetas incompletas, produtos sem defeitos), a recomendação da IA e o feedback exibido após cada decisão.
- **Pontuação, vidas, tempo ou progresso:** pontuação por acertos, contador de erros (limite de 3) e indicador de progresso (produto X de 10), além do recorde salvo em arquivo.

## 11. Controles previstos

**Controles:**

- Seta para esquerda / seta para direita: mover o inspetor entre as faixas.
- Tecla A: aprovar o produto.
- Tecla R: rejeitar o produto.
- Tecla ESC: sair do jogo.

## 12. Principais dificuldades esperadas

- Dificuldade 1: Sincronizar a movimentação do inspetor com a faixa e a posição do produto na esteira, para saber quando a decisão é válida.
- Dificuldade 2: Simular a IA de modo que erre em um número fixo de produtos por partida, sorteados a cada partida, e gerar o feedback correspondente.
- Dificuldade 3: Organizar o código em funções e módulos, escrever testes para as regras e trabalhar em dupla com Git e GitHub sem conflitos.

## 13. Escopo mínimo para a entrega final

**Escopo mínimo:**

Tela principal com esteira de três faixas e área de inspeção, desenhadas com formas simples; inspetor controlado pelo teclado; produtos surgindo um por vez; recomendação simulada da IA, que erra em um número fixo de produtos; decisão com as teclas A e R; feedback após cada decisão; pontuação, contador de erros e progresso na tela; condições de vitória e derrota; e recorde salvo em arquivo. Sem sons, menu inicial ou imagens externas nesta versão.

## 14. Possíveis melhorias, caso haja tempo

- Melhoria 1: IA com viés, que ignora um tipo de defeito, gerando erros com um padrão que o jogador pode aprender a reconhecer.
- Melhoria 2: Mais tipos de produtos e defeitos, com velocidade da esteira e dificuldade crescentes.
- Melhoria 3: Menu inicial com instruções, efeitos sonoros e ranking das melhores pontuações.

## 15. Organização inicial do código

A organização seguirá o template da disciplina, reaproveitando funções já existentes (como colisão e limite de valores) e adaptando os nomes ao jogo. Responsabilidades previstas:

- `src/jogo.py`: inicialização do Pygame, loop principal, leitura das teclas, movimentação do inspetor e dos produtos, e desenho da tela.
- `src/funcoes.py`: regras do jogo em funções simples, sem depender do Pygame, como criar produtos, definir a resposta correta, sortear em quais produtos a IA erra, conferir a decisão, atualizar pontos e erros e verificar o fim da partida.
- `src/dados.py`: leitura e gravação do recorde.
- `src/config.py`: valores fixos, como quantidade de produtos (10), limite de erros (3), número de faixas (3) e pontos por acerto (+10).
- `tests/`: testes das funções de lógica.

Os nomes das funções e a divisão final poderão mudar durante o desenvolvimento.

## 16. Estruturas de dados previstas

- **Dicionários:** cada produto será um dicionário com nome, faixa, lista de defeitos e recomendação da IA. A resposta correta será derivada dos defeitos, e não guardada separadamente, para evitar dados contraditórios.
- **Listas:** produtos da partida e defeitos de cada produto.
- **Tuplas:** posições fixas das faixas de inspeção, se necessário.

## 17. Uso de arquivos

O melhor resultado do jogador será salvo em `data/recorde.txt` (estrutura já prevista no template) e lido no início das partidas seguintes. Um arquivo com os dados dos produtos poderá ser usado apenas se houver tempo, como melhoria.

## 18. Testes planejados

Testes simples com pytest para as funções de lógica:

- produto sem defeitos deve ser aprovado e produto com defeito deve ser rejeitado;
- acerto soma 10 pontos;
- erro aumenta o contador de erros;
- produto sem decisão conta como erro;
- partida termina exatamente no 3º erro;
- vitória é identificada ao concluir os 10 produtos com no máximo 2 erros;
- a IA erra exatamente o número definido de produtos por partida;
- leitura e gravação do recorde em arquivo (usando arquivo temporário).

## 19. Recursos previstos

Python e Pygame, a partir do template oficial da disciplina. Na versão mínima, esteira, faixas, produtos e inspetor serão desenhados com formas simples do próprio Pygame, sem depender de imagens externas. Se forem usados imagens, sons ou fontes externos, o grupo registrará nome, origem e licença no `README.md`.

## 20. Originalidade e autoria

A ideia, as regras, as interações e a implementação serão desenvolvidas pelo grupo a partir do template oficial da disciplina e dos conteúdos estudados. Não há reaproveitamento de jogos de semestres anteriores nem cópia de tutoriais ou repositórios. Eventuais recursos externos serão identificados no `README.md`, com origem e, quando possível, licença.
