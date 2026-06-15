from negocio.promocao_servico import PromocaoServico


class PrecoServico:
    def __init__(self):
        self._promocao_servico = PromocaoServico()

    def preco_efetivo(self, produto, referencia=None):
        return self.detalhes(produto, referencia)["preco_efetivo"]

    def detalhes(self, produto, referencia=None):
        preco_base = round(float(produto.get_preco()), 2)
        promocao = self._promocao_servico.buscar_ativa_por_categoria(
            produto.get_idCategoria(),
            referencia,
        )
        if promocao is None:
            return {
                "preco_base": preco_base,
                "preco_efetivo": preco_base,
                "em_promocao": False,
                "percentual": 0.0,
            }

        percentual = float(promocao.get_percentual())
        preco_efetivo = round(preco_base * (1 - percentual / 100.0), 2)
        return {
            "preco_base": preco_base,
            "preco_efetivo": preco_efetivo,
            "em_promocao": True,
            "percentual": percentual,
        }
