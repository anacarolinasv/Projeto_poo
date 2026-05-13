from views import View
from Templates.uiadmin import UIAdmin
from Templates.uicliente import UICliente


class UI:
    """Camada de interface principal (mesmo fluxo do material: sessao + menu + Templates)."""

    __usuario = None
    __carrinho = {}

    @staticmethod
    def menu_visitante():
        print("1-Entrar no sistema, 2-Abrir conta, 9-Fim")
        try:
            op = int(input("Informe uma opcao: "))
        except ValueError:
            print("Opcao invalida.")
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
                print("IF Comercio Eletronico 2026.1")
                print("Bem-vindo(a), " + str(cls.__usuario["nome"]))
                admin = cls.__usuario["admin"]
                if admin:
                    if UIAdmin.menu() == 9:
                        UI.usuario_sair()
                else:
                    if UICliente.menu(UI.__carrinho, cls.__usuario["id"]) == 9:
                        UI.usuario_sair()

    @classmethod
    def visitante_entrar(cls):
        email = input("Informe o e-mail: ")
        senha = input("Informe a senha: ")
        cls.__usuario = View.usuario_autenticar(email, senha)
        if cls.__usuario is None:
            print("Usuario ou senha invalidos")
        else:
            cls.__carrinho = {}

    @staticmethod
    def visitante_criar_conta():
        print("--- Abrir conta ---")
        nome = input("Nome: ")
        email = input("Email: ")
        fone = input("Fone: ")
        senha = input("Senha: ")
        senha2 = input("Confirmar senha: ")
        try:
            c = View.abrir_conta_visitante(nome, email, fone, senha, senha2)
            print("Conta criada com sucesso. Voce ja pode entrar como cliente.")
            print(f"Seu identificador de cliente: {c.get_id()}")
            print(c)
        except ValueError as e:
            print(str(e))
        except Exception as e:
            print(f"Erro ao abrir conta: {e}")

    @classmethod
    def usuario_sair(cls):
        cls.__usuario = None
        cls.__carrinho = {}
        print("Logout realizado.")


if __name__ == "__main__":
    UI.main()
