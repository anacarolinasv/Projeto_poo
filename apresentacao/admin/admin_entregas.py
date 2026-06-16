import streamlit as st
from views import View


class AdminEntregasUI:
    """Caso de uso do Admin: alocar entregadores e acompanhar as entregas."""

    CORES_STATUS = {
        "PENDENTE": ("#fff3ec", "#e85d30", "#fde0cc", "⏳"),
        "ALOCADA": ("#eef3ff", "#2f6fe8", "#cfe0ff", "📋"),
        "EM_TRANSPORTE": ("#fff7e6", "#d98a00", "#ffe2a8", "🚚"),
        "ENTREGUE": ("#eafaef", "#1f9d54", "#bff0d0", "✅"),
    }

    @staticmethod
    def _css():
        st.markdown(
            """
            <style>
                div[data-testid="stVerticalBlockBorderWrapper"]:has(.entrega-card-mark) {
                    background: #ffffff;
                    border: 1px solid #f0e6dc !important;
                    border-radius: 16px !important;
                    box-shadow: 0 8px 22px rgba(180, 90, 40, 0.08);
                    margin-bottom: 0.9rem;
                    padding: 0.3rem 1.3rem 0.5rem;
                }
                div[data-testid="stHorizontalBlock"]:has(.entrega-card-mark) {
                    align-items: center !important;
                }
                .entrega-card-mark { display: none; }

                .entrega-pedido { margin: 0; font-size: 1.1rem; font-weight: 800; color: #333; }
                .entrega-meta { margin: 0.25rem 0; color: #777; font-size: 0.88rem; }
                .entrega-meta b { color: #555; font-weight: 700; }
                .entrega-badge {
                    display: inline-block; border-radius: 999px;
                    padding: 0.22rem 0.75rem; font-size: 0.78rem; font-weight: 700;
                    white-space: nowrap;
                }
                div[data-testid="stVerticalBlockBorderWrapper"]:has(.entrega-card-mark)
                    div[data-testid="stSelectbox"] > div {
                    border-radius: 10px !important;
                    border-color: #f0e6dc !important;
                    background: #faf7f4 !important;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def _badge(entrega):
        fundo, cor, borda, icone = AdminEntregasUI.CORES_STATUS.get(
            entrega.get_status(), ("#f2f2f2", "#666", "#ddd", "•")
        )
        return (
            f'<span class="entrega-badge" style="background:{fundo};color:{cor};'
            f'border:1px solid {borda};">{icone} {entrega.rotulo_status()}</span>'
        )

    @staticmethod
    def _resumo(pedidos):
        contagem = {"PENDENTE": 0, "ALOCADA": 0, "EM_TRANSPORTE": 0, "ENTREGUE": 0}
        for pedido in pedidos:
            contagem[pedido["entrega"].get_status()] += 1
        cards = [
            ("Aguardando", contagem["PENDENTE"], "#e85d30"),
            ("Alocadas", contagem["ALOCADA"], "#2f6fe8"),
            ("Em transporte", contagem["EM_TRANSPORTE"], "#d98a00"),
            ("Entregues", contagem["ENTREGUE"], "#1f9d54"),
        ]
        blocos = "".join(
            f'<div class="admin-stat"><p class="label">{rotulo}</p>'
            f'<p class="valor" style="color:{cor};">{valor}</p></div>'
            for rotulo, valor, cor in cards
        )
        st.markdown(
            f'<div class="admin-stat-grid">{blocos}</div>', unsafe_allow_html=True
        )

    @staticmethod
    def main():
        AdminEntregasUI._css()
        st.markdown(
            """
            <div class="admin-hero">
                <h2>🚚 Controle de entregas</h2>
                <p>Aloque um entregador para cada pedido e acompanhe o status das entregas.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        entregadores = View.entregador_listar()
        pedidos = View.entrega_listar_pedidos()

        if not entregadores:
            st.info(
                "Nenhum entregador cadastrado ainda. Os entregadores se cadastram "
                "pela tela de login, na opção **Sou entregador**."
            )

        if not pedidos:
            st.markdown(
                '<div class="admin-empty">📭<br>Nenhum pedido para entregar no momento.</div>',
                unsafe_allow_html=True,
            )
            return

        AdminEntregasUI._resumo(pedidos)

        opcoes = {e.get_id(): f"{e.get_nome()} (#{e.get_id()})" for e in entregadores}

        for pedido in pedidos:
            venda = pedido["venda"]
            entrega = pedido["entrega"]
            entregador = pedido["entregador"]

            with st.container(border=True):
                st.markdown(
                    '<span class="entrega-card-mark"></span>', unsafe_allow_html=True
                )
                col_info, col_acao = st.columns([3, 2], gap="medium")

                with col_info:
                    atual = (
                        entregador.get_nome()
                        if entregador
                        else "Sem entregador alocado"
                    )
                    st.markdown(
                        f"""
                        <p class="entrega-pedido">Pedido #{venda.get_id()}</p>
                        <p class="entrega-meta">
                            <b>Cliente:</b> {pedido['cliente']}
                            &nbsp;·&nbsp; <b>Total:</b> R$ {venda.get_total():.2f}
                        </p>
                        <p class="entrega-meta"><b>Entregador:</b> {atual}</p>
                        <p style="margin:0.5rem 0 0.2rem 0;">{AdminEntregasUI._badge(entrega)}</p>
                        """,
                        unsafe_allow_html=True,
                    )

                with col_acao:
                    if entrega.get_status() == "ENTREGUE":
                        st.success("Pedido entregue.")
                    elif not entregadores:
                        st.caption("Cadastre um entregador para alocar.")
                    else:
                        ids = list(opcoes.keys())
                        indice = (
                            ids.index(entrega.get_idEntregador())
                            if entrega.tem_entregador()
                            else 0
                        )
                        escolhido = st.selectbox(
                            "Entregador",
                            ids,
                            index=indice,
                            format_func=lambda i: opcoes[i],
                            key=f"sel_entregador_{venda.get_id()}",
                        )
                        rotulo = (
                            "Realocar" if entrega.tem_entregador() else "Alocar entregador"
                        )
                        if st.button(
                            rotulo,
                            key=f"btn_alocar_{venda.get_id()}",
                            type="primary",
                            use_container_width=True,
                        ):
                            try:
                                View.entrega_alocar(venda.get_id(), int(escolhido))
                                st.session_state.admin_sucesso = (
                                    f"Entregador alocado ao pedido #{venda.get_id()}."
                                )
                                st.rerun()
                            except ValueError as e:
                                st.error(str(e))
