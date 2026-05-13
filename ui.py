# Importa a fachada da aplicacao (View): autenticacao, abrir conta, etc.
from views import View
# Menu e acoes exclusivas do administrador (CRUD de entidades, vendas).
from Templates.uiadmin import UIAdmin
# Menu e acoes do cliente (loja, carrinho, compra, historico).
from Templates.uicliente import UICliente


class UI:
    """Camada de interface principal (mesmo fluxo do material: sessao + menu + Templates)."""

    # Usuario logado: None = visitante; dict com chaves nome, email, admin, id quando logado.
    __usuario = None
    # Carrinho em memoria: chave = id do produto, valor = quantidade (atualizado pela View).
    __carrinho = {}

    @staticmethod
    def menu_visitante():
        # Cabecalho visual do programa (visitante ainda nao identificado).
        print("╔══════════════════════════════════════════════════════╗")
        print("║            IF Comercio Eletronico 2026.1             ║")
        print("║                Bem-vindo(a) visitante                ║")
        print("╚══════════════════════════════════════════════════════╝")
        # Opcoes disponiveis antes do login (1=login, 2=cadastro, 9=sair no loop externo).
        print("┌─────────────────── MENU VISITANTE ───────────────────┐")
        print("│                                                      │")
        print("│     1  Entrar no sistema                             │")
        print("│     2  Abrir conta                                   │")
        print("│     9  Sair                                          │")
        print("│                                                      │")
        print("└──────────────────────────────────────────────────────┘")
        try:
            # Le a opcao como inteiro; texto nao numerico gera ValueError.
            op = int(input("❯ Informe uma opcao: "))
        except ValueError:
            # Usuario digitou letras ou vazio: nao interrompe o programa, so avisa.
            print("✖  Opcao invalida.")
            return 0
        if op == 1:
            # Delega autenticacao para visitante_entrar (preenche __usuario se ok).
            UI.visitante_entrar()
        if op == 2:
            # Cadastro de novo cliente via View.abrir_conta_visitante.
            UI.visitante_criar_conta()
        # Retorna a opcao para o loop em menu(): 9 encerra o programa la.
        return op

    @classmethod
    def main(cls):
        # Carrega dados/arquivos necessarios antes de qualquer tela (implementacao em View).
        View.inicializar_app()
        # Entra no loop principal de menus ate o usuario escolher sair (9).
        cls.menu()

    @classmethod
    def menu(cls):
        # Acumulador da ultima opcao; 0 faz entrar no while na primeira vez.
        op = 0
        while op != 9:
            if cls.__usuario is None:
                # Nao logado: mostra menu de visitante e recebe op em op.
                op = UI.menu_visitante()
            else:
                # Logado: monta saudacao com o nome guardado na sessao.
                nome = str(cls.__usuario["nome"])
                linha_nome = f"Bem-vindo(a), {nome}"
                print("╔══════════════════════════════════════════════════════╗")
                print("║" + "IF Comercio Eletronico 2026.1".center(54) + "║")
                print("║" + linha_nome.center(54) + "║")
                print("╚══════════════════════════════════════════════════════╝")
                # admin True = perfil administrador; False = cliente comum.
                admin = cls.__usuario["admin"]
                if admin:
                    # menu() do admin devolve 9 se escolheu "Sair" da sessao admin.
                    if UIAdmin.menu() == 9:
                        # Propaga logout para limpar usuario e carrinho.
                        UI.usuario_sair()
                else:
                    # Passa o carrinho compartilhado e o id do cliente para o menu da loja.
                    if UICliente.menu(UI.__carrinho, cls.__usuario["id"]) == 9:
                        UI.usuario_sair()
                # Neste ramo `op` nao e alterado; o programa so encerra quando, como visitante,
                # menu_visitante() retornar 9 (apos logout, __usuario volta a None e o menu visitante reaparece).

    @classmethod
    def visitante_entrar(cls):
        print()
        print("── Entrar no sistema ───────────────────────────────────")
        # Credenciais usadas pela camada View para localizar o usuario nos JSON/arquivos.
        email = input("  E-mail: ")
        senha = input("  Senha:  ")
        # View retorna dict do usuario ou None se email/senha nao baterem.
        cls.__usuario = View.usuario_autenticar(email, senha)
        if cls.__usuario is None:
            print("✖  Usuario ou senha invalidos.")
        else:
            # Novo login: carrinho antigo nao deve persistir entre contas.
            cls.__carrinho = {}
            print("✔  Login realizado com sucesso.")

    @staticmethod
    def visitante_criar_conta():
        print()
        print("── Abrir conta ─────────────────────────────────────────")
        # Coleta todos os campos exigidos pelo dominio Cliente.
        nome = input("  Nome:             ")
        email = input("  E-mail:           ")
        fone = input("  Fone:             ")
        senha = input("  Senha:            ")
        senha2 = input("  Confirmar senha:  ")
        try:
            # View valida senhas iguais, email duplicado, etc.; pode lancar ValueError.
            c = View.abrir_conta_visitante(nome, email, fone, senha, senha2)
            print("✔  Conta criada com sucesso. Voce ja pode entrar como cliente.")
            # c e um objeto cliente com get_id() apos persistencia.
            print(f"ℹ  Seu identificador de cliente: {c.get_id()}")
            print(f"  {c}")
        except ValueError as e:
            # Erro de regra de negocio (mensagem amigavel vinda do servico).
            print(f"✖  {e}")
        except Exception as e:
            # Qualquer outro erro (arquivo, tipo, etc.) para nao quebrar o programa sem aviso.
            print(f"✖  Erro ao abrir conta: {e}")

    @classmethod
    def usuario_sair(cls):
        # Encerra sessao: proxima iteracao do while em menu() cai no menu visitante.
        cls.__usuario = None
        cls.__carrinho = {}
        print("!  Logout realizado.")


# Ponto de entrada: rodar `python ui.py` inicia a aplicacao pelo main().
if __name__ == "__main__":
    UI.main()
