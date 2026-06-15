import base64
from pathlib import Path

import streamlit as st
from views import View
from Templates.toast_utils import ToastUtils


class PerfilClienteUI:
    FOTOS_DIR = Path("clientes/fotos")

    @staticmethod
    def _css():
        ToastUtils.css()
        st.markdown(
            """
            <style>
                .perfil-wrap {
                    max-width: 420px;
                    margin: 0 auto;
                }

                .perfil-card {
                    background: #ffffff;
                    border-radius: 24px 24px 0 0;
                    overflow: hidden;
                    box-shadow: 0 12px 32px rgba(180, 90, 40, 0.14);
                    margin-bottom: 0;
                }

                .perfil-card-topo {
                    background: linear-gradient(135deg, #f07043 0%, #e85d30 100%);
                    padding: 2rem 1.5rem 3rem;
                    text-align: center;
                    position: relative;
                }

                .perfil-card-topo h2 {
                    color: #ffffff;
                    font-size: 1.1rem;
                    font-weight: 800;
                    letter-spacing: 0.06em;
                    margin: 0;
                    text-transform: uppercase;
                }

                .perfil-wave {
                    position: absolute;
                    left: 0;
                    bottom: -1px;
                    width: 100%;
                    line-height: 0;
                }

                .perfil-corpo {
                    padding: 0 1.8rem 1.4rem;
                    margin-top: -2.6rem;
                    text-align: center;
                    position: relative;
                    z-index: 1;
                }

                .perfil-avatar-wrap {
                    margin-bottom: 0.6rem;
                }

                .perfil-avatar-img,
                .perfil-avatar-placeholder {
                    width: 110px;
                    height: 110px;
                    border-radius: 50%;
                    border: 4px solid #ffffff;
                    box-shadow: 0 8px 24px rgba(240, 112, 67, 0.25);
                    object-fit: cover;
                }

                .perfil-avatar-placeholder {
                    background: linear-gradient(135deg, #fdebd0 0%, #f9dcc0 100%);
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 2.8rem;
                }

                .perfil-nome {
                    color: #333;
                    font-size: 1.35rem;
                    font-weight: 800;
                    margin: 0.6rem 0 0.25rem 0;
                }

                .perfil-subtitulo {
                    color: #aaa;
                    font-size: 0.85rem;
                    margin: 0 0 1.1rem 0;
                }

                .perfil-info {
                    text-align: left;
                    background: #faf7f4;
                    border-radius: 14px;
                    padding: 0.85rem 1rem;
                    margin-bottom: 0;
                }

                .perfil-info-linha {
                    display: flex;
                    justify-content: space-between;
                    gap: 1rem;
                    padding: 0.45rem 0;
                    border-bottom: 1px solid #f0e6dc;
                    font-size: 0.88rem;
                }

                .perfil-info-linha:last-child {
                    border-bottom: none;
                }

                .perfil-info-label {
                    color: #999;
                    font-weight: 600;
                    flex-shrink: 0;
                }

                .perfil-info-valor {
                    color: #444;
                    font-weight: 700;
                    text-align: right;
                    word-break: break-word;
                }

                .perfil-info-valor.destaque {
                    color: #e85d30;
                }

                [data-testid="column"]:has(.perfil-wrap) div[data-testid="element-container"]:has(div[data-testid="stFileUploader"]) {
                    background: #ffffff;
                    border-top: 1px solid #f5ebe3;
                    box-shadow: 0 12px 32px rgba(180, 90, 40, 0.14);
                    margin-top: -2px;
                    padding: 1rem 1.8rem 0.4rem;
                }

                [data-testid="column"]:has(.perfil-wrap) div[data-testid="element-container"]:has(.stButton) {
                    background: #ffffff;
                    box-shadow: 0 12px 32px rgba(180, 90, 40, 0.14);
                    padding: 0 1.8rem 1.5rem;
                    border-radius: 0 0 24px 24px;
                }

                [data-testid="column"]:has(.perfil-wrap) div[data-testid="stFileUploader"] {
                    background: #faf7f4;
                    border: 1px dashed #e8d5c8;
                    border-radius: 12px;
                    padding: 0.6rem 0.8rem;
                }

                [data-testid="column"]:has(.perfil-wrap) div[data-testid="stFileUploader"] label {
                    font-size: 0.78rem !important;
                    font-weight: 600 !important;
                    color: #777 !important;
                }

                [data-testid="column"]:has(.perfil-wrap) div[data-testid="stFileUploader"] small {
                    font-size: 0.72rem !important;
                    color: #aaa !important;
                }

                [data-testid="column"]:has(.perfil-wrap) .stButton > button[kind="secondary"] {
                    width: 100%;
                    border-radius: 999px !important;
                    border: 1px solid #f07043 !important;
                    color: #f07043 !important;
                    background: #ffffff !important;
                    font-weight: 600 !important;
                    margin-top: 0.4rem;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def _buscar_cliente(id_cliente):
        for cliente in View.cliente_listar():
            if cliente.get_id() == id_cliente:
                return cliente
        return None

    @staticmethod
    def _caminho_foto(id_cliente):
        PerfilClienteUI.FOTOS_DIR.mkdir(parents=True, exist_ok=True)
        for ext in ("jpg", "jpeg", "png", "webp"):
            caminho = PerfilClienteUI.FOTOS_DIR / f"{id_cliente}.{ext}"
            if caminho.exists():
                return caminho
        return None

    @staticmethod
    def _avatar_html(foto):
        if not foto:
            return '<div class="perfil-avatar-placeholder">🐶</div>'

        ext = foto.suffix.lstrip(".").lower()
        mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp"}.get(ext, "jpeg")
        b64 = base64.b64encode(foto.read_bytes()).decode()
        return f'<img class="perfil-avatar-img" src="data:image/{mime};base64,{b64}" alt="Foto de perfil" />'

    @staticmethod
    def _salvar_foto(id_cliente, arquivo):
        ext = (arquivo.name or "").rsplit(".", 1)[-1].lower()
        if ext not in ("jpg", "jpeg", "png", "webp"):
            raise ValueError("Formato inválido. Use JPG, PNG ou WEBP.")
        PerfilClienteUI.FOTOS_DIR.mkdir(parents=True, exist_ok=True)
        for antiga in PerfilClienteUI.FOTOS_DIR.glob(f"{id_cliente}.*"):
            antiga.unlink()
        destino = PerfilClienteUI.FOTOS_DIR / f"{id_cliente}.{ext}"
        destino.write_bytes(arquivo.getvalue())

    @staticmethod
    def _sair_conta():
        st.session_state.usuario = None
        st.session_state.carrinho = {}
        st.session_state.modo_tela = "login"
        st.session_state.pagina_loja = "produtos"
        st.session_state.mostrar_boas_vindas_loja = False
        st.rerun()

    @staticmethod
    def _card_html(nome, id_cliente, email, fone, foto):
        avatar = PerfilClienteUI._avatar_html(foto)
        return f"""
        <div class="perfil-wrap">
            <div class="perfil-card">
                <div class="perfil-card-topo">
                    <h2>Meu perfil</h2>
                    <div class="perfil-wave">
                        <svg viewBox="0 0 500 50" preserveAspectRatio="none" style="height:36px;width:100%;">
                            <path d="M0,25 C80,55 120,0 200,25 C280,50 320,10 400,25 C460,35 480,30 500,25 L500,50 L0,50 Z"
                                  fill="#ffffff"/>
                        </svg>
                    </div>
                </div>
                <div class="perfil-corpo">
                    <div class="perfil-avatar-wrap">{avatar}</div>
                    <p class="perfil-nome">{nome}</p>
                    <p class="perfil-subtitulo">Cliente Pet Shop IF</p>
                    <div class="perfil-info">
                        <div class="perfil-info-linha">
                            <span class="perfil-info-label">ID</span>
                            <span class="perfil-info-valor destaque">#{id_cliente}</span>
                        </div>
                        <div class="perfil-info-linha">
                            <span class="perfil-info-label">E-mail</span>
                            <span class="perfil-info-valor">{email}</span>
                        </div>
                        <div class="perfil-info-linha">
                            <span class="perfil-info-label">Telefone</span>
                            <span class="perfil-info-valor">{fone}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """

    @staticmethod
    def main(usuario):
        PerfilClienteUI._css()

        if st.session_state.pop("perfil_foto_atualizada", False):
            ToastUtils.sucesso("Foto atualizada com sucesso!")

        if "perfil_upload_key" not in st.session_state:
            st.session_state.perfil_upload_key = 0

        id_cliente = usuario["id"]
        nome = usuario["nome"]
        cliente = PerfilClienteUI._buscar_cliente(id_cliente)
        email = cliente.get_email() if cliente else "—"
        fone = cliente.get_fone() if cliente else "—"
        foto = PerfilClienteUI._caminho_foto(id_cliente)

        _, col_mid, _ = st.columns([1, 1.4, 1])
        with col_mid:
            st.markdown(
                PerfilClienteUI._card_html(nome, id_cliente, email, fone, foto),
                unsafe_allow_html=True,
            )

            arquivo = st.file_uploader(
                "Alterar foto de perfil",
                type=["jpg", "jpeg", "png", "webp"],
                key=f"perfil_foto_upload_{st.session_state.perfil_upload_key}",
            )
            if arquivo is not None:
                try:
                    PerfilClienteUI._salvar_foto(id_cliente, arquivo)
                    st.session_state.perfil_foto_atualizada = True
                    st.session_state.perfil_upload_key += 1
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

            if st.button("Sair da conta", use_container_width=True, type="secondary", key="perfil_sair"):
                PerfilClienteUI._sair_conta()
