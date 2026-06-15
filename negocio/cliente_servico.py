from clientes.cliente import Cliente, ClienteDAO


class ClienteServico:  # caso de uso: manter cadastro de clientes

    def __init__(self):
        self._dao = ClienteDAO()

    def listar(self):
        return self._dao.Listar()

    def inserir(self, id_cliente, nome, email, fone, senha):
        cliente = Cliente(id_cliente, nome, email, fone, senha)
        self._dao.Inserir(cliente)

    def atualizar(self, id_cliente, nome, email, fone, senha):
        cliente = Cliente(id_cliente, nome, email, fone, senha)
        if not self._dao.Atualizar(cliente):
            raise ValueError("Cliente não encontrado.")

    def excluir(self, id_cliente):
        return self._dao.Deletar(id_cliente)
