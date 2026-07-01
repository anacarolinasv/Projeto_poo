# Pet Shop IF — versão Web (HTML/CSS/JS)

Cópia do projeto de Comércio Eletrônico **Pet Shop IF** (originalmente em Python/Streamlit),
reescrita como uma **Single Page Application** em HTML, CSS e JavaScript puro (sem framework).

## Como abrir

Basta abrir o `index.html` num navegador. Como as fotos dos produtos ficam em
`../produtos/fotos/`, é melhor servir a pasta raiz do projeto por um servidor local:

```bash
# a partir da raiz do projeto (Projeto_poo/)
python3 -m http.server 8137
# depois acesse: http://localhost:8137/web/index.html
```

## Acessos de teste

| Perfil      | Login              | Senha      |
|-------------|--------------------|------------|
| Admin       | `admin`            | `admin123` |
| Cliente     | `ana@gamil.com`    | `123456`   |
| Entregador  | `joao`             | `1234`     |

Também é possível criar conta de cliente e cadastro de entregador pela tela de login.

## Estrutura

```
web/
├── index.html        # shell da aplicação
├── css/styles.css    # identidade visual (tema laranja Pet Shop IF)
└── js/
    ├── data.js       # dados iniciais (seed) — equivale aos arquivos JSON
    ├── i18n.js       # tradução PT/EN (interface, categorias e produtos)
    ├── store.js      # persistência (localStorage) + regras de negócio + fachada View
    └── app.js        # UI e roteamento (equivale ao index.py + Templates/)
```

O `store.js` espelha a arquitetura em camadas do original: um "DAO" genérico sobre
`localStorage`, os serviços de negócio e a fachada `View` (mesma API do `views.py`).
O `i18n.js` contém a tradução PT/EN (interface, categorias e produtos).

## Idioma (PT / EN)

Há um botão flutuante 🌐 no canto inferior direito que traduz **todas as páginas**
entre Português e Inglês (interface, nomes de categorias e de produtos). A escolha
fica salva no `localStorage`. Os preços são exibidos em dólar ($) e o nome da loja é mantido.

## Funcionalidades

- **Cliente:** catálogo com filtro por categoria, favoritos, carrinho, checkout,
  histórico de compras com status de entrega e edição de perfil.
- **Admin:** dashboard, CRUD de clientes/categorias/produtos/promoções, relatório de
  vendas e alocação de entregadores aos pedidos.
- **Entregador:** painel para avançar o status das entregas
  (PENDENTE → ALOCADA → EM_TRANSPORTE → ENTREGUE).
- **Promoções** por categoria com desconto percentual e vigência por data.

## Observação

Os dados são persistidos no `localStorage` do navegador. Para restaurar o estado
inicial, limpe o armazenamento do site ou rode no console: `View.resetarBanco()`.
