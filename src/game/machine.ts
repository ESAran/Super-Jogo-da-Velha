import { WINNING_LINES } from "./board";
import { GameEngine } from "./engine";

export interface Move {
  mini: number;
  cell: number;
}

// Estrategias futuras podem implementar este contrato sem alterar a interface.
export interface MachineStrategy {
  chooseMove(game: GameEngine): Move | null;
}

export class BasicMachineStrategy implements MachineStrategy {
  constructor(private readonly random: () => number = Math.random) {}

  chooseMove(game: GameEngine): Move | null {
    const moves: Move[] = [];
    for (let mini = 0; mini < 9; mini += 1) {
      for (let cell = 0; cell < 9; cell += 1) {
        if (game.isMoveValid(mini, cell)) moves.push({ mini, cell });
      }
    }
    if (moves.length === 0) return null;

    const completesLine = (move: Move, symbol: string): boolean => {
      const cells = game.board.getMini(move.mini).getCells();
      return WINNING_LINES.some((line) => line.includes(move.cell) &&
        line.every((cell) => cell === move.cell || cells[cell] === symbol));
    };
    const opponent = game.currentPlayer === game.playerOne ? game.playerTwo : game.playerOne;
    const wins = moves.filter((move) => completesLine(move, game.currentPlayer.symbol));
    const blocks = moves.filter((move) => completesLine(move, opponent.symbol));
    const candidates = wins.length > 0 ? wins : blocks.length > 0 ? blocks : moves;
    return candidates[Math.floor(this.random() * candidates.length)];
  }
}

export type MachineDifficulty = "easy" | "medium";

// Pesos separados: conquistar > bloquear > evitar entregar conquista > conectar.
const MEDIUM_WEIGHTS = { win: 1000, block: 100, unsafeDestination: -10, connection: 1 };

export class MediumMachineStrategy implements MachineStrategy {
  constructor(private readonly random: () => number = Math.random) {}

  chooseMove(game: GameEngine): Move | null {
    const own = game.currentPlayer.symbol;
    const opponent = game.currentPlayer === game.playerOne ? game.playerTwo.symbol : game.playerOne.symbol;
    const boards = game.board.getMiniBoards().map((board) => [...board.getCells()]);
    const hasLine = (cells: readonly (string | null)[], symbol: string) =>
      WINNING_LINES.some((line) => line.every((cell) => cells[cell] === symbol));
    const completes = (cells: readonly (string | null)[], cell: number, symbol: string) =>
      WINNING_LINES.some((line) => line.includes(cell) &&
        line.every((index) => index === cell || cells[index] === symbol));
    let bestScore = -Infinity;
    let candidates: Move[] = [];

    for (let mini = 0; mini < 9; mini += 1) {
      for (let cell = 0; cell < 9; cell += 1) {
        if (!game.isMoveValid(mini, cell)) continue;
        const before = boards[mini];
        const wins = completes(before, cell, own);
        const blocks = completes(before, cell, opponent);
        const connections = WINNING_LINES.filter((line) => line.includes(cell) &&
          line.every((index) => before[index] !== opponent) &&
          line.some((index) => before[index] === own)).length;
        const after = boards.map((cells, index) => index === mini
          ? cells.map((value, index) => index === cell ? own : value) : cells);
        const closed = (index: number) => hasLine(after[index], own) ||
          hasLine(after[index], opponent) || after[index].every((value) => value !== null);
        // Um destino fechado libera todos os quadrantes abertos para o humano.
        const destinations = closed(cell) ? after.map((_, index) => index).filter((index) => !closed(index)) : [cell];
        const macro = [...game.board.getMacroCells()];
        if (wins) macro[mini] = own;
        const gameWon = hasLine(macro, own);
        const unsafe = !gameWon && destinations.some((index) => after[index].some((value, target) =>
          value === null && completes(after[index], target, opponent)));
        const score = (gameWon ? 10000 : 0) + (wins ? MEDIUM_WEIGHTS.win : 0) +
          (blocks ? MEDIUM_WEIGHTS.block : 0) + (unsafe ? MEDIUM_WEIGHTS.unsafeDestination : 0) +
          connections * MEDIUM_WEIGHTS.connection;
        if (score > bestScore) {
          bestScore = score;
          candidates = [{ mini, cell }];
        } else if (score === bestScore) candidates.push({ mini, cell });
      }
    }
    return candidates.length ? candidates[Math.floor(this.random() * candidates.length)] : null;
  }
}
