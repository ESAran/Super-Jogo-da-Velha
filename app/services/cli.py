import os

from app.game.board import MiniTabuleiro, Tabuleiro
from app.game.engine import Jogador, MotorJogo, TipoJogador


OPCOES_MENU: tuple[tuple[str, str], ...] = (
    ("1", "JvJ        - Jogador vs Jogador"),
    ("2", "JvM        - Jogador vs Maquina"),
    ("3", "Regras     - Como jogar"),
    ("4", "Partidas   - Historico de jogos"),
    ("5", "Creditos   - Desenvolvedores"),
    ("6", "Conquistas - Desafios concluidos"),
    ("0", "Sair"),
)


def executar_aplicacao() -> None:
    mensagem = ""

    while True:
        limpar_tela()
        print(renderizar_menu_principal(mensagem))

        try:
            opcao = ler_opcao_menu()
            mensagem = ""
            executar_opcao_menu(opcao)

            if opcao == "0":
                return
        except ValueError as erro:
            mensagem = f"Erro: {erro}"


def executar_opcao_menu(opcao: str) -> None:
    if opcao == "1":
        executar_partida()
    elif opcao == "2":
        mostrar_mensagem("Modo jogador vs maquina ainda nao implementado.")
    elif opcao == "3":
        mostrar_tela(renderizar_como_jogar())
    elif opcao == "4":
        mostrar_tela(renderizar_historico())
    elif opcao == "5":
        mostrar_tela(renderizar_creditos())
    elif opcao == "6":
        mostrar_tela(renderizar_conquistas())


def executar_partida() -> None:
    jogadores = cadastrar_jogadores()

    if jogadores is None:
        mostrar_mensagem("Cadastro cancelado pelo usuario.")
        return

    jogo = MotorJogo(*jogadores)
    partida_cancelada = executar_loop_partida(jogo)

    if not partida_cancelada:
        mostrar_resultado_partida(jogo)


def executar_loop_partida(jogo: MotorJogo) -> bool:
    mensagem = ""

    while not jogo.finalizado:
        renderizar_turno(jogo, mensagem)

        try:
            jogada = ler_jogada(jogo)

            if jogada is None:
                mostrar_mensagem("Jogo encerrado pelo usuario.")
                return True

            jogo.jogar(*jogada)
            mensagem = ""
        except ValueError as erro:
            mensagem = f"Erro: {erro}"

    return False


def renderizar_turno(jogo: MotorJogo, mensagem: str) -> None:
    limpar_tela()
    print(renderizar_cabecalho())
    print(renderizar_ajuda_rapida())
    print(renderizar_legenda_jogadores(jogo))
    print(render_jogo(jogo))

    if mensagem:
        print()
        print(mensagem)

    print()


def mostrar_resultado_partida(jogo: MotorJogo) -> None:
    limpar_tela()
    print(renderizar_cabecalho())
    print(renderizar_legenda_jogadores(jogo))
    print(render_jogo(jogo))
    print()
    print(renderizar_resultado_partida(jogo))
    print()
    input("Pressione Enter para voltar ao menu.")


def renderizar_resultado_partida(jogo: MotorJogo) -> str:
    if jogo.vencedor is None:
        return "Fim de jogo."

    return f"Fim de jogo. Vencedor: {jogo.vencedor.nome} ({jogo.vencedor.simbolo})"


def cadastrar_jogadores() -> tuple[Jogador, Jogador] | None:
    limpar_tela()
    print(renderizar_cabecalho())
    print("Cadastro de jogadores")
    print("Digite 'sair' a qualquer momento para voltar ao menu.")
    print()

    jogador_1 = cadastrar_jogador(1)

    if jogador_1 is None:
        return None

    print()
    jogador_2 = cadastrar_jogador(2, {jogador_1.simbolo})

    if jogador_2 is None:
        return None

    return jogador_1, jogador_2


def cadastrar_jogador(
    numero: int,
    simbolos_indisponiveis: set[str] | None = None,
) -> Jogador | None:
    while True:
        print(f"Cadastro do jogador {numero}:")

        nome = ler_texto("Nome: ")
        if nome is None:
            return None

        simbolo = ler_texto("Simbolo: ")
        if simbolo is None:
            return None

        try:
            jogador = Jogador(nome=nome, simbolo=simbolo, tipo=TipoJogador.HUMANO)
            validar_simbolo_disponivel(jogador, simbolos_indisponiveis)
            return jogador
        except ValueError as erro:
            print(f"Erro: {erro}")
            print()


def validar_simbolo_disponivel(
    jogador: Jogador,
    simbolos_indisponiveis: set[str] | None,
) -> None:
    if simbolos_indisponiveis and jogador.simbolo in simbolos_indisponiveis:
        raise ValueError("Esse simbolo ja foi escolhido pelo outro jogador.")


def ler_jogada(jogo: MotorJogo) -> tuple[int, int, int] | None:
    mini_id = ler_mini_tabuleiro(jogo)

    if mini_id is None:
        return None

    posicao = ler_numero(
        "Escolha a posicao dentro do mini tabuleiro (1-9) ou digite 'sair': "
    )

    if posicao is None:
        return None

    linha, coluna = posicao_para_coordenadas(posicao)
    return mini_id, linha, coluna


def ler_mini_tabuleiro(jogo: MotorJogo) -> int | None:
    mini_obrigatorio = jogo.obter_mini_obrigatorio()

    if mini_obrigatorio is not None:
        print(f"Voce deve jogar no mini tabuleiro {mini_obrigatorio + 1}.")
        return mini_obrigatorio

    mini_escolhido = ler_numero(
        "Escolha o mini tabuleiro (1-9) ou digite 'sair': "
    )

    if mini_escolhido is None:
        return None

    if not 1 <= mini_escolhido <= 9:
        raise ValueError("O mini tabuleiro deve estar entre 1 e 9.")

    mini_id = mini_escolhido - 1

    if jogo.mini_esta_encerrado(mini_id):
        raise ValueError(
            f"O mini tabuleiro {mini_escolhido} ja foi encerrado. Escolha outro."
        )

    return mini_id


def posicao_para_coordenadas(posicao: int) -> tuple[int, int]:
    if not 1 <= posicao <= 9:
        raise ValueError("A posicao deve estar entre 1 e 9.")

    indice = posicao - 1
    return indice // 3, indice % 3


def ler_numero(mensagem: str) -> int | None:
    entrada = input(mensagem).strip()

    if entrada.lower() == "sair":
        return None

    try:
        return int(entrada)
    except ValueError as erro:
        raise ValueError("Digite um numero inteiro valido.") from erro


def ler_texto(mensagem: str) -> str | None:
    entrada = input(mensagem).strip()

    if entrada.lower() == "sair":
        return None

    return entrada


def render_jogo(jogo: MotorJogo) -> str:
    return f"{render_status(jogo)}\n\n{render_tabuleiro(jogo.obter_tabuleiro())}"


def render_status(jogo: MotorJogo) -> str:
    if jogo.finalizado and jogo.vencedor is not None:
        return f"Vencedor: {jogo.vencedor.nome} ({jogo.vencedor.simbolo})"

    descricao_jogador = f"{jogo.jogador_atual.nome} ({jogo.jogador_atual.simbolo})"

    if jogo.mini_obrigatorio is None:
        return (
            f"Jogador atual: {descricao_jogador} | "
            "Pode jogar em qualquer mini tabuleiro."
        )

    return (
        f"Jogador atual: {descricao_jogador} | "
        f"Mini obrigatorio: {jogo.mini_obrigatorio + 1}"
    )


def render_tabuleiro(tabuleiro: Tabuleiro) -> str:
    linhas_saida: list[str] = []
    topo_mini = "+-------+-------+-------+"
    meio_mini = "+-------+-------+-------+"
    base_mini = "+-------+-------+-------+"
    topo_bloco = "   " + "  ||  ".join([topo_mini] * 3)
    meio_bloco = "   " + "  ||  ".join([meio_mini] * 3)
    base_bloco = "   " + "  ||  ".join([base_mini] * 3)
    divisoria_macro = "   " + "=" * (len(base_bloco) - 3)

    linhas_saida.append(topo_bloco)

    for linha_bloco in range(3):
        linhas_saida.extend(render_linhas_bloco(tabuleiro, linha_bloco, meio_bloco))
        linhas_saida.append(base_bloco)

        if linha_bloco < 2:
            linhas_saida.append(divisoria_macro)
            linhas_saida.append(topo_bloco)

    return "\n".join(linhas_saida)


def render_linhas_bloco(
    tabuleiro: Tabuleiro,
    linha_bloco: int,
    meio_bloco: str,
) -> list[str]:
    linhas: list[str] = []

    for linha_interna in range(3):
        linhas.append(render_linha_bloco(tabuleiro, linha_bloco, linha_interna))

        if linha_interna < 2:
            linhas.append(meio_bloco)

    return linhas


def render_linha_bloco(
    tabuleiro: Tabuleiro,
    linha_bloco: int,
    linha_interna: int,
) -> str:
    minis_da_linha: list[str] = []

    for coluna_bloco in range(3):
        mini_id = linha_bloco * 3 + coluna_bloco
        mini_tabuleiro = tabuleiro.obter_mini_tabuleiro(mini_id)
        minis_da_linha.append(render_linha_mini(mini_tabuleiro, linha_interna))

    return "   " + "  ||  ".join(minis_da_linha)


def render_linha_mini(mini_tabuleiro: MiniTabuleiro, linha: int) -> str:
    celulas = [
        f"{mini_tabuleiro.obter_celula(linha, coluna):^7}"
        for coluna in range(3)
    ]
    return "|" + "|".join(celulas) + "|"


def renderizar_menu_principal(mensagem: str = "") -> str:
    linhas = [
        renderizar_cabecalho().rstrip(),
        "Menu principal",
        "=" * 50,
    ]

    for codigo, titulo in OPCOES_MENU:
        linhas.append(f"{codigo}. {titulo}")

    if mensagem:
        linhas.extend(["", mensagem])

    linhas.extend(["", "Escolha uma opcao:"])
    return "\n".join(linhas)


def renderizar_cabecalho() -> str:
    return "Super Jogo da Velha\n" + "=" * 50 + "\n"


def renderizar_ajuda_rapida() -> str:
    return "\n".join(
        [
            "Mini tabuleiros: 1 a 9",
            "Posicoes dentro do mini: 1 a 9",
            "",
            "Mapa das posicoes:",
            "1 2 3",
            "4 5 6",
            "7 8 9",
            "",
        ]
    )


def renderizar_legenda_jogadores(jogo: MotorJogo) -> str:
    return "\n".join(
        [
            f"Jogador 1: {jogo.jogador_1.nome} ({jogo.jogador_1.simbolo})",
            f"Jogador 2: {jogo.jogador_2.nome} ({jogo.jogador_2.simbolo})",
            "",
        ]
    )


def renderizar_como_jogar() -> str:
    return "\n".join(
        [
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
        ]
    )


def renderizar_creditos() -> str:
    return "\n".join(
        [
            "Creditos",
            "",
            "Projeto: Super Jogo da Velha",
            "Desenvolvimento: Eduardo Aran",
        ]
    )


def renderizar_historico() -> str:
    return "\n".join(
        [
            "Historico de Jogos",
            "",
            "Historico ainda nao implementado.",
        ]
    )


def renderizar_conquistas() -> str:
    return "\n".join(
        [
            "Conquistas",
            "",
            "Conquistas ainda nao implementadas.",
        ]
    )


def opcao_menu_valida(valor: str) -> bool:
    return any(codigo == valor for codigo, _ in OPCOES_MENU)


def ler_opcao_menu() -> str:
    entrada = input("> ").strip()

    if not opcao_menu_valida(entrada):
        raise ValueError("Opcao invalida. Escolha uma opcao do menu.")

    return entrada


def mostrar_tela(conteudo: str) -> None:
    limpar_tela()
    print(conteudo)
    print()
    input("Pressione Enter para voltar ao menu.")


def mostrar_mensagem(mensagem: str) -> None:
    limpar_tela()
    print(mensagem)
    input("Pressione Enter para voltar ao menu.")


def limpar_tela() -> None:
    os.system("cls" if os.name == "nt" else "clear")
