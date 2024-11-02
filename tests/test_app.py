from http import HTTPStatus

from fastapi.testclient import TestClient

from madr_novels.app import app

client = TestClient(app)


def test_deve_retornar_ok_e_ola_mundo():
    response = client.get('/usuarios/home')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'mensagem': 'gracias a caetano por invitar-me'}
