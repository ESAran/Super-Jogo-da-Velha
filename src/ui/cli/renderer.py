from src.domain.mini_tabuleiro import MiniTabuleiro
from src.domain.tabuleiro import Tabuleiro
from src.services.motor_jogo import MotorJogo


def render_linha_mini(mini_tabuleiro: MiniTabuleiro, linha: int) -> str:
    """Retorna uma linha de um mini tabuleiro com largura fixa."""
    celulas: list[str] = [
        f"{mini_tabuleiro.obter_celula(linha, coluna):^7}"
        for coluna in range(3)
    ]
    return "│" + "│".join(celulas) + "│"


def render_tabuleiro(tabuleiro: Tabuleiro) -> str:
    """Retorna o tabuleiro principal em formato de string."""
    linhas_saida: list[str] = []

    topo_mini: str = "┌───────┬───────┬───────┐"
    meio_mini: str = "├───────┼───────┼───────┤"
    base_mini: str = "└───────┴───────┴───────┘"

    topo_bloco: str = "   " + "  ||  ".join([topo_mini] * 3)
    meio_bloco: str = "   " + "  ||  ".join([meio_mini] * 3)
    base_bloco: str = "   " + "  ||  ".join([base_mini] * 3)
    divisoria_macro: str = "   " + "=" * (len(base_bloco) - 3)

    linhas_saida.append(topo_bloco)

    for linha_bloco in range(3):
        for linha_interna in range(3):
            minis_da_linha: list[str] = []

            for coluna_bloco in range(3):
                mini_id: int = linha_bloco * 3 + coluna_bloco
                mini_tabuleiro: MiniTabuleiro = tabuleiro.obter_mini_tabuleiro(mini_id)
                minis_da_linha.append(render_linha_mini(mini_tabuleiro, linha_interna))

            linhas_saida.append("   " + "  ||  ".join(minis_da_linha))

            if linha_interna < 2:
                linhas_saida.append(meio_bloco)

        linhas_saida.append(base_bloco)

        if linha_bloco < 2:
            linhas_saida.append(divisoria_macro)
            linhas_saida.append(topo_bloco)

    return "\n".join(linhas_saida)


def render_status(jogo: MotorJogo) -> str:
    """Retorna uma linha simples com o estado atual da partida."""
    if jogo.finalizado and jogo.vencedor is not None:
        return f"Vencedor: {jogo.vencedor.nome} ({jogo.vencedor.simbolo})"

    jogador_atual = jogo.jogador_atual
    descricao_jogador = f"{jogador_atual.nome} ({jogador_atual.simbolo})"

    if jogo.mini_obrigatorio is None:
        return (
            f"Jogador atual: {descricao_jogador} | "
            "Pode jogar em qualquer mini tabuleiro."
        )

    return (
        f"Jogador atual: {descricao_jogador} | "
        f"Mini obrigatorio: {jogo.mini_obrigatorio + 1}"
    )


def render_jogo(jogo: MotorJogo) -> str:
    """Retorna a tela completa do jogo."""
    return f"{render_status(jogo)}\n\n{render_tabuleiro(jogo.tabuleiro)}"


def print_jogo(jogo: MotorJogo) -> None:
    """Imprime a tela atual do jogo no terminal."""
    print(render_jogo(jogo))