from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from madr_novels.database import get_session
from madr_novels.models import Romancista, Usuario
from madr_novels.schemas import (
    FiltroPag,
    RomancistaAtualizado,
    RomancistaEntrada,
    RomancistaSaida,
    RomancistasLista,
)
from madr_novels.security import pegar_usuario_autorizado
from madr_novels.utils import sanitiza_string

router = APIRouter(prefix='/romancistas', tags=['romancistas'])

T_FiltroPag = Annotated[FiltroPag, Query()]
T_Sessao = Annotated[AsyncSession, Depends(get_session)]
T_UsuarioAutorizado = Annotated[Usuario, Depends(pegar_usuario_autorizado)]


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=RomancistaSaida,
)
async def novo_romancista(
    romancista: RomancistaEntrada,
    sessao: T_Sessao,
    usuario_autorizado: T_UsuarioAutorizado,
):
    romancista.nome = sanitiza_string(romancista.nome)

    if not romancista.nome:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='É preciso preencher todos os campos',
        )

    db_romancista = await sessao.scalar(
        select(Romancista).where(Romancista.nome == romancista.nome)
    )

    if db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Romancista já cadastrado no acervo bb! ;D',
        )

    romancista = Romancista(nome=romancista.nome)

    sessao.add(romancista)
    await sessao.commit()
    await sessao.refresh(romancista)

    return romancista


@router.get('/', status_code=HTTPStatus.OK, response_model=RomancistasLista)
async def romancistas(filtro_pag: T_FiltroPag, sessao: T_Sessao):
    romancistas = await sessao.scalars(
        select(Romancista).limit(filtro_pag.limit).offset(filtro_pag.offset)
    )

    return {'romancistas': romancistas}


@router.get(
    '/{romancista_id}',
    status_code=HTTPStatus.OK,
    response_model=RomancistaSaida,
)
async def romancista_por_id(romancista_id: int, sessao: T_Sessao):
    db_romancista = await sessao.scalar(
        select(Romancista).where(Romancista.id == romancista_id)
    )

    if not db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não encontrado no acervo',
        )

    return db_romancista


@router.put(
    '/{romancista_id}',
    status_code=HTTPStatus.OK,
    response_model=RomancistaSaida,
)
async def atualizar_romancista(
    romancista_id: int,
    romancista: RomancistaAtualizado,
    sessao: T_Sessao,
    usuario_autorizado: T_UsuarioAutorizado,
):
    db_romancista = await sessao.scalar(
        select(Romancista).where(Romancista.id == romancista_id)
    )

    if not db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não encontrado no acervo',
        )

    db_romancista.nome = sanitiza_string(romancista.nome)

    await sessao.commit()
    await sessao.refresh(db_romancista)

    return db_romancista


@router.delete('/{romancista_id}', status_code=HTTPStatus.OK)
async def deletar_romancista(
    romancista_id: int,
    sessao: T_Sessao,
    usuario_autorizado: T_UsuarioAutorizado,
):
    db_romancista = await sessao.scalar(
        select(Romancista).where(Romancista.id == romancista_id)
    )

    if not db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'{romancista_id} não encontrado no acervo',
        )

    await sessao.delete(db_romancista)
    await sessao.commit()

    return f'Romancista {db_romancista.nome} deletado'
