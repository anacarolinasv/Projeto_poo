from excecoes.excecoes import EntidadeInvalidaError
from util.validacao import validar_descricao


class Categoria:
    def __init__(self, id, descricao):
        self.set_id(id)
        self.set_descricao(descricao)

    def set_id(self, id):
        if not isinstance(id, int) or id <= 0:
            raise EntidadeInvalidaError("ID deve ser um inteiro maior que 0")
        self.__id = id

    def set_descricao(self, descricao):
        self.__descricao = validar_descricao(descricao, "Descrição da categoria")

    def get_id(self):
        return self.__id

    def get_descricao(self):
        return self.__descricao

    def to_dict(self):
        return {
            "id": self.get_id(),
            "descricao": self.get_descricao(),
        }

    def __str__(self):
        return f""" CATEGORIA:
        ID: {self.get_id()}
        DESCRICAO: {self.get_descricao()}
        """
