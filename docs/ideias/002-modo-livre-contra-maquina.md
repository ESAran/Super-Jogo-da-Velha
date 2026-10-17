# IDEIA-002 — Modo livre contra a máquina

- **Registrada em:** 15/10/2026.
- **Atualizada em:** 16/10/2026.
- **Origem:** usuário; encaminhamento técnico sugerido pelo assistente.
- **Situação:** Implementada.

## O que o usuário imaginou

Ter, dentro da experiência de jogador versus máquina, duas possibilidades:

- **Modo livre:** a partida normal contra a máquina, sem precisar seguir a campanha.
- **Modo história:** uma sequência de personagens e acontecimentos próprios.

O usuário se referiu ao modo normal como algo que já existia. Na conferência do código durante a conversa, havia o botão do menu, mas ele ainda mostrava que o módulo de IA estava fora de linha. Portanto, implementar o adversário controlado pelo jogo é uma etapa real, não apenas criar um novo submenu.

## Experiência pretendida

Permitir iniciar uma partida avulsa contra o computador, preservando as regras do Super Jogo da Velha. Esse modo deve continuar disponível mesmo depois de existir a campanha.

Não foi definido se escolheremos um personagem específico, se haverá seleção de dificuldade ou se a partida livre poderá ativar poderes. Essas opções não são requisitos confirmados.

## Sugestões do assistente, não decisões aprovadas

- Começar com uma máquina que respeita as mesmas regras do jogador e não usa habilidades especiais.
- Desenvolver a estratégia da máquina separada das regras do motor, para poder reaproveitá-la na campanha.
- Testar a dificuldade básica antes de combinar inteligência da máquina, poderes, vidas e tempo.
- Fazer deste modo a próxima feature, seguida por uma fase experimental de campanha.

## Atualização de 16/10/2026 — escopo inicial em discussão

O usuário indicou como melhor alternativa começar por jogador versus máquina básico, sem seleção de dificuldade e sem elementos de modo história. Estamos apenas definindo a proposta: ele explicitamente pediu para não iniciar a programação ainda. A situação permanece **Proposta**.

Três níveis (fácil, médio e difícil) foram guardados como possibilidade futura em [IDEIA-004](004-habilidades-e-dificuldade.md), sem compromisso de adoção. A proposta inicial foi refinada posteriormente nesta mesma conversa, conforme abaixo; a dificuldade real ainda precisará ser avaliada jogando.

## Refinamento do planejamento em 16/10/2026

Escopo a apresentar para confirmação: partida básica contra a máquina, sem seleção de dificuldade, pesos, personagens, poderes ou modo história. A máquina tenta conquistar um pequeno quadrante, depois bloquear uma linha imediata do humano e, caso contrário, sorteia entre jogadas válidas. Não antecipa sequências futuras. O desempate aleatório entre opções da mesma prioridade foi sugerido pelo assistente.

O usuário pediu que a estratégia seja fácil de substituir e evoluir no código e que a implementação use uma branch própria da feature. Ao final do pedido, explicitou que deseja primeiro confirmar o entendimento no próximo prompt. Portanto, o registro da ideia está autorizado agora, mas criação da branch e implementação aguardam confirmação. A situação permanece **Proposta**.

A evolução possível para antecipação de jogadas e pesos fica em [IDEIA-004](004-habilidades-e-dificuldade.md).

## Ainda falta decidir

- Quais níveis de dificuldade existirão, se houver seleção?
- Como a máquina decide uma jogada e como sua força varia?
- Haverá tempo de resposta aparente ou animação de pensamento?
- A dificuldade poderá ser alterada durante uma campanha ou só antes dela?
- Partidas livres terão apenas as regras clássicas ou também variantes opcionais?

## Relações

É a base proposta para [modo história](003-modo-historia.md). A discussão sobre dificuldade e habilidades está em [IDEIA-004](004-habilidades-e-dificuldade.md).

## Implementação básica em 16/10/2026

Após a confirmação explícita do usuário, foi criada a branch `codex/jogador-vs-maquina` a partir do checkout existente, preservando alterações locais anteriores. O modo básico está implementado em `src/ui/app.ts`, com estratégia separada em `src/game/machine.ts`: conquistar, bloquear ou sortear, respeitando as jogadas válidas e sorteando empates de prioridade.

O humano inicia de X; o computador joga de O após uma pausa breve. Cliques ficam bloqueados durante a resposta automática, sair cancela a resposta pendente e a revanche preserva o modo. O histórico registra partidas e vitórias da máquina não contam como vitórias humanas nas conquistas. Não foram implementados níveis, pesos, antecipação ou modo história.

Os registros anteriores de espera por autorização são históricos e foram substituídos pela confirmação do usuário. A dificuldade prática continua sujeita à avaliação jogando.

## Conclusão aceita pelo usuário — 16/10/2026

Após testar, o usuário aprovou a primeira versão básica como concluída, com pausa de 0,7 segundo por resposta. Autorizou merge na develop do GitHub e publicação. A máquina ainda é fácil e as partidas rápidas; aumentar o desafio será uma nova feature, registrada em IDEIA-004, sem alterar esta entrega.
