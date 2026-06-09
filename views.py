from negocio.abrir_conta_servico import AbrirContaServico
from negocio.administrador_servico import AdministradorServico
from negocio.autenticacao_servico import AutenticacaoServico
from negocio.carrinho_servico import CarrinhoServico
from negocio.categoria_servico import CategoriaServico
from negocio.checkout_servico import CheckoutServico
from negocio.cliente_servico import ClienteServico
from negocio.favoritos_servico import FavoritosServico
from negocio.preco_servico import PrecoServico
from negocio.produto_servico import ProdutoServico
from negocio.promocao_servico import PromocaoServico
from negocio.venda_relatorio_servico import VendaRelatorioServico


class View:  # classe estatica para a fachada da aplicacao.

    @staticmethod
    def inicializar_app():
        AdministradorServico().garantir_admin_padrao()

    @staticmethod
    def autenticar(login_ou_email, senha):
        return AutenticacaoServico().autenticar(login_ou_email, senha)

    @staticmethod
    def abrir_conta(nome, email, fone, senha, senha_confirmacao):
        return AbrirContaServico().abrir_conta(
            nome, email, fone, senha, senha_confirmacao
        )

    @staticmethod
    def cliente_listar():
        return ClienteServico().listar()

    @staticmethod
    def cliente_inserir(id_cliente, nome, email, fone, senha):
        ClienteServico().inserir(id_cliente, nome, email, fone, senha)

    @staticmethod
    def cliente_atualizar(id_cliente, nome, email, fone, senha):
        ClienteServico().atualizar(id_cliente, nome, email, fone, senha)

    @staticmethod
    def cliente_excluir(id_cliente):
        return ClienteServico().excluir(id_cliente)

    @staticmethod
    def categoria_listar():
        return CategoriaServico().listar()

    @staticmethod
    def categoria_inserir(id_categoria, descricao):
        CategoriaServico().inserir(id_categoria, descricao)

    @staticmethod
    def categoria_atualizar(id_categoria, descricao):
        CategoriaServico().atualizar(id_categoria, descricao)

    @staticmethod
    def categoria_excluir(id_categoria):
        return CategoriaServico().excluir(id_categoria)

    @staticmethod
    def produto_listar():
        return ProdutoServico().listar()

    @staticmethod
    def produtos_disponiveis_venda():
        return ProdutoServico().listar_disponiveis_venda()

    @staticmethod
    def adicionar(carrinho, id_produto, quantidade):
        CarrinhoServico().adicionar(carrinho, id_produto, quantidade)

    @staticmethod
    def montar_resumo(carrinho):
        return CarrinhoServico().montar_resumo(carrinho)

    @staticmethod
    def remover_item(carrinho, id_produto):
        CarrinhoServico().remover_item(carrinho, id_produto)

    @staticmethod
    def esvaziar(carrinho):
        CarrinhoServico().esvaziar(carrinho)

    @staticmethod
    def sincronizar(id_cliente, carrinho):
        CarrinhoServico().sincronizar(id_cliente, carrinho)

    @staticmethod
    def carregar(id_cliente, carrinho):
        CarrinhoServico().carregar(id_cliente, carrinho)

    @staticmethod
    def produto_inserir(descricao, preco, estoque, id_categoria):
        return ProdutoServico().inserir(descricao, preco, estoque, id_categoria)

    @staticmethod
    def produto_atualizar(id_produto, descricao, preco, estoque, id_categoria):
        ProdutoServico().atualizar(id_produto, descricao, preco, estoque, id_categoria)

    @staticmethod
    def produto_excluir(id_produto):
        return ProdutoServico().excluir(id_produto)

    @staticmethod
    def produto_caminho_foto(id_produto):
        return ProdutoServico().caminho_foto(id_produto)

    @staticmethod
    def produto_salvar_foto(id_produto, arquivo):
        ProdutoServico().salvar_foto(id_produto, arquivo)

    @staticmethod
    def produto_excluir_foto(id_produto):
        ProdutoServico().excluir_foto(id_produto)

    @staticmethod
    def produto_html_foto(id_produto, fallback):
        return ProdutoServico().html_foto(id_produto, fallback)

    @staticmethod
    def produto_reajustar_percentual(percentual):
        ProdutoServico().reajustar_percentual(percentual)

    @staticmethod
    def promocao_listar():
        return PromocaoServico().listar()

    @staticmethod
    def promocao_listar_ativas():
        return PromocaoServico().listar_ativas()

    @staticmethod
    def promocao_inserir(id_categoria, percentual, data_inicio, data_fim):
        return PromocaoServico().inserir(id_categoria, percentual, data_inicio, data_fim)

    @staticmethod
    def promocao_atualizar(id_promocao, id_categoria, percentual, data_inicio, data_fim):
        PromocaoServico().atualizar(
            id_promocao, id_categoria, percentual, data_inicio, data_fim
        )

    @staticmethod
    def promocao_excluir(id_promocao):
        return PromocaoServico().excluir(id_promocao)

    @staticmethod
    def produto_preco_detalhes(produto):
        return PrecoServico().detalhes(produto)

    @staticmethod
    def finalizar_compra(id_cliente, carrinho):
        CheckoutServico().finalizar_compra(id_cliente, carrinho)

    @staticmethod
    def listar_por_cliente(id_cliente):
        return VendaRelatorioServico().listar_por_cliente(id_cliente)

    @staticmethod
    def listar_todas():
        return VendaRelatorioServico().listar_todas()

    @staticmethod
    def venda_listar():
        return VendaRelatorioServico().listar()

    @staticmethod
    def favoritar(id_cliente, id_produto):
        FavoritosServico().favoritar(id_cliente, id_produto)

    @staticmethod
    def desfavoritar(id_cliente, id_produto):
        FavoritosServico().desfavoritar(id_cliente, id_produto)

    @staticmethod
    def listar_produtos_favoritos(id_cliente):
        return FavoritosServico().listar_produtos_favoritos(id_cliente)
