import streamlit as st
import streamlit.components.v1 as components
from Templates.admin_dashboard import AdminDashboardUI
from Templates.admin_clientes import AdminClientesUI
from Templates.admin_categorias import AdminCategoriasUI
from Templates.admin_produtos import AdminProdutosUI
from Templates.admin_promocoes import AdminPromocoesUI
from Templates.admin_vendas import AdminVendasUI
from Templates.toast_utils import ToastUtils


class AdminLojaUI:
    PAGINAS = ("dashboard", "clientes", "categorias", "produtos", "promocoes", "vendas")

    @staticmethod
    def _css():
        ToastUtils.css()
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

                #MainMenu, header[data-testid="stHeader"], footer {
                    visibility: hidden;
                }

                .block-container {
                    max-width: 1280px;
                    padding-top: 0;
                    padding-bottom: 2rem;
                }

                .admin-navbar-fundo {
                    width: 100vw;
                    position: relative;
                    left: 50%;
                    margin-left: -50vw;
                    margin-right: -50vw;
                    height: 72px;
                    background: #d94e1a;
                    margin-bottom: -72px;
                    pointer-events: none;
                    box-shadow: 0 4px 18px rgba(160, 60, 10, 0.3);
                }

                #admin-nav-anchor ~ div[data-testid="stHorizontalBlock"] {
                    position: relative;
                    z-index: 2;
                    min-height: 72px;
                    align-items: center !important;
                    max-width: 1280px;
                    margin: 0 auto 1.8rem auto !important;
                    padding: 0 1.25rem !important;
                    background: transparent !important;
                }

                #admin-nav-anchor ~ div[data-testid="stHorizontalBlock"] [data-testid="column"] {
                    background: transparent !important;
                }

                #admin-nav-anchor ~ div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2)
                    div[data-testid="stHorizontalBlock"] {
                    flex-wrap: nowrap !important;
                    gap: 0.15rem !important;
                }

                #admin-nav-anchor ~ div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2)
                    div[data-testid="stHorizontalBlock"] [data-testid="column"] {
                    min-width: 0 !important;
                    flex: 1 1 auto !important;
                }

                #admin-nav-anchor ~ div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2)
                    div[data-testid="stHorizontalBlock"] button {
                    white-space: nowrap !important;
                    font-size: 0.8rem !important;
                    padding: 4px 6px !important;
                    min-height: unset !important;
                    width: 100% !important;
                    line-height: 1.2 !important;
                }

                #admin-nav-anchor ~ div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2)
                    div[data-testid="stHorizontalBlock"] button p,
                #admin-nav-anchor ~ div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2)
                    div[data-testid="stHorizontalBlock"] button span,
                #admin-nav-anchor ~ div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2)
                    div[data-testid="stHorizontalBlock"] button div {
                    white-space: nowrap !important;
                    font-size: 0.8rem !important;
                }

                .admin-logo {
                    display: flex;
                    align-items: center;
                    gap: 0.45rem;
                    color: #ffffff;
                    margin: 0;
                    min-width: 0;
                }

                .admin-logo-texto {
                    display: flex;
                    flex-direction: column;
                    line-height: 1.15;
                    min-width: 0;
                }

                .admin-logo-nome {
                    font-size: 1.3rem;
                    font-weight: 800;
                    white-space: nowrap;
                }

                .admin-logo small {
                    font-size: 0.72rem;
                    font-weight: 600;
                    opacity: 0.85;
                    letter-spacing: 0.04em;
                    text-transform: uppercase;
                    white-space: nowrap;
                }

                .admin-hero {
                    background: #ffffff;
                    border-radius: 20px;
                    padding: 1.4rem 1.6rem;
                    box-shadow: 0 10px 28px rgba(180, 90, 40, 0.1);
                    margin-bottom: 1.2rem;
                }

                .admin-hero h2 {
                    margin: 0 0 0.35rem 0;
                    color: #333;
                    font-size: 1.35rem;
                    font-weight: 800;
                }

                .admin-hero p {
                    margin: 0;
                    color: #888;
                    font-size: 0.92rem;
                }

                .admin-card {
                    background: #ffffff;
                    border-radius: 18px;
                    padding: 1.2rem 1.4rem;
                    box-shadow: 0 8px 24px rgba(180, 90, 40, 0.1);
                    margin-bottom: 1rem;
                }

                .admin-card-titulo {
                    color: #555;
                    font-size: 0.82rem;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 0.04em;
                    margin: 0 0 0.9rem 0;
                }

                .admin-stat-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                    gap: 1rem;
                    margin-bottom: 1.2rem;
                }

                .admin-stat {
                    background: #ffffff;
                    border-radius: 16px;
                    padding: 1.1rem 1.2rem;
                    box-shadow: 0 8px 22px rgba(180, 90, 40, 0.08);
                }

                .admin-stat .label {
                    color: #999;
                    font-size: 0.75rem;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 0.04em;
                    margin: 0 0 0.3rem 0;
                }

                .admin-stat .valor {
                    color: #e85d30;
                    font-size: 1.5rem;
                    font-weight: 800;
                    margin: 0;
                }

                .admin-tabela {
                    width: 100%;
                    border-collapse: collapse;
                    font-size: 0.88rem;
                }

                .admin-tabela th {
                    text-align: left;
                    color: #999;
                    font-size: 0.75rem;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 0.04em;
                    padding: 0.55rem 0.75rem;
                    border-bottom: 2px solid #f3ebe3;
                }

                .admin-tabela td {
                    padding: 0.65rem 0.75rem;
                    border-bottom: 1px solid #f8f2ec;
                    color: #444;
                }

                .admin-tabela tr:last-child td {
                    border-bottom: none;
                }

                .dash-painel {
                    background: #ffffff;
                    border-radius: 18px;
                    overflow: hidden;
                    box-shadow: 0 8px 24px rgba(180, 90, 40, 0.1);
                    height: 100%;
                }

                .dash-painel-topo {
                    display: flex;
                    align-items: center;
                    gap: 0.85rem;
                    padding: 1.1rem 1.3rem;
                    background: linear-gradient(135deg, #fff8f3 0%, #ffffff 100%);
                    border-bottom: 1px solid #f5ebe3;
                }

                .dash-painel-icone {
                    width: 42px;
                    height: 42px;
                    border-radius: 12px;
                    background: #fff3ec;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.25rem;
                    flex-shrink: 0;
                }

                .dash-painel-topo h3 {
                    margin: 0;
                    color: #333;
                    font-size: 1rem;
                    font-weight: 800;
                }

                .dash-painel-topo p {
                    margin: 0.15rem 0 0 0;
                    color: #aaa;
                    font-size: 0.78rem;
                }

                .dash-tabela-wrap {
                    padding: 0.4rem 0.6rem 0.6rem;
                }

                .dash-tabela {
                    width: 100%;
                    border-collapse: separate;
                    border-spacing: 0;
                    font-size: 0.88rem;
                }

                .dash-tabela thead th {
                    text-align: left;
                    color: #aaa;
                    font-size: 0.72rem;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    padding: 0.65rem 0.85rem;
                    background: #faf7f4;
                    border-bottom: 1px solid #f0e6dc;
                }

                .dash-tabela thead th:first-child {
                    border-radius: 10px 0 0 0;
                }

                .dash-tabela thead th:last-child {
                    border-radius: 0 10px 0 0;
                }

                .dash-tabela tbody td {
                    padding: 0.75rem 0.85rem;
                    color: #444;
                    border-bottom: 1px solid #f8f2ec;
                    vertical-align: middle;
                }

                .dash-tabela tbody tr:last-child td {
                    border-bottom: none;
                }

                .dash-tabela tbody tr:hover td {
                    background: #fffcfa;
                }

                .dash-tabela .col-total {
                    text-align: right;
                    color: #e85d30;
                    font-weight: 800;
                    white-space: nowrap;
                }

                .dash-tabela .col-pedido {
                    color: #e85d30;
                    font-weight: 800;
                }

                .dash-tabela .col-produto {
                    font-weight: 600;
                    color: #333;
                }

                .dash-tabela .col-cliente {
                    color: #666;
                }

                .dash-badge-alerta {
                    display: inline-block;
                    background: #fff3ec;
                    color: #e85d30;
                    border: 1px solid #fde0cc;
                    border-radius: 999px;
                    padding: 0.2rem 0.65rem;
                    font-size: 0.75rem;
                    font-weight: 700;
                    white-space: nowrap;
                }

                .dash-vazio {
                    text-align: center;
                    padding: 2rem 1rem;
                    color: #aaa;
                    font-size: 0.9rem;
                }

                .dash-vazio-icon {
                    font-size: 2rem;
                    margin-bottom: 0.5rem;
                }

                .admin-badge {
                    display: inline-block;
                    background: #fff3ec;
                    color: #e85d30;
                    border-radius: 999px;
                    padding: 0.15rem 0.55rem;
                    font-size: 0.72rem;
                    font-weight: 700;
                }

                .admin-empty {
                    text-align: center;
                    color: #888;
                    padding: 2.5rem 1rem;
                    background: #ffffff;
                    border-radius: 18px;
                    box-shadow: 0 8px 24px rgba(180, 90, 40, 0.08);
                }

                .admin-form-box {
                    background: #ffffff;
                    border-radius: 18px;
                    padding: 1.3rem 1.4rem;
                    box-shadow: 0 8px 24px rgba(180, 90, 40, 0.1);
                    margin-top: 0.5rem;
                }

                .admin-form-box h4 {
                    margin: 0 0 0.25rem 0;
                    color: #333;
                    font-size: 1rem;
                    font-weight: 800;
                }

                .admin-form-box .sub {
                    margin: 0 0 1rem 0;
                    color: #999;
                    font-size: 0.85rem;
                }

                .admin-form-box .dica-id {
                    background: #fff3ec;
                    color: #e85d30;
                    border-radius: 10px;
                    padding: 0.55rem 0.85rem;
                    font-size: 0.85rem;
                    font-weight: 600;
                    margin-bottom: 1rem;
                }

                .admin-cliente-preview {
                    background: #faf7f4;
                    border: 1px solid #f0e6dc;
                    border-radius: 14px;
                    padding: 1rem 1.1rem;
                    margin-bottom: 1rem;
                }

                .admin-cliente-preview .nome {
                    color: #333;
                    font-size: 1.05rem;
                    font-weight: 800;
                    margin: 0 0 0.35rem 0;
                }

                .admin-cliente-preview .info {
                    color: #777;
                    font-size: 0.85rem;
                    margin: 0.15rem 0;
                }

                .admin-prod-preview {
                    display: flex;
                    align-items: center;
                    gap: 1.1rem;
                    background: #ffffff;
                    border: 1px solid #f0e6dc;
                    border-radius: 16px;
                    padding: 1rem 1.2rem;
                    box-shadow: 0 6px 18px rgba(180, 90, 40, 0.08);
                    margin: 0.75rem 0 1rem 0;
                }

                .admin-prod-preview-foto {
                    flex-shrink: 0;
                    width: 100px;
                    height: 100px;
                    border-radius: 12px;
                    overflow: hidden;
                    background: linear-gradient(135deg, #fff5ec 0%, #fdebd0 100%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border: 1px solid #f0e6dc;
                }

                .admin-prod-preview-foto img {
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                    display: block;
                }

                .admin-prod-preview-foto .sem-foto {
                    color: #ccc;
                    font-size: 2rem;
                }

                .admin-prod-preview-info {
                    flex: 1;
                    min-width: 0;
                }

                .admin-prod-preview-info .nome {
                    color: #333;
                    font-size: 0.95rem;
                    font-weight: 800;
                    margin: 0 0 0.4rem 0;
                    line-height: 1.35;
                }

                .admin-prod-preview-info .meta {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 0.5rem 1rem;
                    color: #777;
                    font-size: 0.84rem;
                }

                .admin-prod-preview-info .meta span {
                    white-space: nowrap;
                }

                .admin-filtro-produto {
                    background: #ffffff;
                    border: 1px solid #f0e6dc;
                    border-radius: 14px;
                    padding: 1rem 1.1rem;
                    margin-bottom: 0.5rem;
                }

                .admin-alerta-excluir {
                    background: #fff5f5;
                    border: 1px solid #ffd4d4;
                    border-radius: 12px;
                    padding: 0.85rem 1rem;
                    color: #b44;
                    font-size: 0.88rem;
                    margin: 0.75rem 0 1rem 0;
                }

                div[data-testid="stTabs"] button {
                    font-weight: 600 !important;
                }

                div[data-testid="stTabs"] div[data-testid="stForm"] {
                    background: #ffffff;
                    border: 1px solid #f0e6dc;
                    border-radius: 14px;
                    padding: 1.2rem 1.3rem;
                    box-shadow: 0 6px 18px rgba(180, 90, 40, 0.06);
                }

                div[data-testid="stForm"] label {
                    font-size: 0.78rem !important;
                    font-weight: 600 !important;
                    color: #666 !important;
                }

                div[data-testid="stForm"] input {
                    border: 1px solid #e8e8e8 !important;
                    border-radius: 10px !important;
                    background: #fafafa !important;
                }

                div[data-testid="stForm"] input:focus {
                    border-color: #f07043 !important;
                    box-shadow: 0 0 0 2px rgba(240, 112, 67, 0.12) !important;
                }

                div[data-testid="stFormSubmitButton"] button,
                .stButton > button[kind="primary"] {
                    background: linear-gradient(135deg, #f07043 0%, #e85d30 100%) !important;
                    color: #ffffff !important;
                    border: none !important;
                    border-radius: 999px !important;
                    font-weight: 700 !important;
                }

                .stButton > button[kind="secondary"] {
                    border-radius: 999px !important;
                    border: 1px solid #f07043 !important;
                    color: #f07043 !important;
                    background: #ffffff !important;
                    font-weight: 600 !important;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def _estilizar_nav_js(pagina_atual, labels):
        nomes = [labels[p] for p in AdminLojaUI.PAGINAS]
        ativo = labels[pagina_atual]
        nomes_json = str(nomes).replace("'", '"')

        components.html(
            f"""
            <script>
            (function() {{
                const doc = window.parent.document;
                const nomes = {nomes_json};
                const ativo = "{ativo}";

                function estilizarNav() {{
                    doc.querySelectorAll("button").forEach((btn) => {{
                        const txt = (btn.innerText || "").trim();

                        if (txt === "Sair") {{
                            btn.style.setProperty("background", "transparent", "important");
                            btn.style.setProperty("color", "#ffffff", "important");
                            btn.style.setProperty("border", "1px solid rgba(255,255,255,0.65)", "important");
                            btn.style.setProperty("border-radius", "999px", "important");
                            btn.style.setProperty("font-size", "0.85rem", "important");
                            btn.style.setProperty("padding", "4px 14px", "important");
                            btn.style.setProperty("min-height", "unset", "important");
                            btn.style.setProperty("font-weight", "600", "important");
                            btn.querySelectorAll("p, span, div").forEach((el) => {{
                                el.style.setProperty("color", "#ffffff", "important");
                            }});
                            return;
                        }}

                        const nome = nomes.find((n) => txt.startsWith(n));
                        if (!nome) return;

                        btn.style.setProperty("background", "transparent", "important");
                        btn.style.setProperty("background-color", "transparent", "important");
                        btn.style.setProperty("color", "#ffffff", "important");
                        btn.style.setProperty("border", "none", "important");
                        btn.style.setProperty("border-radius", "0", "important");
                        btn.style.setProperty("box-shadow", "none", "important");
                        btn.style.setProperty("font-size", "0.8rem", "important");
                        btn.style.setProperty("padding", "4px 6px", "important");
                        btn.style.setProperty("min-height", "unset", "important");
                        btn.style.setProperty("white-space", "nowrap", "important");
                        btn.style.setProperty("font-weight", nome === ativo ? "700" : "500", "important");
                        btn.querySelectorAll("p, span, div").forEach((el) => {{
                            el.style.setProperty("white-space", "nowrap", "important");
                            el.style.setProperty("font-size", "0.8rem", "important");
                        }});
                        btn.style.setProperty(
                            "border-bottom",
                            nome === ativo ? "2px solid #ffffff" : "2px solid transparent",
                            "important"
                        );
                        btn.querySelectorAll("p, span, div").forEach((el) => {{
                            el.style.setProperty("color", "#ffffff", "important");
                        }});
                    }});
                }}

                estilizarNav();
                setTimeout(estilizarNav, 80);
                setTimeout(estilizarNav, 300);
                new MutationObserver(estilizarNav).observe(doc.body, {{
                    childList: true,
                    subtree: true,
                }});
            }})();
            </script>
            """,
            height=0,
        )

    @staticmethod
    def _sair():
        st.session_state.usuario = None
        st.session_state.carrinho = {}
        st.session_state.modo_tela = "login"
        st.session_state.pagina_admin = "dashboard"
        st.session_state.mostrar_boas_vindas_admin = False
        st.rerun()

    @staticmethod
    def _header(usuario):
        if "pagina_admin" not in st.session_state:
            st.session_state.pagina_admin = "dashboard"

        labels = {
            "dashboard": "Inicio",
            "clientes": "Clientes",
            "categorias": "Categorias",
            "produtos": "Produtos",
            "promocoes": "Promocoes",
            "vendas": "Vendas",
        }

        if st.session_state.pagina_admin not in AdminLojaUI.PAGINAS:
            st.session_state.pagina_admin = "dashboard"

        pagina_atual = st.session_state.pagina_admin

        st.markdown('<div class="admin-navbar-fundo"></div>', unsafe_allow_html=True)
        st.markdown('<div id="admin-nav-anchor"></div>', unsafe_allow_html=True)

        col_logo, col_menu, col_sair = st.columns([1.35, 6.45, 0.75], gap="small")

        with col_logo:
            st.markdown(
                """
                <p class="admin-logo">
                    <span>🐾</span>
                    <span class="admin-logo-texto">
                        <span class="admin-logo-nome">Pet Shop IF</span>
                        <small>Painel Admin</small>
                    </span>
                </p>
                """,
                unsafe_allow_html=True,
            )

        with col_menu:
            nav_pesos = [0.85, 1.0, 1.2, 1.0, 1.15, 0.9]
            nav_cols = st.columns(nav_pesos, gap="small")
            for col, pagina in zip(nav_cols, AdminLojaUI.PAGINAS):
                with col:
                    if st.button(
                        labels[pagina],
                        key=f"admin_nav_{pagina}",
                        type="secondary",
                    ):
                        if pagina != pagina_atual:
                            st.session_state.pagina_admin = pagina
                            st.rerun()

        with col_sair:
            if st.button("Sair", key="admin_sair", type="secondary", help="Sair do sistema"):
                AdminLojaUI._sair()

        AdminLojaUI._estilizar_nav_js(pagina_atual, labels)

        if st.session_state.get("mostrar_boas_vindas_admin", False):
            st.toast(
                f"Bem-vindo(a), {usuario['nome']}! Painel administrativo.",
                icon="🔧",
            )
            st.session_state.mostrar_boas_vindas_admin = False

        msg_sucesso = st.session_state.pop("admin_sucesso", None)
        if msg_sucesso:
            ToastUtils.sucesso(msg_sucesso)

    @staticmethod
    def main(usuario):
        AdminLojaUI._css()
        AdminLojaUI._header(usuario)

        pagina = st.session_state.get("pagina_admin", "dashboard")

        if pagina == "dashboard":
            AdminDashboardUI.main()
        elif pagina == "clientes":
            AdminClientesUI.main()
        elif pagina == "categorias":
            AdminCategoriasUI.main()
        elif pagina == "produtos":
            AdminProdutosUI.main()
        elif pagina == "promocoes":
            AdminPromocoesUI.main()
        elif pagina == "vendas":
            AdminVendasUI.main()
