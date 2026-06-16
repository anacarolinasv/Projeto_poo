import streamlit as st
from views import View
from apresentacao.comum.admin_utils import AdminUtils


class AdminClientesUI:
    @staticmethod
    def _proximo_id():
        clientes = View.cliente_listar()
        if not clientes:
            return 1
        return max(c.get_id() for c in clientes) + 1

    @staticmethod
    def _render_lista(clientes):
        linhas = [
            (f'<span class="col-id">#{c.get_id()}</span>', c.get_nome(), c.get_email(), c.get_fone())
            for c in clientes
        ]
        AdminUtils.render_tabela(
            "Listar clientes",
            ["ID", "Nome", "E-mail", "Telefone"],
            linhas,
            permitir_html=True,
        )

    @staticmethod
    def _preview_cliente(cliente):
        st.markdown(
            f"""
            <div class="admin-cliente-preview">
                <p class="nome">#{cliente.get_id()} — {cliente.get_nome()}</p>
                <p class="info">📧 {cliente.get_email()}</p>
                <p class="info">📱 {cliente.get_fone()}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def _form_inserir():
        proximo = AdminClientesUI._proximo_id()
        st.markdown(
            f'<p class="dica-id">Proximo ID disponivel: <strong>#{proximo}</strong></p>',
            unsafe_allow_html=True,
        )

        with st.form("admin_cliente_inserir", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome completo", placeholder="Ex.: Maria Silva")
                email = st.text_input("E-mail", placeholder="Ex.: maria@email.com")
            with col2:
                fone = st.text_input("Telefone", placeholder="Ex.: (84) 99999-9999")
                senha = st.text_input("Senha de acesso", type="password", placeholder="Mínimo 4 caracteres")
            salvar = st.form_submit_button("Cadastrar cliente", type="primary", use_container_width=True)

        if salvar:
            try:
                AdminUtils.validar_obrigatorios(nome=nome, email=email, fone=fone, senha=senha)
                View.cliente_inserir(proximo, nome.strip(), email.strip(), fone.strip(), senha)
                st.session_state.admin_sucesso = f"Cliente #{proximo} cadastrado!"
                st.rerun()
            except (ValueError, TypeError) as e:
                st.error(str(e))

    @staticmethod
    def _form_atualizar(clientes):
        if not clientes:
            st.info("Nenhum cliente cadastrado para atualizar.")
            return

        opcoes = {f"#{c.get_id()} — {c.get_nome()}": c for c in clientes}
        escolha = st.selectbox(
            "Cliente",
            list(opcoes.keys()),
            key="admin_cli_edit_sel",
        )
        atual = opcoes[escolha]
        AdminClientesUI._preview_cliente(atual)

        with st.form("admin_cliente_atualizar"):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome", value=atual.get_nome())
                email = st.text_input("E-mail", value=atual.get_email())
            with col2:
                fone = st.text_input("Telefone", value=atual.get_fone())
                senha = st.text_input(
                    "Nova senha",
                    type="password",
                    placeholder="Deixe em branco para manter a atual",
                )
            salvar = st.form_submit_button("Salvar alteracoes", type="primary", use_container_width=True)

        if salvar:
            try:
                AdminUtils.validar_obrigatorios(nome=nome, email=email, fone=fone)
                nova_senha = senha.strip() if senha.strip() else atual.get_senha()
                View.cliente_atualizar(
                    atual.get_id(),
                    nome.strip(),
                    email.strip(),
                    fone.strip(),
                    nova_senha,
                )
                st.session_state.admin_sucesso = f"Cliente #{atual.get_id()} atualizado!"
                st.rerun()
            except (ValueError, TypeError) as e:
                st.error(str(e))

    @staticmethod
    def _form_excluir(clientes):
        if not clientes:
            st.info("Nenhum cliente cadastrado para excluir.")
            return

        opcoes = {f"#{c.get_id()} — {c.get_nome()}": c for c in clientes}
        escolha = st.selectbox(
            "Cliente",
            list(opcoes.keys()),
            key="admin_cli_del_sel",
        )
        atual = opcoes[escolha]
        AdminClientesUI._preview_cliente(atual)

        st.markdown(
            '<div class="admin-alerta-excluir">⚠️ Esta acao e permanente e nao pode ser desfeita.</div>',
            unsafe_allow_html=True,
        )

        confirmar = st.checkbox(
            f"Confirmo que desejo excluir o cliente #{atual.get_id()} — {atual.get_nome()}",
            key="admin_cli_confirm_del",
        )

        if st.button(
            "Excluir cliente",
            type="primary",
            use_container_width=True,
            key="admin_cli_del_btn",
            disabled=not confirmar,
        ):
            ok = View.cliente_excluir(atual.get_id())
            if ok:
                st.session_state.admin_sucesso = f"Cliente #{atual.get_id()} excluido!"
                st.session_state.pop("admin_cli_confirm_del", None)
                st.rerun()
            else:
                st.error("Cliente não encontrado.")

    @staticmethod
    def main():
        clientes = View.cliente_listar()

        tab_listar, tab_inserir, tab_atualizar, tab_excluir = st.tabs(
            ["Listar", "Inserir", "Atualizar", "Excluir"]
        )

        with tab_listar:
            AdminClientesUI._render_lista(clientes)
        with tab_inserir:
            AdminClientesUI._form_inserir()
        with tab_atualizar:
            AdminClientesUI._form_atualizar(clientes)
        with tab_excluir:
            AdminClientesUI._form_excluir(clientes)
