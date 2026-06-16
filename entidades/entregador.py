from excecoes.excecoes import EntidadeInvalidaError
from util.validacao import validar_fone, validar_nome, validar_senha


class Entregador:
    def __init__(self, id, nome, fone, login, senha):
        self.set_id(id)
        self.set_nome(nome)
        self.set_fone(fone)
        self.set_login(login)
        self.set_senha(senha)

    def set_id(self, id):
        if not isinstance(id, int) or id <= 0:
            raise EntidadeInvalidaError("ID deve ser um inteiro maior que 0")
        self.__id = id

    def set_nome(self, nome):
        self.__nome = validar_nome(nome)

    def set_fone(self, fone):
        self.__fone = validar_fone(fone)

    def set_login(self, login):
        if not (login or "").strip():
            raise EntidadeInvalidaError("Login é obrigatório")
        self.__login = login.strip()

    def set_senha(self, senha):
        self.__senha = validar_senha(senha, obrigatoria=True)

    def get_id(self):
        return self.__id

    def get_nome(self):
        return self.__nome

    def get_fone(self):
        return self.__fone

    def get_login(self):
        return self.__login

    def get_senha(self):
        return self.__senha

    def to_dict(self):
        return {
            "id": self.get_id(),
            "nome": self.get_nome(),
            "fone": self.get_fone(),
            "login": self.get_login(),
            "senha": self.get_senha(),
        }

    def __str__(self):
        return f""" ENTREGADOR:
        ID: {self.get_id()}
        NOME: {self.get_nome()}
        FONE: {self.get_fone()}
        LOGIN: {self.get_login()}
        """
