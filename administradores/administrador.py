from excecoes.excecoes import EntidadeInvalidaError
from persistencia.dao import DAO

LOGIN_ADMIN_PADRAO = "admin"
SENHA_ADMIN_PADRAO = "admin123"


class Administrador:
    # --------- Constructor ---------#
    def __init__(self, id, login, senha):
        self.set_id(id)
        self.set_login(login)
        self.set_senha(senha)

    # --------- Setters ---------#
    def set_id(self, id):
        if not isinstance(id, int) or id <= 0:
            raise EntidadeInvalidaError("ID deve ser um inteiro maior que 0")
        self.__id = id

    def set_login(self, login):
        if not (login or "").strip():
            raise EntidadeInvalidaError("Login é obrigatório")
        self.__login = login.strip()

    def set_senha(self, senha):
        if not (senha or "").strip():
            raise EntidadeInvalidaError("Senha é obrigatória")
        if len(senha) < 4:
            raise EntidadeInvalidaError("Senha deve ter pelo menos 4 caracteres")
        self.__senha = senha

    # --------- Getters ---------#
    def get_id(self):
        return self.__id

    def get_login(self):
        return self.__login

    def get_senha(self):
        return self.__senha

    def to_dict(self):
        return {
            "id": self.get_id(),
            "login": self.get_login(),
            "senha": self.get_senha(),
        }

    # --------- To String ---------#
    def __str__(self):
        return f""" ADMINISTRADOR:
        ID: {self.get_id()}
        LOGIN: {self.get_login()}
        """


class AdministradorDAO(DAO):
    entidade = "administrador"

    def __init__(self):
        super().__init__("administradores/administradores.json")

    def _from_dict(self, dados):
        return Administrador(dados["id"], dados["login"], dados["senha"])

    def garantir_admin_padrao(self):
        self.Abrir()
        if not self._objetos:
            padrao = Administrador(1, LOGIN_ADMIN_PADRAO, SENHA_ADMIN_PADRAO)
            self._objetos.append(padrao)
            self.Salvar()

    def Buscar_por_login(self, login):
        self.Abrir()
        alvo = (login or "").strip().lower()
        for a in self._objetos:
            if a.get_login().strip().lower() == alvo:
                return a
        return None
