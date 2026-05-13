# Modelo Cliente (entidade) e ClienteDAO (persistencia em JSON).
from clientes.cliente import Cliente, ClienteDAO


class AbrirContaServico:
    """Caso de uso: visitante abre conta para passar a ser cliente cadastrado."""

    def __init__(self):
        # DAO encapsula leitura/gravacao em clientes.json (lista de clientes).
        self._dao = ClienteDAO()

    def abrir_conta(self, nome, email, fone, senha, senha_confirmacao):
        # Normaliza strings: None vira "" e remove espacos nas pontas (nome, email, fone).
        nome = (nome or "").strip()
        email = (email or "").strip()
        fone = (fone or "").strip()
        # Senhas nao recebem strip aqui: espacos no meio/fim podem ser intencionais no cadastro.
        senha = senha or ""
        senha_confirmacao = senha_confirmacao or ""
        # Campos obrigatorios apos normalizacao (string vazia = nao preenchido).
        if not nome:
            raise ValueError("Nome e obrigatorio.")
        if not email:
            raise ValueError("Email e obrigatorio.")
        if not fone:
            raise ValueError("Telefone e obrigatorio.")
        if not senha:
            raise ValueError("Senha e obrigatoria.")
        # Garante que o usuario digitou a mesma senha nos dois campos da UI.
        if senha != senha_confirmacao:
            raise ValueError("As senhas nao conferem.")
        # Politica minima de seguranca (evita senhas triviais de 1-3 caracteres).
        if len(senha) < 4:
            raise ValueError("Senha deve ter pelo menos 4 caracteres.")
        # Email e chave logica: nao pode haver duas contas com o mesmo email.
        if self._dao.Listar_por_email(email) is not None:
            raise ValueError("Ja existe conta com este email.")
        # Proximo id numerico livre na sequencia armazenada (ex.: max(id)+1 ou 1 se vazio).
        novo_id = self._dao.Proximo_id()
        # Instancia o dominio com os dados validados.
        cliente = Cliente(novo_id, nome, email, fone, senha)
        # Persiste no arquivo via DAO e mantem a lista em memoria atualizada conforme implementacao.
        self._dao.Inserir(cliente)
        # Quem chamou (ex.: View) pode exibir id e mensagem de sucesso.
        return cliente
