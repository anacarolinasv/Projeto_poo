import re

from excecoes.excecoes import EntidadeInvalidaError

_EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def validar_nome(nome):
    nome = (nome or "").strip()
    if not nome:
        raise EntidadeInvalidaError("Nome é obrigatório.")
    if len(nome) < 2:
        raise EntidadeInvalidaError("Nome deve ter pelo menos 2 caracteres.")
    return nome


def validar_email(email):
    email = (email or "").strip().lower()
    if not email:
        raise EntidadeInvalidaError("E-mail é obrigatório.")
    if not _EMAIL_RE.match(email):
        raise EntidadeInvalidaError("E-mail inválido.")
    return email


def validar_fone(fone):
    fone = (fone or "").strip()
    if not fone:
        raise EntidadeInvalidaError("Telefone é obrigatório.")
    digitos = re.sub(r"\D", "", fone)
    if len(digitos) < 10 or len(digitos) > 11:
        raise EntidadeInvalidaError(
            "Telefone inválido. Use DDD + número (10 ou 11 dígitos)."
        )
    return fone


def validar_senha(senha, obrigatoria=False):
    senha = senha if senha is not None else ""
    if obrigatoria and not senha:
        raise EntidadeInvalidaError("Senha é obrigatória.")
    if senha and len(senha) < 4:
        raise EntidadeInvalidaError("Senha deve ter pelo menos 4 caracteres.")
    return senha


def validar_descricao(descricao, campo="Descrição"):
    if not isinstance(descricao, str):
        raise EntidadeInvalidaError(f"{campo} deve ser texto.")
    descricao = descricao.strip()
    if not descricao:
        raise EntidadeInvalidaError(f"{campo} é obrigatória.")
    return descricao
