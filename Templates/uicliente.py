from views import View
from Templates.relatorio_vendas import imprimir_vendas_com_itens


class UICliente:
    """Menu do perfil cliente (classe estatica, mesmo padrao do material)."""

    @staticmethod
    def menu(carrinho, id_cliente):
        print("1-Listar produtos")
        print("2-Inserir produto no carrinho")
        print("3-Visualizar carrinho")
        print("4-Comprar carrinho")
        print("5-Listar minhas compras")
        print("9-Sair")
        try:
            op = int(input("Informe uma opcao: "))
        except ValueError:
            print("Opcao invalida.")
            return None
        if op == 1:
            UICliente._listar_produtos()
        elif op == 2:
            UICliente._inserir_carrinho(carrinho)
        elif op == 3:
            UICliente._visualizar_carrinho(carrinho)
        elif op == 4:
            UICliente._comprar_carrinho(carrinho, id_cliente)
        elif op == 5:
            UICliente._listar_minhas_compras(id_cliente)
        elif op == 9:
            return 9
        else:
            print("Opcao invalida.")
        return None

    @staticmethod
    def _listar_produtos():
        lista = View.produtos_disponiveis_venda()
        if not lista:
            print("Nenhum produto disponivel para venda no momento.")
            return
        print("\n--- Produtos a venda (estoque > 0) ---")
        for p in lista:
            print(p)

    @staticmethod
    def _inserir_carrinho(carrinho):
        try:
            id_produto = int(input("Id do produto: "))
            quantidade = int(input("Quantidade: "))
            View.carrinho_adicionar_item(carrinho, id_produto, quantidade)
            print("Carrinho atualizado.")
        except ValueError as e:
            print(str(e))
        except Exception as e:
            print(f"Erro: {e}")

    @staticmethod
    def _visualizar_carrinho(carrinho):
        linhas, total_carrinho = View.carrinho_resumo(carrinho)
        if not linhas:
            print("Carrinho vazio.")
            return
        print("\n--- Carrinho ---")
        for L in linhas:
            print(
                f"  [{L['id']}] {L['descricao']}\n"
                f"      Preco unitario: R$ {L['preco_unitario']:.2f}  |  "
                f"Quantidade: {L['quantidade']}  |  "
                f"Total do item: R$ {L['total_item']:.2f}"
            )
        print(f"\n  Valor total do carrinho: R$ {total_carrinho:.2f}")

    @staticmethod
    def _comprar_carrinho(carrinho, id_cliente):
        try:
            View.comprar_carrinho(id_cliente, carrinho)
            print("Compra realizada com sucesso.")
        except ValueError as e:
            print(str(e))
        except Exception as e:
            print(f"Erro ao finalizar compra: {e}")

    @staticmethod
    def _listar_minhas_compras(id_cliente):
        registros = View.cliente_vendas_com_itens(id_cliente)
        imprimir_vendas_com_itens(registros, "Minhas compras", mostrar_cliente=False)
