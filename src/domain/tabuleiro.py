from src.domain.mini_tabuleiro import MiniTabuleiro


class Tabuleiro:
    """Representa o tabuleiro principal do Super Jogo da Velha."""

    def __init__(self) -> None:
        """Inicializa os 9 mini tabuleiros e o tabuleiro de resultado."""
        self.mini_tabuleiros: list[MiniTabuleiro] = [
            MiniTabuleiro() for _ in range(9)
        ]
        self.resultado: MiniTabuleiro = MiniTabuleiro()

    def mini_tabuleiro_valido(self, mini_id: int) -> bool:
        """Retorna True se o índice do mini tabuleiro estiver entre 0 e 8."""
        return 0 <= mini_id < 9

    def obter_mini_tabuleiro(self, mini_id: int) -> MiniTabuleiro:
        """Retorna o mini tabuleiro correspondente ao índice informado.

        Levanta:
            ValueError: Se o índice do mini tabuleiro for inválido.
        """
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
        """Marca uma célula em um mini tabuleiro e atualiza o resultado local."""
        mini_tabuleiro: MiniTabuleiro = self.obter_mini_tabuleiro(mini_id)
        mini_tabuleiro.marcar_celula(linha, coluna, valor)
        self.atualizar_resultado_mini(mini_id)

    def obter_celula(self, mini_id: int, linha: int, coluna: int) -> str:
        """Retorna o valor de uma célula de um mini tabuleiro."""
        mini_tabuleiro: MiniTabuleiro = self.obter_mini_tabuleiro(mini_id)
        return mini_tabuleiro.obter_celula(linha, coluna)

    def mini_esta_encerrado(self, mini_id: int) -> bool:
        """Retorna True se o mini tabuleiro já terminou."""
        mini_tabuleiro: MiniTabuleiro = self.obter_mini_tabuleiro(mini_id)
        return mini_tabuleiro.esta_encerrado()

    def atualizar_resultado_mini(self, mini_id: int) -> None:
        """Atualiza o tabuleiro de resultado caso um mini tabuleiro tenha vencedor."""
        mini_tabuleiro: MiniTabuleiro = self.obter_mini_tabuleiro(mini_id)
        vencedor: str | None = mini_tabuleiro.checar_vitoria()

        if vencedor is None:
            return

        linha_resultado: int = mini_id // 3
        coluna_resultado: int = mini_id % 3

        if self.resultado.celula_esta_vazia(linha_resultado, coluna_resultado):
            self.resultado.marcar_celula(linha_resultado, coluna_resultado, vencedor)

    def checar_vitoria(self) -> str | None:
        """Verifica se existe um vencedor no tabuleiro principal."""
        return self.resultado.checar_vitoria()
