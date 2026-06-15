from carrinhos.carrinho import CarrinhoDAO
from negocio.preco_servico import PrecoServico
from produtos.produto import ProdutoDAO

class CarrinhoServico: # caso de uso: adicionar, remover, esvaziar e montar resumo do carrinho

    def adicionar(self, carrinho, id_produto, quantidade): # adicionar um item ao carrinho

        if not isinstance(carrinho, dict): # se o carrinho não for um dicionário, levanta um erro
            raise TypeError("Carrinho inválido.")
        if quantidade <= 0: # se a quantidade for menor ou igual a zero, levanta um erro
            raise ValueError("Quantidade deve ser maior que zero.")

        dao = ProdutoDAO() # DAO encapsula leitura/gravacao em produtos.json (lista de produtos)
        produto = dao.Listar_id(id_produto) # buscar um produto pelo id

        if produto is None: # se o produto não for encontrado, levanta um erro
            raise ValueError("Produto não encontrado.")
        if produto.get_estoque() <= 0: # se o estoque do produto for menor ou igual a zero, levanta um erro
            raise ValueError("Produto indisponível para venda.")

        quantidade_no_carrinho = int(carrinho.get(id_produto, 0)) # quantidade ja pedida deste mesmo produto no carrinho (0 se primeira vez)
        if quantidade_no_carrinho + quantidade > produto.get_estoque(): # se a quantidade ja pedida mais a quantidade passada for maior que o estoque, levanta um erro
            raise ValueError(f"Quantidade indisponível. No carrinho: {quantidade_no_carrinho}, estoque: {produto.get_estoque()}.")

        carrinho[id_produto] = quantidade_no_carrinho + quantidade # atualiza ou cria a entrada: mesmo id_produto agrega quantidade

    def remover_item(self, carrinho, id_produto): # remover um item do carrinho
        if not isinstance(carrinho, dict): # se o carrinho não for um dicionário, levanta um erro
            raise TypeError("Carrinho inválido.")

        if id_produto not in carrinho: # se o id do produto não estiver no carrinho, levanta um erro
            raise ValueError("Este produto nao esta no carrinho.")
        del carrinho[id_produto] # remove o item do carrinho

    def esvaziar(self, carrinho): # esvaziar o carrinho
        if not isinstance(carrinho, dict): # se o carrinho não for um dicionário, levanta um erro
            raise TypeError("Carrinho inválido.")
        carrinho.clear() # remove todos os itens do carrinho

    def montar_resumo(self, carrinho): # montar o resumo do carrinho
        dao = ProdutoDAO() # DAO encapsula leitura/gravacao em produtos.json (lista de produtos)
        preco_servico = PrecoServico()
        lista = [] # lista de linhas do carrinho
        total = 0.0 # total do carrinho

        for id_produto, quantidade in list(carrinho.items()): # para cada id_produto e quantidade no carrinho, buscar um produto pelo id
            produto = dao.Listar_id(id_produto)
            if produto is None: # se o produto não for encontrado, remove o item do carrinho e continua o loop
                del carrinho[id_produto] # remove o item do carrinho
                continue

            detalhes = preco_servico.detalhes(produto)
            preco_unitario = float(detalhes["preco_efetivo"])
            quantidade = int(quantidade) # quantidade do produto
            total_item = round(preco_unitario * quantidade, 2) # total do item
            total += total_item # atualiza o total
            lista.append(
                {
                    "id": id_produto,
                    "descricao": produto.get_descricao(),
                    "preco_unitario": preco_unitario,
                    "preco_base": float(detalhes["preco_base"]),
                    "em_promocao": bool(detalhes["em_promocao"]),
                    "percentual": float(detalhes["percentual"]),
                    "quantidade": quantidade,
                    "total_item": total_item,
                }
            ) # adiciona a linha do carrinho

        return lista, round(total, 2) # retorna a lista de linhas e o total arredondado para 2 casas decimais

    def sincronizar(self, id_cliente, carrinho):
        if not isinstance(carrinho, dict):
            raise TypeError("Carrinho inválido.")
        CarrinhoDAO().Salvar_por_cliente(id_cliente, carrinho)

    def carregar(self, id_cliente, carrinho):
        if not isinstance(carrinho, dict):
            raise TypeError("Carrinho inválido.")
        salvos = CarrinhoDAO().Carregar_por_cliente(id_cliente)
        carrinho.clear()
        for id_produto, quantidade in salvos.items():
            carrinho[int(id_produto)] = int(quantidade)
