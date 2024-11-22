from http import HTTPStatus

from fastapi import FastAPI

from madr_novels.routes import livros, romancistas, usuarios
from madr_novels.schemas import Mensagem

app = FastAPI(title='MADR')

app.include_router(usuarios.router)
app.include_router(romancistas.router)
app.include_router(livros.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Mensagem)
def home():
    return {'mensagem': 'gracias a caetano por invitar-me'}
