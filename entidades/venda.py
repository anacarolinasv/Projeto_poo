from datetime import datetime

from excecoes.excecoes import EntidadeInvalidaError


class Venda:
    def __init__(self, id, data, carrinho, total, idCliente):
        self.set_id(id)
        self.set_data(data)
        self.set_carrinho(carrinho)
        self.set_total(total)
        self.set_idCliente(idCliente)

    def set_id(self, id):
        if not isinstance(id, int) or id <= 0:
            raise EntidadeInvalidaError("ID deve ser um inteiro maior que 0")
        self.__id = id

    def set_data(self, data):
        if not isinstance(data, datetime):
            raise EntidadeInvalidaError("Data deve ser um objeto datetime")
        self.__data = data

    def set_carrinho(self, carrinho):
        if not isinstance(carrinho, bool):
            raise EntidadeInvalidaError("Carrinho deve ser bool (True ou False)")
        self.__carrinho = carrinho

    def set_total(self, total):
        if not isinstance(total, (int, float)):
            raise EntidadeInvalidaError("Total deve ser um número")
        total = float(total)
        if total < 0:
            raise EntidadeInvalidaError("Total não pode ser negativo")
        self.__total = total

    def set_idCliente(self, idCliente):
        if not isinstance(idCliente, int) or idCliente <= 0:
            raise EntidadeInvalidaError("ID do cliente deve ser um inteiro maior que 0")
        self.__idCliente = idCliente

    def get_id(self):
        return self.__id

    def get_data(self):
        return self.__data

    def get_carrinho(self):
        return self.__carrinho

    def get_total(self):
        return self.__total

    def get_idCliente(self):
        return self.__idCliente

    def to_dict(self):
        data = self.get_data()
        data_str = data.isoformat() if isinstance(data, datetime) else str(data)
        return {
            "id": self.get_id(),
            "data": data_str,
            "carrinho": self.get_carrinho(),
            "total": self.get_total(),
            "idCliente": self.get_idCliente(),
        }

    def __str__(self):
        return f""" VENDA:
        ID: {self.get_id()}
        DATA: {self.get_data()}
        CARRINHO: {self.get_carrinho()}
        TOTAL: {self.get_total()}
        ID CLIENTE: {self.get_idCliente()}
        """
