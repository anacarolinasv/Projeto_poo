import json
import os

from excecoes.excecoes import EntidadeInvalidaError


class DAO:
    """Classe genérica de persistência (Data Access Object).

    Concentra a funcionalidade comum de leitura/gravação das entidades em
    arquivos JSON. As subclasses informam o caminho do arquivo e como
    reconstruir a entidade a partir de um dicionário (método `_from_dict`).
    Cada entidade persistida deve expor `get_id()` e `to_dict()`.
    """

    # Nome da entidade usado nas mensagens de erro (sobrescrito nas subclasses).
    entidade = "registro"

    def __init__(self, arquivo):
        self._arquivo = arquivo
        self._objetos = []

    # --------- A ser implementado pela subclasse ---------#
    def _from_dict(self, dados):
        raise NotImplementedError(
            "Subclasses de DAO devem implementar _from_dict(dados)"
        )

    # --------- Persistência ---------#
    def Abrir(self):
        try:
            with open(self._arquivo, mode="r", encoding="utf-8") as arquivo:
                registros = json.load(arquivo)
            self._objetos = [self._from_dict(registro) for registro in registros]
        except FileNotFoundError:
            self._objetos = []
        return self._objetos

    def Salvar(self):
        diretorio = os.path.dirname(self._arquivo)
        if diretorio:
            os.makedirs(diretorio, exist_ok=True)
        with open(self._arquivo, mode="w", encoding="utf-8") as arquivo:
            json.dump([obj.to_dict() for obj in self._objetos], arquivo, indent=2)

    # --------- Operações comuns ---------#
    def Listar(self):
        self.Abrir()
        return self._objetos

    def Listar_id(self, id):
        self.Abrir()
        for obj in self._objetos:
            if obj.get_id() == id:
                return obj
        return None

    def Proximo_id(self):
        self.Abrir()
        if not self._objetos:
            return 1
        return max(obj.get_id() for obj in self._objetos) + 1

    def Inserir(self, obj):
        self.Abrir()
        if self.Listar_id(obj.get_id()) is not None:
            raise EntidadeInvalidaError(f"Já existe {self.entidade} com esse id")
        self._objetos.append(obj)
        self.Salvar()

    def Atualizar(self, obj):
        self.Abrir()
        for indice, atual in enumerate(self._objetos):
            if atual.get_id() == obj.get_id():
                self._objetos[indice] = obj
                self.Salvar()
                return True
        return False

    def Excluir(self, id):
        self.Abrir()
        alvo = self.Listar_id(id)
        if alvo is not None:
            self._objetos.remove(alvo)
            self.Salvar()
            return True
        return False
