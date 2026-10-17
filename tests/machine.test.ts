import assert from "node:assert/strict";
import { it } from "node:test";
import { GameEngine, Player } from "../src/game/engine";
import { BasicMachineStrategy } from "../src/game/machine";
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
