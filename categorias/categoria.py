from excecoes.excecoes import EntidadeInvalidaError
from persistencia.dao import DAO
from util.validacao import validar_descricao


class Categoria:
    # --------- Constructor ---------#
    def __init__(self, id, descricao):
        self.set_id(id)
        self.set_descricao(descricao)

    # --------- Setters ----------#
    def set_id(self, id):
        if not isinstance(id, int) or id <= 0:
            raise EntidadeInvalidaError("ID deve ser um inteiro maior que 0")
        self.__id = id

    def set_descricao(self, descricao):
        self.__descricao = validar_descricao(descricao, "Descrição da categoria")

    # --------- Getters ----------#
    def get_id(self):
        return self.__id

    def get_descricao(self):
        return self.__descricao

    def to_dict(self):
        return {
            "id": self.get_id(),
            "descricao": self.get_descricao(),
        }

    # --------- To String ----------#
    def __str__(self):
        return f""" CATEGORIA:
        ID: {self.get_id()}
        DESCRICAO: {self.get_descricao()}
        """


class CategoriaDAO(DAO):
    entidade = "categoria"

    def __init__(self):
        super().__init__("categorias/categorias.json")

    def _from_dict(self, dados):
        return Categoria(dados["id"], dados["descricao"])
