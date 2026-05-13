from clientes.cliente import Cliente, ClienteDAO


class AbrirContaServico:
    """Caso de uso: visitante abre conta para passar a ser cliente cadastrado."""

    def __init__(self):
        self._dao = ClienteDAO()

    def abrir_conta(self, nome, email, fone, senha, senha_confirmacao):
        nome = (nome or "").strip()
        email = (email or "").strip()
        fone = (fone or "").strip()
        senha = senha or ""
        senha_confirmacao = senha_confirmacao or ""
        if not nome:
            raise ValueError("Nome e obrigatorio.")
        if not email:
            raise ValueError("Email e obrigatorio.")
        if not fone:
            raise ValueError("Telefone e obrigatorio.")
        if not senha:
            raise ValueError("Senha e obrigatoria.")
        if senha != senha_confirmacao:
            raise ValueError("As senhas nao conferem.")
        if len(senha) < 4:
            raise ValueError("Senha deve ter pelo menos 4 caracteres.")
        if self._dao.Listar_por_email(email) is not None:
            raise ValueError("Ja existe conta com este email.")
        novo_id = self._dao.Proximo_id()
        cliente = Cliente(novo_id, nome, email, fone, senha)
        self._dao.Inserir(cliente)
        return cliente
