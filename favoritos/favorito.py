from excecoes.excecoes import EntidadeInvalidaError
from persistencia.dao import DAO


class Favorito:
    # --------- Constructor ---------#
    def __init__(self, id, idCliente, idProduto):
        self.set_id(id)
        self.set_idCliente(idCliente)
        self.set_idProduto(idProduto)

    # --------- Setters ---------#
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

    # --------- Getters ---------#
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

    # --------- To String ---------#
    def __str__(self):
        return f""" FAVORITO:
        ID: {self.get_id()}
        ID CLIENTE: {self.get_idCliente()}
        ID PRODUTO: {self.get_idProduto()}
        """


class FavoritoDAO(DAO):
    entidade = "favorito"

    def __init__(self):
        super().__init__("favoritos/favoritos.json")

    def _from_dict(self, dados):
        return Favorito(
            int(dados["id"]),
            int(dados["idCliente"]),
            int(dados["idProduto"]),
        )

    def Inserir(self, favorito):
        if (
            self.Buscar_por_cliente_produto(
                favorito.get_idCliente(), favorito.get_idProduto()
            )
            is not None
        ):
            raise EntidadeInvalidaError(
                "Este produto já está nos favoritos deste cliente."
            )
        super().Inserir(favorito)

    def Buscar_por_cliente_produto(self, id_cliente, id_produto):
        self.Abrir()
        for favorito in self._objetos:
            if (
                favorito.get_idCliente() == id_cliente
                and favorito.get_idProduto() == id_produto
            ):
                return favorito
        return None

    def Listar_por_cliente(self, id_cliente):
        self.Abrir()
        return [
            favorito
            for favorito in self._objetos
            if favorito.get_idCliente() == id_cliente
        ]

    def Excluir_por_cliente_produto(self, id_cliente, id_produto):
        favorito = self.Buscar_por_cliente_produto(id_cliente, id_produto)
        if favorito is not None:
            return self.Excluir(favorito.get_id())
        return False

    def Excluir_por_cliente(self, id_cliente):
        self.Abrir()
        antes = len(self._objetos)
        self._objetos = [f for f in self._objetos if f.get_idCliente() != id_cliente]
        if len(self._objetos) < antes:
            self.Salvar()
            return True
        return False
