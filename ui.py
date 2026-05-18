from views import View
from Templates.uiadmin import UIAdmin
from Templates.uicliente import UICliente
from Templates.estilo_terminal import (
    aviso,
    banner_boas_vindas,
    erro,
    imprimir_caixa_menu,
    info,
    linha_formulario,
    ok,
    prompt_opcao,
)


class UI:

    __usuario = None
    __carrinho = {}

    @staticmethod
    def menu_visitante():
        banner_boas_vindas(
            "IF Comercio Eletronico 2026.1",
            "Bem-vindo(a) visitante",
        )
        grupos = [
            (None, []),
            ("", [(1, "Entrar no sistema"), (2, "Abrir conta"), (9, "Sair")]),
        ]
        imprimir_caixa_menu(" MENU VISITANTE ", grupos)
        try:
            op = int(input(prompt_opcao()))
        except ValueError:
            print(erro("✖  Opcao invalida."))
            return 0
        if op == 1:
            UI.visitante_entrar()
        if op == 2:
            UI.visitante_criar_conta()
        return op

    @classmethod
    def main(cls):
        View.inicializar_app()
        cls.menu()

    @classmethod
    def menu(cls):
        op = 0
        while op != 9:
            if cls.__usuario is None:
                op = UI.menu_visitante()
            else:
                nome = str(cls.__usuario["nome"])
                banner_boas_vindas(
                    "IF Comercio Eletronico 2026.1",
                    f"Bem-vindo(a), {nome}",
                )
                admin = cls.__usuario["admin"]
                if admin:
                    if UIAdmin.menu() == 9:
                        UI.usuario_sair()
                else:
                    if UICliente.menu(UI.__carrinho, cls.__usuario["id"]) == 9:
                        UI.usuario_sair()

    @classmethod
    def visitante_entrar(cls):
        linha_formulario("Entrar no sistema")
        email = input("  E-mail: ")
        senha = input("  Senha:  ")
        cls.__usuario = View.usuario_autenticar(email, senha)
        if cls.__usuario is None:
            print(erro("✖  Usuario ou senha invalidos."))
        else:
            cls.__carrinho = {}
            if not cls.__usuario["admin"]:
                View.cliente_carrinho_carregar(cls.__usuario["id"], cls.__carrinho)
            print(ok("✔  Login realizado com sucesso."))

    @staticmethod
    def visitante_criar_conta():
        linha_formulario("Abrir conta")
        nome = input("  Nome:             ")
        email = input("  E-mail:           ")
        fone = input("  Fone:             ")
        senha = input("  Senha:            ")
        senha2 = input("  Confirmar senha:  ")
        try:
            cliente = View.abrir_conta_visitante(nome, email, fone, senha, senha2)
            print(ok("✔  Conta criada com sucesso. Voce ja pode entrar como cliente."))
            print(info(f"ℹ  Seu identificador de cliente: {cliente.get_id()}"))
            print(f"  {cliente}")
        except ValueError as e:
            print(erro(f"✖  {e}"))
        except Exception as e:
            print(erro(f"✖  Erro ao abrir conta: {e}"))

    @classmethod
    def usuario_sair(cls):
        cls.__usuario = None
        cls.__carrinho = {}
        print(aviso("!  Logout realizado."))


if __name__ == "__main__":
    UI.main()
