# Super Jogo da Velha

Projeto de estudo e evolução arquitetural baseado em um jogo da velha avançado desenvolvido em Python.

O objetivo do projeto é transformar um protótipo inicialmente criado como passatempo em uma aplicação estruturada, escalável e orientada a boas práticas de engenharia de software.

---

# Objetivos do Projeto

* Refatorar a arquitetura original
* Separar regras de negócio da interface
* Construir uma API com FastAPI
* Criar uma interface web estilizada
* Experimentar integração com IA (Codex)
* Evoluir o projeto para nível de portfólio

---

# Stack

## Backend

* Python
* FastAPI
* Pydantic

## Frontend (planejado)

* HTML
* CSS
* JavaScript

## Ferramentas

* Git
* GitHub
* Codex
* VS Code

---

# Estrutura do Projeto

```bash
app/
├── game/
│   ├── engine.py
│   ├── board.py
│   ├── rules.py
│
├── api/
│   ├── routes.py
│
├── schemas/
│
├── services/
│
└── core/

tests/

main.py
```

---

# Roadmap do Projeto

## Fase 1 — Refatoração da Engine ✅

### Objetivos

* reorganizar estrutura
* separar responsabilidades
* remover acoplamentos
* padronizar imports

### Status

Concluído.

---

## Fase 2 — API FastAPI 🚧

### Objetivos

* criar endpoints REST
* expor o `MotorJogo` via API
* implementar schemas Pydantic
* tratar erros adequadamente

### Endpoints planejados

#### Iniciar partida

```http
POST /game/start
```

#### Fazer jogada

```http
POST /game/move
```

#### Obter estado atual

```http
GET /game/state
```

### Status

Em desenvolvimento.

---

## Fase 3 — Melhorias de Backend

### Objetivos

* múltiplas partidas
* gerenciamento de sessões
* serialização avançada
* testes automatizados
* tratamento de exceções customizadas

### Status

Planejado.

---

## Fase 4 — Frontend Web

### Objetivos

* interface web interativa
* integração com API
* visual inspirado em Bandersnatch
* estética neon/pixel/grid

### Status

Planejado.

---

## Fase 5 — Inteligência Artificial

### Objetivos

* implementar algoritmo minimax
* níveis de dificuldade
* jogador automático

### Status

Planejado.

---

# Arquitetura

O projeto segue separação em camadas:

* `game/` → regras e lógica principal
* `api/` → rotas FastAPI
* `schemas/` → contratos da API
* `services/` → orquestração
* `frontend/` → interface visual (futuro)

A lógica do jogo não deve depender da interface.

---

# Convenções do Projeto

* evitar lógica de negócio em rotas
* manter funções pequenas
* separar responsabilidades
* evitar duplicação
* trabalhar em pequenas refatorações incrementais

---

# Objetivo Educacional

Este projeto também funciona como laboratório para aprendizado de:

* arquitetura backend
* FastAPI
* refatoração
* integração com IA
* workflow profissional com Git
* construção de projetos de portfólio

---

# Próximos Passos

* finalizar integração FastAPI
* criar schemas Pydantic
* estruturar respostas da API
* implementar gerenciamento de estado da partida
* iniciar prototipação do frontend web
