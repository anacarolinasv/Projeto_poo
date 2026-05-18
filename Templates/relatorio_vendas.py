# Estilos do terminal: titulo_secao_linha / info sao funcoes prontas;
from Templates.estilo_terminal import (
    BOLD,
    BR_YEL,
    DIM,
    FG_CYN,
    info,
    style,
    titulo_secao_linha,
)

#Esse arquivo não grava vendas —  É a “tela” do relatório de compras.
def imprimir_vendas_com_itens(registros, titulo, mostrar_cliente=False):
    print() # imprime uma linha em branco
    print(titulo_secao_linha(titulo)) # imprime o titulo da seção

    if not registros: # se a lista de vendas estiver vazia, imprime uma mensagem de erro
        print(info("ℹ  Nenhuma venda encontrada."))
        return # retorna a lista de vendas

    for reg in registros: # para cada venda na lista de vendas, imprimir o cabeçalho
        v = reg["venda"] # venda

        cabecalho = (f"  Venda #{v.get_id()}   " f"Data: {v.get_data()}   " f"Total: R$ {float(v.get_total()):.2f}") # cabeçalho da venda

        if mostrar_cliente: # se o mostrar_cliente for True, imprime o id do cliente
            cabecalho += f"   Cliente: {v.get_idCliente()}" # adiciona o id do cliente ao cabeçalho

        # Cabecalho da venda: negrito + amarelo brilhante (destaque principal).
        print()
        print(style(cabecalho, BOLD, BR_YEL))
        # Itens: DIM + ciano normal = texto mais discreto abaixo do cabecalho.
        for it in reg["itens"]:
            linha = (
                f"    - {it['descricao']} (prod. {it['id_produto']})  " # descrição do produto
                f"qtd {it['quantidade']} x R$ {it['preco_unitario']:.2f} " # quantidade do produto
                f"= R$ {it['total_item']:.2f}" # total do item
            )
            print(style(linha, DIM, FG_CYN)) # imprime a linha do item
