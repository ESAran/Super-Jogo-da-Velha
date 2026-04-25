import os

from src.domain.jogador import Jogador, TipoJogador
from src.services.motor_jogo import MotorJogo
from src.ui.cli.renderer import print_jogo


def limpar_tela() -> None:
    """Limpa o terminal."""
    os.system("cls" if os.name == "nt" else "clear")


def posicao_para_coordenadas(posicao: int) -> tuple[int, int]:
    """Converte uma posição de 1 a 9 para linha e coluna."""
    if not 1 <= posicao <= 9:
        raise ValueError("A posicao deve estar entre 1 e 9.")

    indice: int = posicao - 1
    linha: int = indice // 3
    coluna: int = indice % 3
    return linha, coluna


def ler_numero(mensagem: str) -> int | None:
    """Lê um número inteiro ou retorna None se o usuário quiser sair."""
    entrada: str = input(mensagem).strip()

    if entrada.lower() == "sair":
        return None

    try:
        return int(entrada)
    except ValueError as erro:
        raise ValueError("Digite um numero inteiro valido.") from erro


def ler_texto(mensagem: str) -> str | None:
    """Lê um texto ou retorna None se o usuário quiser sair."""
    entrada: str = input(mensagem).strip()

    if entrada.lower() == "sair":
        return None

    return entrada


def cadastrar_jogador(
    numero: int,
    simbolos_indisponiveis: set[str] | None = None,
) -> Jogador | None:
    """Lê e valida os dados de um jogador humano."""
    while True:
        print(f"Cadastro do jogador {numero}:")

        nome = ler_texto("Nome: ")
        if nome is None:
            return None

        simbolo = ler_texto("Simbolo: ")
        if simbolo is None:
            return None

        try:
            jogador = Jogador(
                nome=nome,
                simbolo=simbolo,
                tipo=TipoJogador.HUMANO,
            )

            if simbolos_indisponiveis and jogador.simbolo in simbolos_indisponiveis:
                raise ValueError("Esse simbolo ja foi escolhido pelo outro jogador.")

            return jogador

        except ValueError as erro:
            print(f"Erro: {erro}")
            print()


def cadastrar_jogadores() -> tuple[Jogador, Jogador] | None:
    """Realiza o cadastro dos dois jogadores da partida."""
    limpar_tela()
    print("Ϩ𐌵ⲣⲉꞅ 𝓙ⲟ𝓰ⲟ ⲇⲁ 𝓥ⲉ𝓵ⲏⲁ")
    print("=̷=̷===̷===̷=̷===̷===̷=̷===̷=̷===̷=̷===̷=̷===̷===̷=̷===̷==")
    print()
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


def ler_jogada(jogo: MotorJogo) -> tuple[int, int, int] | None:
    """Lê a jogada respeitando o mini tabuleiro obrigatório."""
    if jogo.mini_obrigatorio is None:
        mini_escolhido: int | None = ler_numero(
            "Escolha o mini tabuleiro (1-9) ou digite 'sair': "
        )
        if mini_escolhido is None:
            return None

        if not 1 <= mini_escolhido <= 9:
            raise ValueError("O mini tabuleiro deve estar entre 1 e 9.")

        mini_id: int = mini_escolhido - 1

        if jogo.tabuleiro.mini_esta_encerrado(mini_id):
            raise ValueError(
                f"O mini tabuleiro {mini_escolhido} ja foi encerrado. Escolha outro."
            )
    else:
        mini_id = jogo.mini_obrigatorio
        print(f"Voce deve jogar no mini tabuleiro {mini_id + 1}.")

    posicao: int | None = ler_numero(
        "Escolha a posicao dentro do mini tabuleiro (1-9) ou digite 'sair': "
    )
    if posicao is None:
        return None

    linha, coluna = posicao_para_coordenadas(posicao)
    return mini_id, linha, coluna


def exibir_legenda_jogadores(jogo: MotorJogo) -> None:
    """Mostra os jogadores cadastrados antes do tabuleiro."""
    print(f"Jogador 1: {jogo.jogador_1.nome} ({jogo.jogador_1.simbolo})")
    print(f"Jogador 2: {jogo.jogador_2.nome} ({jogo.jogador_2.simbolo})")
    print()


def executar_partida() -> None:
    """Executa uma partida jogador vs jogador no terminal."""
    jogadores = cadastrar_jogadores()
    if jogadores is None:
        limpar_tela()
        print("Cadastro cancelado pelo usuario.")
        return

    jogador_1, jogador_2 = jogadores
    jogo = MotorJogo(jogador_1, jogador_2)
    mensagem: str = ""

    while not jogo.finalizado:
        limpar_tela()

        print("Ϩ𐌵ⲣⲉꞅ 𝓙ⲟ𝓰ⲟ ⲇⲁ 𝓥ⲉ𝓵ⲏⲁ")
        print("=̷=̷===̷===̷=̷===̷===̷=̷===̷=̷===̷=̷===̷=̷===̷===̷=̷===̷==")
        print()
        print("Mini tabuleiros: 1 a 9")
        print("Posições dentro do mini: 1 a 9")
        print()
        print("Mapa das posições:")
        print("1 2 3")
        print("4 5 6")
        print("7 8 9")
        print()

        exibir_legenda_jogadores(jogo)
        print_jogo(jogo)

        if mensagem:
            print()
            print(mensagem)

        print()

        try:
            jogada = ler_jogada(jogo)

            if jogada is None:
                limpar_tela()
                print("Jogo encerrado pelo usuario.")
                return

            mini_id, linha, coluna = jogada
            jogo.jogar(mini_id, linha, coluna)
            mensagem = ""

        except ValueError as erro:
            mensagem = f"Erro: {erro}"

    limpar_tela()
    print("Ϩ𐌵ⲣⲉꞅ 𝓙ⲟ𝓰ⲟ ⲇⲁ 𝓥ⲉ𝓵ⲏⲁ")
    print("=̷=̷===̷===̷=̷===̷===̷=̷===̷=̷===̷=̷===̷=̷===̷===̷=̷===̷==")
    print()
    exibir_legenda_jogadores(jogo)
    print_jogo(jogo)
    print()

    if jogo.vencedor is not None:
        limpar_tela()
        print("Ϩ𐌵ⲣⲉꞅ 𝓙ⲟ𝓰ⲟ ⲇⲁ 𝓥ⲉ𝓵ⲏⲁ")
        print("=̷=̷===̷===̷=̷===̷===̷=̷===̷=̷===̷=̷===̷=̷===̷===̷=̷===̷==")
        print(f"""Fim de jogo. 
´´´´´´´´´´´´´´´´´´´´´´´´¶´´´´´´´´´¶´´´´´´´´´´´´´´´´´´´´´´´´´´
´´´´´´´´´´´´´´´´´´´´´´´´´¶´´´´´´´´´¶´´´´´´´´´´´´´´´´´´´´´´´´´
´´´´´´´´´´´´´´´´´´´´´¶´´´¶´´´´´´´´´¶´´´¶´´´´´´´´´´´´´´´´´´´´´
´´´´´´´´´´´´´´´´´´´´´¶´´¶¶´´´´´´´´´¶¶´´¶´´´´´´´´´´´´´´´´´´´´´
´´´´´´´´´´´´´´´´´´´´´¶¶´¶¶¶´´´´´´´¶¶¶´¶¶´´´´´´´´´´´´´´´´´´´´´
´´´´´´´´´´´´´¶´´´´´´¶¶´´´¶¶¶´´´´´¶¶¶´´´¶¶´´´´´´¶´´´´´´´´´´´´´
´´´´´´´´´´´´¶¶´´´´´´¶¶´´´¶¶¶´´´´´¶¶¶´´´¶¶´´´´´´¶¶´´´´´´´´´´´´
´´´´´´´´´´´¶¶´´´´´´¶¶´´´´¶¶¶¶´´´¶¶¶¶´´´´¶¶´´´´´´¶¶´´´´´´´´´´´
´´´´´´´´´´´¶¶´´´´´¶¶¶´´´´¶¶¶¶´´¶¶¶¶¶´´´´¶¶¶´´´´´¶¶¶´´´´´´´´´´
´´´´´´´¶´´¶¶¶´´´´¶¶¶¶´´´´¶¶¶¶´´´¶¶¶¶´´´´¶¶¶¶´´´¶¶¶¶´´¶´´´´´´´
´´´´´´´¶¶´¶¶¶¶¶´´¶¶¶¶´´´¶¶¶¶¶´´´¶¶¶¶¶´´´¶¶¶¶´´¶¶¶¶¶´¶¶´´´´´´´
´´´´´´´¶¶´¶¶¶¶¶´´¶¶¶¶¶¶¶¶¶¶¶´´´´´¶¶¶¶¶¶¶¶¶¶¶´´¶¶¶¶¶´¶¶´´´´´´´
´´´´´´´¶¶´¶¶¶¶¶´´¶¶¶¶¶¶¶¶¶¶¶´´´´´¶¶¶¶¶¶¶¶¶¶¶´´¶¶¶¶¶´¶¶´´´´´´´
´´´´´´¶¶¶´´¶¶¶¶´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´¶¶¶¶´´¶¶¶´´´´´´
´´´´´¶¶¶¶´´¶¶¶¶´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´¶¶¶¶´´¶¶¶¶´´´´´
´´´´¶¶¶¶´´´¶¶¶¶¶´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´¶¶¶¶¶´´´¶¶¶¶´´´´
´´´¶¶¶¶´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´¶¶¶¶´´´´
´´´¶¶¶¶¶´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´¶¶¶¶´´´´
´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´´
´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´´
´´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´´´
´´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´´´
´´´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´´´´
´´´´´¶¶¶¶¶´´´´´´´´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´´´´´´´´´¶¶¶¶¶´´´´´
´´´´´¶¶¶¶¶¶´´´´´´´´´´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶´´´´´´´´´´´´´¶¶¶¶¶¶´´´´´
´´´´´´¶¶¶¶¶¶¶´´´´´´´´..´´´´´¶¶¶¶¶¶¶¶¶´´´´´..´´´´´´´´¶¶¶¶¶¶´´´´´
´´´´´´´¶¶¶¶¶¶¶¶´´´´´´´´´´´´´¶¶¶¶¶´´´´´´´´´´´´´¶¶¶¶¶¶¶¶´´´´´´´
´´´´´´´´¶¶¶¶¶¶¶¶¶¶´´´´´´´´´´´¶¶¶´´´´´´´´´´´¶¶¶¶¶¶¶¶¶¶´´´´´´´´
´´´´´´´´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´´´´´´´´´
´´´´´´´´´´´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´´´´´´´´´´´´
´´´´´´´´´´´´´´´´´´¶¶¶¶¶¶¶¶¶¶´´´´´¶¶¶¶¶¶¶¶¶¶´´´´´´´´´´´´´´´´´´
´´´´´´´´´´´´´´´´´´´¶¶¶¶¶¶¶¶´´´´´´´¶¶¶¶¶¶¶¶´´´´´´´´´´´´´´´´´´´
´´´´´´´´´´´´´´´´´´¶¶¶¶¶¶¶¶¶´´´´´´´¶¶¶¶¶¶¶¶¶´´´´´´´´´´´´´´´´´´
´´´´´´´´´´´´´´´´´´¶¶¶¶¶¶¶¶¶´¶¶¶¶¶´¶¶¶¶¶¶¶¶¶´´´´´´´´´´´´´´´´´´
´´´´´´´´´´´´´´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´´´´´´´´´´´´´´´
´´´´´´´´´´´´´´´´´¶¶¶´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´¶¶¶´´´´´´´´´´´´´´´´´
´´´´´´´´´´´´´´´´´´¶¶´´¶¶¶¶´´¶¶¶¶¶´´¶¶¶¶´´¶¶´´´´´´´´´´´´´´´´´´
´´´´´´´´´´´´´´´´´´´´´´¶¶¶¶´´¶¶¶¶¶´´¶¶¶¶´´´´´´´´´´´´´´´´´´´´´
        Vencedor: """
            f"{jogo.vencedor.nome} ({jogo.vencedor.simbolo})"
        )
    else:
        limpar_tela()
        print("Ϩ𐌵ⲣⲉꞅ 𝓙ⲟ𝓰ⲟ ⲇⲁ 𝓥ⲉ𝓵ⲏⲁ")
        print("=̷=̷===̷===̷=̷===̷===̷=̷===̷=̷===̷=̷===̷=̷===̷===̷=̷===̷==")
        print(f"""Fim de jogo. 
´´´´´´´´´´´´´´´´´´´´´´´´¶´´´´´´´´´¶´´´´´´´´´´´´´´´´´´´´´´´´´´
´´´´´´´´´´´´´´´´´´´´´´´´´¶´´´´´´´´´¶´´´´´´´´´´´´´´´´´´´´´´´´´
´´´´´´´´´´´´´´´´´´´´´¶´´´¶´´´´´´´´´¶´´´¶´´´´´´´´´´´´´´´´´´´´´
´´´´´´´´´´´´´´´´´´´´´¶´´¶¶´´´´´´´´´¶¶´´¶´´´´´´´´´´´´´´´´´´´´´
´´´´´´´´´´´´´´´´´´´´´¶¶´¶¶¶´´´´´´´¶¶¶´¶¶´´´´´´´´´´´´´´´´´´´´´
´´´´´´´´´´´´´¶´´´´´´¶¶´´´¶¶¶´´´´´¶¶¶´´´¶¶´´´´´´¶´´´´´´´´´´´´´
´´´´´´´´´´´´¶¶´´´´´´¶¶´´´¶¶¶´´´´´¶¶¶´´´¶¶´´´´´´¶¶´´´´´´´´´´´´
´´´´´´´´´´´¶¶´´´´´´¶¶´´´´¶¶¶¶´´´¶¶¶¶´´´´¶¶´´´´´´¶¶´´´´´´´´´´´
´´´´´´´´´´´¶¶´´´´´¶¶¶´´´´¶¶¶¶´´¶¶¶¶¶´´´´¶¶¶´´´´´¶¶¶´´´´´´´´´´
´´´´´´´¶´´¶¶¶´´´´¶¶¶¶´´´´¶¶¶¶´´´¶¶¶¶´´´´¶¶¶¶´´´¶¶¶¶´´¶´´´´´´´
´´´´´´´¶¶´¶¶¶¶¶´´¶¶¶¶´´´¶¶¶¶¶´´´¶¶¶¶¶´´´¶¶¶¶´´¶¶¶¶¶´¶¶´´´´´´´
´´´´´´´¶¶´¶¶¶¶¶´´¶¶¶¶¶¶¶¶¶¶¶´´´´´¶¶¶¶¶¶¶¶¶¶¶´´¶¶¶¶¶´¶¶´´´´´´´
´´´´´´´¶¶´¶¶¶¶¶´´¶¶¶¶¶¶¶¶¶¶¶´´´´´¶¶¶¶¶¶¶¶¶¶¶´´¶¶¶¶¶´¶¶´´´´´´´
´´´´´´¶¶¶´´¶¶¶¶´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´¶¶¶¶´´¶¶¶´´´´´´
´´´´´¶¶¶¶´´¶¶¶¶´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´¶¶¶¶´´¶¶¶¶´´´´´
´´´´¶¶¶¶´´´¶¶¶¶¶´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´¶¶¶¶¶´´´¶¶¶¶´´´´
´´´¶¶¶¶´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´¶¶¶¶´´´´
´´´¶¶¶¶¶´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´¶¶¶¶´´´´
´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´´
´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´´
´´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´´´
´´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´´´
´´´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´´´´
´´´´´¶¶¶¶¶´´´´´´´´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´´´´´´´´´¶¶¶¶¶´´´´´
´´´´´¶¶¶¶¶¶´´´´´´´´´´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶´´´´´´´´´´´´´¶¶¶¶¶¶´´´´´
´´´´´´¶¶¶¶¶¶¶´´´´´´´´..´´´´´¶¶¶¶¶¶¶¶¶´´´´´..´´´´´´´´¶¶¶¶¶¶´´´´´
´´´´´´´¶¶¶¶¶¶¶¶´´´´´´´´´´´´´¶¶¶¶¶´´´´´´´´´´´´´¶¶¶¶¶¶¶¶´´´´´´´
´´´´´´´´¶¶¶¶¶¶¶¶¶¶´´´´´´´´´´´¶¶¶´´´´´´´´´´´¶¶¶¶¶¶¶¶¶¶´´´´´´´´
´´´´´´´´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´´´´´´´´´
´´´´´´´´´´´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´´´´´´´´´´´´
´´´´´´´´´´´´´´´´´´¶¶¶¶¶¶¶¶¶¶´´´´´¶¶¶¶¶¶¶¶¶¶´´´´´´´´´´´´´´´´´´
´´´´´´´´´´´´´´´´´´´¶¶¶¶¶¶¶¶´´´´´´´¶¶¶¶¶¶¶¶´´´´´´´´´´´´´´´´´´´
´´´´´´´´´´´´´´´´´´¶¶¶¶¶¶¶¶¶´´´´´´´¶¶¶¶¶¶¶¶¶´´´´´´´´´´´´´´´´´´
´´´´´´´´´´´´´´´´´´¶¶¶¶¶¶¶¶¶´¶¶¶¶¶´¶¶¶¶¶¶¶¶¶´´´´´´´´´´´´´´´´´´
´´´´´´´´´´´´´´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´´´´´´´´´´´´´´´
´´´´´´´´´´´´´´´´´¶¶¶´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´¶¶¶´´´´´´´´´´´´´´´´´
´´´´´´´´´´´´´´´´´´¶¶´´¶¶¶¶´´¶¶¶¶¶´´¶¶¶¶´´¶¶´´´´´´´´´´´´´´´´´´
´´´´´´´´´´´´´´´´´´´´´´¶¶¶¶´´¶¶¶¶¶´´¶¶¶¶´´´´´´´´´´´´´´´´´´´´´""")

    print()
    input("Pressione Enter para voltar ao menu.")