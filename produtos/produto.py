from excecoes.excecoes import EntidadeInvalidaError
from persistencia.dao import DAO
from util.validacao import validar_descricao


class Produto:
    # --------- Constructor ---------#
    def __init__(self, id, descricao, preco, estoque, idCategoria):
        self.set_id(id)
        self.set_descricao(descricao)
        self.set_preco(preco)
        self.set_estoque(estoque)
        self.set_idCategoria(idCategoria)

    # --------- Setters ----------#
    def set_id(self, id):
        if not isinstance(id, int) or id <= 0:
            raise EntidadeInvalidaError("ID deve ser um inteiro maior que 0")
        self.__id = id

    def set_descricao(self, descricao):
        self.__descricao = validar_descricao(descricao, "Descrição do produto")

    def set_preco(self, preco):
        if not isinstance(preco, (int, float)):
            raise EntidadeInvalidaError("Preço deve ser um número")
        preco = float(preco)
        if preco < 0:
            raise EntidadeInvalidaError("Preço não pode ser negativo")
        self.__preco = preco

    def set_estoque(self, estoque):
        if not isinstance(estoque, int):
            raise EntidadeInvalidaError("Estoque deve ser um número inteiro")
        if estoque < 0:
            raise EntidadeInvalidaError("Estoque não pode ser negativo")
        self.__estoque = estoque

    def set_idCategoria(self, idCategoria):
        if not isinstance(idCategoria, int) or idCategoria <= 0:
            raise EntidadeInvalidaError(
                "Produto deve estar vinculado a uma categoria válida"
            )
        self.__idCategoria = idCategoria

    # --------- Getters ----------#
    def get_id(self):
        return self.__id

    def get_descricao(self):
        return self.__descricao

    def get_preco(self):
        return self.__preco

    def get_estoque(self):
        return self.__estoque

    def get_idCategoria(self):
        return self.__idCategoria

    def to_dict(self):
        return {
            "id": self.get_id(),
            "descricao": self.get_descricao(),
            "preco": self.get_preco(),
            "estoque": self.get_estoque(),
            "idCategoria": self.get_idCategoria(),
        }

    # --------- To String ----------#
    def __str__(self):
        return f""" PRODUTO:
        ID: {self.get_id()}
        DESCRICAO: {self.get_descricao()}
        PRECO: {self.get_preco()}
        ESTOQUE: {self.get_estoque()}
        ID CATEGORIA: {self.get_idCategoria()}
        """


class ProdutoDAO(DAO):
    entidade = "produto"

    def __init__(self):
        super().__init__("produtos/produtos.json")

    def _from_dict(self, dados):
        return Produto(
            dados["id"],
            dados["descricao"],
            dados["preco"],
            dados["estoque"],
            dados["idCategoria"],
        )

    def Reajustar_precos_percentual(self, percentual):
        """Aplica reajuste de preço em todos os produtos (percentual pode ser negativo)."""
        self.Abrir()
        fator = 1.0 + float(percentual) / 100.0
        for produto in self._objetos:
            novo_preco = round(produto.get_preco() * fator, 2)
            if novo_preco < 0:
                raise EntidadeInvalidaError("Reajuste resultaria em preço negativo.")
            produto.set_preco(novo_preco)
        self.Salvar()
