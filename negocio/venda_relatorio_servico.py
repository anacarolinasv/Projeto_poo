from persistencia.venda_dao import VendaDAO
from persistencia.venda_item_dao import VendaItemDAO
from persistencia.produto_dao import ProdutoDAO

class VendaRelatorioServico:  # caso de uso: montar vendas com itens

    def _itens_detalhados(self, id_venda):  # itens ligados a esta venda; produtos buscados para mostrar descricao atual ou fallback.

        venda_item_dao = VendaItemDAO()  # vendaItem.json
        produto_dao = ProdutoDAO()  # produtos.json
        itens_detalhados = []  # lista de itens detalhados para o relatorio

        for item_venda in venda_item_dao.Listar_por_venda(id_venda): # para cada item na lista de itens de venda, buscar um produto pelo id

            produto = produto_dao.Listar_id(item_venda.get_idProduto()) # buscar um produto pelo id
            descricao = produto.get_descricao() if produto else "(produto removido)" # descrição do produto ou texto fixo se produto removido
            quantidade = int(item_venda.get_quantidade()) # quantidade do item
            preco_unitario = float(item_venda.get_preco()) # preço unitário do item
            itens_detalhados.append(
                {
                    "id_produto": item_venda.get_idProduto(),
                    "descricao": descricao,
                    "quantidade": quantidade,
                    "preco_unitario": preco_unitario,
                    "total_item": round(preco_unitario * quantidade, 2), # total do item
                }
            ) # adiciona o item detalhado na lista de itens detalhados
        return itens_detalhados # retorna a lista de itens detalhados

    def listar_por_cliente(self, id_cliente):  # listar vendas por cliente

        venda_dao = VendaDAO()  # DAO encapsula leitura/gravacao em vendas.json (lista de vendas)
        vendas_com_itens = []  # lista de vendas com itens detalhados
        
        for venda in sorted(venda_dao.Listar_por_cliente(id_cliente), key=lambda venda: venda.get_id()): # para cada venda na lista de vendas, ordenar por id
            vendas_com_itens.append({"venda": venda, "itens": self._itens_detalhados(venda.get_id())}) # adiciona a venda na lista de vendas com itens detalhados
        return vendas_com_itens # retorna a lista de vendas com itens detalhados

    def listar(self):  # listar vendas sem detalhar itens
        return VendaDAO().Listar()

    def listar_todas(self):  # listar todas as vendas
        venda_dao = VendaDAO()
        vendas_com_itens = [] # lista de vendas com itens detalhados
        for venda in sorted(venda_dao.Listar(), key=lambda venda: venda.get_id()): # para cada venda na lista de vendas, ordenar por id
            vendas_com_itens.append({"venda": venda, "itens": self._itens_detalhados(venda.get_id())}) # adiciona a venda na lista de vendas com itens detalhados
        return vendas_com_itens # retorna a lista de vendas com itens detalhados
