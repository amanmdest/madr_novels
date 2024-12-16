from http import HTTPStatus


def test_deve_retornar_ok_e_gracias(cliente):
    response = cliente.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'mensagem': 'gracias a caetano por invitar-me!'}
