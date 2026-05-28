from app.game.engine import Jogador, MotorJogo
from app.schemas.game import EstadoPartida, JogadaEntrada, JogadorEntrada


def criar_partida(
    jogador_1: JogadorEntrada,
    jogador_2: JogadorEntrada,
) -> MotorJogo:
    """Cria uma partida sem depender de uma interface especifica."""
    return MotorJogo(
        Jogador(jogador_1.nome, jogador_1.simbolo),
        Jogador(jogador_2.nome, jogador_2.simbolo),
    )


def jogar(jogo: MotorJogo, jogada: JogadaEntrada) -> EstadoPartida:
    """Executa uma jogada e devolve um estado serializavel."""
    jogo.jogar(jogada.mini_id, jogada.linha, jogada.coluna)
    return obter_estado(jogo)


def obter_estado(jogo: MotorJogo) -> EstadoPartida:
    vencedor = None

    if jogo.vencedor is not None:
        vencedor = jogo.vencedor.nome

    return EstadoPartida(
        jogador_atual=jogo.jogador_atual.nome,
        finalizado=jogo.finalizado,
        mini_obrigatorio=jogo.mini_obrigatorio,
        vencedor=vencedor,
    )
