from app.services.cli import (
    render_jogo,
    render_linha_mini,
    render_status,
    render_tabuleiro,
)


def print_jogo(jogo) -> None:
    print(render_jogo(jogo))


__all__ = [
    "print_jogo",
    "render_jogo",
    "render_linha_mini",
    "render_status",
    "render_tabuleiro",
]
