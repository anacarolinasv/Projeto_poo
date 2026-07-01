from entidades.promocao import Promocao
from persistencia.dao import DAO


class PromocaoDAO(DAO):
    entidade = "promoção"

    def __init__(self):
        super().__init__("dados/promocoes.json")

    def _from_dict(self, dados):
        return Promocao(
            dados["id"],
            dados["idCategoria"],
            dados["percentual"],
            dados["dataInicio"],
            dados["dataFim"],
        )

    def Listar_por_categoria(self, id_categoria):
        self.Abrir()
        return [p for p in self._objetos if p.get_idCategoria() == id_categoria]
