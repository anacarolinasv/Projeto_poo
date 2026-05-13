# Persistência e modelo de favoritos (cliente x produto) em JSON.
import json


class Favorito:
    """Representa um favorito: vínculo entre um cliente e um produto com identificador único."""

    def __init__(self, id, idCliente, idProduto):
        # Inicializa atributos via setters para garantir validação.
        self.set_id(id)
        self.set_idCliente(idCliente)
        self.set_idProduto(idProduto)

    def set_id(self, id):
        # ID interno do favorito; deve ser positivo.
        if id > 0:
            self.id = id
        else:
            raise ValueError("ID deve ser maior que 0")

    def set_idCliente(self, idCliente):
        # Referência ao cliente dono do favorito.
        if idCliente > 0:
            self.idCliente = idCliente
        else:
            raise ValueError("ID do cliente deve ser maior que 0")

    def set_idProduto(self, idProduto):
        # Referência ao produto favoritado.
        if idProduto > 0:
            self.idProduto = idProduto
        else:
            raise ValueError("ID do produto deve ser maior que 0")

    def get_id(self):
        return self.id

    def get_idCliente(self):
        return self.idCliente

    def get_idProduto(self):
        return self.idProduto

    def __str__(self):
        # Texto legível para exibição ou depuração.
        return f""" FAVORITO:
        ID: {self.id}
        ID CLIENTE: {self.idCliente}
        ID PRODUTO: {self.idProduto}
        """


class FavoritoDAO:
    """Acesso a dados: lista em memória sincronizada com favoritos/favoritos.json."""

    def __init__(self):
        # Lista de instâncias Favorito; preenchida por Abrir().
        self.favoritos = []

    def Salvar(self):
        # Grava a lista atual no arquivo JSON (sobrescreve o arquivo).
        with open("favoritos/favoritos.json", mode="w") as arquivo:
            json.dump(self.favoritos, arquivo, default=vars)

    def Abrir(self):
        # Carrega favoritos do disco; se o arquivo não existir, inicia lista vazia.
        try:
            with open("favoritos/favoritos.json", mode="r") as arquivo:
                dados = json.load(arquivo)
                self.favoritos = []
                for obj in dados:
                    # Reconstrói objetos Favorito a partir dos dicionários do JSON.
                    f = Favorito(
                        int(obj["id"]),
                        int(obj["idCliente"]),
                        int(obj["idProduto"]),
                    )
                    self.favoritos.append(f)
        except FileNotFoundError:
            self.favoritos = []

    def Proximo_id(self):
        # Retorna o próximo ID disponível (1 se não houver registros).
        self.Abrir()
        if not self.favoritos:
            return 1
        return max(x.get_id() for x in self.favoritos) + 1

    def Inserir(self, obj):
        # Garante ID único e par (cliente, produto) único antes de persistir.
        self.Abrir()
        if self.Listar_id(obj.get_id()) is not None:
            raise ValueError("Ja existe favorito com esse id")
        if self.Buscar_por_cliente_produto(obj.get_idCliente(), obj.get_idProduto()) is not None:
            raise ValueError("Este produto ja esta nos favoritos deste cliente.")
        self.favoritos.append(obj)
        self.Salvar()

    def Listar(self):
        # Devolve todos os favoritos após recarregar do arquivo.
        self.Abrir()
        return self.favoritos

    def Listar_id(self, id):
        # Busca um favorito pelo ID ou retorna None.
        self.Abrir()
        for f in self.favoritos:
            if f.get_id() == id:
                return f
        return None

    def Buscar_por_cliente_produto(self, id_cliente, id_produto):
        # Localiza favorito pela combinação cliente + produto.
        self.Abrir()
        for f in self.favoritos:
            if f.get_idCliente() == id_cliente and f.get_idProduto() == id_produto:
                return f
        return None

    def Listar_por_cliente(self, id_cliente):
        # Filtra favoritos de um único cliente.
        self.Abrir()
        return [f for f in self.favoritos if f.get_idCliente() == id_cliente]

    def Excluir(self, id):
        # Remove pelo ID do favorito; retorna True se removeu, False se não achou.
        self.Abrir()
        f = self.Listar_id(id)
        if f is not None:
            self.favoritos.remove(f)
            self.Salvar()
            return True
        return False

    def Excluir_por_cliente_produto(self, id_cliente, id_produto):
        # Remove pelo par cliente/produto; retorna True se removeu.
        self.Abrir()
        f = self.Buscar_por_cliente_produto(id_cliente, id_produto)
        if f is not None:
            self.favoritos.remove(f)
            self.Salvar()
            return True
        return False
