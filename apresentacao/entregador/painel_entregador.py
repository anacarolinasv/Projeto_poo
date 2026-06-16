import streamlit as st
from views import View


class PainelEntregadorUI:
    """Painel do entregador: ver pedidos alocados e avançar o status da entrega."""

    CORES_STATUS = {
        "PENDENTE": ("#fff3ec", "#e85d30", "#fde0cc", "⏳"),
        "ALOCADA": ("#eef3ff", "#2f6fe8", "#cfe0ff", "📋"),
        "EM_TRANSPORTE": ("#fff7e6", "#d98a00", "#ffe2a8", "🚚"),
        "ENTREGUE": ("#eafaef", "#1f9d54", "#bff0d0", "✅"),
    }

    PROXIMA_ACAO = {
        "ALOCADA": "🚚 Sair para entrega",
        "EM_TRANSPORTE": "✅ Confirmar entrega",
    }

    @staticmethod
    def _css():
        st.markdown(
            """
            <style>
                .stApp {
                    background: linear-gradient(180deg, #fdebd0 0%, #f6d5b8 100%);
                }
                #MainMenu, header[data-testid="stHeader"], footer { visibility: hidden; }
                .block-container { max-width: 880px; padding-top: 1.6rem; }

                .ent-hero {
                    background: linear-gradient(135deg, #f07043 0%, #d94e1a 100%);
                    color: #fff;
                    border-radius: 20px;
                    padding: 1.5rem 1.7rem;
                    box-shadow: 0 12px 30px rgba(160, 60, 10, 0.28);
                }
                .ent-hero h2 { margin: 0; font-size: 1.45rem; font-weight: 800; }
                .ent-hero p { margin: 0.35rem 0 0 0; opacity: 0.94; font-size: 0.93rem; }

                .ent-secao {
                    color: #8a4a25;
                    font-size: 0.85rem;
                    font-weight: 800;
                    letter-spacing: 0.06em;
                    text-transform: uppercase;
                    margin: 1.4rem 0 0.7rem 0;
                }

                div[data-testid="stVerticalBlockBorderWrapper"]:has(.ent-card-mark) {
                    background: #ffffff;
                    border: 1px solid #f0e6dc !important;
                    border-radius: 16px !important;
                    box-shadow: 0 8px 22px rgba(180, 90, 40, 0.1);
                    margin-bottom: 0.9rem;
                    padding: 0.4rem 1.3rem 0.6rem;
                }
                div[data-testid="stHorizontalBlock"]:has(.ent-card-mark) {
                    align-items: center !important;
                }
                .ent-card-mark { display: none; }

                .ent-pedido { margin: 0; font-weight: 800; color: #333; font-size: 1.08rem; }
                .ent-meta { margin: 0.22rem 0; color: #777; font-size: 0.88rem; }
                .ent-meta b { color: #555; }
                .ent-badge {
                    display: inline-block; border-radius: 999px;
                    padding: 0.22rem 0.75rem; font-size: 0.78rem; font-weight: 700;
                }
                .ent-concluida {
                    background: #ffffff; border: 1px solid #f0e6dc;
                    border-radius: 12px; padding: 0.7rem 1rem; margin-bottom: 0.5rem;
                    color: #555; font-size: 0.9rem;
                    display: flex; justify-content: space-between; align-items: center;
                }
                .ent-vazio {
                    background: #ffffff; border-radius: 16px; padding: 2rem 1.5rem;
                    text-align: center; color: #999; font-size: 0.95rem;
                    box-shadow: 0 8px 22px rgba(180, 90, 40, 0.08);
                }

                .stButton > button[kind="primary"] {
                    background: linear-gradient(135deg, #f07043 0%, #e85d30 100%) !important;
                    color: #fff !important; border: none !important;
                    border-radius: 999px !important; font-weight: 700 !important;
                }
                .stButton > button[kind="secondary"] {
                    border-radius: 999px !important; border: 1px solid #d94e1a !important;
                    color: #d94e1a !important; background: #fff !important; font-weight: 600 !important;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def _badge(entrega):
        fundo, cor, borda, icone = PainelEntregadorUI.CORES_STATUS.get(
            entrega.get_status(), ("#f2f2f2", "#666", "#ddd", "•")
        )
        return (
            f'<span class="ent-badge" style="background:{fundo};color:{cor};'
            f'border:1px solid {borda};">{icone} {entrega.rotulo_status()}</span>'
        )

    @staticmethod
    def _sair():
        st.session_state.usuario = None
        st.session_state.modo_tela = "login"
        st.rerun()

    @staticmethod
    def main(usuario):
        PainelEntregadorUI._css()
        id_entregador = usuario["id"]

        col_titulo, col_sair = st.columns([5, 1], gap="small")
        with col_titulo:
            st.markdown(
                f"""
                <div class="ent-hero">
                    <h2>🚚 Olá, {usuario['nome']}</h2>
                    <p>Acompanhe e atualize o status das suas entregas.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_sair:
            st.write("")
            st.write("")
            if st.button("Sair", type="secondary", use_container_width=True):
                PainelEntregadorUI._sair()

        pedidos = View.entrega_listar_para_entregador(id_entregador)
        if not pedidos:
            st.markdown(
                '<div class="ent-vazio">📭<br>Você ainda não tem entregas alocadas.'
                "<br>Aguarde o administrador alocar pedidos para você.</div>",
                unsafe_allow_html=True,
            )
            return

        pendentes = [p for p in pedidos if p["entrega"].get_status() != "ENTREGUE"]
        concluidas = [p for p in pedidos if p["entrega"].get_status() == "ENTREGUE"]

        st.markdown('<p class="ent-secao">Entregas em andamento</p>', unsafe_allow_html=True)
        if not pendentes:
            st.markdown(
                '<div class="ent-vazio">Tudo em dia! Nenhuma entrega pendente.</div>',
                unsafe_allow_html=True,
            )
        for pedido in pendentes:
            venda = pedido["venda"]
            entrega = pedido["entrega"]
            with st.container(border=True):
                st.markdown('<span class="ent-card-mark"></span>', unsafe_allow_html=True)
                col_info, col_acao = st.columns([3, 2], gap="medium")
                with col_info:
                    st.markdown(
                        f"""
                        <p class="ent-pedido">Pedido #{venda.get_id()}</p>
                        <p class="ent-meta">
                            <b>Cliente:</b> {pedido['cliente']}
                            &nbsp;·&nbsp; <b>Total:</b> R$ {venda.get_total():.2f}
                        </p>
                        <p style="margin:0.45rem 0 0.2rem 0;">{PainelEntregadorUI._badge(entrega)}</p>
                        """,
                        unsafe_allow_html=True,
                    )
                with col_acao:
                    acao = PainelEntregadorUI.PROXIMA_ACAO.get(entrega.get_status())
                    if acao:
                        if st.button(
                            acao,
                            key=f"avancar_{entrega.get_id()}",
                            type="primary",
                            use_container_width=True,
                        ):
                            try:
                                View.entrega_avancar_status(entrega.get_id(), id_entregador)
                                st.rerun()
                            except ValueError as e:
                                st.error(str(e))

        if concluidas:
            st.markdown('<p class="ent-secao">Entregas concluídas</p>', unsafe_allow_html=True)
            for pedido in concluidas:
                venda = pedido["venda"]
                st.markdown(
                    f"""
                    <div class="ent-concluida">
                        <span>Pedido <b>#{venda.get_id()}</b> · {pedido['cliente']}
                        · R$ {venda.get_total():.2f}</span>
                        <span style="color:#1f9d54;font-weight:700;">Entregue ✅</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
