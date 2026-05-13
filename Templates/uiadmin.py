# Fachada com operacoes de administrador (CRUD e relatorios).
from views import View
from Templates.relatorio_vendas import imprimir_vendas_com_itens


class UIAdmin:
    """Menu do perfil administrador (classe estatica, mesmo padrao do material)."""

    @staticmethod
    def menu():
        # Opcoes agrupadas: clientes (1-4), categorias (5-8), produtos (11-15), vendas (16), sair (9).
        print("┌───────────────── MENU ADMINISTRADOR ─────────────────┐")
        print("│                                                      │")
        print("│  CLIENTES                                            │")
        print("│     1  Inserir                                       │")
        print("│     2  Listar                                        │")
        print("│     3  Atualizar                                     │")
        print("│     4  Excluir                                       │")
        print("│                                                      │")
        print("│  CATEGORIAS                                          │")
        print("│     5  Inserir                                       │")
        print("│     6  Listar                                        │")
        print("│     7  Atualizar                                     │")
        print("│     8  Excluir                                       │")
        print("│                                                      │")
        print("│  PRODUTOS                                            │")
        print("│    11  Inserir                                       │")
        print("│    12  Listar                                        │")
        print("│    13  Atualizar                                     │")
        print("│    14  Excluir                                       │")
        print("│    15  Reajustar precos                              │")
        print("│                                                      │")
        print("│  VENDAS                                              │")
        print("│    16  Listar todas as vendas                        │")
        print("│                                                      │")
        print("│  SESSAO                                              │")
        print("│     9  Sair                                          │")
        print("│                                                      │")
        print("└──────────────────────────────────────────────────────┘")
        try:
            op = int(input("❯ Informe uma opcao: "))
        except ValueError:
            print("✖  Opcao invalida.")
            return None
        try:
            # Cada ramo chama View + metodo estatico auxiliar desta classe.
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
        except ValueError as e:
            print(f"✖  {e}")
        except Exception as e:
            print(f"✖  {e}")
        return None

    @staticmethod
    def cliente_inserir():
        print()
        print("── Inserir cliente ─────────────────────────────────────")
        # Admin informa id manualmente (evita colisao com ids ja usados no JSON).
        id_cliente = int(input("  Id:     "))
        nome = input("  Nome:   ")
        email = input("  E-mail: ")
        fone = input("  Fone:   ")
        senha = input("  Senha:  ")
        View.cliente_inserir(id_cliente, nome, email, fone, senha)
        print("✔  Cliente inserido.")

    @staticmethod
    def cliente_listar():
        print()
        print("── Clientes cadastrados ────────────────────────────────")
        lista = View.cliente_listar()
        if not lista:
            print("ℹ  Nenhum cliente cadastrado.")
            return
        for obj in lista:
            print(f"  {obj}")

    @staticmethod
    def cliente_atualizar():
        # Mostra lista atual para o admin escolher o id com contexto.
        UIAdmin.cliente_listar()
        print()
        print("── Atualizar cliente ───────────────────────────────────")
        id_cliente = int(input("  Id a ser atualizado: "))
        atual = None
        # Busca linear na lista retornada pela View (id unico).
        for c in View.cliente_listar():
            if c.get_id() == id_cliente:
                atual = c
                break
        if atual is None:
            print("!  Cliente nao encontrado.")
            return
        # Enter em branco mantem o valor entre colchetes (padrao "editar in-place").
        nome = input(f"  Nome   [{atual.get_nome()}]: ").strip() or atual.get_nome()
        email = input(f"  E-mail [{atual.get_email()}]: ").strip() or atual.get_email()
        fone = input(f"  Fone   [{atual.get_fone()}]: ").strip() or atual.get_fone()
        senha_txt = input("  Nova senha [Enter para manter]: ").strip()
        senha = senha_txt if senha_txt else atual.get_senha()
        View.cliente_atualizar(id_cliente, nome, email, fone, senha)
        print("✔  Cliente atualizado.")

    @staticmethod
    def cliente_excluir():
        UIAdmin.cliente_listar()
        print()
        print("── Excluir cliente ─────────────────────────────────────")
        id_cliente = int(input("  Id a ser excluido: "))
        ok = View.cliente_excluir(id_cliente)
        if ok:
            print("✔  Cliente excluido.")
        else:
            print("!  Cliente nao encontrado.")

    @staticmethod
    def categoria_inserir():
        print()
        print("── Inserir categoria ───────────────────────────────────")
        id_categoria = int(input("  Id:        "))
        descricao = input("  Descricao: ")
        View.categoria_inserir(id_categoria, descricao)
        print("✔  Categoria inserida.")

    @staticmethod
    def categoria_listar():
        print()
        print("── Categorias cadastradas ──────────────────────────────")
        lista = View.categoria_listar()
        if not lista:
            print("ℹ  Nenhuma categoria cadastrada.")
            return
        for obj in lista:
            print(f"  {obj}")

    @staticmethod
    def categoria_atualizar():
        UIAdmin.categoria_listar()
        print()
        print("── Atualizar categoria ─────────────────────────────────")
        id_categoria = int(input("  Id a ser atualizado: "))
        descricao = input("  Nova descricao:      ")
        View.categoria_atualizar(id_categoria, descricao)
        print("✔  Categoria atualizada.")

    @staticmethod
    def categoria_excluir():
        UIAdmin.categoria_listar()
        print()
        print("── Excluir categoria ───────────────────────────────────")
        id_categoria = int(input("  Id a ser excluido: "))
        ok = View.categoria_excluir(id_categoria)
        if ok:
            print("✔  Categoria excluida.")
        else:
            print("!  Categoria nao encontrada.")

    @staticmethod
    def produto_inserir():
        print()
        print("── Inserir produto ─────────────────────────────────────")
        descricao = input("  Descricao:    ")
        preco = float(input("  Preco:        "))
        estoque = int(input("  Estoque:      "))
        # Vincula o produto a uma categoria ja existente.
        id_categoria = int(input("  Id categoria: "))
        novo_id = View.produto_inserir(descricao, preco, estoque, id_categoria)
        print(f"✔  Produto inserido com id {novo_id}.")

    @staticmethod
    def produto_listar():
        print()
        print("── Produtos cadastrados ────────────────────────────────")
        lista = View.produto_listar()
        if not lista:
            print("ℹ  Nenhum produto cadastrado.")
            return
        for obj in lista:
            print(f"  {obj}")

    @staticmethod
    def produto_atualizar():
        UIAdmin.produto_listar()
        print()
        print("── Atualizar produto ───────────────────────────────────")
        id_produto = int(input("  Id a ser atualizado: "))
        atual = None
        for p in View.produto_listar():
            if p.get_id() == id_produto:
                atual = p
                break
        if atual is None:
            print("!  Produto nao encontrado.")
            return
        descricao = input(f"  Descricao    [{atual.get_descricao()}]: ").strip() or atual.get_descricao()
        preco_txt = input(f"  Preco        [{atual.get_preco()}]: ").strip()
        estoque_txt = input(f"  Estoque      [{atual.get_estoque()}]: ").strip()
        id_cat_txt = input(f"  Id categoria [{atual.get_idCategoria()}]: ").strip()
        # Converte apenas se o usuario digitou algo; senao mantem valores atuais.
        preco = float(preco_txt) if preco_txt else atual.get_preco()
        estoque = int(estoque_txt) if estoque_txt else atual.get_estoque()
        id_categoria = int(id_cat_txt) if id_cat_txt else atual.get_idCategoria()
        View.produto_atualizar(id_produto, descricao, preco, estoque, id_categoria)
        print("✔  Produto atualizado.")

    @staticmethod
    def produto_excluir():
        UIAdmin.produto_listar()
        print()
        print("── Excluir produto ─────────────────────────────────────")
        id_produto = int(input("  Id a ser excluido: "))
        ok = View.produto_excluir(id_produto)
        if ok:
            print("✔  Produto excluido.")
        else:
            print("!  Produto nao encontrado.")

    @staticmethod
    def produto_reajustar():
        print()
        print("── Reajustar precos ────────────────────────────────────")
        # Percentual aplicado a todos os produtos (ex.: 10 aumenta 10%, -5 reduz 5%).
        pct = float(input("  Percentual (ex: 10 = +10%, -5 = -5%): "))
        View.produto_reajustar_percentual(pct)
        print("✔  Precos reajustados.")

    @staticmethod
    def venda_listar():
        # Todas as vendas do sistema, com nome do cliente em cada bloco.
        registros = View.admin_vendas_com_itens()
        imprimir_vendas_com_itens(registros, "Todas as vendas", mostrar_cliente=True)
