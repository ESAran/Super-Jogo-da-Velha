from dataclasses import dataclass

from app.services.cli import (
    OPCOES_MENU as OPCOES_MENU_DADOS,
    ler_opcao_menu,
    opcao_menu_valida,
    renderizar_menu_principal,
)


@dataclass(frozen=True)
class OpcaoMenu:
    codigo: str
    titulo: str


def obter_opcoes_menu() -> list[OpcaoMenu]:
    return [OpcaoMenu(codigo, titulo) for codigo, titulo in OPCOES_MENU_DADOS]


OPCOES_MENU = obter_opcoes_menu()


__all__ = [
    "OPCOES_MENU",
    "OpcaoMenu",
    "ler_opcao_menu",
    "obter_opcoes_menu",
    "opcao_menu_valida",
    "renderizar_menu_principal",
]
