# Caixinha de ideias — Super Jogo da Velha

Memória das ideias que surgem nas conversas sobre o jogo. Aqui podemos guardar detalhes, retomar propostas e reconsiderá-las sem assumir que tudo será implementado.

Registro inicial: **15/10/2026**. As ideias abaixo foram recuperadas das conversas anteriores; esta é a data do registro, não necessariamente a data em que cada proposta surgiu.

## Panorama

| ID | Ideia | Situação | Resumo |
| --- | --- | --- | --- |
| [IDEIA-001](001-identidade-visual.md) | Identidade visual retrô | Em exploração | Referências a Bandersnatch e Doom antigo; seleção de dificuldade por botões após concluir a identidade visual. |
| [IDEIA-002](002-modo-livre-contra-maquina.md) | Modo livre contra a máquina | Implementada | Versão básica: conquistar, bloquear ou sortear; estratégia substituível, sem níveis ou história. |
| [IDEIA-003](003-modo-historia.md) | Campanha e personagens | Em exploração | Sequência de personagens e vidas; run de cerca de meia hora e escolha de Fácil/Médio/Difícil como possibilidades. |
| [IDEIA-004](004-habilidades-e-dificuldade.md) | Poderes e dificuldade | Em exploração | Fácil e Médio publicados; proposta de quatro níveis em avaliação, com topo muito difícil e vencível. Pesos atuais e testes documentados no guia. |
| [IDEIA-005](005-plataforma-e-evolucao.md) | Web agora, evolução depois | Em avaliação futura | Manter a versão web e reconsiderar uma engine apenas se houver necessidade concreta. |
| [IDEIA-006](006-intro-runa-dungeon.md) | Intro com runa e dungeon | Proposta | Tela preta durante o loading; uma runa em pedra aparece ao carregar e, ao clicar, ilumina a dungeon e leva ao menu. |

## Guia para testar as dificuldades

O [guia de dificuldades](../dificuldades/README.md) reúne a lógica atual, os pesos com exemplos de cálculo, limitações e uma ficha de observação para jogar e discutir ajustes. A proposta de quatro níveis ainda não altera o jogo publicado.

## Contexto já existente, não confundir com novas ideias

Na criação desta caixinha, o projeto já tem a versão web em HTML/CSS/TypeScript, duelo local entre duas pessoas, sons, histórico, conquistas e publicação no Sites. Os nomes iniciais Godric e Salazar e as conquistas Say my name., AQUELE QUE NÃO DEVE SER NOMEADO e LIÃO! já foram trabalhados; não são propostas pendentes desta lista.

Na conferência inicial de 15/10/2026, o menu de jogador versus máquina era uma entrada em desenvolvimento: sua presença não significa que já existe uma inteligência artificial jogável. Esta observação foi conferida no código durante a conversa de planejamento de 15/10/2026; confirme novamente antes de usá-la como status atual no futuro.

Atualização de 16/10/2026: após autorização, o modo básico contra a máquina foi implementado no checkout local; veja [IDEIA-002](002-modo-livre-contra-maquina.md). Isso não indica publicação no Sites.

Godric e Salazar são nomes iniciais de jogadores, não personagens confirmados da campanha. As referências visuais também não definem automaticamente o universo narrativo do jogo.

O documento [Contexto do projeto web](../projeto.md) também menciona PWA, acessibilidade e uma avaliação posterior de salas online/backend. Essas são possibilidades registradas no documento, não decisões novas do usuário nem requisitos aprovados para esta campanha.

## Sequência de trabalho sugerida, ainda não aprovada

Sugestão feita pelo assistente na conversa:

1. Criar o modo livre contra a máquina, sem poderes.
2. Fazer uma única fase experimental de história, com personagem provisório, uma habilidade, vitória, derrota e vidas.
3. Refinar a identidade visual e sonora dessa fase.
4. Expandir para os demais adversários e, se mantida a proposta, o chefe final.
5. Ajustar equilíbrio e acabamento geral.

A intenção é testar a diversão e a clareza das mecânicas antes de produzir toda a arte. Isso não exige abandonar a estética retrô atual, nem impede desenvolver conceitos visuais em paralelo. O usuário pediu orientação sobre essa ordem; não confirmou um cronograma nem autorizou sua implementação nesta conversa.

## Como guardar e retomar

- **Salvar:** conte a ideia e peça para guardá-la. Se for continuação de uma ideia existente, o mesmo arquivo é ampliado, sem criar uma duplicata.
- **Consultar:** peça um panorama, todas as ideias ou um tema específico. A resposta pode ser breve; os detalhes permanecem nos arquivos.
- **Reavaliar:** podemos discutir o que ainda faz sentido e suas dependências. Uma nova sugestão do assistente não vira decisão sua automaticamente.
- **Mudar de direção:** quando você confirmar uma alteração, registramos a decisão e o motivo. A versão anterior fica identificada como substituída, adiada ou descartada, sem apagar a memória da discussão.

Consultar não modifica os registros. Salvar ideias modifica somente esta documentação; não significa programar a funcionalidade, fazer commit/push, merge ou publicar o site. Essas ações dependem de um pedido próprio.

## Convenção dos registros

Cada arquivo tem ID estável, título, data de registro/atualização, origem, situação, proposta detalhada, sugestões separadas, decisões e perguntas em aberto. Novos IDs seguem a sequência numérica, sem reutilizar IDs antigos.

Situações possíveis: **Em exploração**, **Proposta**, **Em avaliação futura**, **Aprovada para desenvolver**, **Em desenvolvimento**, **Implementada**, **Adiada** ou **Descartada**. Uma aprovação exige confirmação explícita; implementação exige evidência no projeto. Alterar a situação exige atualizar também este índice.

Preserve números, alternativas e referências importantes, mas marque exemplos como exemplos. Não complete lacunas de história, personagens ou regras como se fossem decisões do usuário.
