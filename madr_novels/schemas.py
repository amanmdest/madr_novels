from pydantic import BaseModel, ConfigDict, EmailStr


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
    model_config = ConfigDict(from_attributes=True)


class UsuarioLista(BaseModel):
    usuarios: list[UsuarioSaida]


class RomancistaEntrada(BaseModel):
    nome: str


class RomancistaSaida(BaseModel):
    id: int
    livros: list


class RomancistasLista(BaseModel):
    romancistas: list[RomancistaSaida]


class LivroEntrada(BaseModel):
    titulo: str
    ano: int
    romancista_id: int


class LivroSaida(BaseModel):
    id: int


class LivrosLista(BaseModel):
    livros: list[LivroSaida]
