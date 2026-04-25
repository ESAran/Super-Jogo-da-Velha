from src.ui.cli.jogo_cli import limpar_tela, executar_partida
from src.ui.cli.menu import ler_opcao_menu, renderizar_menu_principal
from src.ui.cli.telas import (
    mostrar_como_jogar,
    mostrar_conquistas,
    mostrar_creditos,
    mostrar_historico,
)


def executar_aplicacao() -> None:
    """Controla o fluxo principal da aplicacao CLI."""
    mensagem: str = ""

    while True:
        limpar_tela()
        print(renderizar_menu_principal(mensagem))

        try:
            opcao = ler_opcao_menu()
            mensagem = ""

            if opcao == "1":
                executar_partida()
            elif opcao == "2":
                limpar_tela()
                print("Modo jogador vs maquina ainda nao implementado.")
                input("Pressione Enter para voltar ao menu.")
            elif opcao == "3":
                limpar_tela()
                mostrar_como_jogar()
            elif opcao == "4":
                limpar_tela()
                mostrar_historico()
            elif opcao == "5":
                limpar_tela()
                mostrar_creditos()
            elif opcao == "6":
                limpar_tela()
                mostrar_conquistas()
            elif opcao == "0":
                return

        except ValueError as erro:
            mensagem = f"Erro: {erro}"