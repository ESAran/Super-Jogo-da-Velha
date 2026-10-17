import assert from "node:assert/strict";
import { afterEach, beforeEach, describe, it } from "node:test";
import { GameApp } from "../src/ui/app";

// Testa o estado e o HTML sem adicionar uma dependencia de DOM ao projeto.
function createApp(): GameApp {
  const root = { innerHTML: "", addEventListener() {} };
  const app = new GameApp(root as unknown as HTMLElement);
  app["audio"].toggle();
  return app;
}

function startMatch(app: GameApp, first: string, second: string): void {
  const data = new FormData();
  data.set("player-one", first);
  data.set("player-two", second);
  data.set("symbol-one", "X");
  data.set("symbol-two", "O");
  app["startMatch"](data);
}

function finishMatch(app: GameApp, won = true): void {
  startMatch(app, "Godric", "Salazar");
  const game = app["game"]!;
  game.finished = true;
  game.winner = won ? game.playerOne : null;
  game.draw = !won;
  app["saveCurrentMatch"]();
}

// Prepara um tabuleiro sem vencedor; a ultima jogada passa pelo motor real.
function prepareBombonera(
  app: GameApp,
  first = "Vasco",
  second = "Boca",
  winnerIndex = 0,
  winnerQuadrants = 3,
  opponentQuadrants = 4,
): void {
  startMatch(app, first, second);
  const game = app["game"]!;
  const winner = winnerIndex === 0 ? game.playerOne : game.playerTwo;
  const opponent = winnerIndex === 0 ? game.playerTwo : game.playerOne;
  for (const mini of [0, 1, 8].slice(0, winnerQuadrants - 1)) {
    for (const cell of [0, 1, 2]) game.board.place(mini, cell, winner.symbol);
  }
  for (const mini of [3, 4, 6, 7].slice(0, opponentQuadrants)) {
    for (const cell of [0, 1, 2]) game.board.place(mini, cell, opponent.symbol);
  }
  game.board.place(2, 0, winner.symbol);
  game.board.place(2, 1, winner.symbol);
  game.currentPlayer = winner;
  assert.equal(game.board.getWinner(), null);
}

function playWinningMove(app: GameApp): void {
  app["playCell"]({ dataset: { mini: "2", cell: "2" } } as unknown as HTMLButtonElement);
  assert.equal(app["game"]!.finished, true);
}

describe("Conquistas", () => {
  const originalStorage = Object.getOwnPropertyDescriptor(globalThis, "localStorage");

  beforeEach(() => {
    const values = new Map<string, string>();
    Object.defineProperty(globalThis, "localStorage", {
      configurable: true,
      value: {
        getItem: (key: string) => values.get(key) ?? null,
        setItem: (key: string, value: string) => values.set(key, value),
      },
    });
  });

  afterEach(() => {
    if (originalStorage) {
      Object.defineProperty(globalThis, "localStorage", originalStorage);
    } else {
      Reflect.deleteProperty(globalThis, "localStorage");
    }
  });

  it("oculta nomes e instrucoes antes de desbloquear", () => {
    const html = createApp()["renderAchievements"]();
    assert.equal((html.match(/CONQUISTA SECRETA/g) ?? []).length, 3);
    assert.doesNotMatch(html, /Heisenberg|valdemort|Say my name|AQUELE QUE|Vasco|Boca|quadrantes/u);
  });

  for (const [name, title] of [
    ["Heisenberg", "Say my name."],
    ["valdemort", "AQUELE QUE NÃO DEVE SER NOMEADO"],
  ]) {
    for (const position of [0, 1]) {
      it(`desbloqueia ${name} no jogador ${position + 1} e persiste`, () => {
        const names = ["Godric", "Salazar"];
        names[position] = `  ${name.toUpperCase()}  `;
        const app = createApp();
        startMatch(app, names[0], names[1]);
        assert.ok(app["renderAchievements"]().includes(title));
        assert.ok(app["notice"].includes(title));
        assert.ok(createApp()["renderAchievements"]().includes(title));
      });
    }
  }

  it("anuncia as duas conquistas quando desbloqueadas juntas", () => {
    const app = createApp();
    startMatch(app, "Heisenberg", "valdemort");
    assert.match(app["notice"], /Say my name\./u);
    assert.match(app["notice"], /AQUELE QUE NÃO DEVE SER NOMEADO/u);
    assert.equal((app["renderAchievements"]().match(/CONQUISTA SECRETA/g) ?? []).length, 1);
  });

  it("nao desbloqueia nomes parecidos nem partidas invalidas", () => {
    const app = createApp();
    startMatch(app, "Heisenberg2", "valdemort2");
    assert.doesNotMatch(app["renderAchievements"](), /Say my name|AQUELE QUE/u);
    startMatch(app, "", "valdemort");
    assert.doesNotMatch(app["renderAchievements"](), /AQUELE QUE/u);
  });

  it("mantem o desbloqueio na sessao quando o armazenamento esta bloqueado", () => {
    Object.defineProperty(globalThis, "localStorage", {
      configurable: true,
      get() { throw new Error("Armazenamento bloqueado"); },
    });
    const app = createApp();
    startMatch(app, "Heisenberg", "valdemort");
    assert.equal((app["renderAchievements"]().match(/CONQUISTA SECRETA/g) ?? []).length, 1);
  });

  it("mantem Godric e Salazar como nomes iniciais", () => {
    const html = createApp()["renderSetup"]();
    assert.match(html, /value="Godric"/u);
    assert.match(html, /value="Salazar"/u);
  });

  it("libera LIÃO! apenas na decima vitoria e nao conta a mesma partida duas vezes", () => {
    const app = createApp();
    for (let index = 0; index < 9; index += 1) finishMatch(app);
    assert.equal(app["tenWinsUnlocked"], false);
    assert.equal(app["totalWins"], 9);
    app["saveCurrentMatch"]();
    assert.equal(app["totalWins"], 9);
    finishMatch(app);
    assert.equal(app["tenWinsUnlocked"], true);
    assert.match(app["notice"], /CONQUISTA LIBERADA \/\/ LIÃO!/u);
    assert.equal(createApp()["tenWinsUnlocked"], true);
  });

  it("ignora empates e partidas em andamento", () => {
    const app = createApp();
    for (let index = 0; index < 10; index += 1) finishMatch(app, false);
    startMatch(app, "Godric", "Salazar");
    app["saveCurrentMatch"]();
    assert.equal(app["totalWins"], 0);
    assert.equal(app["tenWinsUnlocked"], false);
  });

  it("preserva progresso e desbloqueio alem das ultimas 20 partidas", () => {
    const app = createApp();
    for (let index = 0; index < 9; index += 1) finishMatch(app);
    for (let index = 0; index < 21; index += 1) finishMatch(app, false);
    const restored = createApp();
    assert.equal(restored["totalWins"], 9);
    finishMatch(restored);
    for (let index = 0; index < 21; index += 1) finishMatch(restored, false);
    assert.equal(restored["readHistory"]().length, 20);
    assert.equal(createApp()["tenWinsUnlocked"], true);
  });

  it("aproveita vitorias do historico anterior sem somar novamente a cada abertura", () => {
    localStorage.setItem("sjv84.history.v1", JSON.stringify([
      ...Array.from({ length: 9 }, () => ({ winner: "Godric" })),
      { winner: null },
    ]));
    const app = createApp();
    assert.equal(app["totalWins"], 9);
    finishMatch(app);
    assert.equal(createApp()["totalWins"], 10);
    assert.equal(createApp()["totalWins"], 10);
  });

  it("conta vitorias na sessao mesmo sem acesso ao armazenamento", () => {
    Object.defineProperty(globalThis, "localStorage", {
      configurable: true,
      get() { throw new Error("Armazenamento bloqueado"); },
    });
    const app = createApp();
    for (let index = 0; index < 10; index += 1) finishMatch(app);
    assert.equal(app["tenWinsUnlocked"], true);
  });

  for (const winnerIndex of [0, 1]) {
    it(`libera Vasco na Bombonera com Vasco no jogador ${winnerIndex + 1} e persiste`, () => {
      const app = createApp();
      const names = winnerIndex === 0 ? ["  VASCO  ", "bOcA"] : ["bOcA", "  VASCO  "];
      prepareBombonera(app, names[0], names[1], winnerIndex);
      assert.equal(app["bomboneraUnlocked"], false);
      playWinningMove(app);
      assert.equal(app["bomboneraUnlocked"], true);
      assert.match(app["notice"], /Vasco na Bombonera/u);
      assert.match(app["renderAchievements"](), /Vasco na Bombonera/u);
      assert.equal(createApp()["bomboneraUnlocked"], true);
    });
  }

  for (const [winnerCount, opponentCount] of [[3, 3], [4, 3]]) {
    it(`nao libera com ${winnerCount} quadrantes contra ${opponentCount}`, () => {
      const app = createApp();
      prepareBombonera(app, "Vasco", "Boca", 0, winnerCount, opponentCount);
      playWinningMove(app);
      assert.equal(app["bomboneraUnlocked"], false);
    });
  }

  for (const [first, second] of [["Boca", "Vasco"], ["Vasco2", "Boca"], ["Vasco", "Boca2"]]) {
    it(`nao libera quando ${first} vence ${second}`, () => {
      const app = createApp();
      prepareBombonera(app, first, second);
      playWinningMove(app);
      assert.equal(app["bomboneraUnlocked"], false);
    });
  }

  it("nao libera apenas pelos nomes, em partida aberta ou empate", () => {
    const app = createApp();
    prepareBombonera(app);
    app["saveCurrentMatch"]();
    assert.equal(app["bomboneraUnlocked"], false);
    app["game"]!.finished = true;
    app["game"]!.draw = true;
    app["saveCurrentMatch"]();
    assert.equal(app["bomboneraUnlocked"], false);
  });

  it("anuncia LIÃO! e Vasco na Bombonera na mesma vitoria sem duplicar progresso", () => {
    localStorage.setItem("sjv84.total-wins.v1", "9");
    const app = createApp();
    prepareBombonera(app);
    playWinningMove(app);
    assert.match(app["notice"], /LIÃO! \/\/ Vasco na Bombonera/u);
    app["saveCurrentMatch"]();
    assert.equal(app["totalWins"], 10);
  });

  it("mantem Vasco na Bombonera na sessao sem armazenamento", () => {
    Object.defineProperty(globalThis, "localStorage", {
      configurable: true,
      get() { throw new Error("Armazenamento bloqueado"); },
    });
    const app = createApp();
    prepareBombonera(app);
    playWinningMove(app);
    assert.equal(app["bomboneraUnlocked"], true);
  });
});
