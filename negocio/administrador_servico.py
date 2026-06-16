from persistencia.administrador_dao import AdministradorDAO


class AdministradorServico:  # caso de uso: inicializacao do sistema

    def __init__(self):
        self._dao = AdministradorDAO()

    def garantir_admin_padrao(self):
        self._dao.garantir_admin_padrao()
