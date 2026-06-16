from entidades.produto import Produto
from excecoes.excecoes import EntidadeInvalidaError
from persistencia.dao import DAO


class ProdutoDAO(DAO):
    entidade = "produto"

    def __init__(self):
        super().__init__("dados/produtos.json")

    def _from_dict(self, dados):
        return Produto(
            dados["id"],
            dados["descricao"],
            dados["preco"],
            dados["estoque"],
            dados["idCategoria"],
        )

    def Reajustar_precos_percentual(self, percentual):
        self.Abrir()
        fator = 1.0 + float(percentual) / 100.0
        for produto in self._objetos:
            novo_preco = round(produto.get_preco() * fator, 2)
            if novo_preco < 0:
                raise EntidadeInvalidaError("Reajuste resultaria em preço negativo.")
            produto.set_preco(novo_preco)
        self.Salvar()
