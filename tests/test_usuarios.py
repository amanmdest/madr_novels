from http import HTTPStatus


def test_criar_usuario(cliente):
    response = cliente.post(
        '/usuarios/',
        json={
            'username': 'jusant',
            'email': 'hermoso@juego.com',
            'senha': 'jusant',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'jusant',
        'email': 'hermoso@juego.com',
        'id': 1,
    }


# def test_criar_usuario_username_repetido(cliente):
#     response = cliente.post(
#         '/usuarios/',
#         json={
#             'username': 'jusant',
#             'email': 'hermoso@juego.com',
#             'senha': 'naosei',
#         },
#     )
#
#     assert response.status_code == HTTPStatus.BAD_REQUEST
#     assert response.detail == {'Username já existe'}
#
#
# def test_criar_usuario_email_repetido(cliente): ...
#
