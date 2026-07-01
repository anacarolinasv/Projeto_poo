from entidades.venda_item import VendaItem
from persistencia.dao import DAO


class VendaItemDAO(DAO):
    entidade = "item de venda"

    def __init__(self):
        super().__init__("dados/vendaItem.json")

    def _from_dict(self, dados):
        return VendaItem(
            dados["id"],
            dados["quantidade"],
            dados["preco"],
            dados["idVenda"],
            dados["idProduto"],
        )

    def Listar_por_venda(self, id_venda):
        self.Abrir()
        return [x for x in self._objetos if x.get_idVenda() == id_venda]

    def Listar_por_produto(self, id_produto):
        self.Abrir()
        return [x for x in self._objetos if x.get_idProduto() == id_produto]
