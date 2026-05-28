# Contexto Tecnico do Projeto

## 1. Objetivo do projeto

O projeto implementa um Super Jogo da Velha em Python. A partida usa 9 mini tabuleiros 3x3, em que a posicao jogada dentro de um mini tabuleiro define o proximo mini tabuleiro obrigatorio para o adversario.

O objetivo tecnico atual e manter um nucleo de jogo isolado da interface, permitindo evolucao incremental para CLI, API, persistencia, historico, conquistas e modo jogador contra maquina.

Este documento serve como contexto base para desenvolvimento continuo com IA. Ao modificar o projeto, preservar a separacao entre regras de jogo, estado da partida, adaptadores de interface e contratos de dados.

## 2. Tecnologias utilizadas

- Linguagem: Python 3.12.
- Paradigma principal: orientacao a objetos com funcoes auxiliares pequenas.
- Interface atual: CLI baseada em `input` e `print`.
- Tipagem: type hints nativos (`list[str]`, `int | None`, dataclasses).
- Persistencia: prevista, mas ainda nao implementada.
- API: prevista por fronteira em modulo, mas ainda sem framework HTTP.
- Dependencias externas: nenhuma obrigatoria no nucleo atual.

## 3. Estrutura atual de pastas

```text
.
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── game/
│   │   ├── __init__.py
│   │   ├── board.py
│   │   ├── engine.py
│   │   └── rules.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── game.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── cli.py
│   └── __init__.py
├── docs/
│   ├── alteracoes.txt
│   └── contexto_tecnico.md
├── examples/
│   └── game exemple.txt
├── src/
│   ├── domain/
│   ├── services/
│   └── ui/
├── storage/
│   ├── conquistas_repository.py
│   └── historico_repository.py
└── main.py
```

Observacoes:

- `app/` e a estrutura principal ativa.
- `main.py` e o ponto de entrada atual.
- `src/` mantem wrappers de compatibilidade para imports antigos.
- `storage/` existe como preparacao para persistencia, mas seus repositorios ainda estao vazios.
- `examples/game exemple.txt` contem exemplo legado e pode nao refletir a API atual.
- `__pycache__/` e `venv/` sao artefatos locais e nao fazem parte da arquitetura.

## 4. Responsabilidade de cada modulo

### `main.py`

Ponto de entrada da aplicacao. Importa `executar_aplicacao` de `app.services.cli` e inicia a CLI.

### `app/game/board.py`

Contem as estruturas de tabuleiro:

- `MiniTabuleiro`: representa um tabuleiro 3x3, valida posicoes, marca celulas, consulta celulas, verifica vitoria local e tabuleiro cheio.
- `Tabuleiro`: agrega 9 mini tabuleiros e um tabuleiro de resultado macro. Encapsula marcacao de jogadas, acesso aos mini tabuleiros e verificacao de vitoria principal.

Nao deve conter `input`, `print`, menus, formatacao de terminal, persistencia ou codigo de API.

### `app/game/rules.py`

Contem `RegrasJogo`, responsavel por regras puras:

- calcular o proximo mini tabuleiro obrigatorio;
- verificar se um mini tabuleiro de destino esta disponivel;
- validar se uma jogada respeita mini obrigatorio, limites e celula vazia.

Nao deve alterar interface, ler entrada do usuario ou renderizar estado.

### `app/game/engine.py`

Contem o motor da partida:

- `TipoJogador`: enum para humano ou maquina.
- `Jogador`: entidade simples com nome, simbolo e tipo.
- `MotorJogo`: controla estado da partida, jogador atual, vencedor, mini obrigatorio e execucao de jogadas.

O motor coordena `Tabuleiro` e `RegrasJogo`, mas nao conhece detalhes da CLI.

### `app/services/cli.py`

Adaptador de interface de terminal. Responsavel por:

- menu principal;
- cadastro de jogadores;
- leitura de jogadas;
- renderizacao textual do tabuleiro;
- mensagens de erro;
- fluxo da partida no terminal.

Este modulo pode usar `input`, `print` e `os.system`. Regras de negocio novas nao devem ser colocadas aqui, exceto validacoes especificas de interface, como converter uma opcao digitada para coordenadas.

### `app/api/routes.py`

Fronteira inicial para uma API futura. Hoje fornece funcoes diretas:

- `criar_partida`;
- `jogar`;
- `obter_estado`.

Ainda nao ha framework web configurado. Este modulo deve permanecer como camada de adaptacao entre contratos externos e `app.game`.

### `app/schemas/game.py`

Define contratos simples com dataclasses:

- `JogadorEntrada`;
- `JogadaEntrada`;
- `EstadoPartida`.

Estes objetos ajudam a separar entrada/saida de interfaces do modelo interno do jogo.

### `src/`

Camada legada de compatibilidade. Os arquivos em `src/domain`, `src/services` e `src/ui/cli` redirecionam para a nova estrutura em `app/`.

Novas funcionalidades devem ser implementadas em `app/`, nao em `src/`.

### `storage/`

Local reservado para repositorios de persistencia:

- `historico_repository.py`;
- `conquistas_repository.py`.

Ainda nao possui implementacao real. Ao implementar, estes modulos nao devem conhecer a CLI.

## 5. Estado atual do desenvolvimento

O projeto esta em fase de reorganizacao arquitetural concluida, com funcionamento principal preservado via CLI.

Estado atual:

- nucleo do jogo migrado para `app/game`;
- interface CLI centralizada em `app/services/cli.py`;
- ponto de entrada definido em `main.py`;
- contratos de entrada e saida iniciados em `app/schemas`;
- fronteira de API iniciada em `app/api/routes.py`;
- wrappers legados mantidos em `src/`;
- persistencia, historico, conquistas e IA ainda pendentes;
- nao ha suite automatizada de testes versionada.

Validacoes ja executadas durante a reorganizacao:

```bash
python3 -m compileall app main.py src
printf '0\n' | python3 main.py
```

## 6. Funcionalidades implementadas

- Menu principal no terminal.
- Cadastro de dois jogadores humanos.
- Validacao de nome e simbolo dos jogadores.
- Execucao de partida jogador contra jogador.
- Representacao de 9 mini tabuleiros.
- Validacao de jogadas:
  - mini tabuleiro valido;
  - mini tabuleiro nao encerrado;
  - respeito ao mini tabuleiro obrigatorio;
  - celula vazia;
  - posicao de 1 a 9 convertida para linha e coluna.
- Atualizacao do mini tabuleiro obrigatorio apos cada jogada.
- Deteccao de vitoria em mini tabuleiro.
- Atualizacao do tabuleiro macro de resultado.
- Deteccao de vencedor geral.
- Telas informativas de regras, creditos, historico e conquistas.
- Placeholders para modo jogador contra maquina, historico e conquistas.
- Camada inicial de API funcional em nivel de funcao Python.

## 7. Proximas fases planejadas

1. Criar testes automatizados para `app/game`.
2. Corrigir e formalizar encerramento por empate geral.
3. Implementar persistencia JSON em `storage/` ou mover repositorios para `app/services` conforme decisao arquitetural.
4. Registrar historico de partidas a partir de eventos do motor.
5. Implementar conquistas com regras separadas da CLI.
6. Implementar modo jogador contra maquina com estrategia plugavel.
7. Evoluir `app/api/routes.py` para uma API HTTP real, se necessario.
8. Reduzir dependencia da CLI sobre atributos publicos do motor por meio de metodos de consulta ou snapshots de estado.
9. Remover gradualmente a camada legada `src/` quando nao houver mais imports antigos.
10. Atualizar ou remover `examples/game exemple.txt`, pois ele referencia API antiga.

## 8. Decisoes arquiteturais importantes

- A pasta `app/` e a fonte principal de codigo novo.
- A logica de negocio fica em `app/game`.
- Entrada e saida de terminal ficam em `app/services/cli.py`.
- Regras de jogo nao devem depender da CLI.
- O motor da partida coordena regras e tabuleiro, mas nao deve renderizar telas.
- `src/` existe apenas para compatibilidade temporaria.
- `schemas/` define contratos externos e evita expor diretamente objetos internos quando houver API ou persistencia.
- A API atual e uma fronteira funcional, nao um servidor HTTP.
- Persistencia deve ser implementada como camada separada, sem importar CLI.
- Validacoes de dominio devem lancar `ValueError` com mensagens claras.

## 9. Convencoes do projeto

- Usar nomes em portugues para classes, metodos e variaveis do dominio.
- Manter funcoes pequenas, com responsabilidade unica.
- Evitar colocar regra de jogo em modulos de interface.
- Evitar `input`, `print` e `os.system` fora de adaptadores de interface.
- Usar type hints em funcoes e atributos relevantes.
- Usar dataclasses para contratos simples e entidades sem comportamento complexo.
- Usar `ValueError` para entradas invalidas de dominio ou interface.
- Preservar compatibilidade com Python 3.12.
- Priorizar codigo sem dependencias externas enquanto o nucleo estiver simples.
- Implementar novas funcionalidades primeiro em `app/`; atualizar wrappers de `src/` somente se necessario.
- Antes de entregar mudancas, executar pelo menos:

```bash
python3 -m compileall app main.py src
```

## 10. Roadmap tecnico

### Fase 1: Estabilizacao do nucleo

- Criar testes unitarios para `MiniTabuleiro`, `Tabuleiro`, `RegrasJogo` e `MotorJogo`.
- Cobrir cenarios de vitoria local, vitoria macro, jogada invalida, mini obrigatorio e mini encerrado.
- Definir comportamento oficial para empate geral.

### Fase 2: Modelo de estado e eventos

- Criar snapshot serializavel da partida.
- Fazer `MotorJogo.jogar` retornar resultado estruturado da jogada.
- Registrar eventos como jogada realizada, mini vencido, partida finalizada e partida cancelada.

### Fase 3: Persistencia

- Definir formato JSON para historico.
- Implementar repositorio de historico.
- Implementar repositorio de conquistas.
- Garantir que repositorios nao dependam da CLI.

### Fase 4: Modo maquina

- Criar interface de estrategia para jogador maquina.
- Implementar primeira estrategia simples baseada em jogadas validas.
- Evoluir para heuristica de vitoria, bloqueio e escolha de mini tabuleiro.

### Fase 5: API e integracoes

- Definir se a API sera HTTP.
- Se houver servidor, escolher framework e isolar dependencias no adaptador.
- Manter `app/game` independente de framework web.
- Usar schemas para entrada e saida externas.

### Fase 6: Limpeza de legado

- Remover ou arquivar `src/` apos migracao completa.
- Atualizar exemplos para a API atual.
- Remover arquivos e artefatos gerados do versionamento.
- Consolidar documentacao tecnica em `docs/`.
