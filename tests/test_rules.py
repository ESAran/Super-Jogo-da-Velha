from app.game.board import Tabuleiro
from app.game.rules import RegrasJogo


def test_regras_aceitam_jogada_valida_sem_mini_obrigatorio() -> None:
    regras = RegrasJogo()
    tabuleiro = Tabuleiro()

    assert regras.jogada_valida(tabuleiro, 0, 0, 0, None)


def test_regras_rejeitam_mini_tabuleiro_invalido() -> None:
    regras = RegrasJogo()
    tabuleiro = Tabuleiro()

    assert not regras.jogada_valida(tabuleiro, 9, 0, 0, None)


def test_regras_rejeitam_celula_ocupada() -> None:
    regras = RegrasJogo()
    tabuleiro = Tabuleiro()
    tabuleiro.marcar_celula(0, 0, 0, "X")

    assert not regras.jogada_valida(tabuleiro, 0, 0, 0, None)


def test_regras_rejeitam_mini_diferente_do_obrigatorio_disponivel() -> None:
    regras = RegrasJogo()
    tabuleiro = Tabuleiro()

    assert not regras.jogada_valida(tabuleiro, 1, 0, 0, mini_obrigatorio=0)


def test_regras_permitem_qualquer_mini_quando_obrigatorio_esta_encerrado() -> None:
    regras = RegrasJogo()
    tabuleiro = Tabuleiro()
    tabuleiro.marcar_celula(0, 0, 0, "X")
    tabuleiro.marcar_celula(0, 0, 1, "X")
    tabuleiro.marcar_celula(0, 0, 2, "X")

    assert regras.jogada_valida(tabuleiro, 1, 1, 1, mini_obrigatorio=0)


def test_regras_calculam_proximo_mini_pela_posicao_jogada() -> None:
    regras = RegrasJogo()

    assert regras.obter_proximo_mini(2, 1) == 7
