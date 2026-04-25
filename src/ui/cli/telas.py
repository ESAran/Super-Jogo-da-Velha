def renderizar_como_jogar() -> str:
    """Retorna o texto da tela de instrucoes do jogo."""
    linhas: list[str] = [
        "Como Jogar",
        "",
        "Super Jogo da Velha funciona com 9 mini tabuleiros.",
        "Cada mini tabuleiro tem posicoes de 1 a 9.",
        "",
        "Mapa das posicoes:",
        "1 2 3",
        "4 5 6",
        "7 8 9",
        "",
        "Regras principais:",
        "1. O jogador escolhe uma posicao dentro de um mini tabuleiro.",
        "2. A posicao jogada define o proximo mini tabuleiro obrigatorio.",
        "3. Se o mini tabuleiro de destino ja estiver encerrado,",
        "   o proximo jogador pode jogar em qualquer mini disponivel.",
        "4. Um mini tabuleiro termina quando alguem vence ou quando ele empata.",
        "5. O objetivo final e vencer no tabuleiro principal.",
        "",
        "Pressione Enter para voltar ao menu.",
    ]
    return "\n".join(linhas)


def renderizar_creditos() -> str:
    """Retorna o texto da tela de creditos."""
    linhas: list[str] = [
        "Creditos",
        "",
        "Projeto: Super Jogo da Velha",
        "Desenvolvimento: Eduardo Aran",
        "",
        "Pressione Enter para voltar ao menu.",
    ]
    return "\n".join(linhas)


def renderizar_historico() -> str:
    """Retorna o texto da tela de historico."""
    linhas: list[str] = [
        "Historico de Jogos",
        "",
        "Historico ainda nao implementado.",
        "",
        "Pressione Enter para voltar ao menu.",
    ]
    return "\n".join(linhas)


def renderizar_conquistas() -> str:
    """Retorna o texto da tela de conquistas."""
    linhas: list[str] = [
        "Conquistas",
        "",
        "Conquistas ainda nao implementadas.",
        "",
        "Pressione Enter para voltar ao menu.",
    ]
    return "\n".join(linhas)


def mostrar_como_jogar() -> None:
    """Exibe a tela de instrucoes do jogo."""
    print(renderizar_como_jogar())
    input()


def mostrar_creditos() -> None:
    """Exibe a tela de creditos."""
    print(renderizar_creditos())
    input()


def mostrar_historico() -> None:
    """Exibe a tela de historico."""
    print(renderizar_historico())
    input()


def mostrar_conquistas() -> None:
    """Exibe a tela de conquistas."""
    print(renderizar_conquistas())
    input()