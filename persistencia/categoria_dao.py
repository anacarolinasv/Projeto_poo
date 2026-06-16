from entidades.categoria import Categoria
from persistencia.dao import DAO


class CategoriaDAO(DAO):
    entidade = "categoria"

    def __init__(self):
        super().__init__("dados/categorias.json")

    def _from_dict(self, dados):
        return Categoria(dados["id"], dados["descricao"])
