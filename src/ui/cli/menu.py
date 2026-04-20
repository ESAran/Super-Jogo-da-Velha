from dataclasses import dataclass


@dataclass(frozen=True)
class OpcaoMenu:
    codigo: str
    titulo: str


OPCOES_MENU: list[OpcaoMenu] = [
    OpcaoMenu("1", "JvJ        - Jogador vs Jogador"),
    OpcaoMenu("2", "JvM        - Jogador vs Maquina"),
    OpcaoMenu("3", "Regras     - Como jogar"),
    OpcaoMenu("4", "Partidas   - Historico de jogos"),
    OpcaoMenu("5", "Creditos   - Desenvolvedores"),
    OpcaoMenu("6", "Conquistas - Desafios concluidos"),
    OpcaoMenu("0", "Sair"),
]


def obter_opcoes_menu() -> list[OpcaoMenu]:
    """Retorna as opcoes do menu principal."""
    return OPCOES_MENU


def renderizar_menu_principal(mensagem: str = "") -> str:
    """Monta a tela do menu principal."""
    linhas: list[str] = [
        "Ϩ𐌵ⲣⲉꞅ 𝓙ⲟ𝓰ⲟ ⲇⲁ 𝓥ⲉ𝓵ⲏⲁ",
        "",
        "ᙏҽɳᥙ ρɾιɳ𝓬ιραɬ",
        "=̷=̷===̷===̷=̷===̷===̷=̷===̷=̷===̷=̷===̷=̷===̷===̷=̷===̷==",
    ]

    for opcao in obter_opcoes_menu():
        linhas.append(f"{opcao.codigo}. {opcao.titulo}")

    if mensagem:
        linhas.append("")
        linhas.append(mensagem)

    linhas.append("")
    linhas.append("Escolha uma opção:")

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