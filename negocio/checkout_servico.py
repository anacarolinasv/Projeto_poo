# Data/hora da venda gravada no registro (momento da finalizacao).
from datetime import datetime

# Converte o dict carrinho {id_produto: qtd} em linhas com precos e total (regra de negocio).
from negocio.carrinho_servico import CarrinhoServico
from produtos.produto import Produto, ProdutoDAO
from vendas.venda import Venda, VendaDAO
from vendas.vendaItem import VendaItem, VendaItemDAO


class CheckoutServico:
    """Finaliza compra: grava venda e itens, baixa estoque, esvazia carrinho."""

    def finalizar_compra(self, id_cliente, carrinho):
        # id_cliente deve ser o identificador positivo do cliente logado.
        if id_cliente <= 0:
            raise ValueError("Cliente invalido.")
        # Carrinho vazio antes mesmo de montar resumo.
        if not carrinho:
            raise ValueError("Carrinho vazio.")
        # linhas: lista de dicts com id, quantidade, preco_unitario, etc.; total: soma do carrinho.
        linhas, total = CarrinhoServico().montar_resumo(carrinho)
        # Pode ocorrer se todas as chaves forem invalidas ou quantidades zeradas (conforme carrinho).
        if not linhas:
            raise ValueError("Carrinho vazio.")
        pdao = ProdutoDAO()
        # Fase 1: apenas valida — nada e gravado ate passar em todos os produtos (evita venda parcial).
        for L in linhas:
            p = pdao.Listar_id(L["id"])
            if p is None:
                raise ValueError(f"Produto {L['id']} nao encontrado.")
            if p.get_estoque() < L["quantidade"]:
                raise ValueError(
                    f"Estoque insuficiente para {p.get_descricao()} (disponivel: {p.get_estoque()})."
                )
        # Fase 2: persiste cabecalho da venda (id novo, data atual, total, cliente).
        vdao = VendaDAO()
        id_venda = vdao.Proximo_id()
        # Terceiro parametro e o bool `carrinho` da entidade Venda (modelo exige True/False; aqui False apos fechamento).
        v = Venda(id_venda, datetime.now(), False, total, id_cliente)
        vdao.Inserir(v)
        # Fase 3: um registro de item por linha do carrinho + baixa de estoque no mesmo loop.
        idao = VendaItemDAO()
        for L in linhas:
            id_item = idao.Proximo_id()
            # Congela quantidade e preco unitario no momento da compra (historico nao muda se o produto mudar de preco).
            item = VendaItem(
                id_item,
                int(L["quantidade"]),
                float(L["preco_unitario"]),
                id_venda,
                int(L["id"]),
            )
            idao.Inserir(item)
            p = pdao.Listar_id(L["id"])
            novo_est = int(p.get_estoque()) - int(L["quantidade"])
            # ProdutoDAO exige objeto completo no Atualizar; recria com mesmo id/descricao/preco/categoria.
            atualizado = Produto(
                p.get_id(),
                p.get_descricao(),
                p.get_preco(),
                novo_est,
                p.get_idCategoria(),
            )
            pdao.Atualizar(atualizado)
        # Limpa o dicionario passado por referencia (o mesmo objeto usado na UI).
        carrinho.clear()
