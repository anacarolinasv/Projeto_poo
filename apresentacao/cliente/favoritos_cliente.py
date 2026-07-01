import streamlit as st
from views import View


class FavoritosClienteUI:
    @staticmethod
    def _css():
        st.markdown(
            """
            <style>
                .favoritos-topo {
                    background: linear-gradient(135deg, #fff8f3 0%, #ffffff 55%);
                    border-radius: 20px 20px 0 0;
                    padding: 1.35rem 1.5rem 1.15rem;
                    border: 1px solid rgba(240, 230, 220, 0.9);
                    border-bottom: none;
                    margin-bottom: 0;
                }

                .favoritos-topo .eyebrow {
                    display: inline-block;
                    background: #fff3ec;
                    color: #e85d30;
                    border-radius: 999px;
                    padding: 0.22rem 0.7rem;
                    font-size: 0.72rem;
                    font-weight: 700;
                    letter-spacing: 0.04em;
                    text-transform: uppercase;
                    margin-bottom: 0.55rem;
                }

                .favoritos-topo h2 {
                    margin: 0 0 0.3rem 0;
                    color: #333;
                    font-size: 1.45rem;
                    font-weight: 800;
                }

                .favoritos-topo p {
                    margin: 0;
                    color: #888;
                    font-size: 0.92rem;
                }

                .favoritos-vazio {
                    background: #ffffff;
                    border: 1px solid #f0e6dc;
                    border-radius: 0 0 20px 20px;
                    box-shadow: 0 12px 32px rgba(180, 90, 40, 0.12);
                    text-align: center;
                    padding: 2.5rem 1.75rem;
                }

                .favoritos-vazio-icon {
                    font-size: 2.5rem;
                    margin-bottom: 0.75rem;
                }

                .favoritos-vazio h3 {
                    margin: 0 0 0.5rem 0;
                    color: #333;
                    font-size: 1.2rem;
                    font-weight: 800;
                }

                .favoritos-vazio p {
                    margin: 0;
                    color: #888;
                    font-size: 0.95rem;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def main(id_cliente, carrinho):
        from apresentacao.cliente.loja_cliente import LojaClienteUI

        FavoritosClienteUI._css()
        produtos = View.listar_produtos_favoritos(id_cliente)
        mapa = LojaClienteUI._mapa_categorias()
        favoritos_ids = {p.get_id() for p in produtos}

        st.markdown(
            """
            <div class="favoritos-topo">
                <span class="eyebrow">Seus favoritos</span>
                <h2>Produtos salvos</h2>
                <p>Itens que voce marcou com carinho para comprar depois</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if not produtos:
            st.markdown(
                """
                <div class="favoritos-vazio">
                    <div class="favoritos-vazio-icon">🤍</div>
                    <h3>Nenhum favorito ainda</h3>
                    <p>Explore os produtos e toque no coracao para salvar aqui.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Ver produtos", key="fav_ir_produtos", type="secondary"):
                st.session_state.pagina_loja = "produtos"
                st.rerun()
            return

        n = len(produtos)
        texto = "1 produto salvo" if n == 1 else f"{n} produtos salvos"
        st.markdown(
            f'<p class="loja-contador" style="text-align:right;margin:0.75rem 0 0.5rem;">{texto}</p>',
            unsafe_allow_html=True,
        )

        for inicio in range(0, len(produtos), 3):
            fatia = produtos[inicio : inicio + 3]
            cols = st.columns(3, gap="medium")
            for idx, produto in enumerate(fatia):
                with cols[idx]:
                    LojaClienteUI._card_produto(
                        produto,
                        mapa,
                        id_cliente,
                        carrinho,
                        "fav",
                        favoritos_ids,
                    )
            for idx in range(len(fatia), 3):
                with cols[idx]:
                    st.markdown("&nbsp;", unsafe_allow_html=True)
