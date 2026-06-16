from persistencia.cliente_dao import ClienteDAO
from persistencia.entregador_dao import EntregadorDAO
from entidades.entrega import (
    STATUS_ALOCADA,
    STATUS_EM_TRANSPORTE,
    STATUS_ENTREGUE,
    Entrega,
)
from persistencia.entrega_dao import EntregaDAO
from excecoes.excecoes import RegraNegocioError
from persistencia.venda_dao import VendaDAO

# Próximo status a partir do atual (avanço linear feito pelo entregador).
_PROXIMO_STATUS = {
    STATUS_ALOCADA: STATUS_EM_TRANSPORTE,
    STATUS_EM_TRANSPORTE: STATUS_ENTREGUE,
}


class EntregaServico:
    def __init__(self):
        self._dao = EntregaDAO()
        self._venda_dao = VendaDAO()
        self._entregador_dao = EntregadorDAO()
        self._cliente_dao = ClienteDAO()

    def registrar_para_venda(self, id_venda):
        """Cria a entrega (status PENDENTE) ao finalizar uma venda."""
        if self._dao.Buscar_por_venda(id_venda) is not None:
            return
        nova = Entrega(self._dao.Proximo_id(), id_venda)
        self._dao.Inserir(nova)

    def _nome_cliente(self, id_cliente):
        cliente = self._cliente_dao.Listar_id(id_cliente)
        return cliente.get_nome() if cliente else "(cliente removido)"

    def listar_pedidos(self):
        """Para o admin: todas as vendas com sua entrega e entregador."""
        pedidos = []
        for venda in sorted(self._venda_dao.Listar(), key=lambda v: v.get_id()):
            entrega = self._dao.Buscar_por_venda(venda.get_id())
            if entrega is None:
                # Vendas anteriores ao controle de entregas recebem entrega agora.
                self.registrar_para_venda(venda.get_id())
                entrega = self._dao.Buscar_por_venda(venda.get_id())
            entregador = (
                self._entregador_dao.Listar_id(entrega.get_idEntregador())
                if entrega.tem_entregador()
                else None
            )
            pedidos.append(
                {
                    "venda": venda,
                    "entrega": entrega,
                    "entregador": entregador,
                    "cliente": self._nome_cliente(venda.get_idCliente()),
                }
            )
        return pedidos

    def alocar_entregador(self, id_venda, id_entregador):
        if self._entregador_dao.Listar_id(id_entregador) is None:
            raise RegraNegocioError("Entregador não encontrado.")
        entrega = self._dao.Buscar_por_venda(id_venda)
        if entrega is None:
            raise RegraNegocioError("Entrega não encontrada para esta venda.")
        if entrega.get_status() == STATUS_ENTREGUE:
            raise RegraNegocioError("Pedido já entregue; não é possível realocar.")
        entrega.set_idEntregador(id_entregador)
        entrega.set_status(STATUS_ALOCADA)
        self._dao.Atualizar(entrega)
        return entrega

    def listar_para_entregador(self, id_entregador):
        pedidos = []
        for entrega in self._dao.Listar_por_entregador(id_entregador):
            venda = self._venda_dao.Listar_id(entrega.get_idVenda())
            if venda is None:
                continue
            pedidos.append(
                {
                    "venda": venda,
                    "entrega": entrega,
                    "cliente": self._nome_cliente(venda.get_idCliente()),
                }
            )
        return sorted(pedidos, key=lambda p: p["venda"].get_id())

    def avancar_status(self, id_entrega, id_entregador):
        entrega = self._dao.Listar_id(id_entrega)
        if entrega is None:
            raise RegraNegocioError("Entrega não encontrada.")
        if entrega.get_idEntregador() != id_entregador:
            raise RegraNegocioError("Esta entrega não pertence a você.")
        proximo = _PROXIMO_STATUS.get(entrega.get_status())
        if proximo is None:
            raise RegraNegocioError("A entrega já foi concluída.")
        entrega.set_status(proximo)
        self._dao.Atualizar(entrega)
        return entrega

    def listar_para_cliente(self, id_cliente):
        """Acompanhamento do cliente: entrega de cada venda dele."""
        acompanhamento = {}
        for venda in self._venda_dao.Listar_por_cliente(id_cliente):
            entrega = self._dao.Buscar_por_venda(venda.get_id())
            if entrega is None:
                continue
            entregador = (
                self._entregador_dao.Listar_id(entrega.get_idEntregador())
                if entrega.tem_entregador()
                else None
            )
            acompanhamento[venda.get_id()] = {
                "entrega": entrega,
                "entregador": entregador,
            }
        return acompanhamento
