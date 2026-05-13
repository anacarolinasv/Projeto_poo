# View (fachada): unico ponto que a UI chama para modelo + regras de negocio — sem input/print.
# Imports agrupados: persistencia direta (DAO/entidades) e servicos de negocio (negocio/*).
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
from negocio.favoritos_servico import FavoritosServico


class View:
    """Metodos estaticos que delegam para DAOs ou servicos (padrao fachada para a camada Templates/ui)."""

    @staticmethod
    def inicializar_app():
        # Cria admin padrao (login/senha) se o arquivo de administradores estiver vazio.
        AdministradorDAO().garantir_admin_padrao()

    @staticmethod
    def usuario_autenticar(login_ou_email, senha):
        """Autentica admin (login) ou cliente (email). Retorna dict de sessao ou None."""
        lo = (login_ou_email or "").strip()
        if not lo or not (senha or "").strip():
            return None
        try:
            # Primeiro tenta fluxo administrador (campo na UI e o mesmo para ambos os perfis).
            AutenticacaoServico().login_admin(lo, senha)
            # Sessao admin: id/nome fixos para exibicao (o modelo admin real pode ter outro id no JSON).
            return {"id": 1, "nome": "admin", "admin": True}
        except ValueError:
            pass
        try:
            c = AutenticacaoServico().login_cliente(lo, senha)
            # Sessao cliente: id e nome reais do cadastro; admin False direciona para UICliente.
            return {"id": c.get_id(), "nome": c.get_nome(), "admin": False}
        except ValueError:
            return None

    @staticmethod
    def abrir_conta_visitante(nome, email, fone, senha, senha_confirmacao):
        # Delega validacoes e persistencia ao caso de uso AbrirContaServico.
        return AbrirContaServico().abrir_conta(nome, email, fone, senha, senha_confirmacao)

    @staticmethod
    def cliente_listar():
        # Lista todos os clientes (tela admin).
        return ClienteDAO().Listar()

    @staticmethod
    def cliente_inserir(id_cliente, nome, email, fone, senha):
        # Monta entidade e persiste (admin informa id manualmente na UI).
        c = Cliente(id_cliente, nome, email, fone, senha)
        ClienteDAO().Inserir(c)

    @staticmethod
    def cliente_atualizar(id_cliente, nome, email, fone, senha):
        # Substitui registro com mesmo id (dados completos vindos do formulario admin).
        c = Cliente(id_cliente, nome, email, fone, senha)
        ClienteDAO().Atualizar(c)

    @staticmethod
    def cliente_excluir(id_cliente):
        # Retorno tipicamente bool indicando se removeu (depende do DAO).
        return ClienteDAO().Deletar(id_cliente)

    @staticmethod
    def categoria_listar():
        # Lista categorias para vincular produtos e manutencao.
        return CategoriaDAO().Listar()

    @staticmethod
    def categoria_inserir(id_categoria, descricao):
        # Nova categoria com id informado pelo admin.
        c = Categoria(id_categoria, descricao)
        CategoriaDAO().Inserir(c)

    @staticmethod
    def categoria_atualizar(id_categoria, descricao):
        # Substitui descricao (e valida id) via entidade Categoria.
        c = Categoria(id_categoria, descricao)
        CategoriaDAO().Atualizar(c)

    @staticmethod
    def categoria_excluir(id_categoria):
        # Retorno conforme implementacao do CategoriaDAO (sucesso/nao encontrado).
        return CategoriaDAO().Excluir(id_categoria)

    @staticmethod
    def produto_listar():
        # Todos os produtos (admin); cliente usa produtos_disponiveis_venda.
        return ProdutoDAO().Listar()

    @staticmethod
    def produtos_disponiveis_venda():
        """Produtos cadastrados com estoque disponivel para venda."""
        # Filtra na fachada para a listagem da loja (cliente) sem expor DAO na UI.
        return [p for p in ProdutoDAO().Listar() if p.get_estoque() > 0]

    @staticmethod
    def carrinho_adicionar_item(carrinho, id_produto, quantidade):
        # carrinho e o dict mutavel mantido em UI.__carrinho; regras de estoque em CarrinhoServico.
        CarrinhoServico().adicionar(carrinho, id_produto, quantidade)

    @staticmethod
    def carrinho_resumo(carrinho):
        # Retorno (linhas, total) usado por uicliente para imprimir o carrinho.
        return CarrinhoServico().montar_resumo(carrinho)

    @staticmethod
    def carrinho_remover_item(carrinho, id_produto):
        CarrinhoServico().remover_item(carrinho, id_produto)

    @staticmethod
    def carrinho_esvaziar(carrinho):
        CarrinhoServico().esvaziar(carrinho)

    @staticmethod
    def produto_inserir(descricao, preco, estoque, id_categoria):
        dao = ProdutoDAO()
        novo_id = dao.Proximo_id()
        p = Produto(novo_id, descricao, preco, estoque, id_categoria)
        dao.Inserir(p)
        return novo_id

    @staticmethod
    def produto_atualizar(id_produto, descricao, preco, estoque, id_categoria):
        # Atualizacao completa do registro do produto (preco, estoque, categoria, etc.).
        p = Produto(id_produto, descricao, preco, estoque, id_categoria)
        ProdutoDAO().Atualizar(p)

    @staticmethod
    def produto_excluir(id_produto):
        return ProdutoDAO().Excluir(id_produto)

    @staticmethod
    def produto_reajustar_percentual(percentual):
        # Percentual aplicado em massa no DAO (ex.: +10% ou -5%).
        ProdutoDAO().Reajustar_precos_percentual(percentual)

    @staticmethod
    def comprar_carrinho(id_cliente, carrinho):
        # Grava venda/itens, baixa estoque e esvazia carrinho (mesmo objeto por referencia).
        CheckoutServico().finalizar_compra(id_cliente, carrinho)

    @staticmethod
    def cliente_vendas_com_itens(id_cliente):
        # Lista de {"venda", "itens"} para relatorio_vendas (somente este cliente).
        return VendaRelatorioServico().listar_por_cliente(id_cliente)

    @staticmethod
    def admin_vendas_com_itens():
        # Todas as vendas com itens (relatorio administrativo).
        return VendaRelatorioServico().listar_todas()

    @staticmethod
    def venda_listar():
        # Cabecalhos de venda sem expandir itens (uso direto do VendaDAO se a UI precisar).
        return VendaDAO().Listar()

    @staticmethod
    def cliente_favorito_adicionar(id_cliente, id_produto):
        FavoritosServico().favoritar(id_cliente, id_produto)

    @staticmethod
    def cliente_favorito_remover(id_cliente, id_produto):
        FavoritosServico().desfavoritar(id_cliente, id_produto)

    @staticmethod
    def cliente_favoritos_listar_produtos(id_cliente):
        return FavoritosServico().listar_produtos_favoritos(id_cliente)
