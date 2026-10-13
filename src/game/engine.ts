import { Board } from "./board";
import { GameRules } from "./rules";

export type PlayerKind = "human" | "machine";

export class Player {
  readonly name: string;
  readonly symbol: string;
  readonly kind: PlayerKind;

  constructor(name: string, symbol: string, kind: PlayerKind = "human") {
    this.name = name.trim();
    this.symbol = symbol.trim().toUpperCase();
    this.kind = kind;

    if (this.name.length === 0) {
      throw new Error("O nome do jogador nao pode ser vazio.");
    }

    if ([...this.symbol].length !== 1) {
      throw new Error("O simbolo deve ter exatamente um caractere.");
    }

    if (/^\d$/u.test(this.symbol)) {
      throw new Error("O simbolo do jogador nao pode ser um numero.");
    }
  }
}
export interface MoveResult {
  miniWon: boolean;
  gameWon: boolean;
  draw: boolean;
  nextRequiredMini: number | null;
}

export class GameEngine {
  readonly board = new Board();
  readonly rules = new GameRules();
  readonly playerOne: Player;
  readonly playerTwo: Player;

  currentPlayer: Player;
  requiredMini: number | null = null;
  winner: Player | null = null;
  finished = false;
  draw = false;

  constructor(playerOne: Player, playerTwo: Player) {
    if (playerOne.symbol === playerTwo.symbol) {
      throw new Error("Os jogadores devem usar simbolos diferentes.");
    }

    this.playerOne = playerOne;
    this.playerTwo = playerTwo;
    this.currentPlayer = playerOne;
  }

  isMoveValid(miniIndex: number, cellIndex: number): boolean {
    return (
      !this.finished &&
      this.rules.isMoveValid(this.board, miniIndex, cellIndex, this.requiredMini)
    );
  }

  play(miniIndex: number, cellIndex: number): MoveResult {
    if (this.finished) {
      throw new Error("A partida ja foi encerrada.");
    }

    if (!this.isMoveValid(miniIndex, cellIndex)) {
      throw new Error("Jogada invalida.");
    }

    const previousMiniWinner = this.board.getMini(miniIndex).getWinner();
    this.board.place(miniIndex, cellIndex, this.currentPlayer.symbol);
    const miniWon =
      previousMiniWinner === null && this.board.getMini(miniIndex).getWinner() !== null;

    const winningSymbol = this.board.getWinner();
    if (winningSymbol !== null) {
      this.winner = this.playerForSymbol(winningSymbol);
      this.finished = true;
      return { miniWon, gameWon: true, draw: false, nextRequiredMini: null };
    }

    if (this.board.allMiniBoardsClosed()) {
      this.finished = true;
      this.draw = true;
      return { miniWon, gameWon: false, draw: true, nextRequiredMini: null };
    }

    const nextMini = this.rules.nextRequiredMini(cellIndex);
    this.requiredMini = this.rules.isMiniAvailable(this.board, nextMini) ? nextMini : null;
    this.swapPlayer();

    return {
      miniWon,
      gameWon: false,
      draw: false,
      nextRequiredMini: this.requiredMini,
    };
  }

  private swapPlayer(): void {
    this.currentPlayer =
      this.currentPlayer === this.playerOne ? this.playerTwo : this.playerOne;
  }

  private playerForSymbol(symbol: string): Player {
    if (this.playerOne.symbol === symbol) {
      return this.playerOne;
    }

    if (this.playerTwo.symbol === symbol) {
      return this.playerTwo;
    }

    throw new Error("Simbolo de jogador invalido.");
  }
}
