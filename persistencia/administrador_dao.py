from entidades.administrador import (
    LOGIN_ADMIN_PADRAO,
    SENHA_ADMIN_PADRAO,
    Administrador,
)
from persistencia.dao import DAO


class AdministradorDAO(DAO):
    entidade = "administrador"

    def __init__(self):
        super().__init__("dados/administradores.json")

    def _from_dict(self, dados):
        return Administrador(dados["id"], dados["login"], dados["senha"])

    def garantir_admin_padrao(self):
        self.Abrir()
        if not self._objetos:
            padrao = Administrador(1, LOGIN_ADMIN_PADRAO, SENHA_ADMIN_PADRAO)
            self._objetos.append(padrao)
            self.Salvar()

    def Buscar_por_login(self, login):
        self.Abrir()
        alvo = (login or "").strip().lower()
        for a in self._objetos:
            if a.get_login().strip().lower() == alvo:
                return a
        return None
