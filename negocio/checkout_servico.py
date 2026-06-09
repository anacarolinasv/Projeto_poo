from datetime import datetime
from negocio.carrinho_servico import CarrinhoServico
from produtos.produto import Produto, ProdutoDAO
from vendas.venda import Venda, VendaDAO
from vendas.vendaItem import VendaItem, VendaItemDAO

class CheckoutServico: # caso de uso: finalizar uma compra

    def finalizar_compra(self, id_cliente, carrinho): # finalizar uma compra

        if id_cliente <= 0: # se o id do cliente for menor ou igual a zero, levanta um erro
            raise ValueError("Cliente invalido.")

        if not carrinho: # se o carrinho estiver vazio, levanta um erro
            raise ValueError("Carrinho vazio.")

        lista, total = CarrinhoServico().montar_resumo(carrinho) # montar o resumo do carrinho

        if not lista: # se a lista de linhas estiver vazia, levanta um erro
            raise ValueError("Carrinho vazio.")
        pdao = ProdutoDAO()


        for L in lista: # para cada linha na lista, buscar um produto pelo id
            p = pdao.Listar_id(L["id"]) # buscar um produto pelo id
            if p is None: # se o produto não for encontrado, levanta um erro
                raise ValueError(f"Produto {L['id']} nao encontrado.")

            if p.get_estoque() < L["quantidade"]: # se o estoque do produto for menor que a quantidade, levanta um erro
                raise ValueError(
                    f"Estoque insuficiente para {p.get_descricao()} (disponivel: {p.get_estoque()})."
                )

        vdao = VendaDAO() # DAO encapsula leitura/gravacao em vendas.json (lista de vendas)
        id_venda = vdao.Proximo_id() # gerar um novo id de venda

        v = Venda(id_venda, datetime.now(), False, total, id_cliente) # criar uma nova venda
        vdao.Inserir(v) # inserir a venda na lista de vendas

        idao = VendaItemDAO() # DAO encapsula leitura/gravacao em vendaItem.json (lista de itens de venda)
        for L in lista: # para cada linha na lista, gerar um novo id de item de venda
            id_item = idao.Proximo_id() # gerar um novo id de item de venda

            item = VendaItem(
                id_item,
                int(L["quantidade"]),
                float(L["preco_unitario"]),
                id_venda,
                int(L["id"]),
            ) # criar um novo item de venda
            idao.Inserir(item) # inserir o item de venda na lista de itens de venda

            p = pdao.Listar_id(L["id"]) # buscar um produto pelo id
            novo_est = int(p.get_estoque()) - int(L["quantidade"]) # calcular o novo estoque

            atualizado = Produto(
                p.get_id(),
                p.get_descricao(),
                p.get_preco(),
                novo_est,
                p.get_idCategoria(),
            ) # criar um novo produto
            pdao.Atualizar(atualizado) # atualizar o produto na lista de produtos

        carrinho.clear() # esvaziar o carrinho
        CarrinhoServico().sincronizar(id_cliente, carrinho)
