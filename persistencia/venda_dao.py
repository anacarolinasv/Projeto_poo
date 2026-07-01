from datetime import datetime

from entidades.venda import Venda
from excecoes.excecoes import EntidadeInvalidaError
from persistencia.dao import DAO


def _dict_para_venda(obj):
    raw = obj["data"]
    if isinstance(raw, str):
        data = datetime.fromisoformat(raw)
    elif isinstance(raw, datetime):
        data = raw
    else:
        raise EntidadeInvalidaError("Data da venda inválida no arquivo")
    return Venda(
        int(obj["id"]),
        data,
        bool(obj["carrinho"]),
        float(obj["total"]),
        int(obj["idCliente"]),
    )


class VendaDAO(DAO):
    entidade = "venda"

    def __init__(self):
        super().__init__("dados/vendas.json")

    def _from_dict(self, dados):
        return _dict_para_venda(dados)

    def Listar_por_cliente(self, id_cliente):
        self.Abrir()
        return [v for v in self._objetos if v.get_idCliente() == id_cliente]
