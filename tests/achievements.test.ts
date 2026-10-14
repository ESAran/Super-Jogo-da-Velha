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
    assert.equal((html.match(/CONQUISTA SECRETA/g) ?? []).length, 2);
    assert.doesNotMatch(html, /Heisenberg|valdemort|Say my name|AQUELE QUE/u);
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
    assert.doesNotMatch(app["renderAchievements"](), /CONQUISTA SECRETA/u);
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
    assert.doesNotMatch(app["renderAchievements"](), /CONQUISTA SECRETA/u);
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
});
