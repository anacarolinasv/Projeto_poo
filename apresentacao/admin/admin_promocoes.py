from datetime import date, timedelta

import streamlit as st
from entidades.promocao import ID_CATEGORIA_TODAS
from views import View
from apresentacao.comum.admin_utils import AdminUtils


class AdminPromocoesUI:
    LABEL_TODAS = "Todas as categorias"

    @staticmethod
    def _mapa_categorias():
        return {c.get_id(): c.get_descricao() for c in View.categoria_listar()}

    @staticmethod
    def _rotulo_categoria(id_categoria, mapa_categorias):
        if id_categoria == ID_CATEGORIA_TODAS:
            return AdminPromocoesUI.LABEL_TODAS
        return mapa_categorias.get(id_categoria, f"#{id_categoria}")

    @staticmethod
    def _opcoes_categoria(categorias):
        opcoes = {AdminPromocoesUI.LABEL_TODAS: ID_CATEGORIA_TODAS}
        for c in categorias:
            opcoes[f"#{c.get_id()} — {c.get_descricao()}"] = c.get_id()
        return opcoes

    @staticmethod
    def _status_promocao(promocao):
        hoje = date.today()
        if promocao.get_dataFim() < hoje:
            return "Encerrada", "admin-badge"
        if promocao.get_dataInicio() > hoje:
            return "Agendada", "admin-badge"
        return "Ativa", "dash-badge-alerta"

    @staticmethod
    def _formatar_data(valor):
        return valor.strftime("%d/%m/%Y")

    @staticmethod
    def _render_lista(promocoes, mapa_categorias):
        if not promocoes:
            st.markdown(
                '<div class="admin-empty">Nenhuma promoção cadastrada.</div>',
                unsafe_allow_html=True,
            )
            return

        linhas = []
        for p in promocoes:
            cat = AdminPromocoesUI._rotulo_categoria(p.get_idCategoria(), mapa_categorias)
            status, classe = AdminPromocoesUI._status_promocao(p)
            linhas.append(
                (
                    f'<span class="col-id">#{p.get_id()}</span>',
                    cat,
                    f"{p.get_percentual():.0f}%",
                    AdminPromocoesUI._formatar_data(p.get_dataInicio()),
                    AdminPromocoesUI._formatar_data(p.get_dataFim()),
                    f'<span class="{classe}">{status}</span>',
                )
            )

        AdminUtils.render_tabela(
            "Promoções por categoria",
            ["ID", "Categoria", "Desconto", "Início", "Fim", "Status"],
            linhas,
            permitir_html=True,
        )

    @staticmethod
    def _preview(promocao, mapa_categorias):
        cat = AdminPromocoesUI._rotulo_categoria(promocao.get_idCategoria(), mapa_categorias)
        status, _ = AdminPromocoesUI._status_promocao(promocao)
        st.markdown(
            f"""
            <div class="admin-cliente-preview">
                <p class="nome">#{promocao.get_id()} — {cat}</p>
                <p class="info">Desconto: {promocao.get_percentual():.0f}%</p>
                <p class="info">Período: {AdminPromocoesUI._formatar_data(promocao.get_dataInicio())}
                até {AdminPromocoesUI._formatar_data(promocao.get_dataFim())}</p>
                <p class="info">Status: {status}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def _form_inserir(categorias):
        if not categorias:
            st.info("Cadastre ao menos uma categoria antes de criar promoções.")
            return

        opcoes = AdminPromocoesUI._opcoes_categoria(categorias)
        with st.form("admin_promo_inserir", clear_on_submit=True):
            escolha = st.selectbox("Categoria", list(opcoes.keys()))
            percentual = st.number_input(
                "Desconto (%)",
                min_value=1.0,
                max_value=100.0,
                value=10.0,
                step=1.0,
            )
            col_ini, col_fim = st.columns(2)
            with col_ini:
                data_inicio = st.date_input("Data de início", value=date.today())
            with col_fim:
                data_fim = st.date_input(
                    "Data de fim",
                    value=date.today() + timedelta(days=7),
                )
            salvar = st.form_submit_button(
                "Cadastrar promoção",
                type="primary",
                use_container_width=True,
            )

        if salvar:
            try:
                id_categoria = opcoes[escolha]
                View.promocao_inserir(
                    id_categoria,
                    float(percentual),
                    data_inicio,
                    data_fim,
                )
                destino = (
                    AdminPromocoesUI.LABEL_TODAS
                    if id_categoria == ID_CATEGORIA_TODAS
                    else next(c.get_descricao() for c in categorias if c.get_id() == id_categoria)
                )
                st.session_state.admin_sucesso = (
                    f"Promoção de {percentual:.0f}% para {destino} cadastrada!"
                )
                st.rerun()
            except (ValueError, TypeError) as e:
                st.error(str(e))

    @staticmethod
    def _form_atualizar(promocoes, categorias):
        if not promocoes:
            st.info("Nenhuma promoção cadastrada para atualizar.")
            return
        if not categorias:
            st.info("Nenhuma categoria cadastrada.")
            return

        mapa_categorias = AdminPromocoesUI._mapa_categorias()
        opcoes_promo = {}
        for p in promocoes:
            cat = AdminPromocoesUI._rotulo_categoria(p.get_idCategoria(), mapa_categorias)
            rotulo = (
                f"#{p.get_id()} — {cat} ({p.get_percentual():.0f}% | "
                f"{AdminPromocoesUI._formatar_data(p.get_dataInicio())} a "
                f"{AdminPromocoesUI._formatar_data(p.get_dataFim())})"
            )
            opcoes_promo[rotulo] = p

        escolha = st.selectbox("Promoção", list(opcoes_promo.keys()), key="admin_promo_edit_sel")
        atual = opcoes_promo[escolha]
        AdminPromocoesUI._preview(atual, mapa_categorias)

        opcoes_cat = AdminPromocoesUI._opcoes_categoria(categorias)
        chaves_cat = list(opcoes_cat.keys())
        if atual.get_idCategoria() == ID_CATEGORIA_TODAS:
            indice_cat = 0
        else:
            indice_cat = next(
                i
                for i, chave in enumerate(chaves_cat)
                if opcoes_cat[chave] == atual.get_idCategoria()
            )

        with st.form("admin_promo_atualizar"):
            cat_escolha = st.selectbox(
                "Categoria",
                chaves_cat,
                index=indice_cat,
            )
            percentual = st.number_input(
                "Desconto (%)",
                min_value=1.0,
                max_value=100.0,
                value=float(atual.get_percentual()),
                step=1.0,
            )
            col_ini, col_fim = st.columns(2)
            with col_ini:
                data_inicio = st.date_input(
                    "Data de início",
                    value=atual.get_dataInicio(),
                )
            with col_fim:
                data_fim = st.date_input(
                    "Data de fim",
                    value=atual.get_dataFim(),
                )
            salvar = st.form_submit_button(
                "Salvar alterações",
                type="primary",
                use_container_width=True,
            )

        if salvar:
            try:
                id_categoria = opcoes_cat[cat_escolha]
                View.promocao_atualizar(
                    atual.get_id(),
                    id_categoria,
                    float(percentual),
                    data_inicio,
                    data_fim,
                )
                st.session_state.admin_sucesso = f"Promoção #{atual.get_id()} atualizada!"
                st.rerun()
            except (ValueError, TypeError) as e:
                st.error(str(e))

    @staticmethod
    def _form_excluir(promocoes):
        if not promocoes:
            st.info("Nenhuma promoção cadastrada para excluir.")
            return

        mapa_categorias = AdminPromocoesUI._mapa_categorias()
        opcoes = {}
        for p in promocoes:
            cat = AdminPromocoesUI._rotulo_categoria(p.get_idCategoria(), mapa_categorias)
            opcoes[f"#{p.get_id()} — {cat} ({p.get_percentual():.0f}%)"] = p

        escolha = st.selectbox("Promoção", list(opcoes.keys()), key="admin_promo_del_sel")
        atual = opcoes[escolha]
        AdminPromocoesUI._preview(atual, mapa_categorias)

        st.markdown(
            '<div class="admin-alerta-excluir">Esta acao remove a promocao permanentemente.</div>',
            unsafe_allow_html=True,
        )

        confirmar = st.checkbox(
            f"Confirmo que desejo excluir a promocao #{atual.get_id()}",
            key="admin_promo_confirm_del",
        )

        if st.button(
            "Excluir promoção",
            type="primary",
            use_container_width=True,
            key="admin_promo_del_btn",
            disabled=not confirmar,
        ):
            ok = View.promocao_excluir(atual.get_id())
            if ok:
                st.session_state.admin_sucesso = f"Promoção #{atual.get_id()} excluída!"
                st.session_state.pop("admin_promo_confirm_del", None)
                st.rerun()
            else:
                st.error("Promoção não encontrada.")

    @staticmethod
    def main():
        promocoes = View.promocao_listar()
        categorias = View.categoria_listar()
        mapa_categorias = AdminPromocoesUI._mapa_categorias()

        st.markdown(
            """
            <div class="admin-hero">
                <h2>Promoções</h2>
                <p>Defina descontos por categoria ou para todas, com periodo de inicio e fim.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        tab_listar, tab_inserir, tab_atualizar, tab_excluir = st.tabs(
            ["Listar", "Inserir", "Atualizar", "Excluir"]
        )

        with tab_listar:
            AdminPromocoesUI._render_lista(promocoes, mapa_categorias)
        with tab_inserir:
            AdminPromocoesUI._form_inserir(categorias)
        with tab_atualizar:
            AdminPromocoesUI._form_atualizar(promocoes, categorias)
        with tab_excluir:
            AdminPromocoesUI._form_excluir(promocoes)
