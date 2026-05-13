import json

# Credenciais criadas automaticamente na primeira execucao (garantir_admin_padrao).
LOGIN_ADMIN_PADRAO = "admin"
SENHA_ADMIN_PADRAO = "admin123"


class Administrador:
    def __init__(self, id, login, senha):
        self.set_id(id)
        self.set_login(login)
        self.set_senha(senha)

    def set_id(self, id):
        if id > 0:
            self.id = id
        else:
            raise ValueError("ID deve ser maior que 0")

    def set_login(self, login):
        if not (login or "").strip():
            raise ValueError("Login e obrigatorio")
        self.login = login.strip()

    def set_senha(self, senha):
        if not (senha or "").strip():
            raise ValueError("Senha e obrigatoria")
        self.senha = senha

    def get_id(self):
        return self.id

    def get_login(self):
        return self.login

    def get_senha(self):
        return self.senha

    def __str__(self):
        return f""" ADMINISTRADOR:
        ID: {self.id}
        LOGIN: {self.login}
        """


class AdministradorDAO:
    def __init__(self):
        self.administradores = []

    def Salvar(self):
        with open("administradores/administradores.json", mode="w") as arquivo:
            json.dump(self.administradores, arquivo, default=vars)

    def Abrir(self):
        try:
            with open("administradores/administradores.json", mode="r") as arquivo:
                dados = json.load(arquivo)
                self.administradores = []
                for obj in dados:
                    a = Administrador(obj["id"], obj["login"], obj["senha"])
                    self.administradores.append(a)
        except FileNotFoundError:
            self.administradores = []

    def garantir_admin_padrao(self):
        """Garante um administrador inicial com senha pre-definida (Tarefa 2)."""
        self.Abrir()
        if not self.administradores:
            padrao = Administrador(1, LOGIN_ADMIN_PADRAO, SENHA_ADMIN_PADRAO)
            self.administradores.append(padrao)
            self.Salvar()

    def Buscar_por_login(self, login):
        self.Abrir()
        alvo = (login or "").strip().lower()
        for a in self.administradores:
            if a.get_login().strip().lower() == alvo:
                return a
        return None
