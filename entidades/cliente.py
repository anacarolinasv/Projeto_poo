from excecoes.excecoes import EntidadeInvalidaError
from util.validacao import validar_email, validar_fone, validar_nome, validar_senha


class Cliente:
    def __init__(self, id, nome, email, fone, senha=""):
        self.set_id(id)
        self.set_nome(nome)
        self.set_email(email)
        self.set_fone(fone)
        self.set_senha(senha)

    def set_id(self, id):
        if not isinstance(id, int) or id <= 0:
            raise EntidadeInvalidaError("ID deve ser um inteiro maior que 0")
        self.__id = id

    def set_nome(self, nome):
        self.__nome = validar_nome(nome)

    def set_email(self, email):
        self.__email = validar_email(email)

    def set_fone(self, fone):
        self.__fone = validar_fone(fone)

    def set_senha(self, senha):
        self.__senha = validar_senha(senha if senha is not None else "")

    def get_id(self):
        return self.__id

    def get_nome(self):
        return self.__nome

    def get_email(self):
        return self.__email

    def get_fone(self):
        return self.__fone

    def get_senha(self):
        return self.__senha

    def to_dict(self):
        return {
            "id": self.get_id(),
            "nome": self.get_nome(),
            "email": self.get_email(),
            "fone": self.get_fone(),
            "senha": self.get_senha(),
        }

    def __str__(self):
        return f""" CLIENTE:
        ID: {self.get_id()}
        NOME: {self.get_nome()}
        EMAIL: {self.get_email()}
        FONE: {self.get_fone()}
        """
