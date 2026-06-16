from excecoes.excecoes import EntidadeInvalidaError

SEM_ENTREGADOR = 0

STATUS_PENDENTE = "PENDENTE"
STATUS_ALOCADA = "ALOCADA"
STATUS_EM_TRANSPORTE = "EM_TRANSPORTE"
STATUS_ENTREGUE = "ENTREGUE"

STATUS_VALIDOS = (
    STATUS_PENDENTE,
    STATUS_ALOCADA,
    STATUS_EM_TRANSPORTE,
    STATUS_ENTREGUE,
)

STATUS_ROTULOS = {
    STATUS_PENDENTE: "Aguardando entregador",
    STATUS_ALOCADA: "Entregador alocado",
    STATUS_EM_TRANSPORTE: "Em transporte",
    STATUS_ENTREGUE: "Entregue",
}


class Entrega:
    def __init__(self, id, idVenda, idEntregador=SEM_ENTREGADOR, status=STATUS_PENDENTE):
        self.set_id(id)
        self.set_idVenda(idVenda)
        self.set_idEntregador(idEntregador)
        self.set_status(status)

    def set_id(self, id):
        if not isinstance(id, int) or id <= 0:
            raise EntidadeInvalidaError("ID deve ser um inteiro maior que 0")
        self.__id = id

    def set_idVenda(self, idVenda):
        if not isinstance(idVenda, int) or idVenda <= 0:
            raise EntidadeInvalidaError("ID da venda deve ser um inteiro maior que 0")
        self.__idVenda = idVenda

    def set_idEntregador(self, idEntregador):
        if not isinstance(idEntregador, int) or idEntregador < 0:
            raise EntidadeInvalidaError("ID do entregador inválido")
        self.__idEntregador = idEntregador

    def set_status(self, status):
        if status not in STATUS_VALIDOS:
            raise EntidadeInvalidaError("Status de entrega inválido: " + str(status))
        self.__status = status

    def get_id(self):
        return self.__id

    def get_idVenda(self):
        return self.__idVenda

    def get_idEntregador(self):
        return self.__idEntregador

    def get_status(self):
        return self.__status

    def tem_entregador(self):
        return self.__idEntregador != SEM_ENTREGADOR

    def rotulo_status(self):
        return STATUS_ROTULOS.get(self.__status, self.__status)

    def to_dict(self):
        return {
            "id": self.get_id(),
            "idVenda": self.get_idVenda(),
            "idEntregador": self.get_idEntregador(),
            "status": self.get_status(),
        }

    def __str__(self):
        return f""" ENTREGA:
        ID: {self.get_id()}
        ID VENDA: {self.get_idVenda()}
        ID ENTREGADOR: {self.get_idEntregador()}
        STATUS: {self.rotulo_status()}
        """
