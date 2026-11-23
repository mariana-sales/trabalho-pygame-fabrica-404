# Fundo da composição aprovada

`fundo_fabrica.png` foi preparado com a ferramenta integrada de geração/edição
de imagens, usando `ChatGPT Image Nov 22, 2026, 01_52_17 AM.png` como referência.
O prompt completo está em `prompt-fundo.json`.

A imagem preserva a parede, três aberturas, câmera e materiais da referência.
Esteiras, produtos, personagem, painel inferior e a grande faixa amarela no
piso foram removidos para permitir camadas independentes. As listras das
aberturas da parede permanecem.

O Pygame ajusta o fundo proporcionalmente dentro da área de 800 × 380, abaixo
da interface, sem esticar, com margens azul-marinho nas laterais.

Camadas: fundo → esteiras → portas B → zonas ciano → produto → inspetor A → UI.
O inspetor mantém o PNG original e agora mede 120 px de altura. As esteiras
usam os PNGs separados em `fabrica404_v2`, cuja convergência encaixa nas saídas.
Portas ficam sobre o tampo, atrás do produto parado, com a mesma âncora nos
dois estados. O fundo não contém portas de controle nem objetos decorativos
de produto; as três aberturas são parte da parede.

Dados, decisões e transições permanecem sob controle da lógica existente.

Ajuste de alinhamento: as três esteiras, portas e zonas agora usam perspectiva
frontal, com eixos em x=298, 400 e 502 alinhados às saídas. A inspetora foi
aproximada 20 px da esteira (base y=558), mantendo o produto inteiro visível.
