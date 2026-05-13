import json

class Produto:
#--------- Constructor ---------#
    def __init__(self, id, descricao, preco, estoque, idCategoria):
        self.set_id(id)
        self.set_descricao(descricao)
        self.set_preco(preco)
        self.set_estoque(estoque)
        self.set_idCategoria(idCategoria)
        
#--------- Setters ----------#
    def set_id(self, id):
        if id > 0:
            self.id = id
        else:
            raise ValueError("ID deve ser maior que 0")
    
    def set_descricao(self, descricao):
        if not isinstance(descricao, str): # verifica se a descricao é uma string
            raise TypeError("descricao deve ser str (string)")
        self.descricao = descricao
    
    def set_preco(self, preco):
        if not isinstance(preco, (int, float)): # verifica se o preco é um número decimal
            raise TypeError("preco deve ser float (número decimal)")
        self.preco = float(preco)
    
    def set_estoque(self, estoque):
        if not isinstance(estoque, (int)): # verifica se o estoque é um número inteiro
            raise TypeError("estoque deve ser int (número inteiro)")
        self.estoque = int(estoque)
    
    def set_idCategoria(self, idCategoria):
        if not isinstance(idCategoria, int): # verifica se o idCategoria é um número inteiro
            raise TypeError("idCategoria deve ser int (número inteiro)")
        self.idCategoria = int(idCategoria)
    
#--------- Getters ----------#
    def get_id(self):
        return self.id
    
    def get_descricao(self):
        return self.descricao
    
    def get_preco(self):
        return self.preco
    
    def get_estoque(self):
        return self.estoque
    
    def get_idCategoria(self):
        return self.idCategoria

#--------- To String ----------#
    def __str__(self):  
        return f""" PRODUTO:
        ID: {self.id}
        DESCRICAO: {self.descricao}
        PRECO: {self.preco}
        ESTOQUE: {self.estoque}
        ID CATEGORIA: {self.idCategoria}
        """     

class ProdutoDAO:
    def __init__(self):
        self.produtos = [] # lista de todos os produtos
        
    def Salvar(self): # salvar a lista de produtos no arquivo produtos.json
        with open('produtos/produtos.json' ,mode ='w') as arquivo: # abrir o arquivo produtos.json em modo escrita
            json.dump(self.produtos, arquivo, default= vars) # salvar a lista de produtos no arquivo produtos.json
    
    def Inserir(self, obj):
        self.Abrir() # carregar produtos existentes antes de inserir
        if self.Listar_id(obj.get_id()) is not None:
            raise ValueError("Ja existe produto com esse id")
        self.produtos.append(obj) # adiciona o objeto na lista
        self.Salvar() # salvar a lista de produtos no arquivo produtos.json
    
    def Abrir(self): # abrir o arquivo produtos.json e carregar os dados na lista de produtos
        try: # vai tentar:
            with open('produtos/produtos.json' ,mode ='r') as arquivo: # abrir o arquivo produtos.json em modo leitura
                produtos_json = json.load(arquivo) # carregar os dados do arquivo para uma variável (dicionário)
                self.produtos = [] # limpar a lista de produtos
                for obj in produtos_json: # para cada objeto no dicionário, criar um objeto Produto
                    p = Produto(obj["id"], obj["descricao"], obj["preco"], obj["estoque"], obj["idCategoria"]) # criar um objeto Produto com os dados do objeto
                    self.produtos.append(p) # adicionar o objeto na lista
        except FileNotFoundError: # se o arquivo não for encontrado, limpar a lista de produtos
            self.produtos = [] # limpar a lista de produtos
    def Listar(self): # retornar a lista de produtos
        self.Abrir() # abrir o arquivo produtos.json e carregar os dados na lista de produtos
        return self.produtos # retornar a lista de produtos
    
    def Listar_id(self, id): # retornar a lista de produtos ordenada pelo id
        self.Abrir() # abrir o arquivo produtos.json e carregar os dados na lista de produtos
        for produto in self.produtos: # para cada produto na lista
            if produto.get_id() == id: # se o id do produto for igual ao id passado
                return produto # retornar o produto
        return None # se o produto não for encontrado, retornar None

    def Proximo_id(self):
        self.Abrir()  # Garante lista atualizada a partir do JSON antes de calcular o proximo id livre.
        if not self.produtos: # Arquivo vazio ou sem produtos: primeiro cadastro usa id 1.
            return 1
        return max(p.get_id() for p in self.produtos) + 1  # Pega o maior id ja usado e soma 1.

    def Atualizar(self, obj):
        self.Abrir()
        produto = self.Listar_id(obj.get_id()) # retornar o produto pelo id
        if produto is not None: # se o produto for encontrado
            produto.set_descricao(obj.get_descricao()) # atualizar a descricao do produto
            produto.set_preco(obj.get_preco()) # atualizar o preco do produto
            produto.set_estoque(obj.get_estoque()) # atualizar o estoque do produto
            produto.set_idCategoria(obj.get_idCategoria()) # atualizar o id da categoria do produto
            self.Salvar() # salvar a lista de produtos no arquivo produtos.json
            return True # retornar True se o produto foi atualizado
        return False # retornar False se o produto não foi atualizado

    def Reajustar_precos_percentual(self, percentual):
        """Aplica reajuste de preco em todos os produtos (percentual pode ser negativo)."""
        self.Abrir()
        fator = 1.0 + float(percentual) / 100.0
        for produto in self.produtos:
            novo_preco = round(produto.get_preco() * fator, 2)
            if novo_preco < 0:
                raise ValueError("Reajuste resultaria em preco negativo.")
            produto.set_preco(novo_preco)
        self.Salvar()

    def Excluir(self, id):
        self.Abrir()
        produto = self.Listar_id(id) # retornar o produto pelo id
        if produto is not None: # se o produto for encontrado
            self.produtos.remove(produto) # remover o produto da lista
            self.Salvar() # salvar a lista de produtos no arquivo produtos.json
            return True # retornar True se o produto foi excluído
        return False # retornar False se o produto não foi excluído