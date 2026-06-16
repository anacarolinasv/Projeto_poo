import streamlit as st
import streamlit.components.v1 as components
from views import View


class AdminDashboardUI:
    DASH_CSS = """
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: "Source Sans Pro", sans-serif;
            background: transparent;
            color: #444;
        }
        .dash-painel {
            background: #ffffff;
            border-radius: 18px;
            overflow: hidden;
            box-shadow: 0 8px 24px rgba(180, 90, 40, 0.1);
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
            color: #333;
            font-size: 1rem;
            font-weight: 800;
        }
        .dash-painel-topo p {
            margin-top: 0.15rem;
            color: #aaa;
            font-size: 0.78rem;
        }
        .dash-tabela-wrap { padding: 0.4rem 0.6rem 0.6rem; }
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
        .dash-tabela thead th:first-child { border-radius: 10px 0 0 0; }
        .dash-tabela thead th:last-child { border-radius: 0 10px 0 0; }
        .dash-tabela tbody td {
            padding: 0.75rem 0.85rem;
            border-bottom: 1px solid #f8f2ec;
            vertical-align: middle;
        }
        .dash-tabela tbody tr:last-child td { border-bottom: none; }
        .dash-tabela tbody tr:hover td { background: #fffcfa; }
        .col-total {
            text-align: right;
            color: #e85d30;
            font-weight: 800;
            white-space: nowrap;
        }
        .col-pedido { color: #e85d30; font-weight: 800; }
        .col-produto { font-weight: 600; color: #333; }
        .col-cliente { color: #666; }
        .col-cat { color: #999; font-size: 0.82rem; }
        .dash-badge-alerta {
            display: inline-block;
            background: #fff3ec;
            color: #e85d30;
            border: 1px solid #fde0cc;
            border-radius: 999px;
            padding: 0.2rem 0.65rem;
            font-size: 0.75rem;
            font-weight: 700;
        }
        .dash-vazio {
            text-align: center;
            padding: 2rem 1rem;
            color: #aaa;
            font-size: 0.9rem;
        }
        .dash-vazio-icon { font-size: 2rem; margin-bottom: 0.5rem; }
    </style>
    """

    @staticmethod
    def _render_html(html, altura=300):
        components.html(
            f"<!DOCTYPE html><html><head>{AdminDashboardUI.DASH_CSS}</head><body>{html}</body></html>",
            height=altura,
            scrolling=False,
        )

    @staticmethod
    def _painel_estoque(produtos, mapa_cats):
        estoque_baixo = [p for p in produtos if 0 < p.get_estoque() <= 3]

        if not estoque_baixo:
            corpo = """
            <div class="dash-vazio">
                <div class="dash-vazio-icon">✅</div>
                <p>Nenhum produto com estoque baixo.</p>
            </div>
            """
            altura = 200
        else:
            linhas = ""
            for p in estoque_baixo:
                cat = mapa_cats.get(p.get_idCategoria(), "—")
                linhas += (
                    f"<tr>"
                    f'<td class="col-produto">{p.get_descricao()}</td>'
                    f'<td class="col-cat">{cat}</td>'
                    f'<td><span class="dash-badge-alerta">{p.get_estoque()} un.</span></td>'
                    f"</tr>"
                )
            corpo = f"""
            <div class="dash-tabela-wrap">
                <table class="dash-tabela">
                    <thead>
                        <tr>
                            <th>Produto</th>
                            <th>Categoria</th>
                            <th>Estoque</th>
                        </tr>
                    </thead>
                    <tbody>{linhas}</tbody>
                </table>
            </div>
            """
            altura = 120 + len(estoque_baixo) * 52

        html = f"""
        <div class="dash-painel">
            <div class="dash-painel-topo">
                <span class="dash-painel-icone">📦</span>
                <div>
                    <h3>Estoque baixo</h3>
                    <p>Produtos com ate 3 unidades</p>
                </div>
            </div>
            {corpo}
        </div>
        """
        AdminDashboardUI._render_html(html, altura)

    @staticmethod
    def _painel_vendas(vendas, clientes):
        if not vendas:
            corpo = """
            <div class="dash-vazio">
                <div class="dash-vazio-icon">🛒</div>
                <p>Nenhuma venda registrada.</p>
            </div>
            """
            altura = 200
        else:
            mapa_clientes = {c.get_id(): c.get_nome() for c in clientes}
            linhas = ""
            for bloco in reversed(vendas[-5:]):
                venda = bloco["venda"]
                total = sum(i["total_item"] for i in bloco["itens"])
                nome = mapa_clientes.get(
                    venda.get_idCliente(),
                    f"Cliente #{venda.get_idCliente()}",
                )
                linhas += (
                    f"<tr>"
                    f'<td class="col-pedido">#{venda.get_id()}</td>'
                    f'<td class="col-cliente">{nome}</td>'
                    f'<td class="col-total">R$ {total:.2f}</td>'
                    f"</tr>"
                )
            corpo = f"""
            <div class="dash-tabela-wrap">
                <table class="dash-tabela">
                    <thead>
                        <tr>
                            <th>Pedido</th>
                            <th>Cliente</th>
                            <th style="text-align:right;">Total</th>
                        </tr>
                    </thead>
                    <tbody>{linhas}</tbody>
                </table>
            </div>
            """
            altura = 120 + min(len(vendas), 5) * 52

        html = f"""
        <div class="dash-painel">
            <div class="dash-painel-topo">
                <span class="dash-painel-icone">🧾</span>
                <div>
                    <h3>Ultimas vendas</h3>
                    <p>5 pedidos mais recentes</p>
                </div>
            </div>
            {corpo}
        </div>
        """
        AdminDashboardUI._render_html(html, altura)

    @staticmethod
    def main():
        clientes = View.cliente_listar()
        categorias = View.categoria_listar()
        produtos = View.produto_listar()
        vendas = View.listar_todas()
        mapa_cats = {c.get_id(): c.get_descricao() for c in categorias}

        total_vendas = sum(
            sum(i["total_item"] for i in bloco["itens"]) for bloco in vendas
        )

        st.markdown(
            """
            <div class="admin-hero">
                <h2>Painel administrativo</h2>
                <p>Visao geral do Pet Shop IF</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="admin-stat-grid">
                <div class="admin-stat">
                    <p class="label">Clientes</p>
                    <p class="valor">{len(clientes)}</p>
                </div>
                <div class="admin-stat">
                    <p class="label">Categorias</p>
                    <p class="valor">{len(categorias)}</p>
                </div>
                <div class="admin-stat">
                    <p class="label">Produtos</p>
                    <p class="valor">{len(produtos)}</p>
                </div>
                <div class="admin-stat">
                    <p class="label">Vendas</p>
                    <p class="valor">{len(vendas)}</p>
                </div>
                <div class="admin-stat">
                    <p class="label">Faturamento</p>
                    <p class="valor">R$ {total_vendas:.2f}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2, gap="medium")
        with col1:
            AdminDashboardUI._painel_estoque(produtos, mapa_cats)
        with col2:
            AdminDashboardUI._painel_vendas(vendas, clientes)
