from datetime import date

from persistencia.categoria_dao import CategoriaDAO
from entidades.promocao import ID_CATEGORIA_TODAS, Promocao
from persistencia.promocao_dao import PromocaoDAO


class PromocaoServico:
    def __init__(self):
        self._dao = PromocaoDAO()
        self._categoria_dao = CategoriaDAO()

    def listar(self):
        return self._dao.Listar()

    def inserir(self, id_categoria, percentual, data_inicio, data_fim):
        self._validar_categoria(id_categoria)
        inicio = self._parse_data(data_inicio)
        fim = self._parse_data(data_fim)
        self._validar_sem_sobreposicao(id_categoria, inicio, fim)
        promocao = Promocao(
            self._dao.Proximo_id(),
            id_categoria,
            percentual,
            inicio,
            fim,
        )
        self._dao.Inserir(promocao)
        return promocao.get_id()

    def atualizar(self, id_promocao, id_categoria, percentual, data_inicio, data_fim):
        if self._dao.Listar_id(id_promocao) is None:
            raise ValueError("Promoção não encontrada.")
        self._validar_categoria(id_categoria)
        inicio = self._parse_data(data_inicio)
        fim = self._parse_data(data_fim)
        self._validar_sem_sobreposicao(id_categoria, inicio, fim, id_excluir=id_promocao)
        promocao = Promocao(id_promocao, id_categoria, percentual, inicio, fim)
        if not self._dao.Atualizar(promocao):
            raise ValueError("Promoção não encontrada.")

    def excluir(self, id_promocao):
        return self._dao.Excluir(id_promocao)

    def buscar_ativa_por_categoria(self, id_categoria, referencia=None):
        ref = self._parse_data(referencia) if referencia is not None else date.today()
        ativas = []
        for promocao in self._dao.Listar():
            cat = promocao.get_idCategoria()
            if cat not in (ID_CATEGORIA_TODAS, id_categoria):
                continue
            if promocao.esta_ativa(ref):
                ativas.append(promocao)
        if not ativas:
            return None
        return max(ativas, key=lambda p: p.get_percentual())

    def listar_ativas(self, referencia=None):
        ref = self._parse_data(referencia) if referencia is not None else date.today()
        return [p for p in self._dao.Listar() if p.esta_ativa(ref)]

    def _validar_categoria(self, id_categoria):
        if id_categoria == ID_CATEGORIA_TODAS:
            return
        if self._categoria_dao.Listar_id(id_categoria) is None:
            raise ValueError("Categoria não encontrada.")

    def _categorias_conflitam(self, cat_a, cat_b):
        if cat_a == ID_CATEGORIA_TODAS or cat_b == ID_CATEGORIA_TODAS:
            return True
        return cat_a == cat_b

    def _validar_sem_sobreposicao(self, id_categoria, inicio, fim, id_excluir=None):
        for promocao in self._dao.Listar():
            if id_excluir is not None and promocao.get_id() == id_excluir:
                continue
            if not self._categorias_conflitam(id_categoria, promocao.get_idCategoria()):
                continue
            if inicio <= promocao.get_dataFim() and promocao.get_dataInicio() <= fim:
                raise ValueError(
                    "Já existe promocao conflitante para o periodo informado."
                )

    def _parse_data(self, valor):
        if isinstance(valor, date):
            return valor
        if hasattr(valor, "date"):
            return valor.date()
        if isinstance(valor, str):
            return date.fromisoformat(valor)
        raise TypeError("Data inválida.")
