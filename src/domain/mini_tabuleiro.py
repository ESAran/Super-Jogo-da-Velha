class MiniTabuleiro:
    """Representa um mini tabuleiro 3x3 do Super Jogo da Velha."""

    def __init__(self) -> None:
        """Inicializa o mini tabuleiro com todas as células vazias."""
        self.celula_vazia: str = " "
        self.grid: list[list[str]] = [
            [self.celula_vazia for _ in range(3)]
            for _ in range(3)
        ]

    def marcar_celula(self, linha: int, coluna: int, valor: str) -> None:
        """Marca uma célula com o valor informado.

        Levanta:
            ValueError: Se a posição for inválida ou se a célula já estiver ocupada.
        """
        if not self.posicao_valida(linha, coluna):
            raise ValueError("Posicao invalida.")

        if not self.celula_esta_vazia(linha, coluna):
            raise ValueError("A celula ja esta ocupada.")

        self.grid[linha][coluna] = valor

    def obter_celula(self, linha: int, coluna: int) -> str:
        """Retorna o valor armazenado em uma célula.

        Levanta:
            ValueError: Se a posição for inválida.
        """
        if not self.posicao_valida(linha, coluna):
            raise ValueError("Posicao invalida.")

        return self.grid[linha][coluna]

    def celula_esta_vazia(self, linha: int, coluna: int) -> bool:
        """Informa se a célula está vazia."""
        if not self.posicao_valida(linha, coluna):
            return False

        return self.grid[linha][coluna] == self.celula_vazia

    def posicao_valida(self, linha: int, coluna: int) -> bool:
        """Valida se a posição está dentro dos limites do tabuleiro 3x3."""
        return 0 <= linha < 3 and 0 <= coluna < 3

    def esta_cheio(self) -> bool:
        """Retorna True se não houver mais células vazias."""
        for linha in self.grid:
            for celula in linha:
                if celula == self.celula_vazia:
                    return False
        return True

    def checar_vitoria(self) -> str | None:
        """Verifica se existe um vencedor no mini tabuleiro.

        Retorna:
            O símbolo vencedor, se existir. Caso contrário, retorna None.
        """
        for indice in range(3):
            if (
                self.grid[indice][0] != self.celula_vazia
                and self.grid[indice][0] == self.grid[indice][1] == self.grid[indice][2]
            ):
                return self.grid[indice][0]

            if (
                self.grid[0][indice] != self.celula_vazia
                and self.grid[0][indice] == self.grid[1][indice] == self.grid[2][indice]
            ):
                return self.grid[0][indice]

        if (
            self.grid[0][0] != self.celula_vazia
            and self.grid[0][0] == self.grid[1][1] == self.grid[2][2]
        ):
            return self.grid[0][0]

        if (
            self.grid[0][2] != self.celula_vazia
            and self.grid[0][2] == self.grid[1][1] == self.grid[2][0]
        ):
            return self.grid[0][2]

        return None

    def esta_encerrado(self) -> bool:
        """Retorna True se o mini tabuleiro terminou por vitória ou empate."""
        return self.checar_vitoria() is not None or self.esta_cheio()
