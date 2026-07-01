from entidades.cliente import Cliente
from persistencia.dao import DAO


class ClienteDAO(DAO):
    entidade = "cliente"

    def __init__(self):
        super().__init__("dados/clientes.json")

    def _from_dict(self, dados):
        return Cliente(
            dados["id"],
            dados["nome"],
            dados["email"],
            dados["fone"],
            dados.get("senha", ""),
        )

    def Listar_por_email(self, email):
        self.Abrir()
        alvo = (email or "").strip().lower()
        for cliente in self._objetos:
            if cliente.get_email().strip().lower() == alvo:
                return cliente
        return None

    def Deletar(self, id):
        return self.Excluir(id)
