# Super Jogo da Velha // SJV-84

Versao web do Super Jogo da Velha, executada inteiramente no navegador. O projeto nao depende de API ou servidor Python para jogar.

## Primeira versao web

Versao **1.0.0**, identificada pela tag `web-v1.0.0`. A tag legada `v1.0` continua preservando a versao anterior em Python.

Esta entrega inclui o duelo local entre dois jogadores, identidade visual retro, sons, historico e conquistas persistentes. O modo contra a maquina ainda nao esta disponivel; multiplayer online tambem nao faz parte desta versao.

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

## Funcionalidades

- partida local para dois jogadores;
- validacao do mini tabuleiro obrigatorio;
- vitoria em mini tabuleiro e no tabuleiro principal;
- deteccao de empate geral;
- historico e conquistas salvos localmente no navegador;
- efeitos sonoros sintetizados, sem arquivos externos;
- interface responsiva para computador e celular.
