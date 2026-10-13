from app.game.engine import Jogador, MotorJogo
from app.schemas.game import (
    EstadoPartida,
    JogadaEntrada,
    JogadoresEntrada,
    JogadorSaida,
)


class PartidaService:
    """Mantem e orquestra a partida ativa em memoria."""

    def __init__(self) -> None:
        self._jogo: MotorJogo | None = None

    def iniciar_partida(self, entrada: JogadoresEntrada) -> EstadoPartida:
        jogador_1 = Jogador(entrada.jogador_1.nome, entrada.jogador_1.simbolo)
        jogador_2 = Jogador(entrada.jogador_2.nome, entrada.jogador_2.simbolo)
        self._jogo = MotorJogo(jogador_1, jogador_2)
        return self.obter_estado()

    def realizar_jogada(self, entrada: JogadaEntrada) -> EstadoPartida:
        jogo = self._obter_jogo()
        jogo.jogar(entrada.mini_id, entrada.linha, entrada.coluna)
        return self.obter_estado()

    def obter_estado(self) -> EstadoPartida:
        jogo = self._obter_jogo()
        vencedor = None

        if jogo.vencedor is not None:
            vencedor = jogo.vencedor.nome

        return EstadoPartida(
            jogador_atual=jogo.jogador_atual.nome,
            finalizado=jogo.finalizado,
            mini_obrigatorio=jogo.mini_obrigatorio,
            vencedor=vencedor,
            jogador_1=self._serializar_jogador(jogo.jogador_1),
            jogador_2=self._serializar_jogador(jogo.jogador_2),
            tabuleiro=self._serializar_tabuleiro(jogo),
            resultado=[linha[:] for linha in jogo.tabuleiro.resultado.grid],
        )

    def _obter_jogo(self) -> MotorJogo:
        if self._jogo is None:
            raise ValueError("Nenhuma partida foi iniciada.")

        return self._jogo

    def _serializar_jogador(self, jogador: Jogador) -> JogadorSaida:
        return JogadorSaida(
            nome=jogador.nome,
            simbolo=jogador.simbolo,
            tipo=jogador.tipo.value,
        )

    def _serializar_tabuleiro(self, jogo: MotorJogo) -> list[list[list[str]]]:
        return [
            [linha[:] for linha in mini.grid]
            for mini in jogo.tabuleiro.mini_tabuleiros
        ]
