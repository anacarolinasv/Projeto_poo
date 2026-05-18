import json

# Login e senha usados no admin
LOGIN_ADMIN_PADRAO = "admin"
SENHA_ADMIN_PADRAO = "admin123"


class Administrador:

    #--------- Constructor ---------#
    def __init__(self, id, login, senha):
        self.set_id(id)
        self.set_login(login)
        self.set_senha(senha)

    #--------- Setters ---------#
    def set_id(self, id):

        if id > 0:
            self.id = id
        else:
            raise ValueError("ID deve ser maior que 0")

    def set_login(self, login):
        # (login or "") evita erro se vier None; strip() remove espacos nas pontas
        if not (login or "").strip():
            raise ValueError("Login e obrigatorio")
        # Armazena ja normalizado
        self.login = login.strip()

    def set_senha(self, senha):
        # Senha nao pode ser vazia nem so espacos
        if not (senha or "").strip():
            raise ValueError("Senha e obrigatoria")
        self.senha = senha

    #--------- Getters ---------#
    def get_id(self):
        return self.id

    def get_login(self):
        return self.login

    def get_senha(self):
        return self.senha
    
    #--------- To String ---------#
    def __str__(self):
        return f""" ADMINISTRADOR:
        ID: {self.id}
        LOGIN: {self.login}
        """


class AdministradorDAO:

    def __init__(self):
        self.administradores = [] #lista dos dados do administrador

    def Salvar(self): # salvar a lista de administradores no arquivo administradores.json
        with open("administradores/administradores.json", mode="w") as arquivo:
            json.dump(self.administradores, arquivo, default=vars)

    def Abrir(self): # abrir o arquivo administradores.json e carregar os dados na lista de administradores
        try:
            with open("administradores/administradores.json", mode="r") as arquivo:
                dados = json.load(arquivo)
                self.administradores = []
                for obj in dados:
                    a = Administrador(obj["id"], obj["login"], obj["senha"])
                    self.administradores.append(a)
        except FileNotFoundError:
            self.administradores = []

    def garantir_admin_padrao(self): # garantir um administrador inicial com senha pre-definida
        self.Abrir()
        if not self.administradores: # se a lista de administradores estiver vazia
            # Cria administrador id=1 com as constantes LOGIN_ADMIN_PADRAO / SENHA_ADMIN_PADRAO.
            padrao = Administrador(1, LOGIN_ADMIN_PADRAO, SENHA_ADMIN_PADRAO)
            self.administradores.append(padrao)
            self.Salvar()

    def Buscar_por_login(self, login): # buscar um administrador pelo login
        self.Abrir()
        # Comparacao case-insensitive: "Admin" e "admin" encontram o mesmo registro.
        alvo = (login or "").strip().lower()
        for a in self.administradores:
            if a.get_login().strip().lower() == alvo:
                return a
        # Nenhum login igual ao informado (apos normalizacao).
        return None
