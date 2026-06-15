import html
import streamlit.components.v1 as components


class AdminUtils:
    TABELA_CSS = """
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: "Source Sans Pro", sans-serif;
            background: transparent;
            color: #444;
        }
        .admin-painel {
            background: #ffffff;
            border-radius: 18px;
            overflow: hidden;
            box-shadow: 0 8px 24px rgba(180, 90, 40, 0.1);
        }
        .admin-painel-titulo {
            color: #555;
            font-size: 0.82rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            padding: 1rem 1.2rem 0.75rem;
            border-bottom: 1px solid #f5ebe3;
            background: linear-gradient(135deg, #fff8f3 0%, #ffffff 100%);
        }
        .admin-tabela-wrap { padding: 0.35rem 0.5rem 0.5rem; }
        .admin-tabela {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            font-size: 0.88rem;
        }
        .admin-tabela thead th {
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
        .admin-tabela thead th:first-child { border-radius: 10px 0 0 0; }
        .admin-tabela thead th:last-child { border-radius: 0 10px 0 0; }
        .admin-tabela tbody td {
            padding: 0.75rem 0.85rem;
            border-bottom: 1px solid #f8f2ec;
            vertical-align: middle;
            color: #444;
        }
        .admin-tabela tbody tr:last-child td { border-bottom: none; }
        .admin-tabela tbody tr:hover td { background: #fffcfa; }
        .admin-badge {
            display: inline-block;
            background: #fff3ec;
            color: #e85d30;
            border-radius: 999px;
            padding: 0.15rem 0.55rem;
            font-size: 0.72rem;
            font-weight: 700;
        }
        .admin-vazio {
            text-align: center;
            color: #888;
            padding: 2.2rem 1rem;
            font-size: 0.9rem;
        }
        .venda-card {
            background: #ffffff;
            border-radius: 18px;
            box-shadow: 0 8px 24px rgba(180, 90, 40, 0.1);
            margin-bottom: 1rem;
            overflow: hidden;
        }
        .venda-topo {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            padding: 1.1rem 1.2rem 0.85rem;
            border-bottom: 1px solid #f3ebe3;
            background: linear-gradient(135deg, #fff8f3 0%, #ffffff 100%);
        }
        .venda-topo h3 {
            color: #333;
            font-size: 1.05rem;
            font-weight: 800;
        }
        .venda-topo .data {
            margin-top: 0.25rem;
            color: #aaa;
            font-size: 0.82rem;
        }
        .venda-topo .cliente {
            margin-top: 0.35rem;
            color: #666;
            font-size: 0.88rem;
        }
        .venda-total {
            color: #e85d30;
            font-size: 1.2rem;
            font-weight: 800;
            white-space: nowrap;
        }
        .col-preco { color: #e85d30; font-weight: 800; text-align: right; }
        .col-id { color: #e85d30; font-weight: 800; }
    </style>
    """

    @staticmethod
    def validar_obrigatorios(**campos):
        vazios = [nome for nome, valor in campos.items() if not str(valor or "").strip()]
        if vazios:
            labels = {
                "nome": "Nome",
                "email": "E-mail",
                "fone": "Telefone",
                "senha": "Senha",
                "descricao": "Descricao",
            }
            faltando = ", ".join(labels.get(c, c) for c in vazios)
            raise ValueError(f"Preencha os campos obrigatorios: {faltando}.")

    @staticmethod
    def _esc(texto):
        return html.escape(str(texto))

    @staticmethod
    def render_html(conteudo, altura=200, scrolling=False):
        components.html(
            f"<!DOCTYPE html><html><head>{AdminUtils.TABELA_CSS}</head>"
            f"<body>{conteudo}</body></html>",
            height=altura,
            scrolling=scrolling,
        )

    @staticmethod
    def render_tabela(titulo, colunas, linhas, permitir_html=False):
        if not linhas:
            corpo = '<div class="admin-vazio">Nenhum registro encontrado.</div>'
            altura = 160
        else:
            ths = "".join(f"<th>{AdminUtils._esc(c)}</th>" for c in colunas)
            trs = ""
            for linha in linhas:
                tds = ""
                for celula in linha:
                    if permitir_html:
                        tds += f"<td>{celula}</td>"
                    else:
                        tds += f"<td>{AdminUtils._esc(celula)}</td>"
                trs += f"<tr>{tds}</tr>"
            corpo = f"""
            <div class="admin-tabela-wrap">
                <table class="admin-tabela">
                    <thead><tr>{ths}</tr></thead>
                    <tbody>{trs}</tbody>
                </table>
            </div>
            """
            altura = 100 + len(linhas) * 48

        html_painel = f"""
        <div class="admin-painel">
            <p class="admin-painel-titulo">{AdminUtils._esc(titulo)}</p>
            {corpo}
        </div>
        """
        AdminUtils.render_html(html_painel, altura=altura)

    @staticmethod
    def render_venda(pedido_id, data_fmt, nome_cliente, total_pedido, itens):
        itens_html = ""
        for item in itens:
            itens_html += (
                f"<tr>"
                f"<td>{AdminUtils._esc(item['descricao'])}</td>"
                f"<td>{item['quantidade']}x R$ {item['preco_unitario']:.2f}</td>"
                f'<td class="col-preco">R$ {item["total_item"]:.2f}</td>'
                f"</tr>"
            )
        altura = 130 + len(itens) * 46
        html_card = f"""
        <div class="venda-card">
            <div class="venda-topo">
                <div>
                    <h3>Pedido #{pedido_id}</h3>
                    <p class="data">{AdminUtils._esc(data_fmt)}</p>
                    <p class="cliente">Cliente: <strong>{AdminUtils._esc(nome_cliente)}</strong></p>
                </div>
                <p class="venda-total">R$ {total_pedido:.2f}</p>
            </div>
            <div class="admin-tabela-wrap">
                <table class="admin-tabela">
                    <thead>
                        <tr><th>Produto</th><th>Detalhe</th><th style="text-align:right;">Subtotal</th></tr>
                    </thead>
                    <tbody>{itens_html}</tbody>
                </table>
            </div>
        </div>
        """
        AdminUtils.render_html(html_card, altura=altura)
