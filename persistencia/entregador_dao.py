from entidades.entregador import Entregador
from persistencia.dao import DAO


class EntregadorDAO(DAO):
    entidade = "entregador"

    def __init__(self):
        super().__init__("dados/entregadores.json")

    def _from_dict(self, dados):
        return Entregador(
            dados["id"],
            dados["nome"],
            dados["fone"],
            dados["login"],
            dados["senha"],
        )

    def Buscar_por_login(self, login):
        self.Abrir()
        alvo = (login or "").strip().lower()
        for entregador in self._objetos:
            if entregador.get_login().strip().lower() == alvo:
                return entregador
        return None
