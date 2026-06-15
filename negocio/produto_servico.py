from produtos.produto import Produto, ProdutoDAO
from negocio.produto_foto_servico import ProdutoFotoServico


class ProdutoServico:  # caso de uso: manter cadastro de produtos e reajustar precos

    def __init__(self):
        self._dao = ProdutoDAO()
        self._foto_servico = ProdutoFotoServico()

    def listar(self):
        return self._dao.Listar()

    def listar_disponiveis_venda(self):
        return [
            produto
            for produto in self._dao.Listar()
            if produto.get_estoque() > 0
        ]

    def inserir(self, descricao, preco, estoque, id_categoria):
        id_produto = self._dao.Proximo_id()
        produto = Produto(id_produto, descricao, preco, estoque, id_categoria)
        self._dao.Inserir(produto)
        return id_produto

    def atualizar(self, id_produto, descricao, preco, estoque, id_categoria):
        produto = Produto(id_produto, descricao, preco, estoque, id_categoria)
        if not self._dao.Atualizar(produto):
            raise ValueError("Produto não encontrado.")

    def excluir(self, id_produto):
        ok = self._dao.Excluir(id_produto)
        if ok:
            self._foto_servico.excluir_foto(id_produto)
        return ok

    def reajustar_percentual(self, percentual):
        self._dao.Reajustar_precos_percentual(percentual)

    def caminho_foto(self, id_produto):
        return self._foto_servico.caminho_foto(id_produto)

    def salvar_foto(self, id_produto, arquivo):
        self._foto_servico.salvar_foto(id_produto, arquivo)

    def excluir_foto(self, id_produto):
        self._foto_servico.excluir_foto(id_produto)

    def html_foto(self, id_produto, fallback):
        return self._foto_servico.html_imagem(id_produto, fallback)
