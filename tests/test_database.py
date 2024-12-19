from sqlalchemy import select

from madr_novels.models import Usuario


def test_criando_usuarios(sessao):
    novo_usuario = Usuario(
        username='alice', senha='secret', email='teste@teste.com'
    )
    sessao.add(novo_usuario)
    sessao.commit()

    usuario = sessao.scalar(select(Usuario).where(Usuario.username == 'alice'))

    assert usuario.username == 'alice'
