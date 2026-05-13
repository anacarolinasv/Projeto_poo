from datetime import datetime
import json

class Venda:
#--------- Constructor ---------#
    def __init__(self, id, data, carrinho, total, idCliente):
        self.set_id(id)
        self.set_data(data)
        self.set_carrinho(carrinho)
        self.set_total(total)
        self.set_idCliente(idCliente)

#--------- Setters ----------#
    def set_id(self, id):
        if id > 0 :
            self.id = id
        else:
            raise ValueError("ID deve ser maior que 0")
    
    def set_data(self, data):
        if not isinstance(data, datetime):
            raise TypeError("data deve ser um objeto datetime")
        self.data = data
    
    def set_carrinho(self, carrinho):
        if not isinstance(carrinho, bool): # verifica se o carrinho é um booleano
            raise TypeError("carrinho deve ser bool (True ou False)")
        self.carrinho = carrinho

    def set_total(self, total):
        if not isinstance(total, (int, float)): # verifica se o total é um número decimal
            raise TypeError("total deve ser float (número decimal)")
        self.total = float(total)
    
    def set_idCliente(self, idCliente):
        if idCliente > 0:
            self.idCliente = idCliente
        else:
            raise ValueError("ID do cliente deve ser maior que 0")

#--------- Getters ----------#
    def get_id(self):
        return self.id
    
    def get_data(self):
        return self.data
    
    def get_carrinho(self):
        return self.carrinho
    
    def get_total(self):
        return self.total
    
    def get_idCliente(self):
        return self.idCliente

#--------- To String ----------#
    def __str__(self):
        return f""" VENDA:
        ID: {self.id}
        DATA: {self.data}
        CARRINHO: {self.carrinho}
        TOTAL: {self.total}
        ID CLIENTE: {self.idCliente}        
        """

def _venda_para_dict(v):
    d = v.get_data()
    if isinstance(d, datetime):
        ds = d.isoformat()
    else:
        ds = str(d)
    return {
        "id": v.get_id(),
        "data": ds,
        "carrinho": v.get_carrinho(),
        "total": v.get_total(),
        "idCliente": v.get_idCliente(),
    }


def _dict_para_venda(obj):
    raw = obj["data"]
    if isinstance(raw, str):
        data = datetime.fromisoformat(raw)
    elif isinstance(raw, datetime):
        data = raw
    else:
        raise TypeError("data da venda invalida no arquivo")
    return Venda(
        int(obj["id"]),
        data,
        bool(obj["carrinho"]),
        float(obj["total"]),
        int(obj["idCliente"]),
    )


class VendaDAO:
    def __init__(self):
        self.vendas = [] # lista de todas as vendas

    def Salvar(self): # salvar a lista de vendas no arquivo vendas.json
        with open('vendas/vendas.json' ,mode ='w') as arquivo: # abrir o arquivo vendas.json em modo escrita
            json.dump([_venda_para_dict(v) for v in self.vendas], arquivo, indent=2)
    
    def Inserir(self, obj):
        self.Abrir() # carregar vendas existentes antes de inserir
        if self.Listar_id(obj.get_id()) is not None:
            raise ValueError("Ja existe venda com esse id")
        self.vendas.append(obj) # adiciona o objeto na lista
        self.Salvar() # salvar a lista de vendas no arquivo vendas.json
    
    def Abrir(self): # abrir o arquivo vendas.json e carregar os dados na lista de vendas
        try: # vai tentar:
            with open('vendas/vendas.json' ,mode ='r') as arquivo: # abrir o arquivo vendas.json em modo leitura
                vendas_json = json.load(arquivo) # carregar os dados do arquivo para uma variável (dicionário)
                self.vendas = [] # limpar a lista de vendas
                for obj in vendas_json: # para cada objeto no dicionário, criar um objeto Venda
                    v = _dict_para_venda(obj)
                    self.vendas.append(v) # adicionar o objeto na lista
        except FileNotFoundError: # se o arquivo não for encontrado, limpar a lista de vendas
            self.vendas = [] # limpar a lista de vendas

    def Listar(self): # retornar a lista de vendas
        self.Abrir() # abrir o arquivo vendas.json e carregar os dados na lista de vendas
        return self.vendas # retornar a lista de vendas

    def Proximo_id(self):
        self.Abrir()
        if not self.vendas:
            return 1
        return max(v.get_id() for v in self.vendas) + 1

    def Listar_por_cliente(self, id_cliente):
        self.Abrir()
        return [v for v in self.vendas if v.get_idCliente() == id_cliente]

    def Listar_id(self, id): # retornar a lista de vendas ordenada pelo id
        self.Abrir() # abrir o arquivo vendas.json e carregar os dados na lista de vendas
        for venda in self.vendas: # para cada venda na lista
            if venda.get_id() == id:
                return venda # retornar a venda
        return None # se a venda não for encontrada, retornar None
    
    def Atualizar(self, obj):
        self.Abrir()
        venda = self.Listar_id(obj.get_id()) # retornar a venda pelo id
        if venda is not None: # se a venda for encontrada
            venda.set_data(obj.get_data()) # atualizar a data da venda
            venda.set_carrinho(obj.get_carrinho()) # atualizar o carrinho da venda
            venda.set_total(obj.get_total()) # atualizar o total da venda
            venda.set_idCliente(obj.get_idCliente()) # atualizar o id do cliente da venda
            self.Salvar() # salvar a lista de vendas no arquivo vendas.json
            return True # retornar True se a venda foi atualizada
        return False # retornar False se a venda não foi atualizada
    
    def Excluir(self, id):
        self.Abrir()
        venda = self.Listar_id(id) # retornar a venda pelo id
        if venda is not None: # se a venda for encontrada
            self.vendas.remove(venda) # remover a venda da lista
            self.Salvar() # salvar a lista de vendas no arquivo vendas.json
            return True # retornar True se a venda foi excluída
        return False # retornar False se a venda não foi excluída


