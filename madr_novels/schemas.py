from pydantic import BaseModel, EmailStr


class Mensagem(BaseModel):
    mensagem: str


class UsuarioEntrada(BaseModel):
    username: str
    email: EmailStr
    senha: str


class UsuarioSaida(BaseModel):
    id: int
    username: str
    email: EmailStr


class UsuarioDB(UsuarioEntrada):
    id: int


class UsuarioLista(BaseModel):
    users: list[UsuarioSaida]


class RomancistaEntrada(BaseModel):
    nome: str


class RomancistaSaida(BaseModel):
    id: int


class RomancistasLista(BaseModel):
    romancistas: list[RomancistaSaida]


class LivroEntrada(BaseModel):
    titulo: str
    ano: int
    romancista_id: int


class LivroSaida(BaseModel):
    id: int


class LivrosLista(BaseModel):
    livros: list[RomancistaSaida]
