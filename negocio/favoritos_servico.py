from clientes.cliente import ClienteDAO
from favoritos.favorito import Favorito, FavoritoDAO
from produtos.produto import ProdutoDAO


class FavoritosServico:  # caso de uso: favoritar, desfavoritar e listar favoritos

    def favoritar(self, id_cliente, id_produto):  # favoritar um produto

        if id_cliente <= 0: # se o id do cliente for menor ou igual a zero, levanta um erro
            raise ValueError("Cliente inválido.")
        if id_produto <= 0: # se o id do produto for menor ou igual a zero, levanta um erro
            raise ValueError("Produto inválido.")

        cliente_dao = ClienteDAO() # DAO encapsula leitura/gravacao em clientes.json (lista de clientes)
        if cliente_dao.Listar_id(id_cliente) is None: # se o cliente não for encontrado, levanta um erro
            raise ValueError("Cliente não encontrado.")

        produto_dao = ProdutoDAO() # DAO encapsula leitura/gravacao em produtos.json (lista de produtos)
        if produto_dao.Listar_id(id_produto) is None: # se o produto não for encontrado, levanta um erro
            raise ValueError("Produto não encontrado.")

        favorito_dao = FavoritoDAO() # DAO encapsula leitura/gravacao em favoritos.json (lista de favoritos)
        if favorito_dao.Buscar_por_cliente_produto(id_cliente, id_produto) is not None: # se o produto já estiver nos favoritos do cliente, levanta um erro
            raise ValueError("Este produto ja esta nos seus favoritos.")

        id_favorito = favorito_dao.Proximo_id() # gerar um novo id de favorito
        favorito_dao.Inserir(Favorito(id_favorito, id_cliente, id_produto)) # inserir o favorito na lista de favoritos

    def desfavoritar(self, id_cliente, id_produto):  # desfavoritar um produto

        if id_cliente <= 0: # se o id do cliente for menor ou igual a zero, levanta um erro
            raise ValueError("Cliente inválido.")
        if id_produto <= 0: # se o id do produto for menor ou igual a zero, levanta um erro
            raise ValueError("Produto inválido.")

        favorito_dao = FavoritoDAO() # DAO encapsula leitura/gravacao em favoritos.json (lista de favoritos)
        if not favorito_dao.Excluir_por_cliente_produto(id_cliente, id_produto): # se o favorito não for encontrado, levanta um erro
            raise ValueError("Favorito nao encontrado.")

    def listar_produtos_favoritos(self, id_cliente):  # listar produtos favoritos do cliente

        if id_cliente <= 0: # se o id do cliente for menor ou igual a zero, levanta um erro
            raise ValueError("Cliente inválido.")

        favorito_dao = FavoritoDAO() # DAO encapsula leitura/gravacao em favoritos.json (lista de favoritos)
        produto_dao = ProdutoDAO() # DAO encapsula leitura/gravacao em produtos.json (lista de produtos)
        produtos_favoritos = [] # lista de produtos favoritos

        for favorito in favorito_dao.Listar_por_cliente(id_cliente): # para cada favorito na lista de favoritos, buscar um produto pelo id
            produto = produto_dao.Listar_id(favorito.get_idProduto()) # buscar um produto pelo id
            if produto is not None: # se o produto não for encontrado, continua o loop
                produtos_favoritos.append(produto) # adiciona o produto na lista de produtos favoritos
                
        return produtos_favoritos # retorna a lista de produtos favoritos
