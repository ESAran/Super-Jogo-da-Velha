from dataclasses import dataclass


@dataclass(frozen=True)
class OpcaoMenu:
    codigo: str
    titulo: str


OPCOES_MENU: list[OpcaoMenu] = [
    OpcaoMenu("1", "Jogador vs jogador"),
    OpcaoMenu("2", "Jogador vs maquina"),
    OpcaoMenu("3", "Como jogar"),
    OpcaoMenu("4", "Historico de jogos"),
    OpcaoMenu("5", "Creditos"),
    OpcaoMenu("6", "Conquistas"),
    OpcaoMenu("0", "Sair"),
]


def obter_opcoes_menu() -> list[OpcaoMenu]:
    """Retorna as opcoes do menu principal."""
    return OPCOES_MENU


def renderizar_menu_principal(mensagem: str = "") -> str:
    """Monta a tela do menu principal."""
    linhas: list[str] = [
        "Super Jogo da Velha",
        "",
        "Menu principal",
        "",
    ]

    for opcao in obter_opcoes_menu():
        linhas.append(f"{opcao.codigo}. {opcao.titulo}")

    if mensagem:
        linhas.append("")
        linhas.append(mensagem)

    linhas.append("")
    linhas.append("Escolha uma opcao:")

    return "\n".join(linhas)


def opcao_menu_valida(valor: str) -> bool:
    """Valida se a opcao informada existe no menu."""
    return any(opcao.codigo == valor for opcao in obter_opcoes_menu())


def ler_opcao_menu() -> str:
    """Le a opcao escolhida no menu principal."""
    entrada: str = input("> ").strip()

    if not opcao_menu_valida(entrada):
        raise ValueError("Opcao invalida. Escolha uma opcao do menu.")

    return entrada