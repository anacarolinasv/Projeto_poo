import json


class VendaItem:
#--------- Constructor ---------#
    def __init__(self, id, quantidade, preco, idVenda, idProduto):
        self.set_id(id)
        self.set_quantidade(quantidade)
        self.set_preco(preco)
        self.self_idVenda(idVenda)
        self.set_idProduto(idProduto)

#--------- Setters ----------#
    def set_id(self, id):
        if id > 0:
            self.id = id
        else:
            raise ValueError("ID deve ser maior que 0")
    
    def set_quantidade(self, quantidade):           
        if not isinstance(quantidade, int): # verifica se a quantidade é um número inteiro
            raise TypeError("quantidade deve ser int (número inteiro)")
        self.quantidade = quantidade
    
    def set_preco(self, preco):
        if not isinstance(preco, (int, float)): # verifica se o preco é um número decimal
            raise TypeError("preco deve ser float (número decimal)")
        self.preco = float(preco)
    
    def self_idVenda(self, idVenda):
        if idVenda > 0:
            self.idVenda = idVenda
        else:
            raise ValueError("ID da venda deve ser maior que 0")
    
    def set_idProduto(self, idProduto):
        if idProduto > 0:
            self.idProduto = idProduto
        else:
            raise ValueError("ID do produto deve ser maior que 0")

#--------- Getters ----------#
    def get_id(self):
        return self.id  

    def get_idVenda(self):
        return self.idVenda
    
    def get_idProduto(self):
        return self.idProduto
    
    def get_quantidade(self):
        return self.quantidade
    
    def get_preco(self):
        return self.preco

#--------- To String ----------#    
    def __str__(self):
        return f""" VENDA ITEM:
        ID: {self.id}
        ID VENDA: {self.idVenda}
        ID PRODUTO: {self.idProduto}
        QUANTIDADE: {self.quantidade}
        PRECO: {self.preco}
        """

class VendaItemDAO:
    def __init__(self):
        self.vendaItem = [] # lista de todos os itens de venda
        
    def Salvar(self): # salvar a lista de itens de venda no arquivo vendaItem.json
        with open('vendas/vendaItem.json' ,mode ='w') as arquivo: # abrir o arquivo vendaItem.json em modo escrita
            json.dump(self.vendaItem, arquivo, default= vars) # salvar a lista de itens de venda no arquivo vendaItem.json
    
    def Inserir(self, obj):
        self.Abrir()
        if self.Listar_id(obj.get_id()) is not None:
            raise ValueError("Ja existe item de venda com esse id")
        self.vendaItem.append(obj)
        self.Salvar()

    def Proximo_id(self):
        self.Abrir()
        if not self.vendaItem:
            return 1
        return max(x.get_id() for x in self.vendaItem) + 1

    def Listar_por_venda(self, id_venda):
        self.Abrir()
        return [x for x in self.vendaItem if x.get_idVenda() == id_venda]

    def Abrir(self): # abrir o arquivo vendaItem.json e carregar os dados na lista de itens de venda
        try: # vai tentar:
            with open('vendas/vendaItem.json' ,mode ='r') as arquivo: # abrir o arquivo vendaItem.json em modo leitura     
                vendaItem_json = json.load(arquivo) # carregar os dados do arquivo para uma variável (dicionário)
                self.vendaItem = [] # limpar a lista de itens de venda
                for obj in vendaItem_json: # para cada objeto no dicionário, criar um objeto VendaItem
                    v = VendaItem(obj["id"], obj["quantidade"], obj["preco"], obj["idVenda"], obj["idProduto"]) # criar um objeto VendaItem com os dados do objeto
                    self.vendaItem.append(v) # adicionar o objeto na lista
        except FileNotFoundError: # se o arquivo não for encontrado, limpar a lista de itens de venda
            self.vendaItem = [] # limpar a lista de itens de venda
    
    def Listar(self): # retornar a lista de itens de venda
        self.Abrir() # abrir o arquivo vendaItem.json e carregar os dados na lista de itens de venda
        return self.vendaItem # retornar a lista de itens de venda
    
    def Listar_id(self, id): # retornar a lista de itens de venda ordenada pelo id
        self.Abrir() # abrir o arquivo vendaItem.json e carregar os dados na lista de itens de venda
        for vendaItem in self.vendaItem: # para cada item de venda na lista
            if vendaItem.get_id() == id: # se o id do item de venda for igual ao id passado
                return vendaItem # retornar o item de venda
        return None # se o item de venda não for encontrado, retornar None
    
    def Atualizar(self, obj):
        self.Abrir()
        vendaItem = self.Listar_id(obj.get_id()) # retornar o item de venda pelo id
        if vendaItem is not None: # se o item de venda for encontrado       
            vendaItem.set_quantidade(obj.get_quantidade())
            vendaItem.set_preco(obj.get_preco())
            vendaItem.self_idVenda(obj.get_idVenda())
            vendaItem.set_idProduto(obj.get_idProduto())
            self.Salvar()
            return True
        return False
        
    def Excluir(self, id):
        self.Abrir()
        vendaItem = self.Listar_id(id) # retornar o item de venda pelo id
        if vendaItem is not None: # se o item de venda for encontrado
            self.vendaItem.remove(vendaItem) # remover o item de venda da lista
            self.Salvar() # salvar a lista de itens de venda no arquivo vendaItem.json
            return True # retornar True se o item de venda foi excluído
        return False # retornar False se o item de venda não foi excluído