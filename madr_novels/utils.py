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


def verifica_usuario_existe(session, usuario):
    db_usuario = session.scalar(
        select(Usuario).where(
            (Usuario.username == usuario.username)
            | (Usuario.email == usuario.email)
            # or_(
            #     Usuario.username == usuario.username,
            #     Usuario.email == usuario.email,
            # )
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


def verifica_livro_existe_em_romancista(session, livro):
    db_livro = session.scalar(
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


def verifica_romancista_id_existe(session, livro):
    db_romancista = session.scalar(
        select(Romancista).where((Romancista.id == livro.romancista_id))
    )
    if not db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não encontrado no acervo',
        )
