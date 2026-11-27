# Dados

Esta pasta guarda arquivos de persistencia simples em texto.

## Arquivos

- `recorde.txt`: melhor pontuacao registrada.
- `inspetores.json`: carteira separada (`saldo` inteiro não negativo), IDs
  `comprados` e ID `equipado`. Criado pelo jogo e ignorado pelo Git. O padrão
  gratuito está sempre disponível. Arquivo ausente/inválido usa saldo zero;
  IDs desconhecidos são descartados e equipamento inválido volta ao padrão.
  Gravação atômica por arquivo temporário; falhas não encerram a partida.
- `ranking.txt`: base para ranking de jogadores (opcional neste template).
- `README.txt`: arquivo legado; manter por compatibilidade se necessario.

## Observacao

Evite versionar dados pessoais reais dos jogadores.
