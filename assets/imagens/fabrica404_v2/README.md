# Artes em uso — Fábrica 404 v2

Os 17 PNGs desta pasta são os sprites finais do pacote
`output/Fabrica_404_Sprites_Referencia_v2.zip`, gerados a partir da referência
visual do usuário. Estão na escala nativa da demonstração de 800 × 600.

`src/desenho.py` usa esta pasta. `layout.json` registra a composição original.
`README-pacote.md` contém dimensões e instruções do pacote completo; os arquivos
auxiliares mencionados nele estão em `output/fabrica404-sprites-v2/`.

Esteiras, portas, marcações e inspetor usam tamanho nativo, sem suavização.
Produtos são escolhidos pelo nome recebido; Pacote usa Caixa, Frasco usa Garrafa.
Peça mecânica tem sprite próprio, sem mudar o catálogo ou sorteio da Mariana.

Portas: a chave opcional `estado['portas']` aceita três strings, `aberta` ou
`fechada`, na ordem esquerda/central/direita. Sem a chave, ficam abertas.
O desenho não decide quando fechar. Cada par possui o mesmo canvas e encaixe.

Para visualizar: `python -m src.previa`. Espaço alterna produtos, portas,
feedback e finais. O loop legado em `main.py` ainda aguarda a integração da Mariana.
