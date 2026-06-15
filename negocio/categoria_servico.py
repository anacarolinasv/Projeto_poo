from categorias.categoria import Categoria, CategoriaDAO


class CategoriaServico:  # caso de uso: manter cadastro de categorias

    def __init__(self):
        self._dao = CategoriaDAO()

    def listar(self):
        return self._dao.Listar()

    def inserir(self, id_categoria, descricao):
        categoria = Categoria(id_categoria, descricao)
        self._dao.Inserir(categoria)

    def atualizar(self, id_categoria, descricao):
        categoria = Categoria(id_categoria, descricao)
        if not self._dao.Atualizar(categoria):
            raise ValueError("Categoria nao encontrada.")

    def excluir(self, id_categoria):
        return self._dao.Excluir(id_categoria)
