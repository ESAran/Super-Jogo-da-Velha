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

describe("Conquistas secretas", () => {
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
});
