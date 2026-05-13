import json


class Categoria:
#--------- Constructor ---------#
    def __init__(self, id, descricao):
        self.set_id(id)
        self.set_descricao(descricao)
    
#--------- Setters ----------#
    def set_id(self, id):
        if id > 0:
            self.id = id
        else:
            raise ValueError("ID deve ser maior que 0")
    
    def set_descricao(self, descricao):
        if not isinstance(descricao, str): 
            raise TypeError("descricao deve ser str (string)")
        self.descricao = descricao

#--------- Getters ----------#
    def get_id(self):
        return self.id
    
    def get_descricao(self):
        return self.descricao

#--------- To String ----------#
    def __str__(self):
        return f""" CATEGORIA:
        ID: {self.id}
        DESCRICAO: {self.descricao}
        """     

class CategoriaDAO:
    def __init__(self):
        self.categorias = [] # lista de todas as categorias
        
    def Salvar(self): # salvar a lista de categorias no arquivo categorias.json
        with open('categorias/categorias.json' ,mode ='w') as arquivo: # abrir o arquivo categorias.json em modo escrita
            json.dump(self.categorias, arquivo, default= vars) # salvar a lista de categorias no arquivo categorias.json
    
    def Inserir(self, obj):
        self.Abrir() # carregar categorias existentes antes de inserir
        if self.Listar_id(obj.get_id()) is not None:
            raise ValueError("Ja existe categoria com esse id")
        self.categor1ias.append(obj) # adiciona o objeto na lista
        self.Salvar() # salvar a lista de categorias no arquivo categorias.json
    
    def Abrir(self): # abrir o arquivo categorias.json e carregar os dados na lista de categorias
        try: # vai tentar:
            with open('categorias/categorias.json' ,mode ='r') as arquivo: # abrir o arquivo categorias.json em modo leitura
                categorias_json = json.load(arquivo) # carregar os dados do arquivo para uma variável (dicionário)
                self.categorias = [] # limpar a lista de categorias
                for obj in categorias_json: # para cada objeto no dicionário, criar um objeto Categoria
                    c = Categoria(obj["id"], obj["descricao"]) # criar um objeto Categoria com os dados do objeto
                    self.categorias.append(c) # adicionar o objeto na lista
        except FileNotFoundError: # se o arquivo não for encontrado, limpar a lista de categorias
            self.categorias = [] # limpar a lista de categorias

    def Listar(self): # retornar a lista de categorias
        self.Abrir() # abrir o arquivo categorias.json e carregar os dados na lista de categorias
        return self.categorias # retornar a lista de categorias
    
    def Listar_id(self, id): # retornar a lista de categorias ordenada pelo id
        self.Abrir() # abrir o arquivo categorias.json e carregar os dados na lista de categorias
        for categoria in self.categorias: # para cada categoria na lista
            if categoria.get_id() == id: # se o id da categoria for igual ao id passado
                return categoria # retornar a categoria
        return None # se a categoria não for encontrada, retornar None
    
    def Atualizar(self, obj):
        self.Abrir()
        categoria = self.Listar_id(obj.get_id()) # retornar a categoria pelo id
        if categoria is not None: # se a categoria for encontrada
            categoria.set_descricao(obj.get_descricao()) # atualizar a descricao da categoria
            self.Salvar() # salvar a lista de categorias no arquivo categorias.json
            return True # retornar True se a categoria foi atualizada
        return False # retornar False se a categoria não foi atualizada
    
    def Excluir(self, id):
        self.Abrir()
        categoria = self.Listar_id(id) # retornar a categoria pelo id   
        if categoria is not None: # se a categoria for encontrada
            self.categorias.remove(categoria) # remover a categoria da lista
            self.Salvar() # salvar a lista de categorias no arquivo categorias.json
            return True # retornar True se a categoria foi excluída
        return False # retornar False se a categoria não foi excluída