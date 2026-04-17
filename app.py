import os

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


def main() -> None:
    """Executa uma partida simples no terminal."""
    jogo = MotorJogo()
    mensagem: str = ""

    while not jogo.finalizado:
        limpar_tela()

        print("Super Jogo da Velha")
        print("Mini tabuleiros: 1 a 9")
        print("Posicoes dentro do mini: 1 a 9")
        print("Mapa das posicoes:")
        print("1 2 3")
        print("4 5 6")
        print("7 8 9")
        print()

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
    print("Super Jogo da Velha")
    print()
    print_jogo(jogo)
    print()

    if jogo.vencedor is not None:
        print(f"Fim de jogo. Vencedor: {jogo.vencedor}")
    else:
        print("Fim de jogo.")

    if mensagem:
        print(mensagem)


if __name__ == "__main__":
    main()