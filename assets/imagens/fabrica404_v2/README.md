# Artes em uso — Fábrica 404 v2

Os 17 PNGs originais desta pasta são os sprites finais do pacote
`output/Fabrica_404_Sprites_Referencia_v2.zip`, gerados a partir da referência
visual do usuário. Estão na escala nativa da demonstração de 800 × 600.

`src/desenho.py` usa esta pasta. `layout.json` registra a composição original.
`README-pacote.md` contém dimensões e instruções do pacote completo; os arquivos
auxiliares mencionados nele estão em `output/fabrica404-sprites-v2/`.

Esteiras, portas, marcações e inspetor usam tamanho nativo, sem suavização.
Produtos são escolhidos pelo catálogo único `SPRITES_PRODUTOS` em `src/config.py`.
Caixa, Garrafa, Lata e Peça mecânica usam as artes já disponíveis. A peça passou
a participar do sorteio, junto com Bobina e Bateria (três tipos adicionais).
Pacote e Frasco agora têm desenhos próprios, sem reutilizar Caixa e Garrafa.

## Quatro novos PNGs

| Produto | Arquivo | Tamanho nativo | Silhueta |
|---|---|---|---|
| Pacote | `produto_pacote.png` | 46 × 34 | envelope de papel selado |
| Frasco | `produto_frasco.png` | 38 × 33 | pote baixo de vidro âmbar com tampa larga |
| Bobina | `produto_bobina.png` | 44 × 36 | carretel horizontal com fio de cobre |
| Bateria | `produto_bateria.png` | 28 × 42 | corpo retangular com dois terminais |

Gerados com a ferramenta integrada `image_gen`. Os prompts completos estão em
`prompts-produtos.json`. Foi solicitado um objeto isolado, pixel art de baixa
resolução, contorno azul-marinho, fundo transparente, iluminação superior
esquerda e condição neutra, sem danos, defeitos, texto ou logotipos. As margens
transparentes foram recortadas e as imagens reduzidas por vizinho mais próximo,
preservando o alfa. Nenhuma arte original foi substituída.

O jogo encaixa cada arte no retângulo de transporte (até 46 × 42), conservando
proporção, nitidez e âncora inferior. O retângulo lógico, os prazos e as regras
não variam por tipo. Arquivo ausente ou ilegível usa um ícone informativo neutro;
esse ícone não é sinal de defeito. Defeitos e recomendações continuam sorteados
separadamente do nome e aparecem no painel.

Portas: a chave opcional `estado['portas']` aceita três strings, `aberta` ou
`fechada`, na ordem esquerda/central/direita. Sem a chave, ficam abertas.
O desenho não decide quando fechar. Cada par possui o mesmo canvas e encaixe.

Para visualizar: `python -m src.previa`. Espaço alterna produtos, portas,
feedback e finais. `main.py` executa a partida integrada; a prévia legada usa
dados fictícios e não substitui a validação manual dos modos atuais.
