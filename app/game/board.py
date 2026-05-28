class MiniTabuleiro:
    """Representa um mini tabuleiro 3x3."""

    def __init__(self) -> None:
        self.celula_vazia: str = " "
        self.grid: list[list[str]] = [
            [self.celula_vazia for _ in range(3)]
            for _ in range(3)
        ]

    def marcar_celula(self, linha: int, coluna: int, valor: str) -> None:
        if not self.posicao_valida(linha, coluna):
            raise ValueError("Posicao invalida.")

        if not self.celula_esta_vazia(linha, coluna):
            raise ValueError("A celula ja esta ocupada.")

        self.grid[linha][coluna] = valor

    def obter_celula(self, linha: int, coluna: int) -> str:
        if not self.posicao_valida(linha, coluna):
            raise ValueError("Posicao invalida.")

        return self.grid[linha][coluna]

    def celula_esta_vazia(self, linha: int, coluna: int) -> bool:
        if not self.posicao_valida(linha, coluna):
            return False

        return self.grid[linha][coluna] == self.celula_vazia

    def posicao_valida(self, linha: int, coluna: int) -> bool:
        return 0 <= linha < 3 and 0 <= coluna < 3

    def esta_cheio(self) -> bool:
        return all(
            celula != self.celula_vazia
            for linha in self.grid
            for celula in linha
        )

    def checar_vitoria(self) -> str | None:
        linhas = self.grid
        colunas = [
            [self.grid[0][indice], self.grid[1][indice], self.grid[2][indice]]
            for indice in range(3)
        ]
        diagonais = [
            [self.grid[0][0], self.grid[1][1], self.grid[2][2]],
            [self.grid[0][2], self.grid[1][1], self.grid[2][0]],
        ]

        for combinacao in [*linhas, *colunas, *diagonais]:
            if self._combinacao_vencedora(combinacao):
                return combinacao[0]

        return None

    def esta_encerrado(self) -> bool:
        return self.checar_vitoria() is not None or self.esta_cheio()

    def _combinacao_vencedora(self, combinacao: list[str]) -> bool:
        return (
            combinacao[0] != self.celula_vazia
            and combinacao[0] == combinacao[1] == combinacao[2]
        )


class Tabuleiro:
    """Representa os 9 mini tabuleiros e o resultado principal."""

    def __init__(self) -> None:
        self.mini_tabuleiros: list[MiniTabuleiro] = [
            MiniTabuleiro() for _ in range(9)
        ]
        self.resultado: MiniTabuleiro = MiniTabuleiro()

    def mini_tabuleiro_valido(self, mini_id: int) -> bool:
        return 0 <= mini_id < 9

    def obter_mini_tabuleiro(self, mini_id: int) -> MiniTabuleiro:
        if not self.mini_tabuleiro_valido(mini_id):
            raise ValueError("Mini tabuleiro invalido.")

        return self.mini_tabuleiros[mini_id]

    def marcar_celula(
        self,
        mini_id: int,
        linha: int,
        coluna: int,
        valor: str,
    ) -> None:
        mini_tabuleiro = self.obter_mini_tabuleiro(mini_id)
        mini_tabuleiro.marcar_celula(linha, coluna, valor)
        self.atualizar_resultado_mini(mini_id)

    def obter_celula(self, mini_id: int, linha: int, coluna: int) -> str:
        mini_tabuleiro = self.obter_mini_tabuleiro(mini_id)
        return mini_tabuleiro.obter_celula(linha, coluna)

    def mini_esta_encerrado(self, mini_id: int) -> bool:
        mini_tabuleiro = self.obter_mini_tabuleiro(mini_id)
        return mini_tabuleiro.esta_encerrado()

    def atualizar_resultado_mini(self, mini_id: int) -> None:
        mini_tabuleiro = self.obter_mini_tabuleiro(mini_id)
        vencedor = mini_tabuleiro.checar_vitoria()

        if vencedor is None:
            return

        linha_resultado = mini_id // 3
        coluna_resultado = mini_id % 3

        if self.resultado.celula_esta_vazia(linha_resultado, coluna_resultado):
            self.resultado.marcar_celula(linha_resultado, coluna_resultado, vencedor)

    def checar_vitoria(self) -> str | None:
        return self.resultado.checar_vitoria()
