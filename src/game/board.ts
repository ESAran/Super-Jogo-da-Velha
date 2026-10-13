export type Cell = string | null;

export const WINNING_LINES: ReadonlyArray<ReadonlyArray<number>> = [
  [0, 1, 2],
  [3, 4, 5],
  [6, 7, 8],
  [0, 3, 6],
  [1, 4, 7],
  [2, 5, 8],
  [0, 4, 8],
  [2, 4, 6],
];

function assertIndex(index: number, label: string): void {
  if (!Number.isInteger(index) || index < 0 || index > 8) {
    throw new Error(`${label} invalido.`);
  }
}
export class MiniBoard {
  private readonly cells: Cell[] = Array<Cell>(9).fill(null);

  getCells(): readonly Cell[] {
    return this.cells;
  }

  getCell(index: number): Cell {
    assertIndex(index, "Posicao");
    return this.cells[index];
  }

  place(index: number, symbol: string): void {
    assertIndex(index, "Posicao");

    if (this.isClosed()) {
      throw new Error("O mini tabuleiro ja foi encerrado.");
    }

    if (this.cells[index] !== null) {
      throw new Error("A celula ja esta ocupada.");
    }

    this.cells[index] = symbol;
  }

  getWinner(): Cell {
    for (const [first, second, third] of WINNING_LINES) {
      const symbol = this.cells[first];

      if (symbol !== null && symbol === this.cells[second] && symbol === this.cells[third]) {
        return symbol;
      }
    }

    return null;
  }

  isFull(): boolean {
    return this.cells.every((cell) => cell !== null);
  }

  isClosed(): boolean {
    return this.getWinner() !== null || this.isFull();
  }
}

export class Board {
  private readonly miniBoards: MiniBoard[] = Array.from(
    { length: 9 },
    () => new MiniBoard(),
  );

  private readonly macroCells: Cell[] = Array<Cell>(9).fill(null);

  getMiniBoards(): readonly MiniBoard[] {
    return this.miniBoards;
  }

  getMacroCells(): readonly Cell[] {
    return this.macroCells;
  }

  getMini(index: number): MiniBoard {
    assertIndex(index, "Mini tabuleiro");
    return this.miniBoards[index];
  }

  place(miniIndex: number, cellIndex: number, symbol: string): void {
    const miniBoard = this.getMini(miniIndex);
    miniBoard.place(cellIndex, symbol);

    const winner = miniBoard.getWinner();
    if (winner !== null) {
      this.macroCells[miniIndex] = winner;
    }
  }

  getWinner(): Cell {
    for (const [first, second, third] of WINNING_LINES) {
      const symbol = this.macroCells[first];

      if (
        symbol !== null &&
        symbol === this.macroCells[second] &&
        symbol === this.macroCells[third]
      ) {
        return symbol;
      }
    }

    return null;
  }

  allMiniBoardsClosed(): boolean {
    return this.miniBoards.every((miniBoard) => miniBoard.isClosed());
  }
}
