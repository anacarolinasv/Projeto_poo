from excecoes.excecoes import EntidadeInvalidaError


class VendaItem:
    def __init__(self, id, quantidade, preco, idVenda, idProduto):
        self.set_id(id)
        self.set_quantidade(quantidade)
        self.set_preco(preco)
        self.set_idVenda(idVenda)
        self.set_idProduto(idProduto)

    def set_id(self, id):
        if not isinstance(id, int) or id <= 0:
            raise EntidadeInvalidaError("ID deve ser um inteiro maior que 0")
        self.__id = id

    def set_quantidade(self, quantidade):
        if not isinstance(quantidade, int):
            raise EntidadeInvalidaError("Quantidade deve ser um número inteiro")
        if quantidade <= 0:
            raise EntidadeInvalidaError("Quantidade deve ser maior que zero")
        self.__quantidade = quantidade

    def set_preco(self, preco):
        if not isinstance(preco, (int, float)):
            raise EntidadeInvalidaError("Preço deve ser um número")
        preco = float(preco)
        if preco < 0:
            raise EntidadeInvalidaError("Preço não pode ser negativo")
        self.__preco = preco

    def set_idVenda(self, idVenda):
        if not isinstance(idVenda, int) or idVenda <= 0:
            raise EntidadeInvalidaError("ID da venda deve ser um inteiro maior que 0")
        self.__idVenda = idVenda

    def set_idProduto(self, idProduto):
        if not isinstance(idProduto, int) or idProduto <= 0:
            raise EntidadeInvalidaError("ID do produto deve ser um inteiro maior que 0")
        self.__idProduto = idProduto

    def get_id(self):
        return self.__id

    def get_idVenda(self):
        return self.__idVenda

    def get_idProduto(self):
        return self.__idProduto

    def get_quantidade(self):
        return self.__quantidade

    def get_preco(self):
        return self.__preco

    def to_dict(self):
        return {
            "id": self.get_id(),
            "quantidade": self.get_quantidade(),
            "preco": self.get_preco(),
            "idVenda": self.get_idVenda(),
            "idProduto": self.get_idProduto(),
        }

    def __str__(self):
        return f""" VENDA ITEM:
        ID: {self.get_id()}
        ID VENDA: {self.get_idVenda()}
        ID PRODUTO: {self.get_idProduto()}
        QUANTIDADE: {self.get_quantidade()}
        PRECO: {self.get_preco()}
        """
