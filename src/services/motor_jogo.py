from src.domain.tabuleiro import Tabuleiro
from src.services.regras_jogo import RegrasJogo


class MotorJogo:
    """Controla o fluxo principal de uma partida."""

    def __init__(self) -> None:
        """Inicializa o estado da partida."""
        self.tabuleiro: Tabuleiro = Tabuleiro()
        self.regras: RegrasJogo = RegrasJogo()
        self.jogador_atual: str = "X"
        self.mini_obrigatorio: int | None = None
        self.vencedor: str | None = None
        self.finalizado: bool = False

    def trocar_jogador(self) -> None:
        """Alterna o jogador atual."""
        self.jogador_atual = "O" if self.jogador_atual == "X" else "X"

    def jogar(self, mini_id: int, linha: int, coluna: int) -> None:
        """Executa uma jogada se ela for válida.

        Levanta:
            ValueError: Se a jogada for inválida.
        """
        if self.finalizado:
            raise ValueError("A partida ja foi encerrada.")

        if not self.regras.jogada_valida(
            self.tabuleiro,
            mini_id,
            linha,
            coluna,
            self.mini_obrigatorio,
        ):
            raise ValueError("Jogada invalida.")

        self.tabuleiro.marcar_celula(mini_id, linha, coluna, self.jogador_atual)

        self.vencedor = self.tabuleiro.checar_vitoria()
        if self.vencedor is not None:
            self.finalizado = True
            return

        proximo_mini = self.regras.obter_proximo_mini(linha, coluna)
        if self.regras.mini_destino_esta_disponivel(self.tabuleiro, proximo_mini):
            self.mini_obrigatorio = proximo_mini
        else:
            self.mini_obrigatorio = None

        self.trocar_jogador()