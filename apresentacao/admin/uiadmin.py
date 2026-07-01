from views import View # importa a classe View do arquivo views.py
from apresentacao.comum.relatorio_vendas import imprimir_vendas_com_itens # importa a funcao imprimir_vendas_com_itens do arquivo relatorio_vendas.py
from apresentacao.comum.estilo_terminal import (
    aviso, # importa a funcao aviso do arquivo estilo_terminal.py
    erro, # importa a funcao erro do arquivo estilo_terminal.py
    imprimir_caixa_menu, # importa a funcao imprimir_caixa_menu do arquivo estilo_terminal.py
    info, # importa a funcao info do arquivo estilo_terminal.py
    linha_formulario, # importa a funcao linha_formulario do arquivo estilo_terminal.py
    ok as msg_ok, # importa a funcao ok do arquivo estilo_terminal.py como msg_ok
    prompt_opcao, # importa a funcao prompt_opcao do arquivo estilo_terminal.py
)

class UIAdmin: # classe estatica para o menu do perfil administrador

    @staticmethod
    def menu(): # metodo estatico para o menu do perfil administrador
        grupos = [ # lista de grupos de opcoes
            (None, []), # grupo vazio
            ("CLIENTES", [(1, "Inserir"), (2, "Listar"), (3, "Atualizar"), (4, "Excluir")]),
            (None, []), # grupo vazio
            ("CATEGORIAS", [(5, "Inserir"), (6, "Listar"), (7, "Atualizar"), (8, "Excluir")]),
            (None, []),
            (
                "PRODUTOS",
                [
                    (11, "Inserir"),
                    (12, "Listar"),
                    (13, "Atualizar"),
                    (14, "Excluir"),
                    (15, "Reajustar precos"),
                ],
            ), # grupo de opcoes de produtos
            (None, []),
            ("VENDAS", [(16, "Listar todas as vendas")]),
            (None, []),
            ("SESSAO", [(9, "Sair")]),
        ]
        imprimir_caixa_menu(" MENU ADMINISTRADOR ", grupos) # imprime o menu do perfil administrador

        try:    # tenta ler a opcao do usuario
            op = int(input(prompt_opcao())) # le a opcao do usuario
        except ValueError: # se a opcao do usuario for invalida, imprime uma mensagem de erro
            print(erro("✖  Opcao invalida.")) # imprime uma mensagem de erro se a opcao do usuario for invalida
            return None # retorna None se a opcao do usuario for invalida

        try:  # tenta executar a opcao do usuario
            # Cada ramo chama View + metodo estatico auxiliar desta classe.
            if op == 1: # se a opcao do usuario for 1, chama o metodo cliente_inserir
                UIAdmin.cliente_inserir()
            if op == 2: # se a opcao do usuario for 2, chama o metodo cliente_listar
                UIAdmin.cliente_listar()
            if op == 3: # se a opcao do usuario for 3, chama o metodo cliente_atualizar
                UIAdmin.cliente_atualizar()
            if op == 4: # se a opcao do usuario for 4, chama o metodo cliente_excluir
                UIAdmin.cliente_excluir()
            if op == 5: # se a opcao do usuario for 5, chama o metodo categoria_inserir
                UIAdmin.categoria_inserir()
            if op == 6: # se a opcao do usuario for 6, chama o metodo categoria_listar
                UIAdmin.categoria_listar()
            if op == 7: # se a opcao do usuario for 7, chama o metodo categoria_atualizar
                UIAdmin.categoria_atualizar()
            if op == 8: # se a opcao do usuario for 8, chama o metodo categoria_excluir
                UIAdmin.categoria_excluir()
            if op == 11: # se a opcao do usuario for 11, chama o metodo produto_inserir
                UIAdmin.produto_inserir()
            if op == 12: # se a opcao do usuario for 12, chama o metodo produto_listar
                UIAdmin.produto_listar()
            if op == 13: # se a opcao do usuario for 13, chama o metodo produto_atualizar
                UIAdmin.produto_atualizar()
            if op == 14: # se a opcao do usuario for 14, chama o metodo produto_excluir                         
                UIAdmin.produto_excluir()
            if op == 15: # se a opcao do usuario for 15, chama o metodo produto_reajustar   
                UIAdmin.produto_reajustar()
            if op == 16: # se a opcao do usuario for 16, chama o metodo venda_listar
                UIAdmin.venda_listar()
            if op == 9: # se a opcao do usuario for 9, retorna 9
                return 9
        except ValueError as e: # se ocorrer um erro de valor, imprime uma mensagem de erro
            print(erro(f"✖  {e}")) # imprime uma mensagem de erro se ocorrer um erro de valor
        except Exception as e: # se ocorrer um erro, imprime uma mensagem de erro
            print(erro(f"✖  {e}")) # imprime uma mensagem de erro se ocorrer um erro
        return None # retorna None se ocorrer um erro

    @staticmethod
    def cliente_inserir(): # metodo estatico para inserir um cliente
        linha_formulario("Inserir cliente") # imprime o titulo do formulario de insercao de cliente
        # Admin informa id manualmente (evita colisao com ids ja usados no JSON).
        id_cliente = int(input("  Id:     "))
        nome = input("  Nome:   ")
        email = input("  E-mail: ")
        fone = input("  Fone:   ")
        senha = input("  Senha:  ")
        View.cliente_inserir(id_cliente, nome, email, fone, senha) # chama o metodo cliente_inserir da classe View
        print(msg_ok("✔  Cliente inserido.")) # imprime uma mensagem de sucesso se o cliente foi inserido

    @staticmethod
    def cliente_listar(): # metodo estatico para listar os clientes
        linha_formulario("Clientes cadastrados") # imprime o titulo do formulario de listagem de clientes
        lista = View.cliente_listar() # chama o metodo cliente_listar da classe View
        if not lista: # se a lista de clientes for vazia, imprime uma mensagem de informacao    
            print(info("ℹ  Nenhum cliente cadastrado."))
            return # retorna None se a lista de clientes for vazia
        for obj in lista: # para cada objeto na lista de clientes, imprime o objeto
            print(f"  {obj}") # imprime o objeto

    @staticmethod
    def cliente_atualizar(): # metodo estatico para atualizar um cliente
        # Mostra lista atual para o admin escolher o id com contexto.
        UIAdmin.cliente_listar() # chama o metodo cliente_listar da classe View
        linha_formulario("Atualizar cliente") # imprime o titulo do formulario de atualizacao de cliente
        id_cliente = int(input("  Id a ser atualizado: ")) # le o id do cliente a ser atualizado
        atual = None # inicializa a variavel atual como None
        # Busca linear na lista retornada pela View (id unico).
        for c in View.cliente_listar(): # para cada objeto na lista de clientes, verifica se o id do objeto é igual ao id do cliente a ser atualizado
            if c.get_id() == id_cliente: # se o id do objeto for igual ao id do cliente a ser atualizado, atribui o objeto a variavel atual
                atual = c # atribui o objeto a variavel atual
                break # sai do loop
        if atual is None: # se a variavel atual for None, imprime uma mensagem de aviso
            print(aviso("!  Cliente não encontrado.")) # imprime uma mensagem de aviso se o cliente nao for encontrado
            return # retorna None se o cliente nao for encontrado
        # Enter em branco mantem o valor entre colchetes (padrao "editar in-place").
        nome = input(f"  Nome   [{atual.get_nome()}]: ").strip() or atual.get_nome() # le o nome do cliente a ser atualizado
        email = input(f"  E-mail [{atual.get_email()}]: ").strip() or atual.get_email() # le o email do cliente a ser atualizado
        fone = input(f"  Fone   [{atual.get_fone()}]: ").strip() or atual.get_fone() # le o telefone do cliente a ser atualizado
        senha_txt = input("  Nova senha [Enter para manter]: ").strip() # le a nova senha do cliente a ser atualizada
        senha = senha_txt if senha_txt else atual.get_senha() # atribui a nova senha a variavel senha
        View.cliente_atualizar(id_cliente, nome, email, fone, senha) # chama o metodo cliente_atualizar da classe View
        print(msg_ok("✔  Cliente atualizado.")) # imprime uma mensagem de sucesso se o cliente foi atualizado

    @staticmethod
    def cliente_excluir(): # metodo estatico para excluir um cliente
        UIAdmin.cliente_listar() # chama o metodo cliente_listar da classe View
        linha_formulario("Excluir cliente") # imprime o titulo do formulario de exclusao de cliente
        id_cliente = int(input("  Id a ser excluido: ")) # le o id do cliente a ser excluido
        ok = View.cliente_excluir(id_cliente) # chama o metodo cliente_excluir da classe View
        if ok: # se o cliente foi excluido, imprime uma mensagem de sucesso
            print(msg_ok("✔  Cliente excluido.")) # imprime uma mensagem de sucesso se o cliente foi excluido
        else: # se o cliente nao foi excluido, imprime uma mensagem de aviso
            print(aviso("!  Cliente não encontrado.")) # imprime uma mensagem de aviso se o cliente nao foi encontrado

    @staticmethod
    def categoria_inserir(): # metodo estatico para inserir uma categoria
        linha_formulario("Inserir categoria") # imprime o titulo do formulario de insercao de categoria
        id_categoria = int(input("  Id:        ")) # le o id da categoria a ser inserida
        descricao = input("  Descricao: ") # le a descricao da categoria a ser inserida
        View.categoria_inserir(id_categoria, descricao) # chama o metodo categoria_inserir da classe View
        print(msg_ok("✔  Categoria inserida.")) # imprime uma mensagem de sucesso se a categoria foi inserida

    @staticmethod
    def categoria_listar(): # metodo estatico para listar as categorias
        linha_formulario("Categorias cadastradas")
        lista = View.categoria_listar() # chama o metodo categoria_listar da classe View
        if not lista: # se a lista de categorias for vazia, imprime uma mensagem de informacao    
            print(info("ℹ  Nenhuma categoria cadastrada.")) # imprime uma mensagem de informacao se a lista de categorias for vazia
            return # retorna None se a lista de categorias for vazia
        for obj in lista: # para cada objeto na lista de categorias, imprime o objeto
            print(f"  {obj}") # imprime o objeto

    @staticmethod
    def categoria_atualizar(): # metodo estatico para atualizar uma categoria
        UIAdmin.categoria_listar() # chama o metodo categoria_listar da classe View
        linha_formulario("Atualizar categoria") # imprime o titulo do formulario de atualizacao de categoria
        id_categoria = int(input("  Id a ser atualizado: ")) # le o id da categoria a ser atualizada
        descricao = input("  Nova descricao:      ") # le a nova descricao da categoria a ser atualizada
        View.categoria_atualizar(id_categoria, descricao) # chama o metodo categoria_atualizar da classe View
        print(msg_ok("✔  Categoria atualizada.")) # imprime uma mensagem de sucesso se a categoria foi atualizada

    @staticmethod
    def categoria_excluir(): # metodo estatico para excluir uma categoria
        UIAdmin.categoria_listar() # chama o metodo categoria_listar da classe View
        linha_formulario("Excluir categoria") # imprime o titulo do formulario de exclusao de categoria
        id_categoria = int(input("  Id a ser excluido: ")) # le o id da categoria a ser excluida
        ok = View.categoria_excluir(id_categoria) # chama o metodo categoria_excluir da classe View
        if ok: # se a categoria foi excluida, imprime uma mensagem de sucesso
            print(msg_ok("✔  Categoria excluida.")) # imprime uma mensagem de sucesso se a categoria foi excluida
        else: # se a categoria nao foi excluida, imprime uma mensagem de aviso
            print(aviso("!  Categoria não encontrada.")) # imprime uma mensagem de aviso se a categoria nao foi encontrada

    @staticmethod
    def produto_inserir(): # metodo estatico para inserir um produto    
        linha_formulario("Inserir produto") # imprime o titulo do formulario de insercao de produto
        descricao = input("  Descricao:    ") # le a descricao do produto a ser inserido
        preco = float(input("  Preco:        ")) # le o preco do produto a ser inserido
        estoque = int(input("  Estoque:      ")) # le o estoque do produto a ser inserido
        # Vincula o produto a uma categoria ja existente.
        id_categoria = int(input("  Id categoria: ")) # le o id da categoria a ser vinculada ao produto
        novo_id = View.produto_inserir(descricao, preco, estoque, id_categoria) # chama o metodo produto_inserir da classe View
        print(msg_ok(f"✔  Produto inserido com id {novo_id}.")) # imprime uma mensagem de sucesso se o produto foi inserido

    @staticmethod
    def produto_listar(): # metodo estatico para listar os produtos
        linha_formulario("Produtos cadastrados") # imprime o titulo do formulario de listagem de produtos
        lista = View.produto_listar() # chama o metodo produto_listar da classe View
        if not lista: # se a lista de produtos for vazia, imprime uma mensagem de informacao    
            print(info("ℹ  Nenhum produto cadastrado.")) # imprime uma mensagem de informacao se a lista de produtos for vazia
            return # retorna None se a lista de produtos for vazia
        for obj in lista: # para cada objeto na lista de produtos, imprime o objeto
            print(f"  {obj}") # imprime o objeto

    @staticmethod
    def produto_atualizar(): # metodo estatico para atualizar um produto
        UIAdmin.produto_listar() # chama o metodo produto_listar da classe View
        linha_formulario("Atualizar produto")
        id_produto = int(input("  Id a ser atualizado: ")) # le o id do produto a ser atualizado
        atual = None # inicializa a variavel atual como None
        for p in View.produto_listar(): # para cada objeto na lista de produtos, verifica se o id do objeto é igual ao id do produto a ser atualizado
            if p.get_id() == id_produto: # se o id do objeto for igual ao id do produto a ser atualizado, atribui o objeto a variavel atual
                atual = p # atribui o objeto a variavel atual
                break # sai do loop
        if atual is None: # se a variavel atual for None, imprime uma mensagem de aviso
            print(aviso("!  Produto não encontrado.")) # imprime uma mensagem de aviso se o produto nao for encontrado
            return # retorna None se o produto nao for encontrado
        descricao = input(f"  Descricao    [{atual.get_descricao()}]: ").strip() or atual.get_descricao()
        preco_txt = input(f"  Preco        [{atual.get_preco()}]: ").strip()
        estoque_txt = input(f"  Estoque      [{atual.get_estoque()}]: ").strip()
        id_cat_txt = input(f"  Id categoria [{atual.get_idCategoria()}]: ").strip()
        # Converte apenas se o usuario digitou algo; senao mantem valores atuais.
        preco = float(preco_txt) if preco_txt else atual.get_preco() 
        estoque = int(estoque_txt) if estoque_txt else atual.get_estoque()
        id_categoria = int(id_cat_txt) if id_cat_txt else atual.get_idCategoria()
        View.produto_atualizar(id_produto, descricao, preco, estoque, id_categoria) # chama o metodo produto_atualizar da classe View       
        print(msg_ok("✔  Produto atualizado.")) # imprime uma mensagem de sucesso se o produto foi atualizado

    @staticmethod
    def produto_excluir(): # metodo estatico para excluir um produto
        UIAdmin.produto_listar() # chama o metodo produto_listar da classe View
        linha_formulario("Excluir produto") # imprime o titulo do formulario de exclusao de produto
        id_produto = int(input("  Id a ser excluido: ")) # le o id do produto a ser excluido
        ok = View.produto_excluir(id_produto) # chama o metodo produto_excluir da classe View
        if ok: # se o produto foi excluido, imprime uma mensagem de sucesso
            print(msg_ok("✔  Produto excluido.")) # imprime uma mensagem de sucesso se o produto foi excluido
        else: # se o produto nao foi excluido, imprime uma mensagem de aviso
            print(aviso("!  Produto não encontrado.")) # imprime uma mensagem de aviso se o produto nao for encontrado

    @staticmethod
    def produto_reajustar(): # metodo estatico para reajustar os precos dos produtos
        linha_formulario("Reajustar precos")
        # Percentual aplicado a todos os produtos (ex.: 10 aumenta 10%, -5 reduz 5%).
        pct = float(input("  Percentual (ex: 10 = +10%, -5 = -5%): ")) # le o percentual de reajuste dos produtos
        View.produto_reajustar_percentual(pct) # chama o metodo produto_reajustar_percentual da classe View
        print(msg_ok("✔  Precos reajustados.")) # imprime uma mensagem de sucesso se os precos dos produtos foram reajustados

    @staticmethod
    def venda_listar(): # metodo estatico para listar as vendas
        # Todas as vendas do sistema, com nome do cliente em cada bloco.
        registros = View.listar_todas()
        imprimir_vendas_com_itens(registros, "Todas as vendas", mostrar_cliente=True) # imprime as vendas com os itens e o nome do cliente em cada bloco
