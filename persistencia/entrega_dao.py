from entidades.entrega import (
    SEM_ENTREGADOR,
    STATUS_PENDENTE,
    Entrega,
)
from persistencia.dao import DAO


class EntregaDAO(DAO):
    entidade = "entrega"

    def __init__(self):
        super().__init__("dados/entregas.json")

    def _from_dict(self, dados):
        return Entrega(
            int(dados["id"]),
            int(dados["idVenda"]),
            int(dados.get("idEntregador", SEM_ENTREGADOR)),
            dados.get("status", STATUS_PENDENTE),
        )

    def Buscar_por_venda(self, id_venda):
        self.Abrir()
        for entrega in self._objetos:
            if entrega.get_idVenda() == id_venda:
                return entrega
        return None

    def Listar_por_entregador(self, id_entregador):
        self.Abrir()
        return [e for e in self._objetos if e.get_idEntregador() == id_entregador]
