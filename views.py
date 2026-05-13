# View: acesso ao modelo e regras de negocio — sem input/print (camada de apresentacao fica na UI/Templates).
from administradores.administrador import AdministradorDAO
from clientes.cliente import Cliente, ClienteDAO
from categorias.categoria import Categoria, CategoriaDAO
from produtos.produto import Produto, ProdutoDAO
from vendas.venda import VendaDAO
from negocio.abrir_conta_servico import AbrirContaServico
from negocio.autenticacao_servico import AutenticacaoServico
from negocio.carrinho_servico import CarrinhoServico
from negocio.checkout_servico import CheckoutServico
from negocio.venda_relatorio_servico import VendaRelatorioServico


class View:
    @staticmethod
    def inicializar_app():
        AdministradorDAO().garantir_admin_padrao()

    @staticmethod
    def usuario_autenticar(login_ou_email, senha):
        """Autentica admin (login) ou cliente (email). Retorna dict de sessao ou None."""
        lo = (login_ou_email or "").strip()
        if not lo or not (senha or "").strip():
            return None
        try:
            AutenticacaoServico().login_admin(lo, senha)
            return {"id": 1, "nome": "admin", "admin": True}
        except ValueError:
            pass
        try:
            c = AutenticacaoServico().login_cliente(lo, senha)
            return {"id": c.get_id(), "nome": c.get_nome(), "admin": False}
        except ValueError:
            return None

    @staticmethod
    def abrir_conta_visitante(nome, email, fone, senha, senha_confirmacao):
        return AbrirContaServico().abrir_conta(nome, email, fone, senha, senha_confirmacao)

    @staticmethod
    def cliente_listar():
        return ClienteDAO().Listar()

    @staticmethod
    def cliente_inserir(id_cliente, nome, email, fone, senha):
        c = Cliente(id_cliente, nome, email, fone, senha)
        ClienteDAO().Inserir(c)

    @staticmethod
    def cliente_atualizar(id_cliente, nome, email, fone, senha):
        c = Cliente(id_cliente, nome, email, fone, senha)
        ClienteDAO().Atualizar(c)

    @staticmethod
    def cliente_excluir(id_cliente):
        return ClienteDAO().Deletar(id_cliente)

    @staticmethod
    def categoria_listar():
        return CategoriaDAO().Listar()

    @staticmethod
    def categoria_inserir(id_categoria, descricao):
        c = Categoria(id_categoria, descricao)
        CategoriaDAO().Inserir(c)

    @staticmethod
    def categoria_atualizar(id_categoria, descricao):
        c = Categoria(id_categoria, descricao)
        CategoriaDAO().Atualizar(c)

    @staticmethod
    def categoria_excluir(id_categoria):
        return CategoriaDAO().Excluir(id_categoria)

    @staticmethod
    def produto_listar():
        return ProdutoDAO().Listar()

    @staticmethod
    def produtos_disponiveis_venda():
        """Produtos cadastrados com estoque disponivel para venda."""
        return [p for p in ProdutoDAO().Listar() if p.get_estoque() > 0]

    @staticmethod
    def carrinho_adicionar_item(carrinho, id_produto, quantidade):
        CarrinhoServico().adicionar(carrinho, id_produto, quantidade)

    @staticmethod
    def carrinho_resumo(carrinho):
        return CarrinhoServico().montar_resumo(carrinho)

    @staticmethod
    def produto_inserir(id_produto, descricao, preco, estoque, id_categoria):
        p = Produto(id_produto, descricao, preco, estoque, id_categoria)
        ProdutoDAO().Inserir(p)

    @staticmethod
    def produto_atualizar(id_produto, descricao, preco, estoque, id_categoria):
        p = Produto(id_produto, descricao, preco, estoque, id_categoria)
        ProdutoDAO().Atualizar(p)

    @staticmethod
    def produto_excluir(id_produto):
        return ProdutoDAO().Excluir(id_produto)

    @staticmethod
    def produto_reajustar_percentual(percentual):
        ProdutoDAO().Reajustar_precos_percentual(percentual)

    @staticmethod
    def comprar_carrinho(id_cliente, carrinho):
        CheckoutServico().finalizar_compra(id_cliente, carrinho)

    @staticmethod
    def cliente_vendas_com_itens(id_cliente):
        return VendaRelatorioServico().listar_por_cliente(id_cliente)

    @staticmethod
    def admin_vendas_com_itens():
        return VendaRelatorioServico().listar_todas()

    @staticmethod
    def venda_listar():
        return VendaDAO().Listar()
