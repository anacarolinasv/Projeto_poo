from views import View
from Templates.relatorio_vendas import imprimir_vendas_com_itens


class UIAdmin:
    """Menu do perfil administrador (classe estatica, mesmo padrao do material)."""

    @staticmethod
    def menu():
        print("Clientes   : 1-Inserir, 2-Listar, 3-Atualizar, 4-Excluir")
        print("Categorias : 5-Inserir, 6-Listar, 7-Atualizar, 8-Excluir")
        print("Produtos   : 11-Inserir, 12-Listar, 13-Atualizar, 14-Excluir")
        print("15-Reajustar precos, 16-Listar vendas")
        print("9-Sair")
        try:
            op = int(input("Informe uma opcao: "))
        except ValueError:
            print("Opcao invalida.")
            return None
        try:
            if op == 1:
                UIAdmin.cliente_inserir()
            if op == 2:
                UIAdmin.cliente_listar()
            if op == 3:
                UIAdmin.cliente_atualizar()
            if op == 4:
                UIAdmin.cliente_excluir()
            if op == 5:
                UIAdmin.categoria_inserir()
            if op == 6:
                UIAdmin.categoria_listar()
            if op == 7:
                UIAdmin.categoria_atualizar()
            if op == 8:
                UIAdmin.categoria_excluir()
            if op == 11:
                UIAdmin.produto_inserir()
            if op == 12:
                UIAdmin.produto_listar()
            if op == 13:
                UIAdmin.produto_atualizar()
            if op == 14:
                UIAdmin.produto_excluir()
            if op == 15:
                UIAdmin.produto_reajustar()
            if op == 16:
                UIAdmin.venda_listar()
            if op == 9:
                return 9
        except ValueError as erro:
            print(" ---- Erro ---->", erro)
        except Exception as erro:
            print(" ---- Erro ---->", erro)
        return None

    @staticmethod
    def cliente_inserir():
        id_cliente = int(input("Informe o id: "))
        nome = input("Informe o nome: ")
        email = input("Informe o e-mail: ")
        fone = input("Informe o fone: ")
        senha = input("Informe a senha: ")
        View.cliente_inserir(id_cliente, nome, email, fone, senha)
        print("Cliente inserido.")

    @staticmethod
    def cliente_listar():
        lista = View.cliente_listar()
        if not lista:
            print("Nenhum cliente cadastrado.")
            return
        for obj in lista:
            print(obj)

    @staticmethod
    def cliente_atualizar():
        UIAdmin.cliente_listar()
        id_cliente = int(input("Informe o id a ser atualizado: "))
        atual = None
        for c in View.cliente_listar():
            if c.get_id() == id_cliente:
                atual = c
                break
        if atual is None:
            print("Cliente nao encontrado.")
            return
        nome = input(f"Nome [{atual.get_nome()}]: ").strip() or atual.get_nome()
        email = input(f"E-mail [{atual.get_email()}]: ").strip() or atual.get_email()
        fone = input(f"Fone [{atual.get_fone()}]: ").strip() or atual.get_fone()
        senha_txt = input("Nova senha [Enter para manter]: ").strip()
        senha = senha_txt if senha_txt else atual.get_senha()
        View.cliente_atualizar(id_cliente, nome, email, fone, senha)
        print("Cliente atualizado.")

    @staticmethod
    def cliente_excluir():
        UIAdmin.cliente_listar()
        id_cliente = int(input("Informe o id a ser excluido: "))
        ok = View.cliente_excluir(id_cliente)
        print("Cliente excluido." if ok else "Cliente nao encontrado.")

    @staticmethod
    def categoria_inserir():
        id_categoria = int(input("Informe o id: "))
        descricao = input("Informe a descricao: ")
        View.categoria_inserir(id_categoria, descricao)
        print("Categoria inserida.")

    @staticmethod
    def categoria_listar():
        lista = View.categoria_listar()
        if not lista:
            print("Nenhuma categoria cadastrada.")
            return
        for obj in lista:
            print(obj)

    @staticmethod
    def categoria_atualizar():
        UIAdmin.categoria_listar()
        id_categoria = int(input("Informe o id a ser atualizado: "))
        descricao = input("Informe a nova descricao: ")
        View.categoria_atualizar(id_categoria, descricao)
        print("Categoria atualizada.")

    @staticmethod
    def categoria_excluir():
        UIAdmin.categoria_listar()
        id_categoria = int(input("Informe o id a ser excluido: "))
        ok = View.categoria_excluir(id_categoria)
        print("Categoria excluida." if ok else "Categoria nao encontrada.")

    @staticmethod
    def produto_inserir():
        id_produto = int(input("Informe o id: "))
        descricao = input("Informe a descricao: ")
        preco = float(input("Informe o preco: "))
        estoque = int(input("Informe o estoque: "))
        id_categoria = int(input("Informe o id da categoria: "))
        View.produto_inserir(id_produto, descricao, preco, estoque, id_categoria)
        print("Produto inserido.")

    @staticmethod
    def produto_listar():
        lista = View.produto_listar()
        if not lista:
            print("Nenhum produto cadastrado.")
            return
        for obj in lista:
            print(obj)

    @staticmethod
    def produto_atualizar():
        UIAdmin.produto_listar()
        id_produto = int(input("Informe o id do produto a ser atualizado: "))
        atual = None
        for p in View.produto_listar():
            if p.get_id() == id_produto:
                atual = p
                break
        if atual is None:
            print("Produto nao encontrado.")
            return
        descricao = input(f"Descricao [{atual.get_descricao()}]: ").strip() or atual.get_descricao()
        preco_txt = input(f"Preco [{atual.get_preco()}]: ").strip()
        estoque_txt = input(f"Estoque [{atual.get_estoque()}]: ").strip()
        id_cat_txt = input(f"Id categoria [{atual.get_idCategoria()}]: ").strip()
        preco = float(preco_txt) if preco_txt else atual.get_preco()
        estoque = int(estoque_txt) if estoque_txt else atual.get_estoque()
        id_categoria = int(id_cat_txt) if id_cat_txt else atual.get_idCategoria()
        View.produto_atualizar(id_produto, descricao, preco, estoque, id_categoria)
        print("Produto atualizado.")

    @staticmethod
    def produto_excluir():
        UIAdmin.produto_listar()
        id_produto = int(input("Informe o id do produto a ser excluido: "))
        ok = View.produto_excluir(id_produto)
        print("Produto excluido." if ok else "Produto nao encontrado.")

    @staticmethod
    def produto_reajustar():
        pct = float(input("Percentual de reajuste (ex: 10 para +10%, -5 para -5%): "))
        View.produto_reajustar_percentual(pct)
        print("Precos reajustados.")

    @staticmethod
    def venda_listar():
        registros = View.admin_vendas_com_itens()
        imprimir_vendas_com_itens(registros, "Todas as vendas", mostrar_cliente=True)
