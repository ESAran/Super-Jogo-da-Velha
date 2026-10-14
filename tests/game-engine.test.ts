import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { Board, MiniBoard } from "../src/game/board";
import { GameEngine, Player } from "../src/game/engine";
import { GameRules } from "../src/game/rules";

describe("MiniBoard", () => {
  it("registra uma jogada e detecta vitoria", () => {
    const mini = new MiniBoard();
    mini.place(0, "X");
    mini.place(1, "X");
    mini.place(2, "X");

    assert.equal(mini.getWinner(), "X");
    assert.equal(mini.isClosed(), true);
  });

  it("rejeita celula ocupada", () => {
    const mini = new MiniBoard();
    mini.place(4, "X");

    assert.throws(() => mini.place(4, "O"), /ocupada/u);
  });
});

describe("Board", () => {
  it("atualiza o mapa principal quando um setor e vencido", () => {
    const board = new Board();
    board.place(4, 0, "O");
    board.place(4, 1, "O");
    board.place(4, 2, "O");

    assert.equal(board.getMacroCells()[4], "O");
  });

  it("detecta vitoria no mapa principal", () => {
    const board = new Board();

    for (const mini of [0, 1, 2]) {
      board.place(mini, 0, "X");
      board.place(mini, 1, "X");
      board.place(mini, 2, "X");
    }

    assert.equal(board.getWinner(), "X");
  });
});

describe("GameRules", () => {
  it("obriga a proxima jogada no setor definido pela celula", () => {
    const rules = new GameRules();
    const board = new Board();

    assert.equal(rules.nextRequiredMini(7), 7);
    assert.equal(rules.isMoveValid(board, 7, 0, 7), true);
    assert.equal(rules.isMoveValid(board, 6, 0, 7), false);
  });
});

describe("GameEngine", () => {
  it("executa uma jogada e troca o jogador", () => {
    const alice = new Player("Alice", "X");
    const bruno = new Player("Bruno", "O");
    const game = new GameEngine(alice, bruno);

    const result = game.play(0, 5);

    assert.equal(game.board.getMini(0).getCell(5), "X");
    assert.equal(game.currentPlayer, bruno);
    assert.equal(result.nextRequiredMini, 5);
  });

  it("rejeita uma jogada fora do setor obrigatorio", () => {
    const game = new GameEngine(new Player("Alice", "X"), new Player("Bruno", "O"));
    game.play(0, 0);

    assert.throws(() => game.play(1, 0), /invalida/u);
  });

  it("valida nomes e simbolos dos jogadores", () => {
    assert.throws(() => new Player("", "X"), /nome/u);
    assert.throws(() => new Player("Alice", "10"), /exatamente/u);
    assert.throws(() => new Player("Alice", "1"), /numero/u);
  });
});
