from pydantic import BaseModel, Field


class JogadorEntrada(BaseModel):
    nome: str = Field(..., min_length=1)
    simbolo: str = Field(..., min_length=1, max_length=1)


class JogadoresEntrada(BaseModel):
    jogador_1: JogadorEntrada
    jogador_2: JogadorEntrada


class JogadaEntrada(BaseModel):
    mini_id: int
    linha: int
    coluna: int


class JogadorSaida(BaseModel):
    nome: str
    simbolo: str
    tipo: str


class EstadoPartida(BaseModel):
    jogador_atual: str
    finalizado: bool
    mini_obrigatorio: int | None
    vencedor: str | None
    jogador_1: JogadorSaida
    jogador_2: JogadorSaida
    tabuleiro: list[list[list[str]]]
    resultado: list[list[str]]
