# Fachada: orquestra servicos de produto, carrinho, checkout, listagens.
from views import View
# Funcao que formata e imprime vendas com itens (reutilizada no admin tambem).
from Templates.relatorio_vendas import imprimir_vendas_com_itens


class UICliente:
    """Menu do perfil cliente (classe estatica, mesmo padrao do material)."""

    @staticmethod
    def menu(carrinho, id_cliente):
        # Quadro de opcoes: loja, carrinho, historico e saida (9 devolvido ao caller).
        print("┌──────────────────── MENU CLIENTE ────────────────────┐")
        print("│                                                      │")
        print("│  LOJA                                                │")
        print("│     1  Listar produtos                               │")
        print("│     2  Inserir produto no carrinho                   │")
        print("│                                                      │")
        print("│  CARRINHO                                            │")
        print("│     3  Visualizar carrinho                           │")
        print("│     4  Comprar carrinho                              │")
        print("│    10  Remover produto do carrinho                   │")
        print("│    11  Esvaziar carrinho                             │")
        print("│                                                      │")
        print("│  HISTORICO                                           │")
        print("│     5  Listar minhas compras                         │")
        print("│                                                      │")
        print("│  FAVORITOS                                           │")
        print("│     6  Listar meus favoritos                         │")
        print("│     7  Favoritar produto                             │")
        print("│     8  Remover produto dos favoritos                 │")
        print("│                                                      │")
        print("│  SESSAO                                              │")
        print("│     9  Sair                                          │")
        print("│                                                      │")
        print("└──────────────────────────────────────────────────────┘")
        try:
            op = int(input("❯ Informe uma opcao: "))
        except ValueError:
            # Entrada nao numerica: retorna None (loop em ui.py continua no menu logado).
            print("✖  Opcao invalida.")
            return None
        if op == 1:
            UICliente._listar_produtos()
        elif op == 2:
            # carrinho e o mesmo dict mutavel mantido em UI.__carrinho.
            UICliente._inserir_carrinho(carrinho)
        elif op == 3:
            UICliente._visualizar_carrinho(carrinho)
        elif op == 4:
            # Finaliza venda para este id_cliente e esvazia carrinho conforme View.
            UICliente._comprar_carrinho(carrinho, id_cliente)
        elif op == 10:
            UICliente._remover_do_carrinho(carrinho)
        elif op == 11:
            UICliente._esvaziar_carrinho(carrinho)
        elif op == 5:
            UICliente._listar_minhas_compras(id_cliente)
        elif op == 6:
            UICliente._listar_favoritos(id_cliente)
        elif op == 7:
            UICliente._favoritar_produto(id_cliente)
        elif op == 8:
            UICliente._remover_favorito(id_cliente)
        elif op == 9:
            # Sinal para ui.py encerrar sessao (usuario_sair).
            return 9
        else:
            print("✖  Opcao invalida.")
        # Qualquer opcao exceto 9: caller trata como "continuar logado".
        return None

    @staticmethod
    def _listar_produtos():
        print()
        print("── Produtos a venda (estoque > 0) ──────────────────────")
        # View filtra produtos que podem ser vendidos (ex.: estoque positivo).
        lista = View.produtos_disponiveis_venda()
        if not lista:
            print("ℹ  Nenhum produto disponivel para venda no momento.")
            return
        for p in lista:
            # __str__ ou representacao do objeto produto para exibir na tela.
            print(f"  {p}")

    @staticmethod
    def _inserir_carrinho(carrinho):
        print()
        print("── Inserir produto no carrinho ─────────────────────────")
        try:
            id_produto = int(input("  Id do produto: "))
            quantidade = int(input("  Quantidade:    "))
            # Atualiza o dict carrinho (agrega quantidade ou valida estoque).
            View.carrinho_adicionar_item(carrinho, id_produto, quantidade)
            print("✔  Carrinho atualizado.")
        except ValueError as e:
            # Erros de validacao (produto inexistente, quantidade invalida, etc.).
            print(f"✖  {e}")
        except Exception as e:
            print(f"✖  {e}")

    @staticmethod
    def _visualizar_carrinho(carrinho):
        print()
        print("── Carrinho ────────────────────────────────────────────")
        # linhas: lista de dicts com id, descricao, preco_unitario, quantidade, total_item.
        linhas, total_carrinho = View.carrinho_resumo(carrinho)
        if not linhas:
            print("ℹ  Carrinho vazio.")
            return
        for L in linhas:
            print(f"  [{L['id']}] {L['descricao']}")
            print(
                f"      Preco unit.: R$ {L['preco_unitario']:.2f}   "
                f"Qtd: {L['quantidade']}   "
                f"Total item: R$ {L['total_item']:.2f}"
            )
        print()
        print(f"  Valor total do carrinho: R$ {total_carrinho:.2f}")

    @staticmethod
    def _remover_do_carrinho(carrinho):
        print()
        print("── Remover produto do carrinho ─────────────────────────")
        try:
            id_produto = int(input("  Id do produto a remover: "))
            View.carrinho_remover_item(carrinho, id_produto)
            print("✔  Item removido do carrinho.")
        except ValueError as e:
            print(f"✖  {e}")
        except Exception as e:
            print(f"✖  {e}")

    @staticmethod
    def _esvaziar_carrinho(carrinho):
        print()
        print("── Esvaziar carrinho ───────────────────────────────────")
        if not carrinho:
            print("ℹ  Carrinho ja estava vazio.")
            return
        try:
            View.carrinho_esvaziar(carrinho)
            print("✔  Carrinho vazio.")
        except ValueError as e:
            print(f"✖  {e}")
        except Exception as e:
            print(f"✖  {e}")

    @staticmethod
    def _comprar_carrinho(carrinho, id_cliente):
        print()
        print("── Finalizar compra ────────────────────────────────────")
        try:
            # Persiste venda e itens; esvazia carrinho em memoria conforme implementacao.
            View.comprar_carrinho(id_cliente, carrinho)
            print("✔  Compra realizada com sucesso.")
        except ValueError as e:
            print(f"✖  {e}")
        except Exception as e:
            print(f"✖  Erro ao finalizar compra: {e}")

    @staticmethod
    def _listar_minhas_compras(id_cliente):
        # Busca vendas deste cliente com lista de itens para o relatorio.
        registros = View.cliente_vendas_com_itens(id_cliente)
        # mostrar_cliente=False porque o proprio usuario ja sabe quem e.
        imprimir_vendas_com_itens(registros, "Minhas compras", mostrar_cliente=False)

    @staticmethod
    def _listar_favoritos(id_cliente):
        print()
        print("── Meus favoritos ──────────────────────────────────────")
        try:
            lista = View.cliente_favoritos_listar_produtos(id_cliente)
        except ValueError as e:
            print(f"✖  {e}")
            return
        if not lista:
            print("ℹ  Voce ainda nao favoritou nenhum produto (ou os itens foram removidos do catalogo).")
            return
        for p in lista:
            print(f"  {p}")

    @staticmethod
    def _favoritar_produto(id_cliente):
        print()
        print("── Favoritar produto ───────────────────────────────────")
        try:
            id_produto = int(input("  Id do produto: "))
            View.cliente_favorito_adicionar(id_cliente, id_produto)
            print("✔  Produto adicionado aos favoritos.")
        except ValueError as e:
            print(f"✖  {e}")
        except Exception as e:
            print(f"✖  {e}")

    @staticmethod
    def _remover_favorito(id_cliente):
        print()
        print("── Remover dos favoritos ───────────────────────────────")
        try:
            id_produto = int(input("  Id do produto: "))
            View.cliente_favorito_remover(id_cliente, id_produto)
            print("✔  Produto removido dos favoritos.")
        except ValueError as e:
            print(f"✖  {e}")
        except Exception as e:
            print(f"✖  {e}")
