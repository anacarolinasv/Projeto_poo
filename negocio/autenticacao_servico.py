from administradores.administrador import AdministradorDAO
from clientes.cliente import ClienteDAO

class AutenticacaoServico: # caso de uso: autenticar um administrador ou cliente
    #--------- Constructor ---------#
    def __init__(self):
        self._dao_admin = AdministradorDAO() # DAO encapsula leitura/gravacao em administradores.json (lista de administradores)
        self._dao_cliente = ClienteDAO() # DAO encapsula leitura/gravacao em clientes.json (lista de clientes)

    def login_admin(self, login, senha): # autenticar um administrador
        # Nao aceita login ou senha em branco, levanta um erro.
        if not (login or "").strip() or not (senha or "").strip():
            raise ValueError("Login ou senha invalidos.")
        # Buscar_por_login rele o arquivo e compara login em minusculas (ver AdministradorDAO).
        adm = self._dao_admin.Buscar_por_login(login)
        # Mesma mensagem para "usuario inexistente" e "senha errada" (nao vaza se o login existe).
        if adm is None or adm.get_senha() != senha:
            raise ValueError("Login ou senha invalidos.")
        return adm

    def login_cliente(self, email, senha): # autenticar um cliente
        # Nao aceita email ou senha em branco, levanta um erro.
        if not (email or "").strip() or not (senha or "").strip():
            raise ValueError("Email ou senha invalidos.")

        c = self._dao_cliente.Listar_por_email(email) # buscar um cliente pelo email

        if c is None or c.get_senha() == "": # se o cliente não for encontrado ou a senha estiver em branco, levanta um erro
            raise ValueError("Email ou senha invalidos.")

        if c.get_senha() != senha: # se a senha do cliente for diferente da senha passada, levanta um erro
            raise ValueError("Email ou senha invalidos.")
        # Se a senha do cliente for igual à senha passada, retorna o cliente
        return c 
