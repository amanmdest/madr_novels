# database
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select

from madr_novels.models import Livro, Romancista, Usuario


def sanitiza_string(string):
    sanitizado = ''
    for letra in string:
        if letra.isalnum() or letra.isspace():
            sanitizado += letra.lower()
    return ' '.join(sanitizado.split())


async def verifica_usuario_existe(sessao, usuario):
    db_usuario = await sessao.scalar(
        select(Usuario).where(
            (Usuario.username == usuario.username)
            | (Usuario.email == usuario.email)
        )
    )
    if db_usuario:
        if db_usuario.username == usuario.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Nome de usuário indisponível',
            )
        elif db_usuario.email == usuario.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email já está sendo utilizado',
            )


async def verifica_livro_existe_em_romancista(sessao, livro):
    db_livro = await sessao.scalar(
        select(Livro).where(
            (Livro.titulo == sanitiza_string(livro.titulo))
            & (Livro.romancista_id == (livro.romancista_id))
        )
    )
    if db_livro:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Livro já cadastrado no acervo bb! ;D',
        )


async def verifica_romancista_id_existe(sessao, livro):
    db_romancista = await sessao.scalar(
        select(Romancista).where((Romancista.id == livro.romancista_id))
    )
    if not db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não encontrado no acervo',
        )
