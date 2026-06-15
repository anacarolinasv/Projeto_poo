import streamlit as st
from views import View


class CarrinhoClienteUI:
    @staticmethod
    def _css():
        st.markdown(
            """
            <style>
                .carrinho-titulo {
                    color: #555;
                    font-size: 0.95rem;
                    font-weight: 700;
                    letter-spacing: 0.05em;
                    margin: 0 0 1.2rem 0;
                    text-transform: uppercase;
                }

                .carrinho-vazio-card {
                    background: #ffffff !important;
                    border: 1px solid #f0e6dc;
                    border-radius: 20px;
                    box-shadow: 0 12px 32px rgba(180, 90, 40, 0.12);
                    text-align: center;
                    padding: 2.5rem 1.75rem 4.5rem;
                    margin: 0;
                }

                .carrinho-vazio-inner {
                    text-align: center;
                    padding: 0;
                    background: transparent;
                }

                .carrinho-vazio-eyebrow {
                    display: inline-block;
                    background: #fff3ec;
                    color: #e85d30;
                    border-radius: 999px;
                    padding: 0.22rem 0.7rem;
                    font-size: 0.72rem;
                    font-weight: 700;
                    letter-spacing: 0.04em;
                    text-transform: uppercase;
                    margin-bottom: 1.25rem;
                }

                .carrinho-vazio-icon {
                    width: 88px;
                    height: 88px;
                    margin: 0 auto 1.25rem;
                    border-radius: 50%;
                    background: #fff3ec;
                    border: 1px solid #ffd8c8;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 2.3rem;
                }

                .carrinho-vazio-inner h2 {
                    margin: 0 0 0.5rem 0;
                    color: #333;
                    font-size: 1.35rem;
                    font-weight: 800;
                }

                .carrinho-vazio-inner p {
                    margin: 0;
                    color: #888;
                    font-size: 0.95rem;
                    line-height: 1.55;
                }

                div[data-testid="column"]:has(.carrinho-vazio-card) {
                    background: transparent !important;
                }

                div[data-testid="column"]:has(.carrinho-vazio-card) div[data-testid="element-container"]:has(.carrinho-vazio-card) {
                    padding: 0 !important;
                    margin: 0 !important;
                }

                div[data-testid="column"]:has(.carrinho-vazio-card) div[data-testid="stHorizontalBlock"]:has(.stButton) {
                    margin: -3.25rem 0 2rem 0 !important;
                    width: 100% !important;
                }

                div[data-testid="column"]:has(.carrinho-vazio-card) div[data-testid="stHorizontalBlock"]:has(.stButton) .stButton {
                    display: flex !important;
                    justify-content: center !important;
                    width: 100% !important;
                }

                div[data-testid="column"]:has(.carrinho-vazio-card) div[data-testid="stHorizontalBlock"]:has(.stButton) .stButton > button {
                    width: auto !important;
                    min-width: 220px;
                    max-width: 280px;
                    margin: 0 auto !important;
                    border-radius: 999px !important;
                    border: 1px solid #f07043 !important;
                    color: #f07043 !important;
                    background: #ffffff !important;
                    font-weight: 700 !important;
                    padding: 0.7rem 1.8rem !important;
                }

                div[data-testid="column"]:has(.carrinho-vazio-card) div[data-testid="stHorizontalBlock"]:has(.stButton) .stButton > button:hover {
                    background: #fff3ec !important;
                    border-color: #e85d30 !important;
                    color: #e85d30 !important;
                }

                div[data-testid="stHorizontalBlock"]:has(.carrinho-vazio-card) {
                    margin-top: 2.5rem;
                    margin-bottom: 2rem;
                }

                .carrinho-item {
                    background: #ffffff;
                    border-radius: 16px;
                    padding: 1rem 1.2rem;
                    box-shadow: 0 6px 20px rgba(180, 90, 40, 0.1);
                    margin-bottom: 0.75rem;
                }

                .carrinho-item h3 {
                    margin: 0 0 0.35rem 0;
                    color: #333;
                    font-size: 1.05rem;
                    font-weight: 800;
                }

                .carrinho-item .unitario {
                    color: #999;
                    font-size: 0.85rem;
                    margin: 0;
                }

                .carrinho-item .preco-original {
                    color: #bbb;
                    font-size: 0.8rem;
                    text-decoration: line-through;
                    margin: 0 0 0.1rem 0;
                }

                .carrinho-item .badge-promo {
                    display: inline-block;
                    background: #fff3ec;
                    color: #e85d30;
                    border-radius: 999px;
                    padding: 0.12rem 0.5rem;
                    font-size: 0.7rem;
                    font-weight: 700;
                    margin-left: 0.35rem;
                }

                .carrinho-item .subtotal {
                    color: #e85d30;
                    font-weight: 800;
                    font-size: 1.1rem;
                    margin: 0.35rem 0 0 0;
                }

                .carrinho-resumo {
                    background: #ffffff;
                    border-radius: 20px;
                    padding: 1.4rem 1.5rem;
                    box-shadow: 0 10px 28px rgba(180, 90, 40, 0.12);
                    margin-top: 0.5rem;
                }

                .carrinho-resumo-label {
                    color: #777;
                    font-size: 0.82rem;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    margin: 0 0 0.4rem 0;
                }

                .carrinho-resumo-total {
                    color: #e85d30;
                    font-size: 1.75rem;
                    font-weight: 800;
                    margin: 0 0 1rem 0;
                }

                .carrinho-resumo-itens {
                    color: #999;
                    font-size: 0.88rem;
                    margin: 0 0 1rem 0;
                }

                .carrinho-link {
                    display: inline-block;
                    margin-top: 1rem;
                    color: #e85d30;
                    font-weight: 700;
                    text-decoration: none;
                }

                .carrinho-link:hover {
                    text-decoration: underline;
                }

                #carrinho-pagina div[data-testid="stNumberInput"] input {
                    border-radius: 10px !important;
                    border: 1px solid #ecd9c8 !important;
                    text-align: center !important;
                    font-weight: 700 !important;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def _atualizar_quantidade(carrinho, id_cliente, id_produto, nova_qtd):
        View.remover_item(carrinho, id_produto)
        View.adicionar(carrinho, id_produto, int(nova_qtd))
        View.sincronizar(id_cliente, carrinho)

    @staticmethod
    def main(id_cliente, carrinho):
        CarrinhoClienteUI._css()
        st.markdown('<div id="carrinho-pagina">', unsafe_allow_html=True)

        linhas, total = View.montar_resumo(carrinho)
        View.sincronizar(id_cliente, carrinho)

        if not linhas:
            _, col_card, _ = st.columns([1, 1.4, 1])
            with col_card:
                st.markdown(
                    """
                    <div class="carrinho-vazio-card">
                        <div class="carrinho-vazio-inner">
                            <span class="carrinho-vazio-eyebrow">Seu carrinho</span>
                            <div class="carrinho-vazio-icon">🛒</div>
                            <h2>Nenhum item por aqui</h2>
                            <p>Explore nossos produtos e encontre o ideal para o seu pet.</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                _, btn_col, _ = st.columns([0.6, 2, 0.6])
                with btn_col:
                    if st.button(
                        "Continuar comprando",
                        key="carr_voltar_vazio",
                        use_container_width=True,
                        type="secondary",
                    ):
                        st.session_state.pagina_loja = "produtos"
                        st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            return

        st.markdown('<p class="carrinho-titulo">Seu carrinho</p>', unsafe_allow_html=True)

        col_itens, col_resumo = st.columns([2.2, 1], gap="large")

        with col_itens:
            for linha in linhas:
                col_info, col_qtd, col_del = st.columns([3.5, 1.2, 0.5])
                with col_info:
                    if linha.get("em_promocao"):
                        preco_html = (
                            f'<p class="preco-original">R$ {linha["preco_base"]:.2f}</p>'
                            f'<p class="unitario">R$ {linha["preco_unitario"]:.2f} cada'
                            f'<span class="badge-promo">-{linha["percentual"]:.0f}%</span></p>'
                        )
                    else:
                        preco_html = (
                            f'<p class="unitario">R$ {linha["preco_unitario"]:.2f} cada</p>'
                        )
                    st.markdown(
                        f"""
                        <div class="carrinho-item">
                            <h3>{linha["descricao"]}</h3>
                            {preco_html}
                            <p class="subtotal">R$ {linha["total_item"]:.2f}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with col_qtd:
                    st.markdown("<p style='font-size:0.75rem;color:#999;margin:0 0 0.3rem;'>Qtd</p>",
                                unsafe_allow_html=True)
                    nova_qtd = st.number_input(
                        "Qtd",
                        min_value=1,
                        value=int(linha["quantidade"]),
                        key=f"carr_qtd_{linha['id']}",
                        label_visibility="collapsed",
                    )
                    if nova_qtd != linha["quantidade"]:
                        try:
                            CarrinhoClienteUI._atualizar_quantidade(
                                carrinho, id_cliente, linha["id"], nova_qtd
                            )
                            st.rerun()
                        except ValueError as e:
                            st.error(str(e))
                with col_del:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("✕", key=f"carr_del_{linha['id']}", help="Remover"):
                        try:
                            View.remover_item(carrinho, linha["id"])
                            View.sincronizar(id_cliente, carrinho)
                            st.rerun()
                        except ValueError as e:
                            st.error(str(e))

        with col_resumo:
            qtd_itens = sum(l["quantidade"] for l in linhas)
            st.markdown(
                f"""
                <div class="carrinho-resumo">
                    <p class="carrinho-resumo-label">Resumo do pedido</p>
                    <p class="carrinho-resumo-itens">{qtd_itens} item(ns)</p>
                    <p class="carrinho-resumo-total">R$ {total:.2f}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button("Finalizar compra", use_container_width=True, type="primary", key="carr_finalizar"):
                try:
                    View.finalizar_compra(id_cliente, carrinho)
                    st.success("Compra realizada com sucesso!")
                    st.balloons()
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

            if st.button("Esvaziar carrinho", use_container_width=True, type="secondary", key="carr_esvaziar"):
                View.esvaziar(carrinho)
                View.sincronizar(id_cliente, carrinho)
                st.rerun()

            if st.button("← Continuar comprando", key="carr_voltar"):
                st.session_state.pagina_loja = "produtos"
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
