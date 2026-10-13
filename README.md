# Super Jogo da Velha // SJV-84

Versao web do Super Jogo da Velha, executada inteiramente no navegador. O projeto nao depende de API ou servidor Python para jogar.

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
