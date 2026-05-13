def imprimir_vendas_com_itens(registros, titulo, mostrar_cliente=False):
    if not registros:
        print("Nenhuma venda encontrada.")
        return
    print(f"\n--- {titulo} ---")
    for reg in registros:
        v = reg["venda"]
        linha = (
            f"\nVenda #{v.get_id()} | Data: {v.get_data()} | "
            f"Total: R$ {float(v.get_total()):.2f}"
        )
        if mostrar_cliente:
            linha += f" | Cliente ID: {v.get_idCliente()}"
        print(linha)
        for it in reg["itens"]:
            print(
                f"  - {it['descricao']} (prod. {it['id_produto']})  "
                f"qtd {it['quantidade']} x R$ {it['preco_unitario']:.2f} = R$ {it['total_item']:.2f}"
            )
