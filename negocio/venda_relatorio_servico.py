from vendas.venda import VendaDAO
from vendas.vendaItem import VendaItemDAO
from produtos.produto import ProdutoDAO


class VendaRelatorioServico:
    """Monta vendas com itens (para cliente e admin)."""

    def _itens_detalhados(self, id_venda):
        idao = VendaItemDAO()
        pdao = ProdutoDAO()
        out = []
        for it in idao.Listar_por_venda(id_venda):
            p = pdao.Listar_id(it.get_idProduto())
            desc = p.get_descricao() if p else "(produto removido)"
            q = int(it.get_quantidade())
            pu = float(it.get_preco())
            out.append(
                {
                    "id_produto": it.get_idProduto(),
                    "descricao": desc,
                    "quantidade": q,
                    "preco_unitario": pu,
                    "total_item": round(pu * q, 2),
                }
            )
        return out

    def listar_por_cliente(self, id_cliente):
        vdao = VendaDAO()
        lst = []
        for v in sorted(vdao.Listar_por_cliente(id_cliente), key=lambda x: x.get_id()):
            lst.append({"venda": v, "itens": self._itens_detalhados(v.get_id())})
        return lst

    def listar_todas(self):
        vdao = VendaDAO()
        lst = []
        for v in sorted(vdao.Listar(), key=lambda x: x.get_id()):
            lst.append({"venda": v, "itens": self._itens_detalhados(v.get_id())})
        return lst
