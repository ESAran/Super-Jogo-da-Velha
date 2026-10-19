# IDEIA-004 — Habilidades especiais e dificuldade

- **Registrada em:** 15/10/2026.
- **Atualizada em:** 17/10/2026.
- **Origem:** exemplos do usuário; análises e alternativas do assistente explicitadas.
- **Situação:** Em exploração.

## Proposta geral do usuário

Dar habilidades especiais aos personagens do modo história, criando situações diferentes dentro das partidas. A relação entre personagem, poder e dificuldade ainda será pensada. Nenhum número abaixo deve ser tratado como balanceamento final.

## 1. Cegueira parcial

**Ideia do usuário:** um personagem deixa o jogador meio cego, impedindo que veja, por exemplo, **cinco dos nove tabuleiros** no mapa.

**Em aberto:** esconder setores inteiros ou apenas suas peças; duração; frequência; quais setores são afetados; possibilidade de jogar nos setores ocultos; visibilidade do setor obrigatório; informação disponível para a máquina.

**Sugestões do assistente:** avisar antes do efeito, limitar sua duração e começar os testes escondendo menos setores. A habilidade deve criar um desafio compreensível, não deixar o jogador sem saber quais ações são possíveis. Cinco setores foi o exemplo do usuário, não uma quantidade já aprovada para a primeira implementação.

## 2. Inversão do tabuleiro ou troca de células

**Ideia do usuário:** outro personagem poderia inverter o tabuleiro ou trocar células de lugar.

**Distinção importante levantada pelo assistente:** girar ou espelhar apenas a apresentação não é o mesmo que mudar o estado real da partida. São alternativas diferentes, ainda não escolhidas.

Se a alteração for só visual, é preciso manter a correspondência clara entre o clique, a célula real e o próximo setor obrigatório. Se peças ou células forem realmente movidas, será necessário definir o que acontece com linhas completas, setores já conquistados, possíveis novas vitórias e a regra que envia o próximo jogador a um setor.

**Em aberto:** girar, espelhar ou permutar; afetar o mapa todo, um setor ou algumas peças; duração; reversão; aviso ao jogador; momento em que ocorre.

**Sugestão do assistente:** testar primeiro uma inversão visual, pois alterar posições reais exige resolver mais regras. Não houve escolha definitiva do usuário.

## 3. Pressão de tempo

**Ideia do usuário:** um personagem ou desafio exige fazer a jogada rapidamente, usando limite de tempo.

**Em aberto:** tempo por jogada; momento em que o relógio começa; aplicação permanente ou temporária; pausa; comportamento ao sair da aba; consequência do tempo esgotado; ajustes de acessibilidade.

**Sugestão do assistente:** tornar a consequência explícita e, inicialmente, evitar retirar uma vida inteira por uma única jogada atrasada. Passar a vez, outra penalidade ou perder a partida são questões a discutir, não regras escolhidas.

## 4. Como definir a dificuldade

**Pedido do usuário:** pensar em como definir a dificuldade dessas partidas e habilidades. Na discussão inicial, não foram estabelecidos níveis, valores ou algoritmo de IA; a evolução da proposta está registrada abaixo.

**Sugestões do assistente:** separar força de decisão da máquina e intensidade dos poderes. Testar cada componente isoladamente antes de combiná-los, para entender o que gera desafio e o que gera frustração.

Possíveis parâmetros a avaliar, sem valores aprovados:

- qualidade das escolhas da máquina;
- frequência e duração das habilidades;
- quantidade de setores afetados;
- tempo disponível para agir;
- momento em que cada novidade é apresentada;
- interação com vidas e novas tentativas.

O assistente sugeriu que o chefe final combine habilidades já apresentadas, em vez de simplesmente usar uma máquina forte, esconder muitos setores e reduzir o tempo ao mesmo tempo.

## Atualização de 16/10/2026 — níveis como possibilidade

**Ideia do usuário:** considerar futuramente três níveis: fácil, médio e difícil. É uma possibilidade guardada para reavaliar, não uma decisão de adotar esses níveis. O usuário quer evitar uma máquina que antecipe tão bem as jogadas que pareça impossível de vencer.

**Orientação atual de planejamento:** começar pelo modo jogador versus máquina básico, sem seleção de dificuldade e sem modo história. Inicialmente a estratégia ainda estava em discussão; a proposta mais recente está detalhada a seguir.

**Limite confirmado:** estamos na fase de pensar e definir. O usuário explicitou que não autorizou começar a programar; a implementação depende de um pedido posterior.

A possibilidade de níveis não substitui a ideia de personagens no modo história. A relação entre essas alternativas continua aberta.

## Complemento de 16/10/2026 — visão futura e comportamento inicial

**Possibilidades propostas pelo usuário, sem compromisso de implementar níveis:**

- Primeira dificuldade: reage ao estado atual, sem antecipar sequências futuras.
- Segunda dificuldade: considera possíveis jogadas posteriores para decidir. O usuário sugeriu avaliar um sistema de pesos; profundidade da busca, critérios e pesos não foram definidos.
- Dificuldade superior: comportamento ainda indefinido.

**Comportamento inicial discutido e aceito como base do planejamento:** conquistar um pequeno quadrante quando houver uma jogada válida que complete sua linha; caso contrário, bloquear uma linha imediata do humano quando permitido; na ausência dessas opções, sortear uma jogada válida. O assistente propôs sortear também entre opções da mesma prioridade. Sem pesos, busca de sequências futuras ou avaliação estratégica do setor para onde o humano será enviado. A referência a algo aleatório e básico foi entendida neste contexto, preservando as prioridades de conquistar e bloquear, e será apresentada para confirmação.

**Estrutura solicitada pelo usuário:** separar a estratégia de escolha das jogadas do restante do jogo, permitindo alterar e evoluir a IA depois. Desenvolver em uma branch própria da feature, após confirmação.

**Próximo passo autorizado agora:** guardar as ideias e apresentar o entendimento do escopo. O usuário reservou a confirmação para o próximo prompt; criar a branch e implementar devem aguardar essa confirmação.

## Perguntas para retomar

- Qual habilidade é mais interessante para a primeira fase experimental?
- O jogador pode antecipar ou reagir ao poder? Como?
- Os efeitos alteram apenas a informação/apresentação ou também as regras do motor?
- Qual é a consequência de falhar em cada desafio?
- Como testar dificuldade sem exigir a arte final e os cinco adversários prontos?

## Relações

As vidas e o elenco pertencem a [modo história](003-modo-historia.md). A aparência dos avisos e efeitos está em [identidade visual](001-identidade-visual.md).

## Confirmação posterior em 16/10/2026

O usuário autorizou desenvolver o escopo apresentado. A estratégia básica de conquistar, bloquear ou sortear foi implementada com contrato substituível, conforme [IDEIA-002](002-modo-livre-contra-maquina.md). Os níveis futuros, a antecipação e o sistema de pesos permanecem apenas possibilidades, sem implementação.

## Avaliação do usuário após jogar — 16/10/2026

A primeira máquina ficou fácil de vencer. O usuário considera improvável que o sorteio, sozinho, gere dificuldade consistente. Será necessário aumentar a força da máquina numa feature futura para oferecer um desafio real; o algoritmo e os níveis continuam por definir.

A versão básica foi considerada concluída e suficiente para esta primeira entrega. O usuário autorizou integrar à develop no GitHub e publicar como está, sem acrescentar dificuldade agora. O atraso de resposta escolhido nos testes foi de **0,7 segundo**.

## Decisão de 17/10/2026 — nível fácil

O usuário confirmou que a estratégia atual da máquina será o **nível fácil**: conquistar um pequeno quadrante, bloquear uma linha imediata do humano ou sortear entre jogadas válidas, conforme a implementação básica. Essa decisão define a classificação da estratégia existente; não significa que a interface já tenha seleção de dificuldade.

O comportamento do nível médio está em discussão e será apresentado ao usuário para conferir o entendimento antes de fechar suas regras. Os registros anteriores que tratavam todos os níveis como possibilidades foram substituídos por esta confirmação quanto ao nível fácil; os demais continuam em aberto.


## Decisão e implementação de 17/10/2026 — médio e seleção de dificuldade

**Confirmação do usuário:** o texto proposto para o médio corresponde ao que imaginou. Autorizou implementar em uma branch de dificuldade e atualizar os registros. A branch criada foi `feat/dificuldade`.

**Regras aprovadas:** manter conquistar um quadrante e bloquear uma vitória imediata acima da construção de linhas. Nas demais escolhas, favorecer conexões com as próprias peças em linhas ainda possíveis e reduzir a prioridade de uma posição que envie o humano a um quadrante onde possa conquistar imediatamente. Vitória direta, neste contexto, inclui conquistar o quadrante de destino, sem precisar vencer a partida inteira.

**Exemplo do usuário:** com uma peça na posição 7 do quadrante 7, considerar a posição 4 ao voltar a jogar nesse quadrante, construindo a linha 1–4–7. Essa opção deixa de ser preferível se enviar o humano ao quadrante 4 permitir uma conquista imediata. A posição 4 é um exemplo, não uma abertura obrigatória nem preferência fixa sobre outras conexões equivalentes.

**Implementado localmente:** estratégia `MediumMachineStrategy`, separada da estratégia fácil. Avalia o estado após cada jogada candidata, inclusive quando ela fecha o destino ou bloqueia uma ameaça no próprio destino. Destino fechado libera todos os quadrantes abertos; nesse caso, verifica se o humano pode conquistar em algum deles. Empates de avaliação são sorteados. Não faz busca profunda de sequências.

**Pesos iniciais escolhidos pelo assistente para concretizar a hierarquia:** vitória da partida +10000; conquista de quadrante +1000; bloqueio +100; destino que permite conquista humana −10; cada linha possível conectada a uma peça própria +1. Esses números são ajustes iniciais de implementação, não valores de balanceamento escolhidos pelo usuário. Conquistar e bloquear continuam acima da segurança de destino; entre alternativas da mesma prioridade, a segurança supera as conexões.

**Interface solicitada e implementada:** seleção na tela de nomes ao jogar contra o computador, com Fácil, Médio e Difícil. Fácil e Médio estão disponíveis; Difícil aparece desabilitado como “em breve”, pois sua lógica será definida depois. O nome do computador agora é editável. A revanche mantém nomes e dificuldade, e o nível aparece durante a partida.

**Futuro solicitado pelo usuário:**

- Definir e implementar o nível difícil em outra etapa; algoritmo e regras ainda em aberto.
- Planejar uma dificuldade impossível e adicioná-la posteriormente. Não aparece na interface atual, não tem algoritmo definido e o nome não garante invencibilidade.
- Considerar escolher Fácil, Médio ou Difícil também ao iniciar o modo história; ver IDEIA-003. É uma possibilidade futura, sem implementação da campanha nesta entrega.

A seleção e a lógica média foram implementadas no checkout local. A dificuldade prática ainda precisa da avaliação do usuário jogando; não há publicação ou integração desta entrega registrada aqui.


## Autorização de publicação em 17/10/2026

O usuário aceitou manter o design provisório do seletor e autorizou publicar Fácil e Médio no site existente para testar à distância e compartilhar com outras pessoas. Sua preferência futura é escolher a dificuldade por botões, a retomar após concluir a identidade visual (IDEIA-001). Difícil continua como “em breve” e Impossível fica para uma etapa futura.


**Publicação confirmada em 17/10/2026:** versão 4 do Sites publicada com sucesso em https://super-jogo-da-velha.airygrass64.chatgpt.site, mantendo acesso público. Fácil e Médio disponíveis para testes; Difícil permanece desabilitado. O checkout principal continua na branch `feat/dificuldade`; esta publicação não representa merge no GitHub.

## Reavaliação de 17/10/2026 — quatro níveis e balanceamento

**Observação do usuário:** o Fácil parece muito fácil e bastante aleatório; o Médio ainda parece fácil. Gostou da lógica de pesos, mas não considera o balanceamento confirmado. Pretende continuar jogando e passar o jogo para pessoas que não conhecem a lógica da IA.

**Proposta do usuário, ainda em avaliação:** organizar quatro níveis com diferenças perceptíveis: um fácil de jogar, um intermediário (“mais ou menos”), um difícil e um muito difícil, em que seria necessária uma partida excelente ou quase perfeita para vencer, preservando a possibilidade de vitória. Cogitou os nomes “Muito fácil / Fácil / Médio / Difícil”; quantidade, nomes finais e enquadramento das estratégias atuais não foram fechados.

**Relação com decisões anteriores:** o usuário antes havia definido a máquina básica como Fácil e proposto um Impossível futuro. Agora considera reclassificar os níveis, mas não confirmou renomeação. A intenção mais recente para o topo é ser muito difícil e vencível. O papel do nome Impossível fica em aberto; não inferir um quinto nível nem uma exigência de invencibilidade. Os rótulos e comportamentos publicados permanecem como estão.

**Hipótese levantada pelo usuário:** talvez uma máquina pudesse nunca perder por sua capacidade de analisar possibilidades. Isso não foi demonstrado para este jogo. A implementação atual usa regras e pontuação heurística, não probabilidades de vitória calculadas. “Partida perfeita” permanece uma referência de experiência, sem garantia técnica.

**Pedido atendido:** criado o [guia de dificuldades](../dificuldades/README.md), com funcionamento do Fácil, fórmula e exemplos exatos do Médio, limitações, caminhos sugeridos pelo assistente e uma ficha para observações durante os testes. Os valores atuais foram escolhidos pelo assistente para estabelecer prioridades; não resultam de balanceamento comprovado. Conquista e bloqueio superam a penalidade de destino, inclusive quando ceder uma conquista pode encerrar a partida para o humano.

**Escopo desta atualização:** documentação para leitura e reflexão. Manter o jogo atual enquanto o usuário e outras pessoas testam; novos pesos, algoritmos, nomes e níveis aguardam decisão. Sugestões de ajuste no guia não são requisitos aprovados.
