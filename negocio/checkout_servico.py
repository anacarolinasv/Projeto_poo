from datetime import datetime

from negocio.carrinho_servico import CarrinhoServico
from produtos.produto import Produto, ProdutoDAO
from vendas.venda import Venda, VendaDAO
from vendas.vendaItem import VendaItem, VendaItemDAO


class CheckoutServico:
    """Finaliza compra: grava venda e itens, baixa estoque, esvazia carrinho."""

    def finalizar_compra(self, id_cliente, carrinho):
        if id_cliente <= 0:
            raise ValueError("Cliente invalido.")
        if not carrinho:
            raise ValueError("Carrinho vazio.")
        linhas, total = CarrinhoServico().montar_resumo(carrinho)
        if not linhas:
            raise ValueError("Carrinho vazio.")
        pdao = ProdutoDAO()
        for L in linhas:
            p = pdao.Listar_id(L["id"])
            if p is None:
                raise ValueError(f"Produto {L['id']} nao encontrado.")
            if p.get_estoque() < L["quantidade"]:
                raise ValueError(
                    f"Estoque insuficiente para {p.get_descricao()} (disponivel: {p.get_estoque()})."
                )
        vdao = VendaDAO()
        id_venda = vdao.Proximo_id()
        v = Venda(id_venda, datetime.now(), False, total, id_cliente)
        vdao.Inserir(v)
        idao = VendaItemDAO()
        for L in linhas:
            id_item = idao.Proximo_id()
            item = VendaItem(
                id_item,
                int(L["quantidade"]),
                float(L["preco_unitario"]),
                id_venda,
                int(L["id"]),
            )
            idao.Inserir(item)
            p = pdao.Listar_id(L["id"])
            novo_est = int(p.get_estoque()) - int(L["quantidade"])
            atualizado = Produto(
                p.get_id(),
                p.get_descricao(),
                p.get_preco(),
                novo_est,
                p.get_idCategoria(),
            )
            pdao.Atualizar(atualizado)
        carrinho.clear()
