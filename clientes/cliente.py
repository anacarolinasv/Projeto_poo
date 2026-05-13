import json

class Cliente:
#--------- Constructor ---------#
    def __init__(self, id, nome, email, fone, senha=""):
        self.set_id(id)
        self.set_nome(nome)
        self.set_email(email)
        self.set_fone(fone)
        self.set_senha(senha)

#--------- Setters ----------#
    def set_id(self, id):
        if id > 0 : 
            self.id = id
        else:
            raise ValueError("ID deve ser maior que 0")  # interrompe esse caminho e mostra o erro
    
    def set_nome(self, nome):
        self.nome = nome
    
    def set_email(self, email):
        self.email = email
    
    def set_fone(self, fone):
        self.fone = fone

    def set_senha(self, senha):
        self.senha = senha if senha is not None else ""

#--------- Getters ----------#
    def get_id(self):
        return self.id
    
    def get_nome(self):
        return self.nome
    
    def get_email(self):
        return self.email
    
    def get_fone(self):
        return self.fone

    def get_senha(self):
        return self.senha

#--------- To String ----------#
    def __str__(self):
        return f""" CLIENTE:
        ID: {self.id}
        NOME: {self.nome}
        EMAIL: {self.email}
        FONE: {self.fone}
        """

class ClienteDAO:
    def __init__(self):
        self.cliente = [] # lista de todos os clientes

    def Salvar(self): # salvar a lista de clientes no arquivo clientes.json
        with open('clientes/clientes.json' ,mode ='w') as arquivo: # abrir o arquivo clientes.json em modo escrita
            json.dump(self.cliente, arquivo, default= vars) # salvar a lista de clientes no arquivo clientes.json

    def Inserir(self, obj):
        self.Abrir() # carregar clientes existentes antes de inserir
        if self.Listar_id(obj.get_id()) is not None:
            raise ValueError("Ja existe cliente com esse id")
        self.cliente.append(obj) # adiciona o objeto na lista
        self.Salvar() # salvar a lista de clientes no arquivo clientes.json
    
    def Abrir(self): # abrir o arquivo clientes.json e carregar os dados na lista de clientes
        try: # vai tentar:
            with open('clientes/clientes.json' ,mode ='r') as arquivo: # abrir o arquivo clientes.json em modo leitura
                clientes_json = json.load(arquivo) # carregar os dados do arquivo para uma variável (dicionário)
                self.cliente = [] # limpar a lista de clientes
                for obj in clientes_json: # para cada objeto no dicionário, criar um objeto Cliente
                    senha = obj.get("senha", "")
                    c = Cliente(obj["id"], obj["nome"], obj["email"], obj["fone"], senha)
                    self.cliente.append(c) # adicionar o objeto na lista
        
        except FileNotFoundError: # se o arquivo não for encontrado, limpar a lista de clientes
            self.cliente = [] # limpar a lista de clientes

    def Listar(self): # retornar a lista de clientes
        self.Abrir() # abrir o arquivo clientes.json e carregar os dados na lista de clientes
        return self.cliente # retornar a lista de clientes  
    
    def Listar_id(self, id): # retornar a lista de clientes ordenada pelo id
        self.Abrir() # abrir o arquivo clientes.json e carregar os dados na lista de clientes
        for cliente in self.cliente: # para cada cliente na lista
            if cliente.get_id() == id: # se o id do cliente for igual ao id passado
                return cliente # retornar o cliente
        return None # se o cliente não for encontrado, retornar None

    def Listar_por_email(self, email):
        self.Abrir()
        alvo = (email or "").strip().lower()
        for cliente in self.cliente:
            if cliente.get_email().strip().lower() == alvo:
                return cliente
        return None

    def Proximo_id(self):
        self.Abrir()
        if not self.cliente:
            return 1
        return max(c.get_id() for c in self.cliente) + 1

    def Atualizar(self, obj):
        self.Abrir()
        x = self.Listar_id(obj.get_id())
        if x is not None:
            x.set_nome(obj.get_nome())
            x.set_email(obj.get_email())
            x.set_fone(obj.get_fone())
            x.set_senha(obj.get_senha())
            self.Salvar()
            return True
        return False
    
    def Deletar(self, id): # deletar um cliente pelo id
        self.Abrir() # abrir o arquivo clientes.json e carregar os dados na lista de clientes
        for cliente in self.cliente: # para cada cliente na lista
            if cliente.get_id() == id: # se o id do cliente for igual ao id passado
                self.cliente.remove(cliente) # remover o cliente da lista
                self.Salvar() # salvar a lista de clientes no arquivo clientes.json
                return True
        return False