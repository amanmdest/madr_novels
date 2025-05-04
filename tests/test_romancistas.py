from http import HTTPStatus

from tests.factories import RomancistaFabrica


def test_novo_romancista(cliente, token):
    response = cliente.post(
        '/romancistas/',
        json={'nome': 'Herman Melville'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'nome': 'Herman Melville',
        'livros': [],
    }


def test_romancista_ja_cadastrado_no_acervo(cliente, sessao, token):
    romancista = RomancistaFabrica()
    sessao.add(romancista)
    sessao.commit()
    sessao.refresh(romancista)
    response = cliente.post(
        '/romancistas/',
        json={'nome': romancista.nome},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': 'Romancista já cadastrado no acervo bb! ;D'
    }


def test_listar_romancistas(cliente):
    response = cliente.get('/romancistas/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'romancistas': []}


# def test_romancista_por_id(cliente, romancista):
#     response = cliente.get(f'/romancistas/{romancista.id}')
#
#     assert response.status_code == HTTPStatus.OK
#     assert response.json() == {'romancista': romancista}


# def test_romancista_por_id_errado(cliente):
#     response = cliente.get('/romancistas/666')
#
#     assert response.status_code == HTTPStatus.OK
#     assert response.json() == {'romancista': romancista}


def test_atualizar_romancista(cliente, sessao, token):
    romancista = RomancistaFabrica()
    sessao.add(romancista)
    sessao.commit()
    sessao.refresh(romancista)
    response = cliente.put(
        f'/romancistas/{romancista.id}',
        json={'nome': 'Clarice Lispector'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': romancista.id,
        'nome': romancista.nome,
        'livros': [],
    }


def test_atualizar_romancista_nao_encontrado(cliente, token):
    # romancista = RomancistaFabrica()
    # sessao.add(romancista)
    # sessao.commit()
    # sessao.refresh(romancista)
    response = cliente.put(
        '/romancistas/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        'detail': 'Romancista não encontrado no acervo.'
    }


def test_deletar_romancista(cliente, sessao, token):
    romancista = RomancistaFabrica()
    sessao.add(romancista)
    sessao.commit()
    sessao.refresh(romancista)
    response = cliente.delete(
        f'/romancistas/{romancista.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == f'Romancista {romancista.nome} deletadao'
