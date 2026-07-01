// data.js — dados iniciais (seed) que alimentam o localStorage.
// Equivalente aos arquivos JSON do projeto Python (produtos/, clientes/, etc.).

const SEED = {
  administradores: [
    { id: 1, login: "admin", senha: "admin123" },
  ],

  clientes: [
    { id: 1, nome: "Ana", email: "ana@gamil.com", fone: "84999999999", senha: "123456" },
    { id: 2, nome: "teste", email: "teste2@email.com", fone: "84912345678", senha: "12345" },
    { id: 3, nome: "Lielly", email: "lielly@email.com", fone: "84912344321", senha: "12345678910" },
    { id: 4, nome: "teste", email: "teste4@email.com", fone: "84987025305", senha: "12345678" },
  ],

  entregadores: [
    { id: 1, nome: "Joao Entregas", fone: "(84) 99999-0000", login: "joao", senha: "1234" },
  ],

  categorias: [
    { id: 1, descricao: "Banho" },
    { id: 2, descricao: "Alimentos" },
    { id: 3, descricao: "Brinquedos" },
    { id: 4, descricao: "Farmácia" },
    { id: 5, descricao: "Acessórios" },
  ],

  produtos: [
    { id: 1, descricao: "Kit Banho para Cães e Gatos - Shampoo Condicionador Todos os Pelos - Pets para Cachorro", preco: 48.5, estoque: 23, idCategoria: 1 },
    { id: 2, descricao: "Shampoo e Condicionador Gatos e Cães Procão 500ml", preco: 24.9, estoque: 34, idCategoria: 1 },
    { id: 3, descricao: "Condicionador Procão Cães e Gatos 200ml", preco: 25.9, estoque: 1, idCategoria: 1 },
    { id: 4, descricao: "Banho a Seco KDog 500ml", preco: 29.9, estoque: 33, idCategoria: 1 },
    { id: 5, descricao: "Sabonete Dugs Clorexidina Gatos e Cães 80g", preco: 16.9, estoque: 5, idCategoria: 1 },
    { id: 6, descricao: "Ração ND Prime Cordeiro Cães Filhotes Raças Pequenas e Mini 800g", preco: 109.0, estoque: 23, idCategoria: 2 },
    { id: 7, descricao: "Ração Bionatural Frango Cães Senior Raças Pequenas 1kg", preco: 46.9, estoque: 2, idCategoria: 2 },
    { id: 8, descricao: "Ração Quatree Supreme Cães Adultos Raças Pequenas 15kg", preco: 279.91, estoque: 35, idCategoria: 2 },
    { id: 9, descricao: "Ração Matisse Gato Castrado Salmão 7,5kg", preco: 195.99, estoque: 17, idCategoria: 2 },
    { id: 10, descricao: "Ração Quatree Gourmet Delícias do Mar Gatos Castrados 10kg", preco: 147.6, estoque: 25, idCategoria: 2 },
    { id: 11, descricao: "Arranhador Pelúcia Laranja 1 Plataforma São Pet", preco: 139.9, estoque: 10, idCategoria: 3 },
    { id: 12, descricao: "Arranhador Gato Bombeiro Vermelho", preco: 229.98, estoque: 5, idCategoria: 3 },
    { id: 13, descricao: "Biobone Mordedor Carne", preco: 79.8, estoque: 20, idCategoria: 3 },
    { id: 14, descricao: "Brinquedo Rosca de Borracha com Corda Colorido 18cm", preco: 15.9, estoque: 30, idCategoria: 3 },
    { id: 15, descricao: "Vinil Bola Cara Cachorro 7cm", preco: 13.9, estoque: 22, idCategoria: 3 },
    { id: 16, descricao: "Brinquedo Gato Varinha Penacho Circular 113cm", preco: 29.9, estoque: 33, idCategoria: 3 },
    { id: 17, descricao: "Brinquedo Bola Interativa com Pelúcia Para Gatos", preco: 56.9, estoque: 8, idCategoria: 3 },
    { id: 18, descricao: "Carproflan 100mg com 14 Comprimidos", preco: 129.9, estoque: 18, idCategoria: 4 },
    { id: 19, descricao: "Cort-Trat SM Antinflamatório Dexametasona 20 Comp", preco: 29.9, estoque: 19, idCategoria: 4 },
    { id: 20, descricao: "Dipirona 25% Cães e Gatos Pradodog 20ml", preco: 19.9, estoque: 29, idCategoria: 4 },
    { id: 21, descricao: "Dexium Antinflamatório Dexametasona 20 comp", preco: 29.9, estoque: 17, idCategoria: 4 },
    { id: 22, descricao: "Floral de Bach Stress e Agressividade Animal Flower Cães e Gatos", preco: 37.9, estoque: 29, idCategoria: 4 },
    { id: 23, descricao: "Floral de Bach Ansiedade Animal Flower Cães e Gatos", preco: 37.9, estoque: 29, idCategoria: 4 },
    { id: 24, descricao: "Quetin 10 Suplemento Calmante Para Cães 60 comp", preco: 109.9, estoque: 16, idCategoria: 4 },
    { id: 25, descricao: "Homeopet Anizen Controle de Estresse Cães e Gatos 30ml", preco: 99.9, estoque: 4, idCategoria: 4 },
    { id: 26, descricao: "Suplemento Alimentar NutraFases Relax 20 Tabletes", preco: 67.9, estoque: 12, idCategoria: 4 },
    { id: 27, descricao: "Focinheira PVC com Velcro N3 São Pet", preco: 13.9, estoque: 20, idCategoria: 5 },
    { id: 28, descricao: "Guia Cinto de Segurança Para Cães Automóvel Flit P", preco: 36.9, estoque: 20, idCategoria: 5 },
    { id: 29, descricao: "Bolsa Smash Azul São Pet", preco: 199.99, estoque: 5, idCategoria: 5 },
    { id: 30, descricao: "Caixa de Transporte Panther Gold Azul n5", preco: 249.9, estoque: 25, idCategoria: 5 },
    { id: 31, descricao: "Mala Vision Plus Preta Chalesco", preco: 199.9, estoque: 10, idCategoria: 5 },
    { id: 32, descricao: "Mala Vision Moderna Chalesco", preco: 194.5, estoque: 12, idCategoria: 5 },
    { id: 33, descricao: "Guia Selva São Pet Azul 110cm", preco: 59.0, estoque: 16, idCategoria: 5 },
    { id: 34, descricao: "Peitoral Ajustável G Rosa", preco: 44.9, estoque: 4, idCategoria: 5 },
    { id: 35, descricao: "Kit Colete Aerado e Guia Rosé Para Cães PP São Pet", preco: 129.0, estoque: 15, idCategoria: 5 },
  ],

  promocoes: [
    { id: 1, idCategoria: 4, percentual: 10.0, dataInicio: "2026-06-09", dataFim: "2026-06-16" },
  ],

  favoritos: [
    { id: 1, idCliente: 3, idProduto: 3 },
    { id: 2, idCliente: 1, idProduto: 1 },
    { id: 3, idCliente: 1, idProduto: 5 },
  ],

  vendas: [
    { id: 1, data: "2026-05-12T22:58:13.797803", carrinho: false, total: 12.0, idCliente: 1 },
    { id: 2, data: "2026-05-12T23:30:57.635047", carrinho: false, total: 24.0, idCliente: 1 },
    { id: 3, data: "2026-05-18T11:40:49.817136", carrinho: false, total: 3.0, idCliente: 3 },
    { id: 4, data: "2026-06-08T23:21:11.200044", carrinho: false, total: 29.99, idCliente: 1 },
    { id: 5, data: "2026-06-08T23:31:02.372935", carrinho: false, total: 132.99, idCliente: 1 },
    { id: 6, data: "2026-06-09T10:12:35.826265", carrinho: false, total: 97.0, idCliente: 4 },
  ],

  vendaItens: [
    { id: 1, quantidade: 1, preco: 12.0, idVenda: 1, idProduto: 1 },
    { id: 2, quantidade: 2, preco: 12.0, idVenda: 2, idProduto: 1 },
    { id: 3, quantidade: 1, preco: 3.0, idVenda: 3, idProduto: 3 },
    { id: 4, quantidade: 1, preco: 29.99, idVenda: 4, idProduto: 1 },
    { id: 5, quantidade: 1, preco: 100.0, idVenda: 5, idProduto: 2 },
    { id: 6, quantidade: 1, preco: 29.99, idVenda: 5, idProduto: 1 },
    { id: 7, quantidade: 1, preco: 3.0, idVenda: 5, idProduto: 3 },
    { id: 8, quantidade: 2, preco: 48.5, idVenda: 6, idProduto: 1 },
  ],

  // Entregas: status PENDENTE -> ALOCADA -> EM_TRANSPORTE -> ENTREGUE
  entregas: [],
};
