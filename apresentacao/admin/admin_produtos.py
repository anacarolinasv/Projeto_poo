import base64
import html

import streamlit as st
from views import View
from apresentacao.comum.admin_utils import AdminUtils


FOTO_TIPOS = ["jpg", "jpeg", "png", "webp"]


class AdminProdutosUI:
    @staticmethod
    def _mapa_categorias():
        return {c.get_id(): c.get_descricao() for c in View.categoria_listar()}

    @staticmethod
    def _render_lista(produtos, categorias):
        col_filtro, col_busca, col_contador = st.columns([2, 2, 1])
        with col_filtro:
            nomes_cats = sorted(set(categorias.values()))
            opcoes_cat = ["Todas as categorias"] + nomes_cats
            cat_escolha = st.selectbox(
                "Filtrar por categoria",
                opcoes_cat,
                key="admin_prod_list_cat",
            )
        with col_busca:
            busca = st.text_input(
                "Buscar por descrição",
                placeholder="Digite parte do nome...",
                key="admin_prod_list_busca",
            ).strip().lower()

        filtrados = produtos
        if cat_escolha != "Todas as categorias":
            id_cat = next(
                (cid for cid, nome in categorias.items() if nome == cat_escolha),
                None,
            )
            if id_cat is not None:
                filtrados = [p for p in filtrados if p.get_idCategoria() == id_cat]
        if busca:
            filtrados = [p for p in filtrados if busca in p.get_descricao().lower()]

        filtrados = sorted(filtrados, key=lambda p: p.get_descricao().lower())

        with col_contador:
            n = len(filtrados)
            texto = "1 produto" if n == 1 else f"{n} produtos"
            st.markdown(
                f'<p style="margin-top:1.85rem;color:#888;font-size:0.88rem;text-align:right;">{texto}</p>',
                unsafe_allow_html=True,
            )

        linhas = []
        for p in filtrados:
            cat = categorias.get(p.get_idCategoria(), "—")
            linhas.append((
                f'<span class="col-id">#{p.get_id()}</span>',
                p.get_descricao(),
                cat,
                f"R$ {p.get_preco():.2f}",
                f'<span class="admin-badge">{p.get_estoque()} un.</span>',
            ))
        AdminUtils.render_tabela(
            "Listar produtos",
            ["ID", "Descrição", "Categoria", "Preco", "Estoque"],
            linhas,
            permitir_html=True,
        )

    @staticmethod
    def _selecionar_produto(produtos, categorias, key_prefix):
        if not produtos:
            return None

        por_categoria = {}
        for p in produtos:
            cat_nome = categorias.get(p.get_idCategoria(), "Sem categoria")
            por_categoria.setdefault(cat_nome, []).append(p)

        cat_opcoes = sorted(por_categoria.keys())

        col_cat, col_prod = st.columns([1, 2])
        with col_cat:
            cat_escolha = st.selectbox(
                "Filtrar por categoria",
                cat_opcoes,
                key=f"{key_prefix}_cat",
            )
        filtrados = sorted(por_categoria[cat_escolha], key=lambda p: p.get_descricao().lower())
        opcoes = {f"#{p.get_id()} — {p.get_descricao()}": p for p in filtrados}

        with col_prod:
            escolha = st.selectbox(
                f"Produto ({len(filtrados)} em {cat_escolha})",
                list(opcoes.keys()),
                key=f"{key_prefix}_prod",
            )
        return opcoes[escolha]

    @staticmethod
    def _html_foto_preview(id_produto):
        foto = View.produto_caminho_foto(id_produto)
        if not foto:
            return '<span class="sem-foto">📦</span>'
        ext = foto.suffix.lstrip(".").lower()
        mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp"}.get(ext, "jpeg")
        b64 = base64.b64encode(foto.read_bytes()).decode()
        return f'<img src="data:image/{mime};base64,{b64}" alt="Foto do produto" />'

    @staticmethod
    def _preview(produto, categorias, mostrar_foto=False):
        cat = html.escape(categorias.get(produto.get_idCategoria(), "—"))
        nome = html.escape(produto.get_descricao())

        if mostrar_foto:
            img_html = AdminProdutosUI._html_foto_preview(produto.get_id())
            st.markdown(
                f"""
                <div class="admin-prod-preview">
                    <div class="admin-prod-preview-foto">{img_html}</div>
                    <div class="admin-prod-preview-info">
                        <p class="nome">#{produto.get_id()} — {nome}</p>
                        <div class="meta">
                            <span>📂 {cat}</span>
                            <span>💰 R$ {produto.get_preco():.2f}</span>
                            <span>📦 {produto.get_estoque()} un.</span>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            return

        st.markdown(
            f"""
            <div class="admin-cliente-preview">
                <p class="nome">#{produto.get_id()} — {nome}</p>
                <p class="info">📂 {cat}</p>
                <p class="info">💰 R$ {produto.get_preco():.2f} · 📦 {produto.get_estoque()} un.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def _form_inserir(lista_cats, opcoes_cat):
        if not lista_cats:
            st.warning("Cadastre uma categoria antes de inserir produtos.")
            return

        with st.form("admin_prod_inserir", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                descricao = st.text_input("Descrição", placeholder="Ex.: Ração premium")
                cat_nome = st.selectbox("Categoria", list(opcoes_cat.keys()))
            with col2:
                preco = st.number_input("Preco (R$)", min_value=0.01, value=10.0, step=0.5, format="%.2f")
                estoque = st.number_input("Estoque", min_value=0, value=1, step=1)
            foto = st.file_uploader(
                "Foto do produto (opcional)",
                type=FOTO_TIPOS,
                key="admin_prod_inserir_foto",
            )
            salvar = st.form_submit_button("Cadastrar produto", type="primary", use_container_width=True)

        if salvar:
            try:
                AdminUtils.validar_obrigatorios(descricao=descricao)
                novo_id = View.produto_inserir(
                    descricao.strip(),
                    float(preco),
                    int(estoque),
                    opcoes_cat[cat_nome],
                )
                if foto is not None:
                    View.produto_salvar_foto(novo_id, foto)
                st.session_state.admin_sucesso = f"Produto #{novo_id} cadastrado!"
                st.rerun()
            except (ValueError, TypeError) as e:
                st.error(str(e))

    @staticmethod
    def _form_atualizar(produtos, categorias, opcoes_cat):
        if not produtos:
            st.info("Nenhum produto cadastrado para atualizar.")
            return

        if not categorias:
            st.warning("Cadastre categorias antes de atualizar produtos.")
            return

        atual = AdminProdutosUI._selecionar_produto(produtos, categorias, "admin_prod_edit")
        if atual is None:
            return

        AdminProdutosUI._preview(atual, categorias, mostrar_foto=True)

        cat_atual = categorias.get(atual.get_idCategoria(), list(opcoes_cat.keys())[0] if opcoes_cat else "")
        tem_foto = View.produto_caminho_foto(atual.get_id()) is not None

        with st.form("admin_prod_atualizar"):
            col1, col2 = st.columns(2)
            with col1:
                descricao = st.text_input("Descrição", value=atual.get_descricao())
                if opcoes_cat:
                    nomes = list(opcoes_cat.keys())
                    idx = nomes.index(cat_atual) if cat_atual in nomes else 0
                    cat_nome = st.selectbox("Categoria", nomes, index=idx)
            with col2:
                preco = st.number_input(
                    "Preco (R$)",
                    min_value=0.01,
                    value=float(atual.get_preco()),
                    step=0.5,
                    format="%.2f",
                )
                estoque = st.number_input(
                    "Estoque",
                    min_value=0,
                    value=int(atual.get_estoque()),
                    step=1,
                )
            foto = st.file_uploader(
                "Nova foto do produto (opcional)",
                type=FOTO_TIPOS,
                key=f"admin_prod_edit_foto_{atual.get_id()}",
            )
            if tem_foto:
                remover_foto = st.checkbox("Remover foto atual", key=f"admin_prod_rem_foto_{atual.get_id()}")
            else:
                remover_foto = False
            salvar = st.form_submit_button("Salvar alteracoes", type="primary", use_container_width=True)

        if salvar and opcoes_cat:
            try:
                AdminUtils.validar_obrigatorios(descricao=descricao)
                View.produto_atualizar(
                    atual.get_id(),
                    descricao.strip(),
                    float(preco),
                    int(estoque),
                    opcoes_cat[cat_nome],
                )
                if remover_foto:
                    View.produto_excluir_foto(atual.get_id())
                elif foto is not None:
                    View.produto_salvar_foto(atual.get_id(), foto)
                st.session_state.admin_sucesso = f"Produto #{atual.get_id()} atualizado!"
                st.rerun()
            except (ValueError, TypeError) as e:
                st.error(str(e))

    @staticmethod
    def _form_excluir(produtos, categorias):
        if not produtos:
            st.info("Nenhum produto cadastrado para excluir.")
            return

        if not categorias:
            st.warning("Nenhuma categoria cadastrada.")
            return

        atual = AdminProdutosUI._selecionar_produto(produtos, categorias, "admin_prod_del")
        if atual is None:
            return

        AdminProdutosUI._preview(atual, categorias, mostrar_foto=True)

        st.markdown(
            '<div class="admin-alerta-excluir">⚠️ Esta acao e permanente e nao pode ser desfeita.</div>',
            unsafe_allow_html=True,
        )

        confirmar = st.checkbox(
            f"Confirmo que desejo excluir o produto #{atual.get_id()} — {atual.get_descricao()}",
            key="admin_prod_confirm_del",
        )

        if st.button(
            "Excluir produto",
            type="primary",
            use_container_width=True,
            key="admin_prod_del_btn",
            disabled=not confirmar,
        ):
            ok = View.produto_excluir(atual.get_id())
            if ok:
                st.session_state.admin_sucesso = f"Produto #{atual.get_id()} excluido!"
                st.session_state.pop("admin_prod_confirm_del", None)
                st.rerun()
            else:
                st.error("Produto não encontrado.")

    @staticmethod
    def main():
        produtos = View.produto_listar()
        categorias = AdminProdutosUI._mapa_categorias()
        lista_cats = View.categoria_listar()
        opcoes_cat = {c.get_descricao(): c.get_id() for c in lista_cats}

        tab_listar, tab_inserir, tab_atualizar, tab_excluir = st.tabs(
            ["Listar", "Inserir", "Atualizar", "Excluir"]
        )

        with tab_listar:
            AdminProdutosUI._render_lista(produtos, categorias)
        with tab_inserir:
            AdminProdutosUI._form_inserir(lista_cats, opcoes_cat)
        with tab_atualizar:
            AdminProdutosUI._form_atualizar(produtos, categorias, opcoes_cat)
        with tab_excluir:
            AdminProdutosUI._form_excluir(produtos, categorias)
