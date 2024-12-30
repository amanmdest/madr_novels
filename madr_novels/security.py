from pwdlib import PasswordHash  # type: ignore

pwd_context = PasswordHash.recommended()


def senha_hash(senha: str):
    return pwd_context.hash(senha)


def verificar_senha(senha_crua: str, senha_hash: str):
    return pwd_context.verify(senha_crua, senha_hash)
