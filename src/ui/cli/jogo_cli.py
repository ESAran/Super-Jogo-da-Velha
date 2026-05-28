from app.services.cli import (
    cadastrar_jogador,
    cadastrar_jogadores,
    executar_partida,
    ler_jogada,
    ler_numero,
    ler_texto,
    limpar_tela,
    posicao_para_coordenadas,
    renderizar_legenda_jogadores,
)


def exibir_legenda_jogadores(jogo) -> None:
    print(renderizar_legenda_jogadores(jogo))

__all__ = [
    "cadastrar_jogador",
    "cadastrar_jogadores",
    "executar_partida",
    "exibir_legenda_jogadores",
    "ler_jogada",
    "ler_numero",
    "ler_texto",
    "limpar_tela",
    "posicao_para_coordenadas",
]
