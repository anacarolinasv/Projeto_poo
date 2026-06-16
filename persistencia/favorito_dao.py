from entidades.favorito import Favorito
from excecoes.excecoes import EntidadeInvalidaError
from persistencia.dao import DAO


class FavoritoDAO(DAO):
    entidade = "favorito"

    def __init__(self):
        super().__init__("dados/favoritos.json")

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
