import streamlit as st
from views import View
from Templates.admin_utils import AdminUtils


class AdminCategoriasUI:
    @staticmethod
    def _proximo_id():
        categorias = View.categoria_listar()
        if not categorias:
            return 1
        return max(c.get_id() for c in categorias) + 1

    @staticmethod
    def _render_lista(categorias):
        linhas = [
            (f'<span class="col-id">#{c.get_id()}</span>', c.get_descricao())
            for c in categorias
        ]
        AdminUtils.render_tabela(
            "Listar categorias",
            ["ID", "Descrição"],
            linhas,
            permitir_html=True,
        )

    @staticmethod
    def _preview(categoria):
        st.markdown(
            f"""
            <div class="admin-cliente-preview">
                <p class="nome">#{categoria.get_id()} — {categoria.get_descricao()}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def _form_inserir():
        proximo = AdminCategoriasUI._proximo_id()
        st.markdown(
            f'<p class="dica-id">Proximo ID disponivel: <strong>#{proximo}</strong></p>',
            unsafe_allow_html=True,
        )
        with st.form("admin_cat_inserir", clear_on_submit=True):
            descricao = st.text_input("Descrição", placeholder="Ex.: Roupas")
            salvar = st.form_submit_button("Cadastrar categoria", type="primary", use_container_width=True)
        if salvar:
            try:
                AdminUtils.validar_obrigatorios(descricao=descricao)
                View.categoria_inserir(proximo, descricao.strip())
                st.session_state.admin_sucesso = f"Categoria #{proximo} cadastrada!"
                st.rerun()
            except (ValueError, TypeError) as e:
                st.error(str(e))

    @staticmethod
    def _form_atualizar(categorias):
        if not categorias:
            st.info("Nenhuma categoria cadastrada para atualizar.")
            return

        opcoes = {f"#{c.get_id()} — {c.get_descricao()}": c for c in categorias}
        escolha = st.selectbox("Categoria", list(opcoes.keys()), key="admin_cat_edit_sel")
        atual = opcoes[escolha]
        AdminCategoriasUI._preview(atual)

        with st.form("admin_cat_atualizar"):
            descricao = st.text_input("Descrição", value=atual.get_descricao())
            salvar = st.form_submit_button("Salvar alteracoes", type="primary", use_container_width=True)
        if salvar:
            try:
                AdminUtils.validar_obrigatorios(descricao=descricao)
                View.categoria_atualizar(atual.get_id(), descricao.strip())
                st.session_state.admin_sucesso = f"Categoria #{atual.get_id()} atualizada!"
                st.rerun()
            except (ValueError, TypeError) as e:
                st.error(str(e))

    @staticmethod
    def _form_excluir(categorias):
        if not categorias:
            st.info("Nenhuma categoria cadastrada para excluir.")
            return

        opcoes = {f"#{c.get_id()} — {c.get_descricao()}": c for c in categorias}
        escolha = st.selectbox("Categoria", list(opcoes.keys()), key="admin_cat_del_sel")
        atual = opcoes[escolha]
        AdminCategoriasUI._preview(atual)

        st.markdown(
            '<div class="admin-alerta-excluir">⚠️ Produtos vinculados podem ficar inconsistentes. '
            "Esta acao e permanente.</div>",
            unsafe_allow_html=True,
        )

        confirmar = st.checkbox(
            f"Confirmo que desejo excluir a categoria #{atual.get_id()} — {atual.get_descricao()}",
            key="admin_cat_confirm_del",
        )

        if st.button(
            "Excluir categoria",
            type="primary",
            use_container_width=True,
            key="admin_cat_del_btn",
            disabled=not confirmar,
        ):
            ok = View.categoria_excluir(atual.get_id())
            if ok:
                st.session_state.admin_sucesso = f"Categoria #{atual.get_id()} excluida!"
                st.session_state.pop("admin_cat_confirm_del", None)
                st.rerun()
            else:
                st.error("Categoria não encontrada.")

    @staticmethod
    def main():
        categorias = View.categoria_listar()

        tab_listar, tab_inserir, tab_atualizar, tab_excluir = st.tabs(
            ["Listar", "Inserir", "Atualizar", "Excluir"]
        )

        with tab_listar:
            AdminCategoriasUI._render_lista(categorias)
        with tab_inserir:
            AdminCategoriasUI._form_inserir()
        with tab_atualizar:
            AdminCategoriasUI._form_atualizar(categorias)
        with tab_excluir:
            AdminCategoriasUI._form_excluir(categorias)
