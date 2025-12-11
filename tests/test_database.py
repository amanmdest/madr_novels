import pytest
from sqlalchemy import select

from madr_novels.models import Usuario


@pytest.mark.asyncio
async def test_criar_usuario(sessao):
    novo_usuario = Usuario(
        username='alice', senha='secret', email='teste@teste.com'
    )
    sessao.add(novo_usuario)
    await sessao.commit()

    usuario = await sessao.scalar(
        select(Usuario).where(Usuario.username == 'alice')
    )

    assert usuario.username == 'alice'
