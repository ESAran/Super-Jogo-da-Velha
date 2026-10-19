# Dificuldades — guia para jogar, observar e ajustar

Atualizado em **17/10/2026**. Este documento descreve a lógica conferida em [machine.ts](../../src/game/machine.ts) e organiza propostas para avaliar durante os testes. O histórico das decisões está na [IDEIA-004](../ideias/004-habilidades-e-dificuldade.md).

## Onde estamos

No site, os níveis jogáveis continuam sendo **Fácil** e **Médio**. **Difícil** aparece como “em breve”. A versão publicada é a 4. Os nomes não são uma medida comprovada da força das estratégias.

O usuário achou o Fácil muito fácil e o Médio ainda fácil. Gostou do sistema de pesos, mas quer entender e testar seu equilíbrio antes de alterá-lo. Pretende pedir a pessoas que não conhecem a lógica da máquina para jogar também. A orientação atual é manter o jogo como está enquanto reunimos observações.

## A proposta de quatro níveis

A intenção do usuário é ter quatro experiências perceptivelmente diferentes:

| Faixa desejada | Sensação buscada | Relação possível com o que existe |
| --- | --- | --- |
| Entrada | Fácil de jogar e aprender | A estratégia básica atual pode ocupar essa faixa. |
| Intermediária | “Mais ou menos”: exige alguma atenção | A estratégia com pesos atual pode ser uma base, sujeita a testes. |
| Difícil | “Pô, esse é difícil”: exige planejamento | Ainda sem algoritmo definido. |
| Muito difícil | Exige uma partida excelente, idealmente quase perfeita, mas ainda permite vencer | Ainda sem algoritmo definido. |

**Nomes em avaliação:** o usuário cogitou “Muito fácil / Fácil / Médio / Difícil”. Também descreveu o topo como muito difícil. Não foi confirmada uma renomeação, nem a posição definitiva das duas estratégias existentes nessa escala.

A ideia anterior de um nível chamado **Impossível** continua no histórico, mas a nova intenção enfatiza um topo vencível. Falta decidir se “Impossível” seria apenas um nome desse quarto nível, se seria descartado ou se teria outro lugar. Não presumimos um quinto nível.

“Precisar de uma partida perfeita” é uma referência de experiência desejada, não uma garantia técnica. Ainda não definimos o que conta como erro tolerável, nem demonstramos que exista uma estratégia invencível para esta implementação. A máquina atual não calcula probabilidades de vitória: ela aplica regras e pontuações. A capacidade de examinar mais jogadas não demonstra, por si só, que um humano nunca poderá ganhar.

## Fácil atual: conquistar, bloquear ou sortear

A máquina lista somente as jogadas permitidas pelas regras e segue esta ordem:

1. Se puder completar uma linha e conquistar um quadrante, escolhe uma dessas jogadas.
2. Caso contrário, se puder ocupar a casa em que o humano completaria uma linha, escolhe um desses bloqueios.
3. Sem conquista ou bloqueio, sorteia entre todas as jogadas válidas.

Dentro de cada prioridade, empates são sorteados. Portanto, o Fácil tem bastante aleatoriedade, mas não é totalmente aleatório. Ele não avalia o destino entregue ao humano nem procura construir linhas nas demais jogadas. Também não diferencia uma conquista comum de uma que encerra a partida ao desempatar suas conquistas.

## Médio atual: como calcula cada jogada

Para cada jogada válida, soma:

| Critério | Valor | Quando entra |
| --- | ---: | --- |
| Vitória da partida | +10.000 | A jogada faz a máquina vencer o mapa principal. |
| Conquista | +1.000 | Completa uma linha no quadrante jogado. |
| Bloqueio | +100 | Ocupa uma casa que completaria uma linha humana naquele quadrante. |
| Destino perigoso | −10 | Após a jogada, o humano tem alguma conquista imediata disponível em seu destino permitido. |
| Conexões | +1 por linha | A casa pertence a uma linha com alguma peça própria e sem peças humanas, antes da jogada. |

```text
pontuação = 10000 × vitória_da_partida
          + 1000 × conquista
          +  100 × bloqueio
          −   10 × destino_perigoso
          +    1 × quantidade_de_linhas_conectadas
```

Os quatro primeiros indicadores valem 1 quando verdadeiros e 0 quando falsos. As conexões são contadas por linha, não por peça. Uma casa pode participar de até quatro linhas. Uma linha completada também pode contar como conexão; os bônus são cumulativos.

A máquina escolhe a maior pontuação. Se houver empate, sorteia entre as melhores. Esses valores não são porcentagens, chances de vitória nem pesos aprendidos com partidas: foram escolhidos pelo assistente como ponto de partida para implementar as prioridades aprovadas.

### Como verifica o destino

A posição escolhida determina o quadrante em que o humano deverá jogar. A máquina examina o tabuleiro **depois de sua própria jogada**, incluindo uma ameaça que ela acabou de bloquear ou um quadrante que acabou de fechar.

Se o destino estiver fechado, o humano pode jogar em qualquer quadrante aberto. Nesse caso, basta existir uma conquista humana imediata em algum deles para aplicar −10. A penalidade entra uma vez, independentemente de haver uma ou várias ameaças. Se a jogada já vence a partida para a máquina, não há penalidade de destino.

### Exemplo da peça na posição 7

Usamos aqui posições de 1 a 9, como na conversa; o código usa índices de 0 a 8.

A máquina já tem uma peça na posição 7 do quadrante 7. Jogar na posição 4 pode construir a linha 1–4–7. Supondo que não haja conquista, bloqueio ou outra conexão:

| Alternativa | Cálculo | Resultado |
| --- | --- | ---: |
| Posição 4 conecta e envia para um quadrante 4 seguro | +1 | 1 |
| Posição 4 conecta, mas permite conquista humana no quadrante 4 | +1 −10 | −9 |
| Outra posição conecta uma linha e tem destino seguro | +1 | 1 |
| Uma posição sem conexão, mas com destino seguro | 0 | 0 |

Uma jogada segura sem conexão vence uma conexão perigosa: 0 é maior que −9. A posição 4 não tem preferência fixa; outras conexões equivalentes empatam com ela.

### Exemplo que explica uma fragilidade atual

Suponha que conquistar um quadrante também complete uma linha própria, mas envie o humano para uma conquista imediata:

```text
Conquistar e entregar oportunidade: 1000 + 1 − 10 = 991
Apenas conectar com segurança:         0 + 1      =   1
```

A máquina escolhe conquistar. O mesmo princípio vale para bloqueios: o bônus de +100 supera a penalidade de −10.

Isso implementa a ordem **vencer a partida → conquistar → bloquear → evitar destino perigoso → conectar**. Na prática, os pesos estão tão separados que funcionam principalmente como prioridades, não como uma troca equilibrada entre benefícios e riscos.

## O que pode estar deixando o Médio fácil

Estas são análises do assistente a partir do código, não conclusões dos testes com jogadores:

- Entregar ao humano o quadrante que vence a partida recebe a mesma penalidade de −10 que entregar qualquer conquista comum. Não há um critério específico para impedir derrota da partida.
- Conquistar ou bloquear supera evitar um destino perigoso. A máquina pode ganhar algo local e entregar uma oportunidade mais importante.
- O bloqueio vale +100 mesmo quando aquela ameaça não seria acessível ao humano no próximo turno. O valor do bloqueio não considera essa urgência.
- Conexões contam linhas possíveis, mas não avaliam a probabilidade de voltar ao quadrante e completá-las.
- Não há busca por sequências de várias jogadas nem avaliação explícita de armadilhas e controle de destinos futuros.
- Muitas opções podem empatar; nesses casos, a decisão permanece aleatória. Em um tabuleiro vazio, por exemplo, todos os critérios pontuam zero.

Os testes automatizados verificam regras e comportamentos esperados. Eles não comprovam que o nível seja desafiador para pessoas.

## Caminhos para discutir depois

**Sugestões do assistente; nenhuma alteração aprovada nesta etapa:**

| Possível ajuste | O que buscaria melhorar | O que observar |
| --- | --- | --- |
| Distinguir perder a partida de ceder um quadrante | Evitar derrotas imediatas previsíveis | A máquina deixa de entregar o quadrante decisivo? |
| Rever a relação entre conquista, bloqueio e destino | Permitir que segurança supere um ganho local quando necessário | Ela troca conquistas de maneira mais sensata? |
| Avaliar a importância dos quadrantes no mapa principal | Relacionar decisões locais ao objetivo da partida | Ela disputa os quadrantes que realmente importam? |
| Antecipar algumas respostas e continuações | Reconhecer consequências além do próximo turno | A força aumenta sem deixar a resposta lenta? |
| Regular a escolha entre alternativas boas | Diferenciar níveis e preservar variedade | O nível fica vencível sem parecer que entrega a partida? |

Apenas multiplicar todos os pesos pelo mesmo número positivo mantém a ordem das pontuações e não muda a escolha. Precisamos mudar proporções ou critérios. Mesmo mudar um peso isolado pode não alterar decisões se ele continuar abaixo da prioridade seguinte.

Ainda não escolhemos novos pesos, profundidade de busca, taxas de erro ou metas de vitória. O topo vencível pode ser estudado com essas ferramentas, mas seu comportamento precisa de testes; não há promessa de vitória disponível em toda posição.

## Ficha para consultar durante os testes

Sugestão de registro manual, sem coleta automática implementada:

| Campo | Anotação |
| --- | --- |
| Nível e versão | Fácil ou Médio; versão 4 como referência inicial |
| Experiência da pessoa | Primeira vez / algumas partidas / já conhece bem |
| Conhecia a lógica da IA? | Sim / não |
| Resultado e duração aproximada | Vitória / derrota / empate; tempo |
| Sensação de dificuldade | Muito fácil / fácil / equilibrado / difícil / muito difícil |
| Momento marcante | Quadrante, posição, destino e peças relevantes; captura se possível |
| O que a máquina fez | Conquistou, bloqueou, conectou ou pareceu escolher ao acaso |
| O que parecia melhor | Alternativa que o jogador esperava e motivo |

Ao revisar uma jogada, perguntar: ela conquistou algo, mas entregou a partida? Bloqueou uma ameaça sem urgência? Deixou passar uma conexão? Havia duas opções equivalentes? O humano já havia criado uma situação sem saída?

Para comparar mudanças futuras, sugerimos mudar um critério por vez e guardar as posições que motivaram o ajuste. Vitórias e derrotas de várias pessoas ajudam, mas também importa entender **como** a máquina perdeu e se o desafio parece justo.

## Decisões pendentes

- Confirmar se serão quatro níveis e quais serão seus nomes.
- Decidir onde entram as duas estratégias existentes, após os testes.
- Definir o papel do antigo nome “Impossível” diante da intenção de um topo vencível.
- Escolher quais falhas corrigir primeiro e quais pesos revisar.
- Definir o grau de planejamento e de erro aceitável em cada nível.
- Retomar como a dificuldade se relaciona com poderes e campanha.

Por enquanto, mantemos a lógica, os nomes e o seletor publicados. A preferência por botões fica para a revisão da identidade visual.
