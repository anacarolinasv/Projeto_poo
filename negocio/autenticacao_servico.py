# DAO do administrador: busca por login no JSON (credenciais admin).
from administradores.administrador import AdministradorDAO
# DAO do cliente: busca por e-mail no cadastro de clientes.
from clientes.cliente import ClienteDAO


class AutenticacaoServico:
    """Regras de autenticacao (camada de negocio)."""

    def __init__(self):
        # Duas fontes de usuario: perfil admin e perfil cliente.
        self._dao_admin = AdministradorDAO()
        self._dao_cliente = ClienteDAO()

    def login_admin(self, login, senha):
        # Nao aceita login ou senha em branco (evita consulta inutil e mensagens ambiguas).
        if not (login or "").strip() or not (senha or "").strip():
            raise ValueError("Login ou senha invalidos.")
        # Buscar_por_login rele o arquivo e compara login em minusculas (ver AdministradorDAO).
        adm = self._dao_admin.Buscar_por_login(login)
        # Mesma mensagem para "usuario inexistente" e "senha errada" (nao vaza se o login existe).
        if adm is None or adm.get_senha() != senha:
            raise ValueError("Login ou senha invalidos.")
        return adm

    def login_cliente(self, email, senha):
        if not (email or "").strip() or not (senha or "").strip():
            raise ValueError("Email ou senha invalidos.")
        # Localiza cliente pelo e-mail cadastrado (chave logica do sistema).
        c = self._dao_cliente.Listar_por_email(email)
        # Conta inexistente ou registro sem senha tratados como falha de login generica.
        if c is None or c.get_senha() == "":
            raise ValueError("Email ou senha invalidos.")
        # Comparacao literal da senha armazenada (sem hash neste projeto didatico).
        if c.get_senha() != senha:
            raise ValueError("Email ou senha invalidos.")
        return c
