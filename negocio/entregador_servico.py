from entidades.entregador import Entregador
from persistencia.entregador_dao import EntregadorDAO
from excecoes.excecoes import RegraNegocioError
from util.validacao import validar_senha


class EntregadorServico:
    def __init__(self):
        self._dao = EntregadorDAO()

    def listar(self):
        return self._dao.Listar()

    def listar_id(self, id_entregador):
        return self._dao.Listar_id(id_entregador)

    def cadastrar(self, nome, fone, login, senha, senha_confirmacao):
        senha = senha or ""
        senha_confirmacao = senha_confirmacao or ""
        validar_senha(senha, obrigatoria=True)
        if senha != senha_confirmacao:
            raise RegraNegocioError("As senhas não conferem.")
        if self._dao.Buscar_por_login(login) is not None:
            raise RegraNegocioError("Já existe entregador com este login.")
        novo_id = self._dao.Proximo_id()
        entregador = Entregador(novo_id, nome, fone, login, senha)
        self._dao.Inserir(entregador)
        return entregador

    def autenticar(self, login, senha):
        if not (login or "").strip() or not (senha or "").strip():
            return None
        entregador = self._dao.Buscar_por_login(login)
        if entregador is None or entregador.get_senha() != senha:
            return None
        return entregador
