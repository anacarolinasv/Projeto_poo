from datetime import date

from excecoes.excecoes import EntidadeInvalidaError

ID_CATEGORIA_TODAS = 0


class Promocao:
    def __init__(self, id, idCategoria, percentual, dataInicio, dataFim):
        self.set_id(id)
        self.set_idCategoria(idCategoria)
        self.set_percentual(percentual)
        self.set_dataInicio(dataInicio)
        self.set_dataFim(dataFim)

    def set_id(self, id):
        if not isinstance(id, int) or id <= 0:
            raise EntidadeInvalidaError("ID deve ser um inteiro maior que 0")
        self.__id = id

    def set_idCategoria(self, idCategoria):
        if not isinstance(idCategoria, int) or idCategoria < 0:
            raise EntidadeInvalidaError("idCategoria inválido")
        self.__idCategoria = idCategoria

    def aplica_todas_categorias(self):
        return self.__idCategoria == ID_CATEGORIA_TODAS

    def set_percentual(self, percentual):
        if not isinstance(percentual, (int, float)):
            raise EntidadeInvalidaError("Percentual deve ser um número")
        pct = float(percentual)
        if pct <= 0 or pct > 100:
            raise EntidadeInvalidaError(
                "Percentual deve estar entre 0 e 100 (exclusivo de 0)"
            )
        self.__percentual = pct

    def set_dataInicio(self, dataInicio):
        self.__dataInicio = _parse_data(dataInicio, "dataInicio")

    def set_dataFim(self, dataFim):
        self.__dataFim = _parse_data(dataFim, "dataFim")
        if self.__dataFim < self.__dataInicio:
            raise EntidadeInvalidaError(
                "dataFim deve ser igual ou posterior a dataInicio"
            )

    def get_id(self):
        return self.__id

    def get_idCategoria(self):
        return self.__idCategoria

    def get_percentual(self):
        return self.__percentual

    def get_dataInicio(self):
        return self.__dataInicio

    def get_dataFim(self):
        return self.__dataFim

    def to_dict(self):
        return {
            "id": self.get_id(),
            "idCategoria": self.get_idCategoria(),
            "percentual": self.get_percentual(),
            "dataInicio": self.get_dataInicio().isoformat(),
            "dataFim": self.get_dataFim().isoformat(),
        }

    def esta_ativa(self, referencia=None):
        ref = referencia or date.today()
        return self.__dataInicio <= ref <= self.__dataFim

    def __str__(self):
        return f""" PROMOCAO:
        ID: {self.get_id()}
        ID CATEGORIA: {self.get_idCategoria()}
        PERCENTUAL: {self.get_percentual()}%
        INICIO: {self.get_dataInicio()}
        FIM: {self.get_dataFim()}
        """


def _parse_data(valor, nome_campo):
    if isinstance(valor, date):
        return valor
    if isinstance(valor, str):
        try:
            return date.fromisoformat(valor)
        except ValueError as e:
            raise EntidadeInvalidaError(
                f"{nome_campo} inválida: use formato AAAA-MM-DD"
            ) from e
    raise EntidadeInvalidaError(f"{nome_campo} deve ser date ou str (AAAA-MM-DD)")
