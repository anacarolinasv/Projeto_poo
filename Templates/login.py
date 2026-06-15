import streamlit as st
from views import View


class LoginUI:
    @staticmethod
    def _css():
        st.markdown(
            """
            <style>
                .stApp {
                    background: linear-gradient(
                        180deg,
                        #fdebd0 0%,
                        #f9dcc0 45%,
                        #f0c9a8 100%
                    );
                }

                div.block-container:has(.login-top) {
                    max-width: 420px !important;
                    background: #ffffff;
                    border-radius: 24px;
                    box-shadow: 0 18px 45px rgba(180, 90, 40, 0.18);
                    padding: 0 0 1.6rem 0 !important;
                    margin-top: 3rem;
                    overflow: hidden;
                }

                .login-top {
                    background: linear-gradient(135deg, #f07043 0%, #e85d30 100%);
                    padding: 2.4rem 2rem 2rem;
                    text-align: center;
                }

                .login-top .icone {
                    font-size: 2rem;
                    margin-bottom: 0.35rem;
                }

                .login-top h1 {
                    color: #ffffff;
                    font-size: 1.45rem;
                    font-weight: 800;
                    letter-spacing: 0.08em;
                    margin: 0 0 0.35rem 0;
                }

                .login-top p {
                    color: rgba(255, 255, 255, 0.92);
                    font-size: 0.92rem;
                    margin: 0;
                    line-height: 1.45;
                }

                div.block-container:has(.login-top) div[data-testid="stForm"] {
                    border: none;
                    padding: 1.5rem 2rem 0.25rem;
                    background: transparent;
                }

                div.block-container:has(.login-top) div[data-testid="stForm"] label {
                    font-size: 0.78rem !important;
                    font-weight: 600 !important;
                    color: #555 !important;
                }

                div.block-container:has(.login-top) div[data-testid="stForm"] input {
                    border: 1px solid #e8e8e8 !important;
                    border-radius: 10px !important;
                    padding: 0.65rem 0.85rem !important;
                    background: #fafafa !important;
                }

                div.block-container:has(.login-top) div[data-testid="stForm"] input:focus {
                    border-color: #f07043 !important;
                    box-shadow: 0 0 0 2px rgba(240, 112, 67, 0.15) !important;
                }

                div.block-container:has(.login-top) div[data-testid="stFormSubmitButton"] button {
                    width: 100%;
                    background: linear-gradient(135deg, #f07043 0%, #e85d30 100%) !important;
                    color: #ffffff !important;
                    border: none !important;
                    border-radius: 999px !important;
                    padding: 0.7rem 1rem !important;
                    font-weight: 700 !important;
                    letter-spacing: 0.06em !important;
                    margin-top: 0.35rem;
                }

                div.block-container:has(.login-top) div[data-testid="stFormSubmitButton"] button:hover {
                    background: linear-gradient(135deg, #e86538 0%, #d95320 100%) !important;
                }

                div.block-container:has(.login-top) .login-extra {
                    padding: 0 2rem;
                }

                div.block-container:has(.login-top) .login-divider {
                    border-top: 1px solid #f0e6dc;
                    margin: 1.1rem 2rem 1rem;
                }

                div.block-container:has(.login-top) .login-rodape {
                    padding: 0 2rem;
                    text-align: center;
                    color: #888;
                    font-size: 0.86rem;
                    margin-bottom: 0.65rem;
                }

                div.block-container:has(.login-top) .stButton {
                    padding: 0 2rem;
                }

                div.block-container:has(.login-top) .stButton > button[kind="secondary"] {
                    width: 100%;
                    border-radius: 999px !important;
                    border: 1px solid #f07043 !important;
                    color: #f07043 !important;
                    background: #ffffff !important;
                    font-weight: 600 !important;
                }

                div.block-container:has(.login-top) .stAlert {
                    margin: 0 2rem 0.5rem;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def _banner(titulo, subtitulo):
        st.markdown(
            f"""
            <div class="login-top">
                <div class="icone">🐾</div>
                <h1>{titulo}</h1>
                <p>{subtitulo}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def _form_login():
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("E-mail ou login", placeholder="Digite seu e-mail ou login")
            senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            entrar = st.form_submit_button("ENTRAR", type="primary", use_container_width=True)

        if entrar:
            usuario = View.autenticar(email, senha)
            if usuario is None:
                st.error("E-mail/login ou senha invalidos.")
            else:
                st.session_state.usuario = usuario
                st.session_state.carrinho = {}
                if usuario["admin"]:
                    st.session_state.pagina_admin = "dashboard"
                    st.session_state.mostrar_boas_vindas_admin = True
                else:
                    View.carregar(usuario["id"], st.session_state.carrinho)
                    st.session_state.mostrar_boas_vindas_loja = True
                st.rerun()


    @staticmethod
    def _form_cadastro():
        with st.form("cadastro_form", clear_on_submit=False):
            nome = st.text_input("Nome completo", placeholder="Seu nome")
            email = st.text_input("E-mail", placeholder="seu@email.com")
            fone = st.text_input("Telefone", placeholder="(00) 00000-0000")
            senha = st.text_input("Senha", type="password", placeholder="Mínimo 4 caracteres")
            senha2 = st.text_input("Confirmar senha", type="password", placeholder="Repita a senha")
            criar = st.form_submit_button("CRIAR CONTA", type="primary", use_container_width=True)

        if criar:
            try:
                cliente = View.abrir_conta(nome, email, fone, senha, senha2)
                st.success(f"Conta criada! Seu ID de cliente é {cliente.get_id()}.")
                st.session_state.modo_tela = "login"
                st.rerun()
            except ValueError as e:
                st.error(str(e))

    @staticmethod
    def _form_cadastro_entregador():
        with st.form("cadastro_entregador_form", clear_on_submit=False):
            nome = st.text_input("Nome completo", placeholder="Seu nome")
            fone = st.text_input("Telefone", placeholder="(00) 00000-0000")
            login = st.text_input("Login", placeholder="Crie um login de acesso")
            senha = st.text_input("Senha", type="password", placeholder="Mínimo 4 caracteres")
            senha2 = st.text_input("Confirmar senha", type="password", placeholder="Repita a senha")
            criar = st.form_submit_button("CADASTRAR", type="primary", use_container_width=True)

        if criar:
            try:
                entregador = View.entregador_cadastrar(nome, fone, login, senha, senha2)
                st.success(
                    f"Cadastro feito! Entre com o login '{entregador.get_login()}'."
                )
                st.session_state.modo_tela = "login"
                st.rerun()
            except ValueError as e:
                st.error(str(e))

    @staticmethod
    def _rodape_entregador():
        st.markdown('<div class="login-divider"></div>', unsafe_allow_html=True)
        st.markdown(
            '<p class="login-rodape">Já tem cadastro de entregador?</p>',
            unsafe_allow_html=True,
        )
        if st.button("Entrar", key="ent_voltar_login", use_container_width=True):
            st.session_state.modo_tela = "login"
            st.rerun()

    @staticmethod
    def _rodape_cadastro():
        st.markdown('<div class="login-divider"></div>', unsafe_allow_html=True)
        st.markdown(
            '<p class="login-rodape">Já possui uma conta?</p>',
            unsafe_allow_html=True,
        )
        if st.button("Entrar", use_container_width=True):
            st.session_state.modo_tela = "login"
            st.rerun()

    @staticmethod
    def _rodape_login():
        st.markdown('<div class="login-divider"></div>', unsafe_allow_html=True)
        st.markdown(
            '<p class="login-rodape">Não tem conta?</p>',
            unsafe_allow_html=True,
        )
        if st.button("Abrir conta", use_container_width=True):
            st.session_state.modo_tela = "cadastro"
            st.rerun()
        if st.button("Sou entregador", key="ir_entregador", use_container_width=True):
            st.session_state.modo_tela = "entregador"
            st.rerun()

    @staticmethod
    def main():
        LoginUI._css()

        if "modo_tela" not in st.session_state:
            st.session_state.modo_tela = "login"

        if st.session_state.modo_tela == "cadastro":
            LoginUI._banner("CRIAR CONTA", "Cadastre-se no Pet Shop IF")
            LoginUI._form_cadastro()
            LoginUI._rodape_cadastro()
            return

        if st.session_state.modo_tela == "entregador":
            LoginUI._banner("SOU ENTREGADOR", "Cadastre-se para realizar entregas")
            LoginUI._form_cadastro_entregador()
            LoginUI._rodape_entregador()
            return

        LoginUI._banner("BEM-VINDO(A)", "Entre na sua conta Pet Shop IF")
        LoginUI._form_login()
        LoginUI._rodape_login()
