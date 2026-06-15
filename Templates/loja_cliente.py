import base64
import html

import streamlit as st
import streamlit.components.v1 as components
from views import View
from Templates.carrinho_cliente import CarrinhoClienteUI
from Templates.compras_cliente import ComprasClienteUI
from Templates.perfil_cliente import PerfilClienteUI
from Templates.toast_utils import ToastUtils


class LojaClienteUI:
    PAGINAS = ("produtos", "favoritos", "carrinho", "compras", "perfil")

    @staticmethod
    def _css():
        ToastUtils.css()
        st.markdown(
            """
            <style>
                .stApp {
                    background: linear-gradient(
                        180deg,
                        #fff9f5 0%,
                        #fdebd0 42%,
                        #f6d5b8 100%
                    );
                }

                #MainMenu, header[data-testid="stHeader"], footer {
                    visibility: hidden;
                }

                .block-container {
                    max-width: 1100px;
                    padding-top: 0;
                    padding-bottom: 2rem;
                }

                .loja-navbar-fundo {
                    width: 100vw;
                    position: relative;
                    left: 50%;
                    margin-left: -50vw;
                    margin-right: -50vw;
                    height: 72px;
                    background: #ff8c2e;
                    margin-bottom: -72px;
                    pointer-events: none;
                    box-shadow: 0 4px 18px rgba(200, 90, 20, 0.25);
                }

                #nav-anchor ~ div[data-testid="stHorizontalBlock"] {
                    position: relative;
                    z-index: 2;
                    min-height: 72px;
                    align-items: center !important;
                    max-width: 1100px;
                    margin: 0 auto 1.8rem auto !important;
                    padding: 0 2rem !important;
                    background: transparent !important;
                }

                #nav-anchor ~ div[data-testid="stHorizontalBlock"] [data-testid="column"] {
                    background: transparent !important;
                }

                .loja-logo {
                    display: flex;
                    align-items: center;
                    gap: 0.45rem;
                    color: #ffffff;
                    font-size: 1.65rem;
                    font-weight: 800;
                    letter-spacing: -0.02em;
                    margin: 0;
                    white-space: nowrap;
                }

                .loja-logo-icon {
                    font-size: 1.5rem;
                    line-height: 1;
                }

                #nav-anchor ~ div[data-testid="stHorizontalBlock"] [data-testid="column"] > div {
                    background: transparent !important;
                }

                #nav-anchor ~ div[data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid="stHorizontalBlock"] {
                    justify-content: center !important;
                    gap: 0.15rem !important;
                    flex-wrap: nowrap !important;
                }

                #nav-anchor ~ div[data-testid="stHorizontalBlock"] > div:nth-child(2)
                    [data-testid="stHorizontalBlock"] button {
                    white-space: nowrap !important;
                    font-size: 0.78rem !important;
                    padding: 4px 6px !important;
                    min-height: unset !important;
                }

                #nav-anchor ~ div[data-testid="stHorizontalBlock"] > div:nth-child(2)
                    [data-testid="stHorizontalBlock"] button p,
                #nav-anchor ~ div[data-testid="stHorizontalBlock"] > div:nth-child(2)
                    [data-testid="stHorizontalBlock"] button span,
                #nav-anchor ~ div[data-testid="stHorizontalBlock"] > div:nth-child(2)
                    [data-testid="stHorizontalBlock"] button div {
                    white-space: nowrap !important;
                    font-size: 0.78rem !important;
                }

                .loja-produtos-topo {
                    background: linear-gradient(135deg, #fff8f3 0%, #ffffff 55%);
                    border-radius: 20px;
                    padding: 1.35rem 1.5rem 1.15rem;
                    border: 1px solid rgba(240, 230, 220, 0.9);
                    margin-bottom: 1.25rem;
                    box-shadow: 0 8px 24px rgba(180, 90, 40, 0.08);
                }

                .loja-produtos-topo .eyebrow {
                    display: inline-block;
                    background: #fff3ec;
                    color: #e85d30;
                    border-radius: 999px;
                    padding: 0.22rem 0.7rem;
                    font-size: 0.72rem;
                    font-weight: 700;
                    letter-spacing: 0.04em;
                    text-transform: uppercase;
                    margin-bottom: 0.55rem;
                }

                .loja-produtos-topo h2 {
                    margin: 0 0 0.3rem 0;
                    color: #333;
                    font-size: 1.45rem;
                    font-weight: 800;
                    letter-spacing: -0.02em;
                }

                .loja-produtos-topo p {
                    margin: 0;
                    color: #888;
                    font-size: 0.92rem;
                    line-height: 1.45;
                }

                div[data-testid="stHorizontalBlock"]:has(.loja-filtro-mark) {
                    background: #ffffff;
                    border: 1px solid rgba(240, 230, 220, 0.9);
                    border-top: 1px solid #f5ebe3;
                    border-radius: 0 0 20px 20px;
                    padding: 0.95rem 1.5rem 1.15rem;
                    box-shadow: 0 10px 28px rgba(180, 90, 40, 0.1);
                    margin-bottom: 1.5rem;
                    align-items: flex-end !important;
                    gap: 1rem !important;
                }

                div[data-testid="stHorizontalBlock"]:has(.loja-filtro-mark) > div[data-testid="column"]:last-child {
                    display: flex !important;
                    align-items: flex-end !important;
                    justify-content: flex-end !important;
                    padding-bottom: 0.1rem !important;
                }

                div[data-testid="stHorizontalBlock"]:has(.loja-filtro-mark) label {
                    font-size: 0.72rem !important;
                    font-weight: 700 !important;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    color: #aaa !important;
                    margin-bottom: 0.35rem !important;
                }

                div[data-testid="stHorizontalBlock"]:has(.loja-filtro-mark) div[data-testid="stSelectbox"] > div {
                    border-radius: 12px !important;
                    border-color: #f0e6dc !important;
                    background: #faf7f4 !important;
                    min-height: 2.65rem !important;
                }

                div[data-testid="stHorizontalBlock"]:has(.loja-filtro-mark) div[data-testid="stSelectbox"] > div:hover {
                    border-color: #f07043 !important;
                }

                div[data-testid="stHorizontalBlock"]:has(.loja-filtro-mark) > div[data-testid="column"]:last-child div[data-testid="element-container"] {
                    display: flex !important;
                    align-items: center !important;
                    justify-content: flex-end !important;
                    height: 100% !important;
                }

                .loja-filtro-mark {
                    display: none;
                }

                .loja-contador {
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    gap: 0.35rem;
                    background: linear-gradient(135deg, #fff3ec 0%, #ffe8dc 100%);
                    color: #e85d30;
                    border: 1px solid #ffd8c8;
                    border-radius: 999px;
                    padding: 0.5rem 0.95rem;
                    font-size: 0.82rem;
                    font-weight: 800;
                    margin: 0 0 0 auto;
                    white-space: nowrap;
                }

                .loja-contador::before {
                    content: "📦";
                    font-size: 0.9rem;
                    line-height: 1;
                }

                .loja-produto-shell,
                .loja-fav-anchor,
                .loja-comprar-anchor {
                    display: none;
                }

                [data-testid="column"]:has(.loja-produto-shell) {
                    position: relative !important;
                    background: #ffffff !important;
                    border-radius: 14px !important;
                    border: 1px solid #ececec !important;
                    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.07) !important;
                    overflow: hidden !important;
                    margin-bottom: 1.25rem !important;
                    display: flex !important;
                    flex-direction: column !important;
                }

                [data-testid="column"]:has(.loja-produto-shell) > div {
                    gap: 0 !important;
                    display: flex !important;
                    flex-direction: column !important;
                    flex: 1 1 auto !important;
                    height: 100% !important;
                    width: 100% !important;
                }

                [data-testid="column"]:has(.loja-produto-shell) div[data-testid="element-container"] {
                    background: transparent !important;
                    box-shadow: none !important;
                    margin: 0 !important;
                    padding-left: 0 !important;
                    padding-right: 0 !important;
                }

                [data-testid="column"]:has(.loja-produto-shell)
                    div[data-testid="element-container"]:has(.loja-produto-shell) {
                    display: none !important;
                    height: 0 !important;
                    min-height: 0 !important;
                    padding: 0 !important;
                    margin: 0 !important;
                }

                [data-testid="column"]:has(.loja-produto-shell)
                    div[data-testid="element-container"]:has(iframe) {
                    flex-shrink: 0 !important;
                    margin: 0 !important;
                    padding: 0 !important;
                    line-height: 0;
                }

                [data-testid="column"]:has(.loja-produto-shell)
                    div[data-testid="element-container"]:has(iframe)
                    + div[data-testid="element-container"] {
                    position: absolute !important;
                    top: 0.6rem !important;
                    right: 0.6rem !important;
                    left: auto !important;
                    z-index: 15 !important;
                    width: 2.25rem !important;
                    padding: 0 !important;
                    margin: 0 !important;
                }

                [data-testid="column"]:has(.loja-produto-shell)
                    div[data-testid="element-container"]:has(iframe)
                    + div[data-testid="element-container"] .stButton {
                    width: 2.25rem !important;
                }

                [data-testid="column"]:has(.loja-produto-shell)
                    div[data-testid="element-container"]:has(iframe)
                    + div[data-testid="element-container"] .stButton > button {
                    width: 2.25rem !important;
                    height: 2.25rem !important;
                    min-height: 2.25rem !important;
                    padding: 0 !important;
                    border-radius: 50% !important;
                    background: rgba(255, 255, 255, 0.95) !important;
                    border: 1px solid #e0e0e0 !important;
                    color: #ccc !important;
                    font-size: 0.95rem !important;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
                }

                [data-testid="column"]:has(.loja-produto-favorito)
                    div[data-testid="element-container"]:has(iframe)
                    + div[data-testid="element-container"] .stButton > button {
                    color: #e85d30 !important;
                    border-color: #f5c4a8 !important;
                    background: #fff5ef !important;
                }

                [data-testid="column"]:has(.loja-produto-shell)
                    div[data-testid="element-container"]:has(.loja-produto-card) {
                    flex: 1 1 auto !important;
                    display: flex !important;
                    flex-direction: column !important;
                }

                div[data-testid="stHorizontalBlock"]:has(.loja-produto-shell) {
                    align-items: stretch !important;
                }

                div[data-testid="stHorizontalBlock"]:has(.loja-produto-shell) > div[data-testid="column"] {
                    display: flex !important;
                    flex-direction: column !important;
                }

                .loja-produto-card {
                    flex: 1 1 auto;
                    display: flex;
                    flex-direction: column;
                }

                .loja-produto-corpo {
                    padding: 0.85rem 1rem 0.5rem;
                    display: flex;
                    flex-direction: column;
                    gap: 0.45rem;
                    flex: 1 1 auto;
                    min-height: 8.5rem;
                }

                .loja-produto-corpo h3 {
                    margin: 0;
                    color: #222;
                    font-size: 0.9rem;
                    font-weight: 700;
                    line-height: 1.35;
                    min-height: 2.7em;
                    max-height: 2.7em;
                    overflow: hidden;
                    display: -webkit-box;
                    -webkit-line-clamp: 2;
                    -webkit-box-orient: vertical;
                }

                .loja-cat-wrap {
                    line-height: 1;
                }

                .loja-cat-chip {
                    display: inline-block;
                    width: auto;
                    max-width: max-content;
                    border: 1px solid #444;
                    border-radius: 5px;
                    padding: 0.15rem 0.45rem;
                    font-size: 0.65rem;
                    font-weight: 700;
                    color: #333;
                    letter-spacing: 0.02em;
                }

                .loja-preco-ref {
                    min-height: 2.2rem;
                }

                .loja-preco-ref .preco-cheio {
                    margin: 0;
                    color: #222;
                    font-size: 1.35rem;
                    font-weight: 800;
                    line-height: 1.1;
                }

                .loja-preco-ref .preco-cheio.riscado {
                    color: #999;
                    font-size: 0.95rem;
                    font-weight: 600;
                    text-decoration: line-through;
                }

                .loja-preco-promo-linha {
                    display: flex;
                    align-items: center;
                    gap: 0.45rem;
                    margin-top: 0.2rem;
                }

                .loja-preco-ref .preco-oferta {
                    color: #e85d30;
                    font-size: 1.2rem;
                    font-weight: 800;
                    line-height: 1;
                }

                .loja-badge-off {
                    display: inline-block;
                    background: #e85d30;
                    color: #ffffff;
                    border-radius: 4px;
                    padding: 0.12rem 0.38rem;
                    font-size: 0.68rem;
                    font-weight: 800;
                }

                .loja-estoque-linha {
                    margin: 0;
                    font-size: 0.72rem;
                    font-weight: 600;
                    color: #888;
                    min-height: 1.1rem;
                }

                .loja-estoque-linha.baixo {
                    color: #e85d30;
                }

                [data-testid="column"]:has(.loja-produto-shell)
                    div[data-testid="element-container"]:has(.loja-comprar-anchor) {
                    display: none !important;
                    height: 0 !important;
                    margin: 0 !important;
                    padding: 0 !important;
                }

                [data-testid="column"]:has(.loja-produto-shell)
                    div[data-testid="element-container"]:has(.loja-comprar-anchor)
                    + div[data-testid="element-container"] {
                    padding: 0.5rem 1rem 1rem !important;
                    margin-top: auto !important;
                    flex-shrink: 0 !important;
                }

                [data-testid="column"]:has(.loja-produto-shell)
                    div[data-testid="element-container"]:has(.loja-comprar-anchor)
                    + div[data-testid="element-container"] .stButton {
                    width: 100% !important;
                }

                [data-testid="column"]:has(.loja-produto-shell)
                    div[data-testid="element-container"]:has(.loja-comprar-anchor)
                    + div[data-testid="element-container"] .stButton > button {
                    width: 100% !important;
                    height: 2.75rem !important;
                    min-height: 2.75rem !important;
                    background: linear-gradient(135deg, #f07043 0%, #e85d30 100%) !important;
                    color: #ffffff !important;
                    border: none !important;
                    border-radius: 10px !important;
                    font-weight: 800 !important;
                    font-size: 0.82rem !important;
                    letter-spacing: 0.06em !important;
                    text-transform: uppercase !important;
                    box-shadow: 0 6px 16px rgba(232, 93, 48, 0.22) !important;
                }

                [data-testid="column"]:has(.loja-produto-shell)
                    div[data-testid="element-container"]:has(.loja-comprar-anchor)
                    + div[data-testid="element-container"] .stButton > button:hover {
                    background: linear-gradient(135deg, #e85d30 0%, #d94e1a 100%) !important;
                }

                [data-testid="column"]:has(.loja-produto-shell)
                    div[data-testid="element-container"]:has(.loja-comprar-anchor)
                    + div[data-testid="element-container"] .stButton > button p {
                    margin: 0 !important;
                    font-weight: 800 !important;
                    letter-spacing: 0.06em !important;
                }

                .loja-section-title {
                    color: #555;
                    font-size: 0.95rem;
                    font-weight: 700;
                    letter-spacing: 0.05em;
                    margin: 0 0 1rem 0;
                    text-transform: uppercase;
                }

                .loja-empty {
                    text-align: center;
                    color: #888;
                    padding: 2.5rem 1rem;
                    background: #ffffff;
                    border-radius: 18px;
                    box-shadow: 0 8px 24px rgba(180, 90, 40, 0.08);
                }

                div[data-testid="stForm"] {
                    border: none;
                    padding: 0;
                    background: transparent;
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
    def _mapa_categorias():
        return {c.get_id(): c.get_descricao() for c in View.categoria_listar()}

    @staticmethod
    def _ids_favoritos(id_cliente):
        return {p.get_id() for p in View.listar_produtos_favoritos(id_cliente)}

    @staticmethod
    def _processar_nav_query():
        if "nav" not in st.query_params:
            return
        nav = st.query_params["nav"]
        if isinstance(nav, list):
            nav = nav[0]
        if nav in LojaClienteUI.PAGINAS:
            st.session_state.pagina_loja = nav
        restante = {chave: st.query_params[chave] for chave in st.query_params if chave != "nav"}
        st.query_params.from_dict(restante)
        st.rerun()

    @staticmethod
    def _estilizar_nav_js(pagina_atual, labels):
        nomes = [labels[p] for p in LojaClienteUI.PAGINAS]
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
                        const nome = nomes.find((n) => txt.startsWith(n));
                        if (!nome) return;

                        btn.style.setProperty("background", "transparent", "important");
                        btn.style.setProperty("background-color", "transparent", "important");
                        btn.style.setProperty("color", "#ffffff", "important");
                        btn.style.setProperty("border", "none", "important");
                        btn.style.setProperty("border-radius", "0", "important");
                        btn.style.setProperty("box-shadow", "none", "important");
                        btn.style.setProperty("font-size", "0.78rem", "important");
                        btn.style.setProperty("padding", "4px 6px", "important");
                        btn.style.setProperty("min-height", "unset", "important");
                        btn.style.setProperty("white-space", "nowrap", "important");
                        btn.style.setProperty("font-weight", nome === ativo ? "700" : "500", "important");
                        btn.querySelectorAll("p, span, div").forEach((el) => {{
                            el.style.setProperty("white-space", "nowrap", "important");
                            el.style.setProperty("font-size", "0.78rem", "important");
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
    def _header(usuario):
        if "pagina_loja" not in st.session_state:
            st.session_state.pagina_loja = "produtos"

        labels = {
            "produtos": "Produtos",
            "favoritos": "Favoritos",
            "carrinho": "Carrinho",
            "compras": "Compras",
            "perfil": "Perfil",
        }

        if st.session_state.pagina_loja not in LojaClienteUI.PAGINAS:
            st.session_state.pagina_loja = "produtos"

        pagina_atual = st.session_state.pagina_loja

        st.markdown('<div class="loja-navbar-fundo"></div>', unsafe_allow_html=True)
        st.markdown('<div id="nav-anchor"></div>', unsafe_allow_html=True)

        col_logo, col_menu = st.columns([1.5, 5.5], gap="small")

        with col_logo:
            st.markdown(
                """
                <p class="loja-logo">
                    <span class="loja-logo-icon">🐾</span> Pet Shop IF
                </p>
                """,
                unsafe_allow_html=True,
            )

        with col_menu:
            nav_pesos = [1.0, 1.05, 0.95, 1.0, 0.9]
            nav_cols = st.columns(nav_pesos, gap="small")
            for col, pagina in zip(nav_cols, LojaClienteUI.PAGINAS):
                with col:
                    if st.button(
                        f"{labels[pagina]}  ▾",
                        key=f"nav_{pagina}",
                        type="secondary",
                    ):
                        if pagina != pagina_atual:
                            st.session_state.pagina_loja = pagina
                            st.rerun()

        LojaClienteUI._estilizar_nav_js(pagina_atual, labels)

        if st.session_state.get("mostrar_boas_vindas_loja", False):
            ToastUtils.boas_vindas(usuario["nome"])
            st.session_state.mostrar_boas_vindas_loja = False

        if st.session_state.pop("produto_adicionado_carrinho", False):
            ToastUtils.sucesso("Produto adicionado ao carrinho!", "🛒")

        if st.session_state.pop("produto_favoritado", False):
            ToastUtils.sucesso("Produto adicionado aos favoritos!", "❤️")

        if st.session_state.pop("produto_desfavoritado", False):
            ToastUtils.sucesso("Produto removido dos favoritos.", "🤍")

    @staticmethod
    def _icone_categoria(cat_nome):
        icones = {
            "Roupas": "👕",
            "Comida": "🍖",
            "Limpeza": "🧹",
        }
        return icones.get(cat_nome, "🐾")

    @staticmethod
    def _html_estoque(estoque):
        if estoque <= 3:
            return f'<p class="loja-estoque-linha baixo">Ultimas {estoque} unidades</p>'
        return '<p class="loja-estoque-linha">Em estoque</p>'

    @staticmethod
    def _render_imagem_produto(id_produto, icone):
        foto = View.produto_caminho_foto(id_produto)
        if foto:
            ext = foto.suffix.lstrip(".").lower()
            mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp"}.get(
                ext, "jpeg"
            )
            b64 = base64.b64encode(foto.read_bytes()).decode()
            conteudo = (
                f'<img src="data:image/{mime};base64,{b64}" alt="Foto do produto" />'
            )
        else:
            conteudo = f'<span class="icone">{icone}</span>'

        components.html(
            f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
                    body {{
                        margin: 0;
                        font-family: "Source Sans Pro", sans-serif;
                        background: transparent;
                    }}
                    .wrap {{
                        position: relative;
                        height: 200px;
                        background: #fafafa;
                        border-radius: 14px 14px 0 0;
                        overflow: hidden;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        padding: 1rem;
                    }}
                    .wrap img {{
                        max-width: 100%;
                        max-height: 100%;
                        width: auto;
                        height: auto;
                        object-fit: contain;
                        display: block;
                    }}
                    .icone {{
                        font-size: 3.5rem;
                        line-height: 1;
                    }}
                </style>
            </head>
            <body>
                <div class="wrap">
                    {conteudo}
                </div>
            </body>
            </html>
            """,
            height=204,
            scrolling=False,
        )

    @staticmethod
    def _html_preco(produto):
        detalhes = View.produto_preco_detalhes(produto)
        if detalhes["em_promocao"]:
            return f"""
                <div class="loja-preco-ref">
                    <p class="preco-cheio riscado">R$ {detalhes["preco_base"]:.2f}</p>
                    <div class="loja-preco-promo-linha">
                        <span class="preco-oferta">R$ {detalhes["preco_efetivo"]:.2f}</span>
                        <span class="loja-badge-off">-{detalhes["percentual"]:.0f}%</span>
                    </div>
                </div>
            """
        return (
            f'<div class="loja-preco-ref">'
            f'<p class="preco-cheio">R$ {detalhes["preco_base"]:.2f}</p>'
            f"</div>"
        )

    @staticmethod
    def _card_produto(produto, categorias, id_cliente, carrinho, key_prefix, favoritos_ids):
        cat_nome = categorias.get(produto.get_idCategoria(), "Sem categoria")
        icone = LojaClienteUI._icone_categoria(cat_nome)
        estoque_html = LojaClienteUI._html_estoque(produto.get_estoque())
        detalhes = View.produto_preco_detalhes(produto)
        preco_html = LojaClienteUI._html_preco(produto)
        nome = html.escape(produto.get_descricao())
        cat_html = html.escape(cat_nome)
        eh_favorito = produto.get_id() in favoritos_ids
        shell_cls = "loja-produto-shell"
        if eh_favorito:
            shell_cls += " loja-produto-favorito"

        st.markdown(f'<div class="{shell_cls}"></div>', unsafe_allow_html=True)

        LojaClienteUI._render_imagem_produto(produto.get_id(), icone)

        if st.button(
            "♥" if eh_favorito else "♡",
            key=f"{key_prefix}_fav_{produto.get_id()}",
            help="Remover dos favoritos" if eh_favorito else "Favoritar",
        ):
            try:
                if eh_favorito:
                    View.desfavoritar(id_cliente, produto.get_id())
                    st.session_state.produto_desfavoritado = True
                else:
                    View.favoritar(id_cliente, produto.get_id())
                    st.session_state.produto_favoritado = True
                st.rerun()
            except ValueError as e:
                st.error(str(e))

        st.markdown(
            f"""
            <div class="loja-produto-card">
                <div class="loja-produto-corpo">
                    <h3>{nome}</h3>
                    <div class="loja-cat-wrap"><span class="loja-cat-chip">{cat_html}</span></div>
                    {preco_html}
                    {estoque_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<span class="loja-comprar-anchor"></span>', unsafe_allow_html=True)
        if st.button(
            "COMPRAR",
            key=f"{key_prefix}_add_{produto.get_id()}",
            use_container_width=True,
            type="primary",
        ):
            try:
                View.adicionar(carrinho, produto.get_id(), 1)
                View.sincronizar(id_cliente, carrinho)
                st.session_state.produto_adicionado_carrinho = True
                st.rerun()
            except ValueError as e:
                st.error(str(e))

    @staticmethod
    def _pagina_produtos(id_cliente, carrinho):
        lista_categorias = View.categoria_listar()
        mapa = LojaClienteUI._mapa_categorias()
        favoritos_ids = LojaClienteUI._ids_favoritos(id_cliente)
        produtos = View.produtos_disponiveis_venda()

        st.markdown(
            """
            <div class="loja-produtos-topo">
                <span class="eyebrow">Catalogo</span>
                <h2>Produtos disponiveis</h2>
                <p>Escolha com carinho o melhor para o seu pet</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_filtro, col_contador = st.columns([4, 1], gap="medium")
        with col_filtro:
            st.markdown('<div class="loja-filtro-mark"></div>', unsafe_allow_html=True)
            if lista_categorias:
                opcoes = ["Todas as categorias"] + [
                    c.get_descricao() for c in lista_categorias
                ]
                escolha = st.selectbox(
                    "Filtrar por categoria",
                    opcoes,
                    label_visibility="visible",
                )
                if escolha != "Todas as categorias":
                    id_cat = next(
                        c.get_id() for c in lista_categorias if c.get_descricao() == escolha
                    )
                    produtos = [p for p in produtos if p.get_idCategoria() == id_cat]
            else:
                st.selectbox(
                    "Filtrar por categoria",
                    ["Todas as categorias"],
                    label_visibility="visible",
                    disabled=True,
                )
        with col_contador:
            n = len(produtos)
            texto = "1 produto" if n == 1 else f"{n} produtos"
            st.markdown(f'<p class="loja-contador">{texto}</p>', unsafe_allow_html=True)

        if not produtos:
            st.markdown(
                '<div class="loja-empty">Nenhum produto encontrado com esse filtro.</div>',
                unsafe_allow_html=True,
            )
            return

        for inicio in range(0, len(produtos), 3):
            fatia = produtos[inicio:inicio + 3]
            cols = st.columns(3, gap="medium")
            for idx, produto in enumerate(fatia):
                with cols[idx]:
                    LojaClienteUI._card_produto(
                        produto, mapa, id_cliente, carrinho, "prod", favoritos_ids
                    )
            for idx in range(len(fatia), 3):
                with cols[idx]:
                    st.markdown("&nbsp;", unsafe_allow_html=True)

    @staticmethod
    def main(usuario, carrinho):
        LojaClienteUI._processar_nav_query()
        LojaClienteUI._css()
        LojaClienteUI._header(usuario)

        id_cliente = usuario["id"]
        pagina = st.session_state.get("pagina_loja", "produtos")

        if pagina == "produtos":
            LojaClienteUI._pagina_produtos(id_cliente, carrinho)
        elif pagina == "favoritos":
            from Templates.favoritos_cliente import FavoritosClienteUI

            FavoritosClienteUI.main(id_cliente, carrinho)
        elif pagina == "carrinho":
            CarrinhoClienteUI.main(id_cliente, carrinho)
        elif pagina == "compras":
            ComprasClienteUI.main(id_cliente)
        elif pagina == "perfil":
            PerfilClienteUI.main(usuario)
