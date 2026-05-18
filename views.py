import json
import os

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

_CARRINHOS_PATH = "carrinhos/carrinhos.json"


class View:  # classe estatica para a fachada da aplicacao.

    @staticmethod
    def inicializar_app(): # metodo estatico para inicializar a aplicacao.
        AdministradorDAO().garantir_admin_padrao()

    @staticmethod
    def usuario_autenticar(login_ou_email, senha): # metodo estatico para autenticar o usuario.
        login_normalizado = (login_ou_email or "").strip() # remove espacos em branco do login ou email.
        senha_normalizada = (senha or "").strip() # remove espacos em branco da senha.
        if not login_normalizado or not senha_normalizada: # se o login ou email ou a senha for vazio, retorna None
            return None # retorna None se o login ou email ou a senha for vazio
        try:
            AutenticacaoServico().login_admin(login_normalizado, senha_normalizada) # chama o metodo login_admin do servico de autenticacao para autenticar o usuario
            return {"id": 1, "nome": "admin", "admin": True} # retorna o id, nome e admin do usuario
        except ValueError:
            pass # se ocorrer um erro de valor, passa para o proximo try
        try:
            cliente = AutenticacaoServico().login_cliente(
                login_normalizado, senha_normalizada
            ) # chama o metodo login_cliente do servico de autenticacao para autenticar o usuario
            return {
                "id": cliente.get_id(),
                "nome": cliente.get_nome(),
                "admin": False,
            } # retorna o id, nome e admin do usuario
        except ValueError:
            return None # retorna None se ocorrer um erro de valor

    @staticmethod
    def abrir_conta_visitante(nome, email, fone, senha, senha_confirmacao):
        return AbrirContaServico().abrir_conta(
            nome, email, fone, senha, senha_confirmacao
        )

    @staticmethod
    def cliente_listar():
        return ClienteDAO().Listar()

    @staticmethod
    def cliente_inserir(id_cliente, nome, email, fone, senha):
        cliente = Cliente(id_cliente, nome, email, fone, senha)
        ClienteDAO().Inserir(cliente)

    @staticmethod
    def cliente_atualizar(id_cliente, nome, email, fone, senha):
        cliente = Cliente(id_cliente, nome, email, fone, senha)
        ClienteDAO().Atualizar(cliente)

    @staticmethod
    def cliente_excluir(id_cliente):
        return ClienteDAO().Deletar(id_cliente)

    @staticmethod
    def categoria_listar():
        return CategoriaDAO().Listar()

    @staticmethod
    def categoria_inserir(id_categoria, descricao):
        categoria = Categoria(id_categoria, descricao)
        CategoriaDAO().Inserir(categoria)

    @staticmethod
    def categoria_atualizar(id_categoria, descricao):
        categoria = Categoria(id_categoria, descricao)
        CategoriaDAO().Atualizar(categoria)

    @staticmethod
    def categoria_excluir(id_categoria):
        return CategoriaDAO().Excluir(id_categoria)

    @staticmethod
    def produto_listar():
        return ProdutoDAO().Listar()

    @staticmethod
    def produtos_disponiveis_venda():
        return [
            produto
            for produto in ProdutoDAO().Listar()
            if produto.get_estoque() > 0
        ]

    @staticmethod
    def carrinho_adicionar_item(carrinho, id_produto, quantidade):
        CarrinhoServico().adicionar(carrinho, id_produto, quantidade)

    @staticmethod
    def carrinho_resumo(carrinho):
        return CarrinhoServico().montar_resumo(carrinho)

    @staticmethod
    def carrinho_remover_item(carrinho, id_produto):
        CarrinhoServico().remover_item(carrinho, id_produto)

    @staticmethod
    def carrinho_esvaziar(carrinho):
        CarrinhoServico().esvaziar(carrinho)

    @staticmethod
    def _carregar_carrinhos_arquivo():
        try:
            with open(_CARRINHOS_PATH, mode="r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
                return dados if isinstance(dados, dict) else {}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    @staticmethod
    def _salvar_carrinhos_arquivo(dados):
        os.makedirs(os.path.dirname(_CARRINHOS_PATH), exist_ok=True)
        with open(_CARRINHOS_PATH, mode="w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo)

    @staticmethod
    def cliente_carrinho_sincronizar(id_cliente, carrinho):
        """Grava o carrinho em memoria no JSON (ex.: apos resumo limpar itens invalidos)."""
        todos = View._carregar_carrinhos_arquivo()
        chave = str(int(id_cliente))
        todos[chave] = {str(int(id_produto)): int(qtd) for id_produto, qtd in carrinho.items()}
        View._salvar_carrinhos_arquivo(todos)

    @staticmethod
    def cliente_carrinho_carregar(id_cliente, carrinho):
        """Restaura o carrinho salvo do cliente no dict em memoria."""
        todos = View._carregar_carrinhos_arquivo()
        salvos = todos.get(str(int(id_cliente)), {})
        carrinho.clear()
        for id_produto, quantidade in salvos.items():
            carrinho[int(id_produto)] = int(quantidade)

    @staticmethod
    def produto_inserir(descricao, preco, estoque, id_categoria):
        produto_dao = ProdutoDAO()
        id_produto = produto_dao.Proximo_id()
        produto = Produto(id_produto, descricao, preco, estoque, id_categoria)
        produto_dao.Inserir(produto)
        return id_produto

    @staticmethod
    def produto_atualizar(id_produto, descricao, preco, estoque, id_categoria):
        produto = Produto(id_produto, descricao, preco, estoque, id_categoria)
        ProdutoDAO().Atualizar(produto)

    @staticmethod
    def produto_excluir(id_produto):
        return ProdutoDAO().Excluir(id_produto)

    @staticmethod
    def produto_reajustar_percentual(percentual):
        ProdutoDAO().Reajustar_precos_percentual(percentual)

    @staticmethod
    def comprar_carrinho(id_cliente, carrinho):
        CheckoutServico().finalizar_compra(id_cliente, carrinho)
        View.cliente_carrinho_sincronizar(id_cliente, carrinho)

    @staticmethod
    def cliente_vendas_com_itens(id_cliente):
        return VendaRelatorioServico().listar_por_cliente(id_cliente)

    @staticmethod
    def admin_vendas_com_itens():
        return VendaRelatorioServico().listar_todas()

    @staticmethod
    def venda_listar():
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
