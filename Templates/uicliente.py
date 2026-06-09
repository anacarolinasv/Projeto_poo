from views import View
from Templates.relatorio_vendas import imprimir_vendas_com_itens
from Templates.estilo_terminal import (
    erro,
    imprimir_caixa_menu,
    info,
    linha_formulario,
    ok,
    prompt_opcao,
    rotulo,
) # importa as funcoes do arquivo estilo_terminal.py


class UICliente: # classe estatica para o menu do perfil cliente

    @staticmethod
    def menu(carrinho, id_cliente): # metodo estatico para o menu do perfil cliente
        # Quadro de opcoes: loja, carrinho, historico e saida (9 devolvido ao caller).
        grupos = [
            (None, []),
            ("LOJA", [(1, "Listar produtos"), (2, "Inserir produto no carrinho")]),
            (None, []),
            (
                "CARRINHO",
                [
                    (3, "Visualizar carrinho"),
                    (4, "Comprar carrinho"),
                    (10, "Remover produto do carrinho"),
                    (11, "Esvaziar carrinho"),
                ],
            ),
            (None, []),
            ("HISTORICO", [(5, "Listar minhas compras")]),
            (None, []),
            (
                "FAVORITOS",
                [
                    (6, "Listar meus favoritos"),
                    (7, "Favoritar produto"),
                    (8, "Remover produto dos favoritos"),
                ],
            ),
            (None, []),
            ("SESSAO", [(9, "Sair")]),
        ]
        imprimir_caixa_menu(" MENU CLIENTE ", grupos) # imprime o menu do perfil cliente
        try:
            op = int(input(prompt_opcao())) # le a opcao do usuario
        except ValueError:
            # Entrada nao numerica: retorna None (loop em ui.py continua no menu logado).
            print(erro("✖  Opcao invalida.")) # imprime uma mensagem de erro se a opcao do usuario for invalida
            return None # retorna None se a opcao do usuario for invalida

        if op == 1: # se a opcao do usuario for 1, chama o metodo _listar_produtos
            UICliente._listar_produtos()
        elif op == 2: # se a opcao do usuario for 2, chama o metodo _inserir_carrinho
            # carrinho e o mesmo dict mutavel mantido em UI.__carrinho.
            UICliente._inserir_carrinho(carrinho, id_cliente)
        elif op == 3: # se a opcao do usuario for 3, chama o metodo _visualizar_carrinho
            UICliente._visualizar_carrinho(carrinho, id_cliente)
        elif op == 4:
            # Finaliza venda para este id_cliente e esvazia carrinho conforme View.
            UICliente._comprar_carrinho(carrinho, id_cliente)
        elif op == 10: # se a opcao do usuario for 10, chama o metodo _remover_do_carrinho
            UICliente._remover_do_carrinho(carrinho, id_cliente)
        elif op == 11: # se a opcao do usuario for 11, chama o metodo _esvaziar_carrinho
            UICliente._esvaziar_carrinho(carrinho, id_cliente)
        elif op == 5: # se a opcao do usuario for 5, chama o metodo _listar_minhas_compras
            UICliente._listar_minhas_compras(id_cliente)
        elif op == 6: # se a opcao do usuario for 6, chama o metodo _listar_favoritos
            UICliente._listar_favoritos(id_cliente)
        elif op == 7: # se a opcao do usuario for 7, chama o metodo _favoritar_produto
            UICliente._favoritar_produto(id_cliente)
        elif op == 8: # se a opcao do usuario for 8, chama o metodo _remover_favorito
            UICliente._remover_favorito(id_cliente)
        elif op == 9: # se a opcao do usuario for 9, retorna 9
            return 9 # retorna 9 se a opcao do usuario for 9
        else: # se a opcao do usuario for invalida, imprime uma mensagem de erro
            print(erro("✖  Opcao invalida.")) # imprime uma mensagem de erro se a opcao do usuario for invalida
        # Qualquer opcao exceto 9: caller trata como "continuar logado".
        return None # retorna None se a opcao do usuario for invalida

    @staticmethod
    def _listar_produtos(): # metodo estatico para listar os produtos disponiveis para venda
        linha_formulario("Produtos a venda (estoque > 0)") # imprime o titulo do formulario de listagem de produtos disponiveis para venda
        # View filtra produtos que podem ser vendidos (ex.: estoque positivo).
        lista = View.produtos_disponiveis_venda() # chama o metodo produtos_disponiveis_venda da classe View
        if not lista:
            print(info("ℹ  Nenhum produto disponivel para venda no momento.")) # imprime uma mensagem de informacao se a lista de produtos disponiveis para venda for vazia
            return # retorna None se a lista de produtos disponiveis para venda for vazia
        for p in lista:
            # __str__ ou representacao do objeto produto para exibir na tela.
            print(f"  {p}") # imprime o objeto produto

    @staticmethod
    def _inserir_carrinho(carrinho, id_cliente): # metodo estatico para inserir um produto no carrinho
        linha_formulario("Inserir produto no carrinho") # imprime o titulo do formulario de insercao de produto no carrinho
        try:
            id_produto = int(input("  Id do produto: ")) # le o id do produto a ser inserido no carrinho
            quantidade = int(input("  Quantidade:    ")) # le a quantidade do produto a ser inserido no carrinho
            # Atualiza o dict carrinho (agrega quantidade ou valida estoque).
            View.adicionar(carrinho, id_produto, quantidade)
            View.sincronizar(id_cliente, carrinho)
            print(ok("✔  Carrinho atualizado.")) # imprime uma mensagem de sucesso se o carrinho foi atualizado
        except ValueError as e:
            # Erros de validacao (produto inexistente, quantidade invalida, etc.).
            print(erro(f"✖  {e}")) # imprime uma mensagem de erro se ocorrer um erro de validacao
        except Exception as e:
            print(erro(f"✖  {e}")) # imprime uma mensagem de erro se ocorrer um erro

    @staticmethod
    def _visualizar_carrinho(carrinho, id_cliente): # metodo estatico para visualizar o carrinho
        linha_formulario("Carrinho") # imprime o titulo do formulario de visualizacao de carrinho
        # linhas: lista de dicts com id, descricao, preco_unitario, quantidade, total_item.
        linhas, total_carrinho = View.montar_resumo(carrinho)
        View.sincronizar(id_cliente, carrinho)
        if not linhas: 
            print(info("ℹ  Carrinho vazio.")) # imprime uma mensagem de informacao se o carrinho for vazio              
            return # retorna None se o carrinho for vazio
        for L in linhas:
            print(f"  [{L['id']}] {L['descricao']}") # imprime o id e a descricao do produto
            print(
                f"      Preco unit.: R$ {L['preco_unitario']:.2f}   " # imprime o preco unitario do produto
                f"Qtd: {L['quantidade']}   " # imprime a quantidade do produto
                f"Total item: R$ {L['total_item']:.2f}" # imprime o total do item
            )
        print() # imprime uma linha em branco
        print(rotulo(f"  Valor total do carrinho: R$ {total_carrinho:.2f}")) # imprime o valor total do carrinho

    @staticmethod
    def _remover_do_carrinho(carrinho, id_cliente): # metodo estatico para remover um produto do carrinho       
        linha_formulario("Remover produto do carrinho") # imprime o titulo do formulario de remocao de produto do carrinho
        try:
            id_produto = int(input("  Id do produto a remover: ")) # le o id do produto a ser removido do carrinho
            View.remover_item(carrinho, id_produto)
            View.sincronizar(id_cliente, carrinho)
            print(ok("✔  Item removido do carrinho.")) # imprime uma mensagem de sucesso se o item foi removido do carrinho
        except ValueError as e:
            print(erro(f"✖  {e}")) # imprime uma mensagem de erro se ocorrer um erro de validacao
        except Exception as e:
            print(erro(f"✖  {e}")) # imprime uma mensagem de erro se ocorrer um erro

    @staticmethod
    def _esvaziar_carrinho(carrinho, id_cliente): # metodo estatico para esvaziar o carrinho
        linha_formulario("Esvaziar carrinho")
        if not carrinho:
            print(info("ℹ  Carrinho ja estava vazio.")) # imprime uma mensagem de informacao se o carrinho ja estava vazio
            return # retorna None se o carrinho ja estava vazio
        try:
            View.esvaziar(carrinho)
            View.sincronizar(id_cliente, carrinho)
            print(ok("✔  Carrinho vazio.")) # imprime uma mensagem de sucesso se o carrinho foi esvaziado
        except ValueError as e:
            print(erro(f"✖  {e}")) # imprime uma mensagem de erro se ocorrer um erro de validacao
        except Exception as e:
            print(erro(f"✖  {e}")) # imprime uma mensagem de erro se ocorrer um erro

    @staticmethod
    def _comprar_carrinho(carrinho, id_cliente): # metodo estatico para comprar o carrinho
        linha_formulario("Finalizar compra")
        try:
            # Persiste venda e itens; esvazia carrinho em memoria conforme implementacao.
            View.finalizar_compra(id_cliente, carrinho)
            print(ok("✔  Compra realizada com sucesso.")) # imprime uma mensagem de sucesso se a compra foi realizada com sucesso
        except ValueError as e: 
            print(erro(f"✖  {e}")) # imprime uma mensagem de erro se ocorrer um erro de validacao
        except Exception as e:
            print(erro(f"✖  Erro ao finalizar compra: {e}")) # imprime uma mensagem de erro se ocorrer um erro

    @staticmethod
    def _listar_minhas_compras(id_cliente): # metodo estatico para listar as compras do cliente
        # Busca vendas deste cliente com lista de itens para o relatorio.
        registros = View.listar_por_cliente(id_cliente)
        # mostrar_cliente=False porque o proprio usuario ja sabe quem e.
        imprimir_vendas_com_itens(registros, "Minhas compras", mostrar_cliente=False) # imprime as compras do cliente com os itens e o nome do cliente em cada bloco

    @staticmethod
    def _listar_favoritos(id_cliente): # metodo estatico para listar os favoritos do cliente
        linha_formulario("Meus favoritos") # imprime o titulo do formulario de listagem de favoritos do cliente
        try:
            lista = View.listar_produtos_favoritos(id_cliente)
        except ValueError as e:
            print(erro(f"✖  {e}")) # imprime uma mensagem de erro se ocorrer um erro de validacao
            return
        if not lista:
            print(
                info(
                    "ℹ  Voce ainda nao favoritou nenhum produto "
                    "(ou os itens foram removidos do catalogo)."
                )
            )
            return # retorna None se a lista de favoritos for vazia                 
        for p in lista:
            print(f"  {p}") # imprime o objeto produto

    @staticmethod
    def _favoritar_produto(id_cliente): # metodo estatico para favoritar um produto 
        linha_formulario("Favoritar produto")
        try:
            id_produto = int(input("  Id do produto: ")) # le o id do produto a ser favoritado
            View.favoritar(id_cliente, id_produto)
            print(ok("✔  Produto adicionado aos favoritos.")) # imprime uma mensagem de sucesso se o produto foi adicionado aos favoritos
        except ValueError as e:
            print(erro(f"✖  {e}")) # imprime uma mensagem de erro se ocorrer um erro de validacao
        except Exception as e:
            print(erro(f"✖  {e}")) # imprime uma mensagem de erro se ocorrer um erro

    @staticmethod
    def _remover_favorito(id_cliente): # metodo estatico para remover um produto dos favoritos
        linha_formulario("Remover dos favoritos") # imprime o titulo do formulario de remocao de produto dos favoritos
        try:    
            id_produto = int(input("  Id do produto: ")) # le o id do produto a ser removido dos favoritos
            View.desfavoritar(id_cliente, id_produto)
            print(ok("✔  Produto removido dos favoritos.")) # imprime uma mensagem de sucesso se o produto foi removido dos favoritos
        except ValueError as e:
            print(erro(f"✖  {e}")) # imprime uma mensagem de erro se ocorrer um erro de validacao
        except Exception as e:
            print(erro(f"✖  {e}")) # imprime uma mensagem de erro se ocorrer um erro
