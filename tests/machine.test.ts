import assert from "node:assert/strict";
import { it } from "node:test";
import { GameEngine, Player } from "../src/game/engine";
import { BasicMachineStrategy, MediumMachineStrategy } from "../src/game/machine";
import { GameApp } from "../src/ui/app";

function game() {
  const game = new GameEngine(new Player("Pessoa", "X"), new Player("Computador", "O", "machine"));
  game.currentPlayer = game.playerTwo;
  return game;
}

it("prioriza conquistar sobre bloquear e nao altera o tabuleiro ao escolher", () => {
  const g = game();
  g.board.place(0, 0, "O"); g.board.place(0, 1, "O");
  g.board.place(1, 0, "X"); g.board.place(1, 1, "X");
  assert.deepEqual(new BasicMachineStrategy(() => 0).chooseMove(g), { mini: 0, cell: 2 });
  assert.equal(g.board.getMini(0).getCell(2), null);
});

it("bloqueia uma linha imediata, respeitando o setor obrigatorio", () => {
  const g = game();
  g.board.place(0, 0, "O"); g.board.place(0, 1, "O");
  g.board.place(1, 0, "X"); g.board.place(1, 1, "X");
  g.requiredMini = 1;
  assert.deepEqual(new BasicMachineStrategy(() => 0).chooseMove(g), { mini: 1, cell: 2 });
});

it("sorteia entre opcoes da mesma prioridade e entre casas livres", () => {
  const g = game();
  assert.deepEqual(new BasicMachineStrategy(() => 0).chooseMove(g), { mini: 0, cell: 0 });
  assert.deepEqual(new BasicMachineStrategy(() => 0.999).chooseMove(g), { mini: 8, cell: 8 });
  for (const mini of [0, 1]) {
    g.board.place(mini, 0, "O"); g.board.place(mini, 1, "O");
  }
  assert.deepEqual(new BasicMachineStrategy(() => 0.999).chooseMove(g), { mini: 1, cell: 2 });
});

it("libera a rota quando o destino fecha e nunca escolhe setores fechados", () => {
  const g = game();
  for (const cell of [0, 1, 2]) g.board.place(0, cell, "X");
  g.requiredMini = 0;
  assert.deepEqual(new BasicMachineStrategy(() => 0).chooseMove(g), { mini: 1, cell: 0 });
  g.finished = true;
  assert.equal(new BasicMachineStrategy().chooseMove(g), null);
});

it("conclui partidas inteiras com jogadas validas", () => {
  const bot = new BasicMachineStrategy();
  for (let match = 0; match < 50; match += 1) {
    const g = game();
    let turns = 0;
    while (!g.finished) {
      const move = bot.chooseMove(g)!;
      assert.ok(move && g.isMoveValid(move.mini, move.cell));
      g.play(move.mini, move.cell);
      assert.ok(++turns <= 81);
    }
    assert.equal(bot.chooseMove(g), null);
  }
});

function app(machine = true) {
  const app = new GameApp({ innerHTML: "", addEventListener() {} } as unknown as HTMLElement,
    new BasicMachineStrategy(() => 0));
  app["audio"].toggle();
  app["machineMode"] = machine;
  const data = new FormData();
  for (const [key, value] of Object.entries({ "player-one": "Pessoa", "symbol-one": "X", "player-two": "Outra", "symbol-two": "O" })) data.set(key, value);
  app["startMatch"](data);
  return app;
}
function play(app: GameApp, mini: number, cell: number) {
  app["playCell"]({ dataset: { mini: String(mini), cell: String(cell) } } as unknown as HTMLButtonElement);
}

it("responde automaticamente uma vez, bloqueia cliques e nao duplica ao renderizar", (t) => {
  t.mock.timers.enable({ apis: ["setTimeout"] });
  const a = app();
  play(a, 0, 4);
  assert.equal(a["isMachineTurn"](), true);
  assert.match(a["renderGame"](), /MAQUINA ESCOLHENDO/);
  assert.doesNotMatch(a["renderMiniBoard"](4), /type="button"[\s\S]*?aria-label="[^"]*"\s*>/);
  play(a, 4, 8);
  assert.equal(a["game"]!.board.getMini(4).getCell(8), null);
  a["render"]();
  t.mock.timers.tick(700);
  assert.equal(a["game"]!.board.getMini(4).getCell(0), "O");
  assert.equal(a["isMachineTurn"](), false);
  assert.equal(a["machineTimer"], null);
});

it("cancela respostas ao reiniciar ou sair e preserva a maquina na revanche", (t) => {
  t.mock.timers.enable({ apis: ["setTimeout"] });
  const a = app();
  play(a, 0, 4);
  a["restartMatch"]();
  t.mock.timers.tick(700);
  assert.equal(a["game"]!.playerTwo.kind, "machine");
  assert.ok(a["game"]!.board.getMiniBoards().every((b) => b.getCells().every((c) => c === null)));
  play(a, 0, 4);
  a["handleAction"]({ dataset: { action: "menu" } } as unknown as HTMLButtonElement);
  t.mock.timers.tick(700);
  assert.equal(a["game"], null);
  assert.equal(a["machineTimer"], null);
});

it("mantem dois humanos no modo local e nao agenda respostas", () => {
  const a = app(false);
  play(a, 0, 4);
  assert.equal(a["game"]!.playerTwo.kind, "human");
  assert.equal(a["machineTimer"], null);
  play(a, 4, 0);
  assert.equal(a["game"]!.currentPlayer, a["game"]!.playerOne);
});

it("encerra uma vitoria da maquina sem agendar outra jogada ou contar vitoria humana", (t) => {
  t.mock.timers.enable({ apis: ["setTimeout"] });
  const a = app();
  const g = a["game"]!;
  for (const mini of [0, 1]) for (const cell of [0, 1, 2]) g.board.place(mini, cell, "O");
  g.board.place(2, 0, "O"); g.board.place(2, 1, "O");
  play(a, 3, 2);
  t.mock.timers.tick(700);
  assert.equal(g.winner, g.playerTwo);
  assert.equal(a["totalWins"], 0);
  assert.equal(a["matchSaved"], true);
  assert.equal(a["machineTimer"], null);
});


it("medio conecta a peca 7 com a posicao 4 e evita destino com conquista humana", () => {
  const g = game();
  g.requiredMini = 6;
  g.board.place(6, 6, "O");
  const bot = new MediumMachineStrategy(() => 0);
  assert.deepEqual(bot.chooseMove(g), { mini: 6, cell: 0 });
  // Bloqueia a diagonal para isolar a conexao vertical 1–4–7.
  g.board.place(6, 2, "X");
  g.board.place(0, 0, "X"); g.board.place(0, 1, "X");
  assert.deepEqual(bot.chooseMove(g), { mini: 6, cell: 3 });
  g.board.place(3, 0, "X"); g.board.place(3, 1, "X");
  const before = JSON.stringify(g.board);
  const move = bot.chooseMove(g)!;
  assert.notEqual(move.cell, 3);
  assert.notEqual(move.cell, 0);
  assert.equal(JSON.stringify(g.board), before);
});

it("medio prioriza conquistar e bloquear antes de construir conexoes", () => {
  const g = game();
  g.requiredMini = 6;
  g.board.place(6, 0, "X"); g.board.place(6, 1, "X");
  g.board.place(6, 6, "O");
  const bot = new MediumMachineStrategy(() => 0);
  assert.deepEqual(bot.chooseMove(g), { mini: 6, cell: 2 });
  g.board.place(6, 7, "O");
  assert.deepEqual(bot.chooseMove(g), { mini: 6, cell: 8 });
});

it("medio avalia escolha livre quando envia a um quadrante fechado", () => {
  const g = game();
  g.requiredMini = 6;
  for (const cell of [0, 1, 2]) g.board.place(0, cell, "O");
  g.board.place(3, 0, "X"); g.board.place(3, 1, "X");
  const move = new MediumMachineStrategy(() => 0).chooseMove(g)!;
  assert.notEqual(move.cell, 0);
  assert.notEqual(move.cell, 3);
});

it("medio simula o proprio destino apos bloquear a linha humana", () => {
  const g = game();
  g.requiredMini = 2;
  g.board.place(2, 0, "X"); g.board.place(2, 1, "X");
  assert.deepEqual(new MediumMachineStrategy(() => 0).chooseMove(g), { mini: 2, cell: 2 });
});

it("medio joga partidas completas validas contra facil", () => {
  const medium = new MediumMachineStrategy();
  const easy = new BasicMachineStrategy();
  for (let match = 0; match < 20; match += 1) {
    const g = game();
    let turns = 0;
    while (!g.finished) {
      const bot = g.currentPlayer === g.playerTwo ? medium : easy;
      const move = bot.chooseMove(g)!;
      assert.ok(move && g.isMoveValid(move.mini, move.cell));
      g.play(move.mini, move.cell);
      assert.ok(++turns <= 81);
    }
    assert.equal(medium.chooseMove(g), null);
  }
});

it("seleciona medio, usa sua estrategia e preserva dificuldade e nomes na revanche", (t) => {
  t.mock.timers.enable({ apis: ["setTimeout"] });
  const a = app();
  const data = new FormData();
  data.set("player-one", "Pessoa"); data.set("player-two", "Robo"); data.set("difficulty", "medium");
  a["startMatch"](data);
  const choose = t.mock.method(a["mediumStrategy"], "chooseMove");
  play(a, 0, 4);
  t.mock.timers.tick(700);
  assert.equal(choose.mock.callCount(), 1);
  a["restartMatch"]();
  assert.equal(a["difficulty"], "medium");
  assert.equal(a["game"]!.playerTwo.name, "Robo");
  assert.match(a["renderSetup"](), /value="medium" selected/);
  assert.match(a["renderSetup"](), /value="hard" disabled/);
  a["machineMode"] = false;
  assert.doesNotMatch(a["renderSetup"](), /name="difficulty"/);
});
