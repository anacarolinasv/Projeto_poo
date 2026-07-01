// i18n.js — internacionalizacao (Portugues <-> Ingles).
// t(s) traduz textos de interface; tCat / tProd traduzem dados (categorias/produtos).

const I18N = {
  lang: localStorage.getItem("petshopif_lang") || "pt",

  setLang(l) {
    this.lang = l;
    localStorage.setItem("petshopif_lang", l);
  },
  toggle() {
    this.setLang(this.lang === "pt" ? "en" : "pt");
  },

  // ---- Textos de interface (chave = string em PT) ----
  ui: {
    // Login / cadastro
    "BEM-VINDO(A)": "WELCOME",
    "Entre na sua conta Pet Shop IF": "Sign in to your Pet Shop IF account",
    "CRIAR CONTA": "CREATE ACCOUNT",
    "Cadastre-se no Pet Shop IF": "Sign up at Pet Shop IF",
    "SOU ENTREGADOR": "I'M A COURIER",
    "Cadastre-se para realizar entregas": "Sign up to make deliveries",
    "E-mail ou login": "Email or login",
    "Senha": "Password",
    "Nome completo": "Full name",
    "E-mail": "Email",
    "Telefone": "Phone",
    "Confirmar senha": "Confirm password",
    "Login": "Login",
    "ENTRAR": "SIGN IN",
    "CADASTRAR": "SIGN UP",
    "Digite seu e-mail ou login": "Enter your email or login",
    "Digite sua senha": "Enter your password",
    "Seu nome": "Your name",
    "(00) 00000-0000": "(000) 000-0000",
    "Mínimo 4 caracteres": "At least 4 characters",
    "Repita a senha": "Repeat the password",
    "Crie um login de acesso": "Create an access login",
    "Não tem conta?": "Don't have an account?",
    "Já possui uma conta?": "Already have an account?",
    "Já tem cadastro de entregador?": "Already registered as a courier?",
    "Abrir conta": "Create account",
    "Sou entregador": "I'm a courier",
    "Entrar": "Sign in",

    // Navbar
    "Produtos": "Products",
    "Favoritos": "Favorites",
    "Carrinho": "Cart",
    "Compras": "Orders",
    "Perfil": "Profile",
    "Sair": "Log out",
    "Início": "Home",
    "Clientes": "Customers",
    "Categorias": "Categories",
    "Promoções": "Promotions",
    "Vendas": "Sales",
    "Entregas": "Deliveries",
    "Pet Shop IF": "Pet Shop IF",
    "Painel Admin": "Admin Panel",
    "Painel Entregador": "Courier Panel",

    // Loja - produtos
    "Catálogo": "Catalog",
    "Produtos disponíveis": "Available products",
    "Escolha com carinho o melhor para o seu pet": "Lovingly pick the best for your pet",
    "Filtrar por categoria": "Filter by category",
    "Todas as categorias": "All categories",
    "produto": "product",
    "produtos": "products",
    "Nenhum produto encontrado com esse filtro.": "No products found with this filter.",
    "Em estoque": "In stock",
    "🛒 Adicionar": "🛒 Add to cart",

    // Favoritos
    "Meus favoritos": "My favorites",
    "Você ainda não favoritou nenhum produto.": "You haven't favorited any products yet.",

    // Carrinho
    "Seu carrinho está vazio.": "Your cart is empty.",
    "Ver produtos": "Browse products",
    "Meu carrinho": "My cart",
    "cada": "each",
    "promoção": "on sale",
    "Total": "Total",
    "Esvaziar": "Empty cart",
    "Finalizar compra": "Checkout",

    // Compras
    "Você ainda não fez nenhuma compra.": "You haven't placed any orders yet.",
    "Minhas compras": "My orders",
    "Pedido": "Order",
    "Produto removido": "Removed product",
    "Aguardando alocação": "Awaiting assignment",
    "Entregador a caminho": "Courier on the way",
    "Em transporte": "In transit",
    "Entregue": "Delivered",

    // Perfil
    "Meu perfil": "My profile",
    "Dados da conta": "Account details",
    "Nome": "Name",
    "Salvar alterações": "Save changes",

    // Admin dashboard
    "Painel administrativo": "Admin dashboard",
    "Visão geral do Pet Shop IF": "Pet Shop IF overview",
    "Faturamento": "Revenue",
    "Últimas vendas": "Latest sales",
    "Cliente": "Customer",
    "Data": "Date",
    "Nenhuma venda ainda.": "No sales yet.",
    "Estoque baixo (≤ 3)": "Low stock (≤ 3)",
    "Estoque": "Stock",
    "Estoque saudável 🎉": "Stock is healthy 🎉",

    // Admin genericos
    "Novo cliente": "New customer",
    "Adicionar cliente": "Add customer",
    "Ações": "Actions",
    "Excluir": "Delete",
    "Nova categoria": "New category",
    "Descrição": "Description",
    "Adicionar categoria": "Add category",
    "Salvar": "Save",
    "Novo produto": "New product",
    "Categoria": "Category",
    "Preço": "Price",
    "Adicionar produto": "Add product",
    "Reajustar preços (%)": "Adjust prices (%)",
    "Nova promoção": "New promotion",
    "Percentual (%)": "Percentage (%)",
    "Data início": "Start date",
    "Data fim": "End date",
    "Adicionar promoção": "Add promotion",
    "Ativa": "Active",
    "Inativa": "Inactive",
    "Início": "Start",
    "Fim": "End",
    "Status": "Status",
    "Nenhuma promoção.": "No promotions.",
    "Descontos por categoria": "Discounts by category",
    "no catálogo": "in the catalog",
    "Relatório de vendas — total:": "Sales report — total:",
    "Itens": "Items",
    "Nenhuma venda registrada.": "No sales recorded.",
    "Aloque entregadores aos pedidos": "Assign couriers to orders",
    "Alocação": "Assignment",
    "Alocar": "Assign",
    "Nenhum pedido para entrega.": "No orders to deliver.",

    // Entregador
    "Suas entregas alocadas": "Your assigned deliveries",
    "Minhas entregas": "My deliveries",
    "Ação": "Action",
    "Iniciar transporte": "Start transport",
    "Marcar como entregue": "Mark as delivered",
    "Nenhuma entrega alocada para você ainda.": "No deliveries assigned to you yet.",

    // Status (badges)
    "PENDENTE": "PENDING",
    "ALOCADA": "ASSIGNED",
    "EM TRANSPORTE": "IN TRANSIT",
    "ENTREGUE": "DELIVERED",

    // Toasts / mensagens
    "Produto adicionado ao carrinho!": "Product added to cart!",
    "Adicionado aos favoritos!": "Added to favorites!",
    "Removido dos favoritos.": "Removed from favorites.",
    "Perfil atualizado!": "Profile updated!",
    "Cliente adicionado!": "Customer added!",
    "Cliente excluído.": "Customer deleted.",
    "Categoria adicionada!": "Category added!",
    "Categoria atualizada!": "Category updated!",
    "Categoria excluída.": "Category deleted.",
    "Produto adicionado!": "Product added!",
    "Preços reajustados!": "Prices adjusted!",
    "Produto excluído.": "Product deleted.",
    "Promoção adicionada!": "Promotion added!",
    "Promoção excluída.": "Promotion deleted.",
    "Entregador alocado!": "Courier assigned!",
    "Status atualizado!": "Status updated!",

    // Confirmacoes / prompts
    "Excluir cliente?": "Delete this customer?",
    "Excluir produto?": "Delete this product?",
    "Percentual de reajuste (ex.: 10 para +10%, -5 para -5%):":
      "Adjustment percentage (e.g. 10 for +10%, -5 for -5%):",

    // Erros (vindos do store.js / validacoes)
    "E-mail/login ou senha inválidos.": "Invalid email/login or password.",
    "Preencha todos os campos.": "Please fill in all fields.",
    "Preencha nome e e-mail.": "Please fill in name and email.",
    "A senha deve ter no mínimo 4 caracteres.": "The password must be at least 4 characters long.",
    "As senhas não conferem.": "The passwords don't match.",
    "Já existe uma conta com esse e-mail.": "An account with this email already exists.",
    "Cliente não encontrado.": "Customer not found.",
    "Descrição obrigatória.": "Description is required.",
    "Categoria não encontrada.": "Category not found.",
    "Não é possível excluir: há produtos nessa categoria.":
      "Cannot delete: there are products in this category.",
    "Produto não encontrado.": "Product not found.",
    "Preço inválido.": "Invalid price.",
    "Estoque inválido.": "Invalid stock.",
    "Data final antes da inicial.": "End date is before the start date.",
    "Quantidade acima do estoque disponível.": "Quantity exceeds available stock.",
    "Carrinho vazio.": "Cart is empty.",
    "Login de entregador já existe.": "Courier login already exists.",
    "Entrega não encontrada.": "Delivery not found.",
    "Entrega não é sua.": "This delivery is not yours.",
  },

  // Regras para textos com partes dinamicas (interpolacao)
  patterns: [
    [/^Estoque insuficiente para (.+)\.$/, (m, x) => `Insufficient stock for ${x}.`],
  ],

  // ---- Categorias (chave = descricao em PT) ----
  categorias: {
    "Banho": "Bath",
    "Alimentos": "Food",
    "Brinquedos": "Toys",
    "Farmácia": "Pharmacy",
    "Acessórios": "Accessories",
  },

  // ---- Produtos (chave = id) ----
  produtos: {
    1: "Bath Kit for Dogs and Cats - Shampoo & Conditioner for All Coats - Pet Supplies for Dogs",
    2: "Procão Shampoo & Conditioner for Cats and Dogs 500ml",
    3: "Procão Conditioner for Dogs and Cats 200ml",
    4: "KDog Dry Bath 500ml",
    5: "Dugs Chlorhexidine Soap for Cats and Dogs 80g",
    6: "ND Prime Lamb Dry Food for Puppies of Small & Toy Breeds 800g",
    7: "Bionatural Chicken Dry Food for Senior Dogs of Small Breeds 1kg",
    8: "Quatree Supreme Dry Food for Adult Dogs of Small Breeds 15kg",
    9: "Matisse Salmon Dry Food for Neutered Cats 7.5kg",
    10: "Quatree Gourmet Sea Delights Dry Food for Neutered Cats 10kg",
    11: "São Pet Orange Plush Scratching Post, 1 Platform",
    12: "Red Firefighter Cat Scratching Post",
    13: "Biobone Meat-Flavored Chew Toy",
    14: "Colorful Rubber Ring Toy with Rope 18cm",
    15: "Vinyl Dog-Face Ball 7cm",
    16: "Cat Teaser Wand with Circular Feather 113cm",
    17: "Interactive Ball Toy with Plush for Cats",
    18: "Carproflan 100mg, 14 Tablets",
    19: "Cort-Trat SM Anti-inflammatory Dexamethasone, 20 Tablets",
    20: "Pradodog Dipyrone 25% for Dogs and Cats 20ml",
    21: "Dexium Anti-inflammatory Dexamethasone, 20 Tablets",
    22: "Animal Flower Bach Remedy for Stress & Aggression, Dogs and Cats",
    23: "Animal Flower Bach Remedy for Anxiety, Dogs and Cats",
    24: "Quetin 10 Calming Supplement for Dogs, 60 Tablets",
    25: "Homeopet Anizen Stress Control for Dogs and Cats 30ml",
    26: "NutraFases Relax Dietary Supplement, 20 Tablets",
    27: "São Pet PVC Muzzle with Velcro, Size 3",
    28: "Flit Car Seatbelt Leash for Dogs, Size S",
    29: "São Pet Smash Blue Carrier Bag",
    30: "Panther Gold Blue Pet Carrier, Size 5",
    31: "Chalesco Vision Plus Black Travel Carrier",
    32: "Chalesco Vision Moderna Travel Carrier",
    33: "São Pet Selva Blue Leash 110cm",
    34: "Adjustable Harness, Size L, Pink",
    35: "São Pet Breathable Vest & Leash Kit for Dogs, Rosé, Size XS",
  },
};

// Traducao de string de interface
function t(s) {
  if (I18N.lang === "pt" || s == null) return s;
  if (Object.prototype.hasOwnProperty.call(I18N.ui, s)) return I18N.ui[s];
  for (const [re, fn] of I18N.patterns) {
    const m = String(s).match(re);
    if (m) return fn(...m);
  }
  return s;
}

// Traducao de categoria (por descricao)
function tCat(desc) {
  if (I18N.lang === "pt") return desc;
  return I18N.categorias[desc] || desc;
}

// Traducao de produto (por objeto ou id)
function tProd(prod) {
  if (I18N.lang === "pt") return prod.descricao;
  return I18N.produtos[prod.id] || prod.descricao;
}

// Locale para datas/numeros conforme idioma
function localeAtual() {
  return I18N.lang === "pt" ? "pt-BR" : "en-US";
}
