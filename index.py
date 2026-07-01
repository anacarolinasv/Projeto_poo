import streamlit as st
from views import View
from apresentacao.visitante.login import LoginUI
from apresentacao.cliente.loja_cliente import LojaClienteUI
from apresentacao.admin.admin_loja import AdminLojaUI
from apresentacao.entregador.painel_entregador import PainelEntregadorUI


st.set_page_config(
    page_title="Pet Shop IF",
    page_icon="🐾",
    layout="wide",
)


class IndexUI:
    @staticmethod
    def Main():
        View.inicializar_app()

        if "usuario" not in st.session_state:
            st.session_state.usuario = None
        if "carrinho" not in st.session_state:
            st.session_state.carrinho = {}

        if st.session_state.usuario is None:
            LoginUI.main()
            return

        if st.session_state.usuario["admin"]:
            AdminLojaUI.main(st.session_state.usuario)
            return

        if st.session_state.usuario.get("tipo") == "entregador":
            PainelEntregadorUI.main(st.session_state.usuario)
            return

        LojaClienteUI.main(st.session_state.usuario, st.session_state.carrinho)


IndexUI.Main()
