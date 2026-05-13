from clientes.cliente import ClienteDAO
from favoritos.favorito import Favorito, FavoritoDAO
from produtos.produto import ProdutoDAO


class FavoritosServico:
    """Favoritar produtos por cliente: valida existencia e evita duplicidade."""

    def favoritar(self, id_cliente, id_produto):
        if id_cliente <= 0:
            raise ValueError("Cliente invalido.")
        if id_produto <= 0:
            raise ValueError("Produto invalido.")
        cdao = ClienteDAO()
        if cdao.Listar_id(id_cliente) is None:
            raise ValueError("Cliente nao encontrado.")
        pdao = ProdutoDAO()
        if pdao.Listar_id(id_produto) is None:
            raise ValueError("Produto nao encontrado.")
        fdao = FavoritoDAO()
        if fdao.Buscar_por_cliente_produto(id_cliente, id_produto) is not None:
            raise ValueError("Este produto ja esta nos seus favoritos.")
        fid = fdao.Proximo_id()
        fdao.Inserir(Favorito(fid, id_cliente, id_produto))

    def desfavoritar(self, id_cliente, id_produto):
        if id_cliente <= 0:
            raise ValueError("Cliente invalido.")
        if id_produto <= 0:
            raise ValueError("Produto invalido.")
        fdao = FavoritoDAO()
        if not fdao.Excluir_por_cliente_produto(id_cliente, id_produto):
            raise ValueError("Favorito nao encontrado.")

    def listar_produtos_favoritos(self, id_cliente):
        """Retorna lista de objetos Produto ainda cadastrados (favoritos deste cliente)."""
        if id_cliente <= 0:
            raise ValueError("Cliente invalido.")
        fdao = FavoritoDAO()
        pdao = ProdutoDAO()
        resultado = []
        for f in fdao.Listar_por_cliente(id_cliente):
            p = pdao.Listar_id(f.get_idProduto())
            if p is not None:
                resultado.append(p)
        return resultado
