from administradores.administrador import AdministradorDAO
from clientes.cliente import ClienteDAO


class AutenticacaoServico:
    """Regras de autenticacao (camada de negocio)."""

    def __init__(self):
        self._dao_admin = AdministradorDAO()
        self._dao_cliente = ClienteDAO()

    def login_admin(self, login, senha):
        if not (login or "").strip() or not (senha or "").strip():
            raise ValueError("Login ou senha invalidos.")
        adm = self._dao_admin.Buscar_por_login(login)
        if adm is None or adm.get_senha() != senha:
            raise ValueError("Login ou senha invalidos.")
        return adm

    def login_cliente(self, email, senha):
        if not (email or "").strip() or not (senha or "").strip():
            raise ValueError("Email ou senha invalidos.")
        c = self._dao_cliente.Listar_por_email(email)
        if c is None or c.get_senha() == "":
            raise ValueError("Email ou senha invalidos.")
        if c.get_senha() != senha:
            raise ValueError("Email ou senha invalidos.")
        return c
