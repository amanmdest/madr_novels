from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr_novels.database import get_session
from madr_novels.models import Livro, Romancista, Usuario
from madr_novels.schemas import (
    FiltroPag,
    LivroAtualiza,
    LivroEntrada,
    LivroSaida,
    LivrosLista,
    Mensagem,
)
from madr_novels.security import pegar_usuario_autorizado
from madr_novels.utils.sanitizador import sanitiza

router = APIRouter(prefix='/livros', tags=['livros'])

T_FiltroPag = Annotated[FiltroPag, Query()]
T_Session = Annotated[Session, Depends(get_session)]
T_UsuarioAutorizado = Annotated[Usuario, Depends(pegar_usuario_autorizado)]


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=LivroSaida,
)
def novo_livro(
    livro: LivroEntrada,
    session: T_Session,
    usuario_autorizado: T_UsuarioAutorizado,
):
    db_livro = session.scalar(
        select(Livro).where(Livro.titulo == sanitiza(livro.titulo))
    )
    db_romancista = session.scalar(
        select(Romancista).where(Romancista.id == livro.romancista_id)
    )

    if not db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não existe no acervo.',
        )

    if db_livro:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Livro já cadastrado no acervo bb! ;D',
        )

    livro = Livro(
        titulo=sanitiza(livro.titulo),
        ano=livro.ano,
        romancista_id=livro.romancista_id,
    )

    session.add(livro)
    session.commit()
    session.refresh(livro)

    return livro


@router.get('/', status_code=HTTPStatus.OK, response_model=LivrosLista)
def livros(filtro_pag: T_FiltroPag, session: T_Session):
    livros = session.scalars(
        select(Livro).limit(filtro_pag.limit).offset(filtro_pag.offset)
    )
    return {'livros': livros}


@router.get(
    '/{livro_id}', status_code=HTTPStatus.OK, response_model=LivroSaida
)
def livro_por_id(livro_id: int, session: T_Session): ...


@router.patch(
    '/{livro_id}', status_code=HTTPStatus.OK, response_model=LivroSaida
)
def atualizar_livro(
    livro_id: int,
    livro: LivroAtualiza,
    session: T_Session,
    usuario_autorizado: T_UsuarioAutorizado,
):
    db_livro = session.scalar(select(Livro).where(Livro.id == livro_id))

    db_livro_title = session.scalar(
        select(Livro).where(Livro.titulo == sanitiza(livro.titulo))
    )

    db_romancista = session.scalar(
        select(Romancista).where(Romancista.id == livro.romancista_id)
    )

    if db_livro_title:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Livro já cadastrado no acervo bb! ;D',
        )

    if not db_livro:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro não encontrado no acervo.',
        )

    if not db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não encontrado no acervo.',
        )

    if livro.titulo:
        db_livro.titulo = sanitiza(livro.titulo)
    if livro.ano:
        db_livro.ano = livro.ano
    if livro.romancista_id:
        db_livro.romancista_id = livro.romancista_id

    session.commit()
    session.refresh(db_livro)

    return db_livro


@router.delete('/{livro_id}', response_model=Mensagem)
def deletar_livro(
    livro_id: int, session: T_Session, usuario_autorizado: T_UsuarioAutorizado
):
    db_livro = session.scalar(select(Livro).where(Livro.id == livro_id))

    if not db_livro:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro não encontrado no acervo.',
        )

    session.delete(db_livro)
    session.commit()

    return {'mensagem': f'Livro {db_livro.titulo} deletadao'}
