_INNER = 54  # largura util entre as bordas verticais da caixa de menu

# Codigos ANSI (cores e estilos no terminal)
END = "\033[0m"  # reset do estilo do terminal
BOLD = "\033[1m" # negrito
DIM = "\033[2m" # diminuido
FG_RED = "\033[31m" # vermelho
FG_GRN = "\033[32m" # verde
FG_YEL = "\033[33m" # amarelo
FG_BLU = "\033[34m" # azul
FG_MAG = "\033[35m" # magenta
FG_CYN = "\033[36m" # ciano
FG_WHT = "\033[37m" # branco        
BR_RED = "\033[91m" # vermelho brilhante
BR_GRN = "\033[92m" # verde brilhante
BR_YEL = "\033[93m" # amarelo brilhante
BR_BLU = "\033[94m" # azul brilhante
BR_MAG = "\033[95m" # magenta brilhante
BR_CYN = "\033[96m" # ciano brilhante
BR_WHT = "\033[97m" # branco brilhante


def style(texto, *codigos):  # aplica codigos ANSI ao texto e encerra com reset
    if not codigos: # se nao forem passados codigos ANSI, retorna o texto original
        return texto
    return "".join(codigos) + texto + END # aplica os codigos ANSI ao texto e encerra com reset


def borda(s): # caracteres da moldura (┌ │ └ etc.) em ciano suave + DIM para nao competir com o conteudo.
    return style(s, DIM, FG_CYN)


def titulo_app(s): # primeira linha do banner do topo (nome do sistema).
    return style(s, BOLD, BR_MAG)


def subtitulo(s): # segunda linha do banner (ex.: nome do usuario logado).
    return style(s, BOLD, BR_CYN)


def secao(s): # titulo de grupo dentro do menu (ex.: LOJA, CARRINHO).
    return style(s, BOLD, BR_YEL)

def num_opcao(s): # numero da opcao no menu (1, 2, 9...) em verde para destacar da descricao.
    return style(str(s), BOLD, BR_GRN)


def rotulo(s): # destaque generico (ex.: total do carrinho).
    return style(s, BOLD, BR_WHT)


def ok(msg): # mensagem de sucesso (login, item adicionado, compra feita).
    return style(msg, BR_GRN)

def erro(msg): # mensagem de erro de validacao ou operacao.
    return style(msg, BR_RED)

def info(msg): # informacao neutra (lista vazia, dica).
    return style(msg, BR_BLU)

def aviso(msg): # aviso (ex.: logout).
    return style(msg, BR_YEL)

def titulo_secao_linha(texto_moldura): # linha decorativa para relatorios e secoes: '── Minhas compras ──────────'.
    moldura = "─" * max(0, 54 - len(texto_moldura) - 4) # preenche os tracos '-' ate completar 54 caracteres visiveis (sem contar os codigos ANSI)
    linha = f"── {texto_moldura} {moldura}" # linha decorativa para relatorios e secoes: '── Minhas compras ──────────'.    
    return style(linha, BOLD, BR_CYN) # retorna a linha decorativa para relatorios e secoes: '── Minhas compras ──────────'.

def prompt_opcao(): # texto do input principal do menu (seta + pergunta).
    return style("❯ Informe uma opcao: ", BOLD, BR_CYN) # retorna o texto do input principal do menu (seta + pergunta).

def linha_menu_lateral(corpo_formatado, corpo_visivel_len): # monta uma linha interna da caixa: │ conteudo........ │
    espacos = _INNER - corpo_visivel_len # calcula o numero de espacos para alinhar a borda direita em _INNER colunas.
    if espacos < 0:
        espacos = 0
    return borda("│") + corpo_formatado + " " * espacos + borda("│") # retorna a linha interna da caixa: │ conteudo........ │

def _imprimir_opcoes_menu(itens):
    for num, desc in itens:
        num_s = str(num)
        pref = " " * max(1, 6 - len(num_s))
        corpo_opcao = pref + num_opcao(num_s) + "  " + desc
        vis_len = len(pref) + len(num_s) + 2 + len(desc)
        print(linha_menu_lateral(corpo_opcao, vis_len))


def imprimir_caixa_menu(titulo_barra, grupos):
    titulo = titulo_barra
    if len(titulo) > _INNER - 2:
        titulo = titulo[: _INNER - 2]
    lado = max(1, (_INNER - len(titulo)) // 2)
    barra_vis = "─" * lado + titulo + "─" * (_INNER - len(titulo) - lado)
    print()
    print(borda("┌") + borda(barra_vis) + borda("┐"))
    for nome_secao, itens in grupos:
        if nome_secao is None:
            print(borda("│") + " " * _INNER + borda("│"))
            continue
        if nome_secao != "":
            corpo_secao = "  " + secao(nome_secao)
            print(linha_menu_lateral(corpo_secao, 2 + len(nome_secao)))
        _imprimir_opcoes_menu(itens)
    print(borda("└") + borda("─" * _INNER) + borda("┘"))


def banner_boas_vindas(linha1, linha2=None): # caixa dupla no topo da tela (╔══╗) ao entrar como visitante ou usuario logado.
    print() # imprime uma linha em branco
    print(borda("╔") + borda("═" * _INNER) + borda("╗")) # imprime a borda superior
    pad1 = max(0, (_INNER - len(linha1)) // 2) # calcula o numero de espacos para alinhar o titulo do app na barra superior.
    pad2 = _INNER - len(linha1) - pad1 # calcula o numero de espacos para alinhar o subtitulo na barra superior.
    linha_vis = " " * pad1 + linha1 + " " * pad2 # calcula o numero de caracteres para preencher a barra superior.
    print(borda("║") + titulo_app(linha_vis) + borda("║")) # imprime a borda superior.
    if linha2 is not None: # se o subtitulo for definido, imprime o subtitulo.              
        p1 = max(0, (_INNER - len(linha2)) // 2) # calcula o numero de espacos para alinhar o subtitulo na barra superior.
        p2 = _INNER - len(linha2) - p1 # calcula o numero de espacos para alinhar o subtitulo na barra superior.
        linha2_vis = " " * p1 + linha2 + " " * p2 # calcula o numero de caracteres para preencher a barra superior.
        print(borda("║") + subtitulo(linha2_vis) + borda("║")) # imprime a borda superior.
    print(borda("╚") + borda("═" * _INNER) + borda("╝")) # imprime a borda inferior.


def linha_formulario(titulo): # separador antes de formularios (login, abrir conta, inserir no carrinho).
    print() # imprime uma linha em branco
    moldura = "─" * max(0, 54 - len(titulo) - 4) # calcula o numero de espacos para alinhar o titulo na barra superior.
    print(style(f"── {titulo} {moldura}", BOLD, BR_MAG)) # imprime a linha superior.
    return moldura # retorna o numero de espacos para alinhar o titulo na barra superior.