import pytest
from fastapi.testclient import TestClient

from app.api import routes
from app.services.game_service import PartidaService


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setattr(routes, "partida_service", PartidaService())
    return TestClient(routes.app)


def iniciar_partida(client: TestClient) -> dict:
    resposta = client.post(
        "/game/start",
        json={
            "jogador_1": {"nome": "Alice", "simbolo": "X"},
            "jogador_2": {"nome": "Bruno", "simbolo": "O"},
        },
    )

    assert resposta.status_code == 200
    return resposta.json()


def test_start_inicia_partida_e_retorna_estado(client: TestClient) -> None:
    estado = iniciar_partida(client)

    assert estado["jogador_atual"] == "Alice"
    assert estado["finalizado"] is False
    assert estado["mini_obrigatorio"] is None
    assert estado["vencedor"] is None
    assert estado["jogador_1"]["simbolo"] == "X"
    assert len(estado["tabuleiro"]) == 9


def test_move_realiza_jogada_e_atualiza_estado(client: TestClient) -> None:
    iniciar_partida(client)

    resposta = client.post(
        "/game/move",
        json={"mini_id": 0, "linha": 0, "coluna": 0},
    )
    estado = resposta.json()

    assert resposta.status_code == 200
    assert estado["jogador_atual"] == "Bruno"
    assert estado["mini_obrigatorio"] == 0
    assert estado["tabuleiro"][0][0][0] == "X"


def test_state_retorna_partida_atual(client: TestClient) -> None:
    iniciar_partida(client)
    client.post("/game/move", json={"mini_id": 0, "linha": 0, "coluna": 0})

    resposta = client.get("/game/state")
    estado = resposta.json()

    assert resposta.status_code == 200
    assert estado["jogador_atual"] == "Bruno"
    assert estado["tabuleiro"][0][0][0] == "X"


def test_move_sem_partida_retorna_http_400(client: TestClient) -> None:
    resposta = client.post(
        "/game/move",
        json={"mini_id": 0, "linha": 0, "coluna": 0},
    )

    assert resposta.status_code == 400
    assert resposta.json()["detail"] == "Nenhuma partida foi iniciada."


def test_jogada_invalida_retorna_http_400(client: TestClient) -> None:
    iniciar_partida(client)
    client.post("/game/move", json={"mini_id": 0, "linha": 0, "coluna": 0})

    resposta = client.post(
        "/game/move",
        json={"mini_id": 1, "linha": 0, "coluna": 0},
    )

    assert resposta.status_code == 400
    assert resposta.json()["detail"] == "Jogada invalida."
