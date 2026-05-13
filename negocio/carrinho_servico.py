from produtos.produto import ProdutoDAO


class CarrinhoServico:
    """Regras do carrinho: estoque, mesmo produto soma quantidade."""

    def adicionar(self, carrinho, id_produto, quantidade):
        if not isinstance(carrinho, dict):
            raise TypeError("Carrinho invalido.")
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero.")
        dao = ProdutoDAO()
        p = dao.Listar_id(id_produto)
        if p is None:
            raise ValueError("Produto nao encontrado.")
        if p.get_estoque() <= 0:
            raise ValueError("Produto indisponivel para venda.")
        ja = int(carrinho.get(id_produto, 0))
        if ja + quantidade > p.get_estoque():
            raise ValueError(
                f"Quantidade indisponivel. No carrinho: {ja}, estoque: {p.get_estoque()}."
            )
        carrinho[id_produto] = ja + quantidade

    def montar_resumo(self, carrinho):
        """Retorna (linhas, total_carrinho). Cada linha: id, descricao, preco_unitario, quantidade, total_item."""
        dao = ProdutoDAO()
        linhas = []
        total = 0.0
        for id_prod, qtd in list(carrinho.items()):
            p = dao.Listar_id(id_prod)
            if p is None:
                del carrinho[id_prod]
                continue
            pu = float(p.get_preco())
            qtd = int(qtd)
            total_item = round(pu * qtd, 2)
            total += total_item
            linhas.append(
                {
                    "id": id_prod,
                    "descricao": p.get_descricao(),
                    "preco_unitario": pu,
                    "quantidade": qtd,
                    "total_item": total_item,
                }
            )
        return linhas, round(total, 2)
