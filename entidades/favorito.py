from excecoes.excecoes import EntidadeInvalidaError


class Favorito:
    def __init__(self, id, idCliente, idProduto):
        self.set_id(id)
        self.set_idCliente(idCliente)
        self.set_idProduto(idProduto)

    def set_id(self, id):
        if not isinstance(id, int) or id <= 0:
            raise EntidadeInvalidaError("ID deve ser um inteiro maior que 0")
        self.__id = id

    def set_idCliente(self, idCliente):
        if not isinstance(idCliente, int) or idCliente <= 0:
            raise EntidadeInvalidaError("ID do cliente deve ser um inteiro maior que 0")
        self.__idCliente = idCliente

    def set_idProduto(self, idProduto):
        if not isinstance(idProduto, int) or idProduto <= 0:
            raise EntidadeInvalidaError("ID do produto deve ser um inteiro maior que 0")
        self.__idProduto = idProduto

    def get_id(self):
        return self.__id

    def get_idCliente(self):
        return self.__idCliente

    def get_idProduto(self):
        return self.__idProduto

    def to_dict(self):
        return {
            "id": self.get_id(),
            "idCliente": self.get_idCliente(),
            "idProduto": self.get_idProduto(),
        }

    def __str__(self):
        return f""" FAVORITO:
        ID: {self.get_id()}
        ID CLIENTE: {self.get_idCliente()}
        ID PRODUTO: {self.get_idProduto()}
        """
