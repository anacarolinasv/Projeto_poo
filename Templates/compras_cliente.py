import streamlit as st
from views import View


class ComprasClienteUI:
    @staticmethod
    def _css():
        st.markdown(
            """
            <style>
                .compras-titulo {
                    color: #555;
                    font-size: 0.95rem;
                    font-weight: 700;
                    letter-spacing: 0.05em;
                    margin: 0 0 1.2rem 0;
                    text-transform: uppercase;
                }

                .compras-resumo-geral {
                    background: #ffffff;
                    border-radius: 18px;
                    padding: 1.2rem 1.4rem;
                    box-shadow: 0 8px 24px rgba(180, 90, 40, 0.1);
                    margin-bottom: 1.2rem;
                    display: flex;
                    gap: 2rem;
                }

                .compras-resumo-geral .stat-label {
                    color: #999;
                    font-size: 0.78rem;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 0.04em;
                    margin: 0 0 0.2rem 0;
                }

                .compras-resumo-geral .stat-valor {
                    color: #e85d30;
                    font-size: 1.35rem;
                    font-weight: 800;
                    margin: 0;
                }

                .compras-pedido {
                    background: #ffffff;
                    border-radius: 18px;
                    padding: 1.2rem 1.4rem;
                    box-shadow: 0 8px 24px rgba(180, 90, 40, 0.1);
                    margin-bottom: 1rem;
                }

                .compras-pedido-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: flex-start;
                    border-bottom: 1px solid #f3ebe3;
                    padding-bottom: 0.8rem;
                    margin-bottom: 0.8rem;
                }

                .compras-pedido-header h3 {
                    margin: 0;
                    color: #333;
                    font-size: 1.05rem;
                    font-weight: 800;
                }

                .compras-pedido-data {
                    color: #aaa;
                    font-size: 0.82rem;
                    margin: 0.25rem 0 0 0;
                }

                .compras-pedido-total {
                    color: #e85d30;
                    font-size: 1.2rem;
                    font-weight: 800;
                    margin: 0;
                    white-space: nowrap;
                }

                .compras-item {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 0.55rem 0;
                    border-bottom: 1px solid #faf5f0;
                    font-size: 0.9rem;
                    color: #555;
                }

                .compras-item:last-child {
                    border-bottom: none;
                }

                .compras-item-nome {
                    font-weight: 600;
                    color: #444;
                }

                .compras-item-detalhe {
                    color: #999;
                    font-size: 0.82rem;
                }

                .compras-item-preco {
                    color: #e85d30;
                    font-weight: 700;
                    white-space: nowrap;
                }

                .compras-vazio {
                    text-align: center;
                    color: #888;
                    padding: 3rem 1.5rem;
                    background: #ffffff;
                    border-radius: 20px;
                    box-shadow: 0 8px 24px rgba(180, 90, 40, 0.08);
                }

                .compras-vazio-icon {
                    font-size: 3rem;
                    margin-bottom: 0.8rem;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def _formatar_data(data):
        if hasattr(data, "strftime"):
            return data.strftime("%d/%m/%Y  %H:%M")
        return str(data)

    @staticmethod
    def _badge_entrega(info):
        """Monta o selo de status de entrega para um pedido."""
        if not info:
            return ""
        entrega = info["entrega"]
        entregador = info["entregador"]
        cores = {
            "PENDENTE": ("#fff3ec", "#e85d30", "#fde0cc"),
            "ALOCADA": ("#eef3ff", "#2f6fe8", "#cfe0ff"),
            "EM_TRANSPORTE": ("#fff7e6", "#d98a00", "#ffe2a8"),
            "ENTREGUE": ("#eafaef", "#1f9d54", "#bff0d0"),
        }
        fundo, cor, borda = cores.get(entrega.get_status(), ("#f2f2f2", "#666", "#ddd"))
        nome = f" · {entregador.get_nome()}" if entregador else ""
        return (
            f'<span style="display:inline-block;background:{fundo};color:{cor};'
            f"border:1px solid {borda};border-radius:999px;padding:0.2rem 0.7rem;"
            f'font-size:0.75rem;font-weight:700;white-space:nowrap;">'
            f"🚚 {entrega.rotulo_status()}{nome}</span>"
        )

    @staticmethod
    def main(id_cliente):
        ComprasClienteUI._css()
        st.markdown('<div id="compras-pagina">', unsafe_allow_html=True)
        st.markdown('<p class="compras-titulo">Minhas compras</p>', unsafe_allow_html=True)

        registros = View.listar_por_cliente(id_cliente)
        acompanhamento = View.entrega_acompanhar_cliente(id_cliente)

        if not registros:
            st.markdown(
                """
                <div class="compras-vazio">
                    <div class="compras-vazio-icon">📦</div>
                    <p>Você ainda não realizou nenhuma compra.</p>
                    <p style="font-size:0.9rem;margin-top:0.3rem;">
                        Explore os produtos e faça seu primeiro pedido!
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("← Ir para produtos", key="compras_voltar_vazio"):
                st.session_state.pagina_loja = "produtos"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            return

        total_gasto = sum(
            sum(i["total_item"] for i in bloco["itens"]) for bloco in registros
        )
        st.markdown(
            f"""
            <div class="compras-resumo-geral">
                <div>
                    <p class="stat-label">Pedidos realizados</p>
                    <p class="stat-valor">{len(registros)}</p>
                </div>
                <div>
                    <p class="stat-label">Total gasto</p>
                    <p class="stat-valor">R$ {total_gasto:.2f}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for bloco in reversed(registros):
            venda = bloco["venda"]
            itens = bloco["itens"]
            total_pedido = sum(i["total_item"] for i in itens)
            data_fmt = ComprasClienteUI._formatar_data(venda.get_data())
            badge_html = ComprasClienteUI._badge_entrega(acompanhamento.get(venda.get_id()))

            itens_html = ""
            for item in itens:
                itens_html += f"""
                <div class="compras-item">
                    <div>
                        <div class="compras-item-nome">{item["descricao"]}</div>
                        <div class="compras-item-detalhe">
                            {item["quantidade"]}x R$ {item["preco_unitario"]:.2f}
                        </div>
                    </div>
                    <div class="compras-item-preco">R$ {item["total_item"]:.2f}</div>
                </div>
                """

            st.markdown(
                f"""
                <div class="compras-pedido">
                    <div class="compras-pedido-header">
                        <div>
                            <h3>Pedido #{venda.get_id()}</h3>
                            <p class="compras-pedido-data">{data_fmt}</p>
                            <p style="margin:0.5rem 0 0 0;">{badge_html}</p>
                        </div>
                        <p class="compras-pedido-total">R$ {total_pedido:.2f}</p>
                    </div>
                    {itens_html}
                </div>
                """,
                unsafe_allow_html=True,
            )

        if st.button("← Continuar comprando", key="compras_voltar"):
            st.session_state.pagina_loja = "produtos"
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
