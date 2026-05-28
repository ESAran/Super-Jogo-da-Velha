import pytest

from app.game.engine import Jogador, MotorJogo


def criar_jogo() -> MotorJogo:
    return MotorJogo(Jogador("Alice", "X"), Jogador("Bruno", "O"))


def preparar_vitoria_geral_para_x(jogo: MotorJogo) -> None:
    jogo.tabuleiro.resultado.marcar_celula(0, 0, "X")
    jogo.tabuleiro.resultado.marcar_celula(0, 1, "X")
    jogo.tabuleiro.marcar_celula(2, 0, 0, "X")
    jogo.tabuleiro.marcar_celula(2, 0, 1, "X")
    jogo.mini_obrigatorio = None


def test_motor_executa_jogada_valida() -> None:
    jogo = criar_jogo()

    jogo.jogar(0, 1, 2)

    assert jogo.tabuleiro.obter_celula(0, 1, 2) == "X"
    assert jogo.mini_obrigatorio == 5
    assert jogo.jogador_atual.nome == "Bruno"


def test_motor_rejeita_jogada_invalida() -> None:
    jogo = criar_jogo()
    jogo.jogar(0, 0, 0)

    with pytest.raises(ValueError, match="Jogada invalida"):
        jogo.jogar(1, 0, 0)


def test_motor_respeita_mini_tabuleiro_obrigatorio() -> None:
    jogo = criar_jogo()

    jogo.jogar(3, 2, 1)

    assert jogo.obter_mini_obrigatorio() == 7


def test_motor_finaliza_partida_com_vitoria_geral() -> None:
    jogo = criar_jogo()
    preparar_vitoria_geral_para_x(jogo)

    jogo.jogar(2, 0, 2)

    assert jogo.finalizado
    assert jogo.vencedor == jogo.jogador_1


def test_motor_rejeita_jogada_apos_partida_finalizada() -> None:
    jogo = criar_jogo()
    preparar_vitoria_geral_para_x(jogo)
    jogo.jogar(2, 0, 2)

    with pytest.raises(ValueError, match="partida ja foi encerrada"):
        jogo.jogar(3, 1, 1)
