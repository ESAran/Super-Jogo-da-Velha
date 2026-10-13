from fastapi import APIRouter, FastAPI, HTTPException

from app.schemas.game import EstadoPartida, JogadaEntrada, JogadoresEntrada
from app.services.game_service import PartidaService


app = FastAPI(title="Super Jogo da Velha API")
router = APIRouter(prefix="/game", tags=["game"])
partida_service = PartidaService()


@router.post("/start", response_model=EstadoPartida)
def iniciar_partida(entrada: JogadoresEntrada) -> EstadoPartida:
    try:
        return partida_service.iniciar_partida(entrada)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro


@router.post("/move", response_model=EstadoPartida)
def realizar_jogada(entrada: JogadaEntrada) -> EstadoPartida:
    try:
        return partida_service.realizar_jogada(entrada)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro


@router.get("/state", response_model=EstadoPartida)
def obter_estado() -> EstadoPartida:
    try:
        return partida_service.obter_estado()
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro


app.include_router(router)
