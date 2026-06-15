import json
import os


class CarrinhoDAO:

    def __init__(self):
        self._path = "carrinhos/carrinhos.json"

    def Abrir(self):
        try:
            with open(self._path, mode="r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
                return dados if isinstance(dados, dict) else {}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def Salvar(self, dados):
        os.makedirs(os.path.dirname(self._path), exist_ok=True)
        with open(self._path, mode="w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo)

    def Carregar_por_cliente(self, id_cliente):
        return self.Abrir().get(str(int(id_cliente)), {})

    def Salvar_por_cliente(self, id_cliente, carrinho):
        todos = self.Abrir()
        todos[str(int(id_cliente))] = {
            str(int(id_produto)): int(qtd) for id_produto, qtd in carrinho.items()
        }
        self.Salvar(todos)
