from app.services.cli import (
    mostrar_tela,
    renderizar_como_jogar,
    renderizar_conquistas,
    renderizar_creditos,
    renderizar_historico,
)


def mostrar_como_jogar() -> None:
    mostrar_tela(renderizar_como_jogar())


def mostrar_creditos() -> None:
    mostrar_tela(renderizar_creditos())


def mostrar_historico() -> None:
    mostrar_tela(renderizar_historico())


def mostrar_conquistas() -> None:
    mostrar_tela(renderizar_conquistas())


__all__ = [
    "mostrar_como_jogar",
    "mostrar_conquistas",
    "mostrar_creditos",
    "mostrar_historico",
    "renderizar_como_jogar",
    "renderizar_conquistas",
    "renderizar_creditos",
    "renderizar_historico",
]
