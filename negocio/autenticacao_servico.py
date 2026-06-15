from administradores.administrador import AdministradorDAO
from clientes.cliente import ClienteDAO
from negocio.entregador_servico import EntregadorServico

class AutenticacaoServico: # caso de uso: autenticar um administrador, cliente ou entregador
    #--------- Constructor ---------#
    def __init__(self):
        self._dao_admin = AdministradorDAO() # DAO encapsula leitura/gravacao em administradores.json (lista de administradores)
        self._dao_cliente = ClienteDAO() # DAO encapsula leitura/gravacao em clientes.json (lista de clientes)
        self._entregador_servico = EntregadorServico() # autentica entregadores cadastrados

    def login_admin(self, login, senha): # autenticar um administrador
        # Nao aceita login ou senha em branco, levanta um erro.
        if not (login or "").strip() or not (senha or "").strip():
            raise ValueError("Login ou senha inválidos.")
        # Buscar_por_login rele o arquivo e compara login em minusculas (ver AdministradorDAO).
        adm = self._dao_admin.Buscar_por_login(login)
        # Mesma mensagem para "usuario inexistente" e "senha errada" (nao vaza se o login existe).
        if adm is None or adm.get_senha() != senha:
            raise ValueError("Login ou senha inválidos.")
        return adm

    def login_cliente(self, email, senha): # autenticar um cliente
        # Nao aceita email ou senha em branco, levanta um erro.
        if not (email or "").strip() or not (senha or "").strip():
            raise ValueError("E-mail ou senha inválidos.")

        c = self._dao_cliente.Listar_por_email(email) # buscar um cliente pelo email

        if c is None or c.get_senha() == "": # se o cliente não for encontrado ou a senha estiver em branco, levanta um erro
            raise ValueError("E-mail ou senha inválidos.")

        if c.get_senha() != senha: # se a senha do cliente for diferente da senha passada, levanta um erro
            raise ValueError("E-mail ou senha inválidos.")
        # Se a senha do cliente for igual à senha passada, retorna o cliente
        return c

    def autenticar(self, login_ou_email, senha):
        login_normalizado = (login_ou_email or "").strip()
        senha_normalizada = (senha or "").strip()
        if not login_normalizado or not senha_normalizada:
            return None
        try:
            self.login_admin(login_normalizado, senha_normalizada)
            return {"id": 1, "nome": "admin", "admin": True, "tipo": "admin"}
        except ValueError:
            pass
        entregador = self._entregador_servico.autenticar(
            login_normalizado, senha_normalizada
        )
        if entregador is not None:
            return {
                "id": entregador.get_id(),
                "nome": entregador.get_nome(),
                "admin": False,
                "tipo": "entregador",
            }
        try:
            cliente = self.login_cliente(login_normalizado, senha_normalizada)
            return {
                "id": cliente.get_id(),
                "nome": cliente.get_nome(),
                "admin": False,
                "tipo": "cliente",
            }
        except ValueError:
            return None
