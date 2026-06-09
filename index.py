import streamlit as st
from views import View
from Templates.login import LoginUI
from Templates.loja_cliente import LojaClienteUI
from Templates.admin_loja import AdminLojaUI


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

        LojaClienteUI.main(st.session_state.usuario, st.session_state.carrinho)


IndexUI.Main()
