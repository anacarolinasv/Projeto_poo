class ExcecaoAplicacao(Exception):
    """Exceção base da aplicação."""


class EntidadeInvalidaError(ExcecaoAplicacao, ValueError):
    """Dados inválidos em uma entidade de domínio."""


class RegraNegocioError(ExcecaoAplicacao, ValueError):
    """Violação de regra de negócio da aplicação."""
