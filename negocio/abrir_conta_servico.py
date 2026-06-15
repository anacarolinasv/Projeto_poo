from clientes.cliente import Cliente, ClienteDAO

class AbrirContaServico: # caso de uso: visitante abre conta para passar a ser cliente cadastrado

    #--------- Constructor ---------#
    def __init__(self):
        self._dao = ClienteDAO() # DAO encapsula leitura/gravacao em clientes.json (lista de clientes)

    def abrir_conta(self, nome, email, fone, senha, senha_confirmacao): # abrir conta
        nome = (nome or "").strip() # normaliza o nome
        email = (email or "").strip() # normaliza o email
        fone = (fone or "").strip() # normaliza o telefone
        senha = senha or "" # normaliza a senha
        senha_confirmacao = senha_confirmacao or "" # normaliza a senha de confirmação
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
            raise ValueError("As senhas não conferem.")
        # Politica minima de seguranca (evita senhas triviais de 1-3 caracteres).
        if len(senha) < 4:
            raise ValueError("Senha deve ter pelo menos 4 caracteres.")
        # Email e chave logica: nao pode haver duas contas com o mesmo email.
        if self._dao.Listar_por_email(email) is not None:
            raise ValueError("Já existe conta com este email.")
        # Proximo id numerico livre na sequencia armazenada (ex.: max(id)+1 ou 1 se vazio).
        novo_id = self._dao.Proximo_id()
        # Instancia o dominio com os dados validados.
        cliente = Cliente(novo_id, nome, email, fone, senha)
        # Persiste no arquivo via DAO e mantem a lista em memoria atualizada conforme implementacao.
        self._dao.Inserir(cliente)
        # Quem chamou (ex.: View) pode exibir id e mensagem de sucesso.
        return cliente
