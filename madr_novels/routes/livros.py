from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr_novels.database import get_session
from madr_novels.models import Livro
from madr_novels.schemas import LivroEntrada, LivroSaida, LivrosLista

router = APIRouter(prefix='/livros', tags=['livros'])

T_session = Annotated[Session, Depends(get_session)]


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=LivroSaida,
)
def novo_livro(livro: LivroEntrada, session: T_session):
    db_livro = session.scalar(
        select(Livro).where(Livro.titulo == livro.titulo)
    )

    if db_livro:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Livro já cadastrado no acervo bb! ;D',
        )

    livro = Livro(
        titulo=livro.titulo, ano=livro.ano, romancista_id=livro.romancista_id
    )

    session.add(livro)
    session.commit()
    session.refresh(livro)

    return livro


@router.get('/', status_code=HTTPStatus.OK, response_model=LivrosLista)
def livros(session: T_session, limit: int = 10, skip: int = 0):
    livros = session.scalars(select(Livro).limit(limit).offset(skip))
    return {'livros': livros}


@router.get(
    '/{livro_id}', status_code=HTTPStatus.OK, response_model=LivroSaida
)
def livro_por_id(livro_id: int, session: T_session): ...


@router.put(
    '/{livro_id}', status_code=HTTPStatus.OK, response_model=LivroSaida
)
def atualizar_livro(livro_id: int, session: T_session):
    db_livro = session.scalar(select(Livro).where(Livro.id == livro_id))

    if not db_livro:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Não encontramos o livro no acervo.',
        )

    session.add(db_livro)
    session.commit()
    session.refresh(db_livro)

    return db_livro


@router.delete(
    '/{livro_id}',
    status_code=HTTPStatus.OK,
)
def deletar_livro(livro_id: int, session: T_session):
    db_livro = session.scalar(select(Livro).where(Livro.id == livro_id))

    if not db_livro:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Não encontramos o livro no acervo.',
        )

    session.delete(db_livro)
    session.commit()

    return db_livro
