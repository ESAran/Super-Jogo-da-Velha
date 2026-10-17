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
