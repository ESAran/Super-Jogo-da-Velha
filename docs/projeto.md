# Contexto do projeto web

## Objetivo

O projeto implementa um Super Jogo da Velha para navegador com identidade visual retrofuturista. A aplicacao funciona localmente e nao exige backend para partidas no mesmo dispositivo.

## Tecnologias

- HTML semantico;
- CSS responsivo com animacoes;
- TypeScript;
- Vite para desenvolvimento e build;
- test runner nativo do Node.js para testes do motor;
- Web Audio API para efeitos sonoros;
- `localStorage` para historico e conquistas locais.

## Arquitetura

O nucleo em `src/game` nao conhece HTML, CSS ou armazenamento. A camada `src/ui` transforma o estado do motor em interface e recebe as interacoes do jogador.

Essa separacao permite trocar a apresentacao, adicionar uma inteligencia artificial ou conectar um backend no futuro sem reescrever as regras basicas.

## Escopo atual

- jogador contra jogador no mesmo dispositivo;
- jogador contra máquina básica: conquistar, bloquear ou sortear, com pausa de 0,7 segundo;
- menu, cadastro, regras, historico, conquistas e creditos;
- motor completo do Super Jogo da Velha;
- funcionamento offline durante a execucao local;
- sem API e sem multiplayer pela internet.

## Evolucao futura

1. Evoluir o desafio da maquina, cuja estrategia ja esta separada do motor.
2. Refinar animacoes, trilha e acessibilidade.
3. Avaliar instalacao como PWA.
4. Somente depois avaliar salas online e backend em tempo real.
