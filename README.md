# Super Jogo da Velha // SJV-84

Versao web do Super Jogo da Velha, executada inteiramente no navegador. O projeto nao depende de API ou servidor Python para jogar.

## Primeira versao web

Versao **1.0.0**, identificada pela tag `web-v1.0.0`. A tag legada `v1.0` continua preservando a versao anterior em Python.

Esta entrega inclui o duelo local entre dois jogadores, identidade visual retro, sons, historico e conquistas persistentes. Na entrega original, o modo contra a maquina ainda nao estava disponivel; multiplayer online tambem nao fazia parte dessa versao.

O progresso fica salvo neste navegador, sem conta ou sincronizacao entre dispositivos. Depois desta entrega, novas alteracoes devem partir de `develop` em branches dedicadas e retornar por pull request.

## Executar localmente

```bash
npm install
npm run dev
```

Abra o endereco local exibido no terminal.

## Comandos

```bash
npm run dev      # ambiente local com atualizacao automatica
npm run build    # gera a versao final em dist/
npm run preview  # abre localmente a versao compilada
npm test         # executa os testes do motor
```

## Estrutura

- `src/game/`: tabuleiro, regras e motor independentes da interface.
- `src/ui/`: interface e audio sintetizado no navegador.
- `src/styles.css`: identidade visual retrofuturista e responsiva.
- `tests/`: testes automatizados das regras principais.

## Caixinha de ideias

As propostas para o futuro do jogo ficam em [docs/ideias/README.md](docs/ideias/README.md). O índice traz um panorama; cada ideia tem um arquivo com contexto, possibilidades e perguntas em aberto. São ideias para discutir, não uma lista de funcionalidades já aprovadas.

Com a skill pessoal `ideias-super-jogo-da-velha`, peça "salva essa ideia para o jogo", "me mostra as ideias guardadas" ou "vamos retomar a ideia do modo história". Salvar uma ideia não inicia implementação nem publicação.

## Funcionalidades

- partida local para dois jogadores;
- partida contra o computador: voce joga de X e inicia, a maquina joga de O;
- validacao do mini tabuleiro obrigatorio;
- vitoria em mini tabuleiro e no tabuleiro principal;
- deteccao de empate geral;
- historico e conquistas salvos localmente no navegador;
- efeitos sonoros sintetizados, sem arquivos externos;
- interface responsiva para computador e celular.

## Maquina basica

No menu, escolha **JOGADOR VS MAQUINA**, informe seu nome e inicie. A maquina responde automaticamente apos uma pequena pausa; durante sua vez, as casas ficam bloqueadas. A revanche preserva o modo escolhido.

A estrategia tenta conquistar um pequeno quadrante; se nao puder, bloqueia uma linha imediata do humano; caso contrario, sorteia uma jogada valida. Empates de prioridade tambem sao sorteados. Nao ha pesos, antecipacao de sequencias, selecao de dificuldade ou modo historia.

`src/game/machine.ts` define o contrato `MachineStrategy` e a implementacao `BasicMachineStrategy`. O `GameApp` recebe a estrategia no construtor, permitindo substitui-la sem alterar o motor ou o fluxo da partida. O sorteio tambem pode ser injetado para testes.

Partidas contra a maquina entram no historico; vitorias do computador nao contam para as conquistas de vitoria do jogador.
