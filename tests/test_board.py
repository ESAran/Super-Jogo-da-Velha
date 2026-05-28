import pytest

from app.game.board import MiniTabuleiro, Tabuleiro


def vencer_mini(tabuleiro: Tabuleiro, mini_id: int, simbolo: str = "X") -> None:
    tabuleiro.marcar_celula(mini_id, 0, 0, simbolo)
    tabuleiro.marcar_celula(mini_id, 0, 1, simbolo)
    tabuleiro.marcar_celula(mini_id, 0, 2, simbolo)


def test_mini_tabuleiro_marca_jogada_valida() -> None:
    mini = MiniTabuleiro()

    mini.marcar_celula(1, 2, "X")

    assert mini.obter_celula(1, 2) == "X"


def test_mini_tabuleiro_rejeita_posicao_invalida() -> None:
    mini = MiniTabuleiro()

    with pytest.raises(ValueError, match="Posicao invalida"):
        mini.marcar_celula(3, 0, "X")


def test_mini_tabuleiro_rejeita_celula_ocupada() -> None:
    mini = MiniTabuleiro()
    mini.marcar_celula(0, 0, "X")

    with pytest.raises(ValueError, match="celula ja esta ocupada"):
        mini.marcar_celula(0, 0, "O")


def test_mini_tabuleiro_detecta_vitoria_em_linha() -> None:
    mini = MiniTabuleiro()

    mini.marcar_celula(0, 0, "X")
    mini.marcar_celula(0, 1, "X")
    mini.marcar_celula(0, 2, "X")

    assert mini.checar_vitoria() == "X"
    assert mini.esta_encerrado()


def test_tabuleiro_atualiza_resultado_quando_mini_e_vencido() -> None:
    tabuleiro = Tabuleiro()

    vencer_mini(tabuleiro, mini_id=4, simbolo="O")

    assert tabuleiro.resultado.obter_celula(1, 1) == "O"
    assert tabuleiro.mini_esta_encerrado(4)


def test_tabuleiro_detecta_vitoria_geral() -> None:
    tabuleiro = Tabuleiro()

    vencer_mini(tabuleiro, mini_id=0)
    vencer_mini(tabuleiro, mini_id=1)
    vencer_mini(tabuleiro, mini_id=2)

    assert tabuleiro.checar_vitoria() == "X"
