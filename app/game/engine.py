from dataclasses import dataclass
from enum import Enum

from app.game.board import Tabuleiro
from app.game.rules import RegrasJogo


class TipoJogador(Enum):
    HUMANO = "humano"
    MAQUINA = "maquina"


@dataclass
class Jogador:
    nome: str
    simbolo: str
    tipo: TipoJogador = TipoJogador.HUMANO

    def __post_init__(self) -> None:
        self.nome = self.nome.strip()
        self.simbolo = self.simbolo.strip().upper()

        if not self.nome:
            raise ValueError("O nome do jogador nao pode ser vazio.")

        if len(self.simbolo) != 1:
            raise ValueError("O simbolo do jogador deve ter exatamente 1 caractere.")

        if self.simbolo.isdigit():
            raise ValueError("O simbolo do jogador nao pode ser um numero.")


class MotorJogo:
    """Controla o estado e o fluxo de uma partida."""

    def __init__(self, jogador_1: Jogador, jogador_2: Jogador) -> None:
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

    def jogar(self, mini_id: int, linha: int, coluna: int) -> None:
        if self.finalizado:
            raise ValueError("A partida ja foi encerrada.")

        if not self.jogada_valida(mini_id, linha, coluna):
            raise ValueError("Jogada invalida.")

        self._marcar_jogada(mini_id, linha, coluna)
        self._atualizar_estado_apos_jogada(linha, coluna)

    def jogada_valida(self, mini_id: int, linha: int, coluna: int) -> bool:
        return self.regras.jogada_valida(
            self.tabuleiro,
            mini_id,
            linha,
            coluna,
            self.mini_obrigatorio,
        )

    def trocar_jogador(self) -> None:
        if self.jogador_atual == self.jogador_1:
            self.jogador_atual = self.jogador_2
            return

        self.jogador_atual = self.jogador_1

    def obter_jogador_por_simbolo(self, simbolo: str) -> Jogador:
        if self.jogador_1.simbolo == simbolo:
            return self.jogador_1

        if self.jogador_2.simbolo == simbolo:
            return self.jogador_2

        raise ValueError("Simbolo de jogador invalido.")

    def obter_tabuleiro(self) -> Tabuleiro:
        return self.tabuleiro

    def obter_mini_obrigatorio(self) -> int | None:
        return self.mini_obrigatorio

    def mini_esta_encerrado(self, mini_id: int) -> bool:
        return self.tabuleiro.mini_esta_encerrado(mini_id)

    def _marcar_jogada(self, mini_id: int, linha: int, coluna: int) -> None:
        self.tabuleiro.marcar_celula(
            mini_id,
            linha,
            coluna,
            self.jogador_atual.simbolo,
        )

    def _atualizar_estado_apos_jogada(self, linha: int, coluna: int) -> None:
        simbolo_vencedor = self.tabuleiro.checar_vitoria()

        if simbolo_vencedor is not None:
            self.vencedor = self.obter_jogador_por_simbolo(simbolo_vencedor)
            self.finalizado = True
            return

        self._atualizar_mini_obrigatorio(linha, coluna)
        self.trocar_jogador()

    def _atualizar_mini_obrigatorio(self, linha: int, coluna: int) -> None:
        proximo_mini = self.regras.obter_proximo_mini(linha, coluna)

        if self.regras.mini_destino_esta_disponivel(self.tabuleiro, proximo_mini):
            self.mini_obrigatorio = proximo_mini
            return

        self.mini_obrigatorio = None
