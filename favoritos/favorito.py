import json

class Favorito:

    #--------- Constructor ---------#
    def __init__(self, id, idCliente, idProduto):
        self.set_id(id)
        self.set_idCliente(idCliente)
        self.set_idProduto(idProduto)

    #--------- Setters ---------#
    def set_id(self, id):
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
    
    #--------- Getters ---------#
    def get_id(self):
        return self.id

    def get_idCliente(self):
        return self.idCliente

    def get_idProduto(self):
        return self.idProduto

    #--------- To String ---------#
    def __str__(self):
        return f""" FAVORITO:
        ID: {self.id}
        ID CLIENTE: {self.idCliente}
        ID PRODUTO: {self.idProduto}
        """


class FavoritoDAO:
 
    def __init__(self):
        self.favoritos = [] # lista de todos os favoritos

    def Salvar(self): # salvar a lista de favoritos no arquivo favoritos.json
        with open("favoritos/favoritos.json", mode="w") as arquivo:
            json.dump(self.favoritos, arquivo, default=vars)

    def Abrir(self): # abrir o arquivo favoritos.json e carregar os dados na lista de favoritos
        try:
            with open("favoritos/favoritos.json", mode="r") as arquivo:
                registros_json = json.load(arquivo)
                self.favoritos = []
                for registro in registros_json:
                    favorito = Favorito(
                        int(registro["id"]),
                        int(registro["idCliente"]),
                        int(registro["idProduto"]),
                    )
                    self.favoritos.append(favorito)
        except FileNotFoundError:
            self.favoritos = []

    def Proximo_id(self): # retornar o próximo ID disponível (1 se não houver registros)
        self.Abrir()
        if not self.favoritos:
            return 1
        return max(favorito.get_id() for favorito in self.favoritos) + 1

    def Inserir(self, favorito): # inserir um favorito na lista de favoritos
        self.Abrir()
        if self.Listar_id(favorito.get_id()) is not None: # se o favorito já existe, levanta um erro
            raise ValueError("Ja existe favorito com esse id")
        if self.Buscar_por_cliente_produto(favorito.get_idCliente(), favorito.get_idProduto()) is not None:
            raise ValueError("Este produto ja esta nos favoritos deste cliente.")
        self.favoritos.append(favorito) # adiciona o favorito na lista de favoritos
        self.Salvar() # salvar a lista de favoritos no arquivo favoritos.json

    def Listar(self): # Devolve todos os favoritos
        self.Abrir()
        return self.favoritos

    def Listar_id(self, id_favorito): # buscar um favorito pelo ID
        self.Abrir()
        for favorito in self.favoritos:
            if favorito.get_id() == id_favorito:
                return favorito
        return None # se o favorito não for encontrado, retorna None

    def Buscar_por_cliente_produto(self, id_cliente, id_produto):  # Localiza favorito pela combinação cliente + produto.
        self.Abrir()
        for favorito in self.favoritos: # para cada favorito na lista de favoritos
            if favorito.get_idCliente() == id_cliente and favorito.get_idProduto() == id_produto:
                return favorito
        return None # se o favorito não for encontrado, retorna None

    def Listar_por_cliente(self, id_cliente):# Filtra favoritos de um único cliente.
        self.Abrir()
        return [
            favorito
            for favorito in self.favoritos
            if favorito.get_idCliente() == id_cliente
        ]

    def Excluir(self, id_favorito):# Remove pelo ID do favorito
        self.Abrir()
        favorito = self.Listar_id(id_favorito) # buscar um favorito pelo ID
        if favorito is not None: # se o favorito for encontrado, remove o favorito da lista de favoritos
            self.favoritos.remove(favorito) # remove o favorito da lista de favoritos
            self.Salvar() # salvar a lista de favoritos no arquivo favoritos.json
            return True # retornar True se o favorito foi removido
        return False # retornar False se o favorito não foi removido

    def Excluir_por_cliente_produto(self, id_cliente, id_produto): # Remove pelo par cliente/produto; retorna True se removeu.
        self.Abrir()
        favorito = self.Buscar_por_cliente_produto(id_cliente, id_produto)
        if favorito is not None: # se o favorito for encontrado, remove o favorito da lista de favoritos
            self.favoritos.remove(favorito) # remove o favorito da lista de favoritos
            self.Salvar() # salvar a lista de favoritos no arquivo favoritos.json
            return True # retornar True se o favorito foi removido
        return False # retornar False se o favorito não foi removido
