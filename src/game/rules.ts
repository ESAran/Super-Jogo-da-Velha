import { Board } from "./board";

export class GameRules {
  nextRequiredMini(cellIndex: number): number {
    return cellIndex;
  }

  isMiniAvailable(board: Board, miniIndex: number): boolean {
    return !board.getMini(miniIndex).isClosed();
  }

  isMoveValid(
    board: Board,
    miniIndex: number,
    cellIndex: number,
    requiredMini: number | null,
  ): boolean {
    if (
      !Number.isInteger(miniIndex) ||
      !Number.isInteger(cellIndex) ||
      miniIndex < 0 ||
      miniIndex > 8 ||
      cellIndex < 0 ||
      cellIndex > 8
    ) {
      return false;
    }

    const miniBoard = board.getMini(miniIndex);
    if (miniBoard.isClosed()) {
      return false;
    }

    if (
      requiredMini !== null &&
      this.isMiniAvailable(board, requiredMini) &&
      miniIndex !== requiredMini
    ) {
      return false;
    }

    return miniBoard.getCell(cellIndex) === null;
  }
}
