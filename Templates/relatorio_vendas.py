def imprimir_vendas_com_itens(registros, titulo, mostrar_cliente=False):
    """
    Exibe no terminal uma lista de vendas com seus itens.

    registros: lista de dicts no formato {"venda": objeto Venda, "itens": [...]}
               (tipico retorno de VendaRelatorioServico).
    titulo: texto da secao (ex.: "Minhas compras", "Todas as vendas").
    mostrar_cliente: se True, inclui id do cliente na linha (uso admin); cliente ve so as proprias vendas.
    """
    print()
    # Completa a linha com tracos ate ~54 caracteres (alinha visual com outros blocos da UI).
    moldura = "─" * max(0, 54 - len(titulo) - 4)
    print(f"── {titulo} {moldura}")
    if not registros:
        print("ℹ  Nenhuma venda encontrada.")
        return
    for reg in registros:
        v = reg["venda"]
        # Linha resumida da venda: id, data gravada no checkout, total monetario.
        cabecalho = (
            f"  Venda #{v.get_id()}   "
            f"Data: {v.get_data()}   "
            f"Total: R$ {float(v.get_total()):.2f}"
        )
        if mostrar_cliente:
            cabecalho += f"   Cliente: {v.get_idCliente()}"
        print()
        print(cabecalho)
        # Cada item: dict com descricao, id_produto, quantidade, preco_unitario, total_item.
        for it in reg["itens"]:
            print(
                f"    - {it['descricao']} (prod. {it['id_produto']})  "
                f"qtd {it['quantidade']} x R$ {it['preco_unitario']:.2f} "
                f"= R$ {it['total_item']:.2f}"
            )
