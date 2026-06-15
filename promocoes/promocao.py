from datetime import date
import json

ID_CATEGORIA_TODAS = 0


class Promocao:
    def __init__(self, id, idCategoria, percentual, dataInicio, dataFim):
        self.set_id(id)
        self.set_idCategoria(idCategoria)
        self.set_percentual(percentual)
        self.set_dataInicio(dataInicio)
        self.set_dataFim(dataFim)

    def set_id(self, id):
        if id > 0:
            self.id = id
        else:
            raise ValueError("ID deve ser maior que 0")

    def set_idCategoria(self, idCategoria):
        if not isinstance(idCategoria, int) or idCategoria < 0:
            raise ValueError("idCategoria invalido")
        self.idCategoria = idCategoria

    def aplica_todas_categorias(self):
        return self.idCategoria == ID_CATEGORIA_TODAS

    def set_percentual(self, percentual):
        if not isinstance(percentual, (int, float)):
            raise TypeError("percentual deve ser float (numero decimal)")
        pct = float(percentual)
        if pct <= 0 or pct > 100:
            raise ValueError("percentual deve estar entre 0 e 100 (exclusivo de 0)")
        self.percentual = pct

    def set_dataInicio(self, dataInicio):
        self.dataInicio = _parse_data(dataInicio, "dataInicio")

    def set_dataFim(self, dataFim):
        self.dataFim = _parse_data(dataFim, "dataFim")
        if self.dataFim < self.dataInicio:
            raise ValueError("dataFim deve ser igual ou posterior a dataInicio")

    def get_id(self):
        return self.id

    def get_idCategoria(self):
        return self.idCategoria

    def get_percentual(self):
        return self.percentual

    def get_dataInicio(self):
        return self.dataInicio

    def get_dataFim(self):
        return self.dataFim

    def esta_ativa(self, referencia=None):
        ref = referencia or date.today()
        return self.dataInicio <= ref <= self.dataFim

    def __str__(self):
        return f""" PROMOCAO:
        ID: {self.id}
        ID CATEGORIA: {self.idCategoria}
        PERCENTUAL: {self.percentual}%
        INICIO: {self.dataInicio}
        FIM: {self.dataFim}
        """


def _parse_data(valor, nome_campo):
    if isinstance(valor, date):
        return valor
    if isinstance(valor, str):
        try:
            return date.fromisoformat(valor)
        except ValueError as e:
            raise ValueError(f"{nome_campo} invalida: use formato AAAA-MM-DD") from e
    raise TypeError(f"{nome_campo} deve ser date ou str (AAAA-MM-DD)")


def _promocao_para_dict(promocao):
    return {
        "id": promocao.get_id(),
        "idCategoria": promocao.get_idCategoria(),
        "percentual": promocao.get_percentual(),
        "dataInicio": promocao.get_dataInicio().isoformat(),
        "dataFim": promocao.get_dataFim().isoformat(),
    }


class PromocaoDAO:
    def __init__(self):
        self.promocoes = []

    def Salvar(self):
        dados = [_promocao_para_dict(p) for p in self.promocoes]
        with open("promocoes/promocoes.json", mode="w") as arquivo:
            json.dump(dados, arquivo)

    def Abrir(self):
        try:
            with open("promocoes/promocoes.json", mode="r") as arquivo:
                promocoes_json = json.load(arquivo)
                self.promocoes = []
                for obj in promocoes_json:
                    p = Promocao(
                        obj["id"],
                        obj["idCategoria"],
                        obj["percentual"],
                        obj["dataInicio"],
                        obj["dataFim"],
                    )
                    self.promocoes.append(p)
        except FileNotFoundError:
            self.promocoes = []

    def Inserir(self, obj):
        self.Abrir()
        if self.Listar_id(obj.get_id()) is not None:
            raise ValueError("Ja existe promocao com esse id")
        self.promocoes.append(obj)
        self.Salvar()

    def Listar(self):
        self.Abrir()
        return self.promocoes

    def Listar_id(self, id):
        self.Abrir()
        for promocao in self.promocoes:
            if promocao.get_id() == id:
                return promocao
        return None

    def Atualizar(self, obj):
        self.Abrir()
        promocao = self.Listar_id(obj.get_id())
        if promocao is not None:
            promocao.set_idCategoria(obj.get_idCategoria())
            promocao.set_percentual(obj.get_percentual())
            promocao.set_dataInicio(obj.get_dataInicio())
            promocao.set_dataFim(obj.get_dataFim())
            self.Salvar()
            return True
        return False

    def Excluir(self, id):
        self.Abrir()
        promocao = self.Listar_id(id)
        if promocao is not None:
            self.promocoes.remove(promocao)
            self.Salvar()
            return True
        return False

    def Proximo_id(self):
        self.Abrir()
        if not self.promocoes:
            return 1
        return max(p.get_id() for p in self.promocoes) + 1
