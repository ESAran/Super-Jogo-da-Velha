from src.domain.jogador import Jogador
from src.domain.tabuleiro import Tabuleiro
from src.services.regras_jogo import RegrasJogo


class MotorJogo:
    """Controla o fluxo principal de uma partida."""

    def __init__(self, jogador_1: Jogador, jogador_2: Jogador) -> None:
        """Inicializa o estado da partida."""
        if jogador_1.simbolo == jogador_2.simbolo:
            raise ValueError("Os jogadores devem ter simbolos diferentes.")

        self.tabuleiro: Tabuleiro = Tabuleiro()
        self.regras: RegrasJogo = RegrasJogo()
        self.jogador_1: Jogador = jogador_1
        self.jogador_2: Jogador = jogador_2
        self.jogador_atual: Jogador = jogador_1
        self.mini_obrigatorio: int | None = None
        self.vencedor: Jogador | None = None
        self.finalizado: bool = False

    def trocar_jogador(self) -> None:
        """Alterna o jogador atual."""
        if self.jogador_atual == self.jogador_1:
            self.jogador_atual = self.jogador_2
        else:
            self.jogador_atual = self.jogador_1

    def obter_jogador_por_simbolo(self, simbolo: str) -> Jogador:
        """Retorna o jogador associado ao simbolo informado."""
        if self.jogador_1.simbolo == simbolo:
            return self.jogador_1

        if self.jogador_2.simbolo == simbolo:
            return self.jogador_2

        raise ValueError("Simbolo de jogador invalido.")

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

        self.tabuleiro.marcar_celula(
            mini_id,
            linha,
            coluna,
            self.jogador_atual.simbolo,
        )

        simbolo_vencedor = self.tabuleiro.checar_vitoria()
        if simbolo_vencedor is not None:
            self.vencedor = self.obter_jogador_por_simbolo(simbolo_vencedor)
            self.finalizado = True
            return

        proximo_mini = self.regras.obter_proximo_mini(linha, coluna)
        if self.regras.mini_destino_esta_disponivel(self.tabuleiro, proximo_mini):
            self.mini_obrigatorio = proximo_mini
        else:
            self.mini_obrigatorio = None

        self.trocar_jogador()