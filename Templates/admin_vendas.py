import streamlit as st
from views import View
from Templates.admin_utils import AdminUtils


class AdminVendasUI:
    @staticmethod
    def _formatar_data(data):
        if hasattr(data, "strftime"):
            return data.strftime("%d/%m/%Y  %H:%M")
        return str(data)

    @staticmethod
    def _render_lista(registros, clientes):
        if not registros:
            AdminUtils.render_html(
                '<div class="admin-vazio">Nenhuma venda registrada.</div>',
                altura=120,
            )
            return

        total_geral = sum(
            sum(i["total_item"] for i in bloco["itens"]) for bloco in registros
        )

        st.markdown(
            f"""
            <div class="admin-stat-grid">
                <div class="admin-stat">
                    <p class="label">Total de pedidos</p>
                    <p class="valor">{len(registros)}</p>
                </div>
                <div class="admin-stat">
                    <p class="label">Faturamento total</p>
                    <p class="valor">R$ {total_geral:.2f}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for bloco in reversed(registros):
            venda = bloco["venda"]
            itens = bloco["itens"]
            total_pedido = sum(i["total_item"] for i in itens)
            data_fmt = AdminVendasUI._formatar_data(venda.get_data())
            nome_cliente = clientes.get(
                venda.get_idCliente(),
                f"Cliente #{venda.get_idCliente()}",
            )
            AdminUtils.render_venda(
                venda.get_id(),
                data_fmt,
                nome_cliente,
                total_pedido,
                itens,
            )

    @staticmethod
    def main():
        registros = View.listar_todas()
        clientes = {c.get_id(): c.get_nome() for c in View.cliente_listar()}

        tab_listar, = st.tabs(["Listar"])

        with tab_listar:
            AdminVendasUI._render_lista(registros, clientes)
