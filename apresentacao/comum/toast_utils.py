import streamlit as st


class ToastUtils:
    CSS = """
        @keyframes pet-toast-in {
            from {
                opacity: 0;
                transform: translateY(-10px) scale(0.96);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }

        div[data-testid="stToast"] {
            animation: pet-toast-in 0.35s ease-out !important;
            background: linear-gradient(135deg, #ffffff 0%, #fff9f5 100%) !important;
            color: #333333 !important;
            border: 1px solid #f0e6dc !important;
            border-left: 5px solid #e85d30 !important;
            border-radius: 16px !important;
            box-shadow: 0 16px 40px rgba(180, 90, 40, 0.16), 0 4px 14px rgba(0, 0, 0, 0.06) !important;
            padding: 0.85rem 1.1rem !important;
            min-width: 260px !important;
            max-width: 360px !important;
        }

        div[data-testid="stToast"] p,
        div[data-testid="stToast"] span,
        div[data-testid="stToast"] div {
            color: #333333 !important;
            font-weight: 600 !important;
            font-size: 0.92rem !important;
            line-height: 1.4 !important;
        }

        div[data-testid="stToast"] svg {
            color: #e85d30 !important;
            fill: #e85d30 !important;
        }
    """

    @staticmethod
    def css():
        st.markdown(f"<style>{ToastUtils.CSS}</style>", unsafe_allow_html=True)

    @staticmethod
    def sucesso(mensagem, icone="✅"):
        st.toast(mensagem, icon=icone)

    @staticmethod
    def info(mensagem, icone="ℹ️"):
        st.toast(mensagem, icon=icone)

    @staticmethod
    def boas_vindas(nome, icone="🐾"):
        st.toast(f"Ola, {nome}! Tudo para o seu pet com carinho!", icon=icone)
