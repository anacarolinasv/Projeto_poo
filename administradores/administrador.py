# Biblioteca padrao para ler/gravar o arquivo JSON dos administradores.
import json

# Login e senha usados quando o arquivo ainda nao existe ou esta vazio.
# A funcao garantir_admin_padrao cria o primeiro registro com estes valores.
LOGIN_ADMIN_PADRAO = "admin"
SENHA_ADMIN_PADRAO = "admin123"


class Administrador:
    """Entidade de dominio: um usuario com perfil administrador (id, login, senha)."""

    def __init__(self, id, login, senha):
        # Delega validacao e atribuicao aos setters (regras centralizadas).
        self.set_id(id)
        self.set_login(login)
        self.set_senha(senha)

    def set_id(self, id):
        # IDs validos sao inteiros positivos (1, 2, ...); zero ou negativo e erro.
        if id > 0:
            self.id = id
        else:
            raise ValueError("ID deve ser maior que 0")

    def set_login(self, login):
        # (login or "") evita erro se vier None; strip() remove espacos nas pontas.
        if not (login or "").strip():
            raise ValueError("Login e obrigatorio")
        # Armazena ja normalizado (sem espacos sobrando nas extremidades).
        self.login = login.strip()

    def set_senha(self, senha):
        # Senha nao pode ser vazia nem so espacos (mesmo padrao do login).
        if not (senha or "").strip():
            raise ValueError("Senha e obrigatoria")
        # Aqui a senha e guardada como digitada (sem strip), exceto que vazio ja foi barrado.
        self.senha = senha

    def get_id(self):
        return self.id

    def get_login(self):
        return self.login

    def get_senha(self):
        return self.senha

    def __str__(self):
        # Texto amigavel para print; senha nao aparece por seguranca.
        return f""" ADMINISTRADOR:
        ID: {self.id}
        LOGIN: {self.login}
        """


class AdministradorDAO:
    """Data Access Object: le/escreve lista de Administrador em administradores.json."""

    def __init__(self):
        # Lista em memoria espelhada no arquivo apos Salvar() / carregada no Abrir().
        self.administradores = []

    def Salvar(self):
        # "w" sobrescreve o arquivo; default=vars serializa cada objeto como dict de atributos.
        with open("administradores/administradores.json", mode="w") as arquivo:
            json.dump(self.administradores, arquivo, default=vars)

    def Abrir(self):
        try:
            with open("administradores/administradores.json", mode="r") as arquivo:
                # dados e uma lista de dicts com chaves id, login, senha (formato JSON).
                dados = json.load(arquivo)
                self.administradores = []
                for obj in dados:
                    # Reconstroi instancias de Administrador a partir de cada dict.
                    a = Administrador(obj["id"], obj["login"], obj["senha"])
                    self.administradores.append(a)
        except FileNotFoundError:
            # Primeira execucao ou arquivo apagado: comeca com lista vazia.
            self.administradores = []

    def garantir_admin_padrao(self):
        """Garante um administrador inicial com senha pre-definida (Tarefa 2)."""
        # Carrega o que ja existe em disco antes de decidir se precisa criar o padrao.
        self.Abrir()
        if not self.administradores:
            # Cria administrador id=1 com as constantes LOGIN_ADMIN_PADRAO / SENHA_ADMIN_PADRAO.
            padrao = Administrador(1, LOGIN_ADMIN_PADRAO, SENHA_ADMIN_PADRAO)
            self.administradores.append(padrao)
            self.Salvar()

    def Buscar_por_login(self, login):
        # Sempre reler do arquivo para ver dados atualizados (outros processos ou testes).
        self.Abrir()
        # Comparacao case-insensitive: "Admin" e "admin" encontram o mesmo registro.
        alvo = (login or "").strip().lower()
        for a in self.administradores:
            if a.get_login().strip().lower() == alvo:
                return a
        # Nenhum login igual ao informado (apos normalizacao).
        return None
