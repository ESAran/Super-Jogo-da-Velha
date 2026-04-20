from dataclasses import dataclass
from enum import Enum


class TipoJogador(Enum):
    HUMANO = "humano"
    MAQUINA = "maquina"


@dataclass
class Jogador:
    nome: str
    simbolo: str
    tipo: TipoJogador = TipoJogador.HUMANO

    def __post_init__(self) -> None:
        self.nome = self.nome.strip()
        self.simbolo = self.simbolo.strip().upper()

        if not self.nome:
            raise ValueError("O nome do jogador nao pode ser vazio.")

        if len(self.simbolo) != 1:
            raise ValueError("O simbolo do jogador deve ter exatamente 1 caractere.")

        if self.simbolo.isdigit():
            raise ValueError("O simbolo do jogador nao pode ser um numero.")