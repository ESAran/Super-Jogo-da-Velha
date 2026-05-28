from dataclasses import dataclass


@dataclass(frozen=True)
class JogadorEntrada:
    nome: str
    simbolo: str


@dataclass(frozen=True)
class JogadaEntrada:
    mini_id: int
    linha: int
    coluna: int


@dataclass(frozen=True)
class EstadoPartida:
    jogador_atual: str
    finalizado: bool
    mini_obrigatorio: int | None
    vencedor: str | None
