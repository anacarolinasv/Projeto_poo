// store.js — camada de dados e regras de negocio.
// Espelha o DAO generico (persistencia/dao.py) + os servicos (negocio/*_servico.py)
// + a fachada View (views.py), mas persistindo em localStorage.

const DB_KEY = "petshopif_db_v1";

// ---------------------------------------------------------------------------
// Persistencia (equivalente ao DAO generico)
// ---------------------------------------------------------------------------
const DB = (() => {
  function carregar() {
    const bruto = localStorage.getItem(DB_KEY);
    if (bruto) {
      try {
        return JSON.parse(bruto);
      } catch (e) {
        console.warn("Banco corrompido, recriando a partir do seed.", e);
      }
    }
    const inicial = JSON.parse(JSON.stringify(SEED));
    salvarTudo(inicial);
    return inicial;
  }

  function salvarTudo(dados) {
    localStorage.setItem(DB_KEY, JSON.stringify(dados));
  }

  let dados = carregar();

  return {
    tabela(nome) {
      return dados[nome] || (dados[nome] = []);
    },
    salvar() {
      salvarTudo(dados);
    },
    proximoId(nome) {
      const tab = this.tabela(nome);
      return tab.reduce((max, o) => Math.max(max, o.id || 0), 0) + 1;
    },
    resetar() {
      dados = JSON.parse(JSON.stringify(SEED));
      salvarTudo(dados);
    },
  };
})();

// ---------------------------------------------------------------------------
// View — fachada estatica da aplicacao (mesma API do views.py)
// ---------------------------------------------------------------------------
const View = {
  // ---------- Autenticacao ----------
  autenticar(loginOuEmail, senha) {
    const chave = (loginOuEmail || "").trim();
    const admin = DB.tabela("administradores").find(
      (a) => a.login === chave && a.senha === senha
    );
    if (admin) {
      return { id: admin.id, nome: "Administrador", admin: true, tipo: "admin" };
    }
    const cliente = DB.tabela("clientes").find(
      (c) => c.email === chave && c.senha === senha
    );
    if (cliente) {
      return { id: cliente.id, nome: cliente.nome, email: cliente.email, admin: false, tipo: "cliente" };
    }
    const entregador = DB.tabela("entregadores").find(
      (e) => e.login === chave && e.senha === senha
    );
    if (entregador) {
      return { id: entregador.id, nome: entregador.nome, admin: false, tipo: "entregador" };
    }
    return null;
  },

  abrirConta(nome, email, fone, senha, senha2) {
    nome = (nome || "").trim();
    email = (email || "").trim();
    fone = (fone || "").trim();
    if (!nome || !email || !fone || !senha) {
      throw new Error("Preencha todos os campos.");
    }
    if (senha.length < 4) {
      throw new Error("A senha deve ter no mínimo 4 caracteres.");
    }
    if (senha !== senha2) {
      throw new Error("As senhas não conferem.");
    }
    if (DB.tabela("clientes").some((c) => c.email === email)) {
      throw new Error("Já existe uma conta com esse e-mail.");
    }
    const cliente = { id: DB.proximoId("clientes"), nome, email, fone, senha };
    DB.tabela("clientes").push(cliente);
    DB.salvar();
    return cliente;
  },

  // ---------- Clientes ----------
  clienteListar() {
    return DB.tabela("clientes");
  },
  clienteInserir(nome, email, fone, senha) {
    const cliente = { id: DB.proximoId("clientes"), nome, email, fone, senha };
    DB.tabela("clientes").push(cliente);
    DB.salvar();
    return cliente;
  },
  clienteAtualizar(id, nome, email, fone, senha) {
    const c = DB.tabela("clientes").find((x) => x.id === id);
    if (!c) throw new Error("Cliente não encontrado.");
    Object.assign(c, { nome, email, fone, senha });
    DB.salvar();
  },
  clienteExcluir(id) {
    const tab = DB.tabela("clientes");
    const i = tab.findIndex((x) => x.id === id);
    if (i >= 0) tab.splice(i, 1);
    DB.salvar();
  },

  // ---------- Categorias ----------
  categoriaListar() {
    return DB.tabela("categorias");
  },
  categoriaInserir(descricao) {
    descricao = (descricao || "").trim();
    if (!descricao) throw new Error("Descrição obrigatória.");
    const cat = { id: DB.proximoId("categorias"), descricao };
    DB.tabela("categorias").push(cat);
    DB.salvar();
    return cat;
  },
  categoriaAtualizar(id, descricao) {
    const c = DB.tabela("categorias").find((x) => x.id === id);
    if (!c) throw new Error("Categoria não encontrada.");
    c.descricao = descricao;
    DB.salvar();
  },
  categoriaExcluir(id) {
    if (DB.tabela("produtos").some((p) => p.idCategoria === id)) {
      throw new Error("Não é possível excluir: há produtos nessa categoria.");
    }
    const tab = DB.tabela("categorias");
    const i = tab.findIndex((x) => x.id === id);
    if (i >= 0) tab.splice(i, 1);
    DB.salvar();
  },

  // ---------- Produtos ----------
  produtoListar() {
    return DB.tabela("produtos");
  },
  produtosDisponiveisVenda() {
    return DB.tabela("produtos").filter((p) => p.estoque > 0);
  },
  produtoPorId(id) {
    return DB.tabela("produtos").find((p) => p.id === id) || null;
  },
  produtoInserir(descricao, preco, estoque, idCategoria) {
    descricao = (descricao || "").trim();
    if (!descricao) throw new Error("Descrição obrigatória.");
    if (preco < 0) throw new Error("Preço inválido.");
    if (estoque < 0) throw new Error("Estoque inválido.");
    const prod = {
      id: DB.proximoId("produtos"),
      descricao,
      preco: Number(preco),
      estoque: Number(estoque),
      idCategoria: Number(idCategoria),
    };
    DB.tabela("produtos").push(prod);
    DB.salvar();
    return prod;
  },
  produtoAtualizar(id, descricao, preco, estoque, idCategoria) {
    const p = DB.tabela("produtos").find((x) => x.id === id);
    if (!p) throw new Error("Produto não encontrado.");
    Object.assign(p, {
      descricao,
      preco: Number(preco),
      estoque: Number(estoque),
      idCategoria: Number(idCategoria),
    });
    DB.salvar();
  },
  produtoExcluir(id) {
    const tab = DB.tabela("produtos");
    const i = tab.findIndex((x) => x.id === id);
    if (i >= 0) tab.splice(i, 1);
    DB.tabela("favoritos").splice(
      0,
      DB.tabela("favoritos").length,
      ...DB.tabela("favoritos").filter((f) => f.idProduto !== id)
    );
    DB.salvar();
  },
  produtoReajustarPercentual(percentual) {
    const fator = 1 + Number(percentual) / 100;
    DB.tabela("produtos").forEach((p) => {
      p.preco = Math.round(p.preco * fator * 100) / 100;
    });
    DB.salvar();
  },
  produtoCaminhoFoto(id) {
    // As fotos ficam em ../produtos/fotos/. Apenas a foto 1 é .jpeg; o resto .png.
    const ext = id === 1 ? "jpeg" : "png";
    return `../produtos/fotos/${id}.${ext}`;
  },

  // ---------- Precos / Promocoes ----------
  produtoPrecoDetalhes(produto, referencia) {
    const precoBase = Math.round(Number(produto.preco) * 100) / 100;
    const promo = View.promocaoBuscarAtivaPorCategoria(produto.idCategoria, referencia);
    if (!promo) {
      return { precoBase, precoEfetivo: precoBase, emPromocao: false, percentual: 0 };
    }
    const percentual = Number(promo.percentual);
    const precoEfetivo = Math.round(precoBase * (1 - percentual / 100) * 100) / 100;
    return { precoBase, precoEfetivo, emPromocao: true, percentual };
  },
  promocaoListar() {
    return DB.tabela("promocoes");
  },
  promocaoBuscarAtivaPorCategoria(idCategoria, referencia) {
    const hoje = (referencia || new Date().toISOString().slice(0, 10));
    return (
      DB.tabela("promocoes").find(
        (p) =>
          p.idCategoria === idCategoria &&
          p.dataInicio <= hoje &&
          hoje <= p.dataFim
      ) || null
    );
  },
  promocaoInserir(idCategoria, percentual, dataInicio, dataFim) {
    if (dataFim < dataInicio) throw new Error("Data final antes da inicial.");
    const promo = {
      id: DB.proximoId("promocoes"),
      idCategoria: Number(idCategoria),
      percentual: Number(percentual),
      dataInicio,
      dataFim,
    };
    DB.tabela("promocoes").push(promo);
    DB.salvar();
    return promo;
  },
  promocaoExcluir(id) {
    const tab = DB.tabela("promocoes");
    const i = tab.findIndex((x) => x.id === id);
    if (i >= 0) tab.splice(i, 1);
    DB.salvar();
  },

  // ---------- Carrinho (em memoria, sincronizado por cliente) ----------
  adicionar(carrinho, idProduto, quantidade) {
    const produto = View.produtoPorId(idProduto);
    if (!produto) throw new Error("Produto não encontrado.");
    const atual = carrinho[idProduto] || 0;
    if (atual + quantidade > produto.estoque) {
      throw new Error("Quantidade acima do estoque disponível.");
    }
    carrinho[idProduto] = atual + quantidade;
  },
  removerItem(carrinho, idProduto) {
    delete carrinho[idProduto];
  },
  esvaziar(carrinho) {
    Object.keys(carrinho).forEach((k) => delete carrinho[k]);
  },
  montarResumo(carrinho) {
    const itens = [];
    let total = 0;
    for (const [idStr, qtd] of Object.entries(carrinho)) {
      const produto = View.produtoPorId(Number(idStr));
      if (!produto) continue;
      const det = View.produtoPrecoDetalhes(produto);
      const subtotal = Math.round(det.precoEfetivo * qtd * 100) / 100;
      total += subtotal;
      itens.push({ produto, quantidade: qtd, detalhes: det, subtotal });
    }
    return { itens, total: Math.round(total * 100) / 100 };
  },
  sincronizar(idCliente, carrinho) {
    const mapa = View._carrinhosPersistidos();
    mapa[idCliente] = { ...carrinho };
    DB.tabela("_carrinhos").length = 0;
    localStorage.setItem("petshopif_carrinhos", JSON.stringify(mapa));
  },
  carregar(idCliente, carrinho) {
    const mapa = View._carrinhosPersistidos();
    const salvo = mapa[idCliente] || {};
    Object.keys(carrinho).forEach((k) => delete carrinho[k]);
    Object.assign(carrinho, salvo);
  },
  _carrinhosPersistidos() {
    try {
      return JSON.parse(localStorage.getItem("petshopif_carrinhos") || "{}");
    } catch {
      return {};
    }
  },

  // ---------- Checkout ----------
  finalizarCompra(idCliente, carrinho) {
    const resumo = View.montarResumo(carrinho);
    if (resumo.itens.length === 0) throw new Error("Carrinho vazio.");

    // valida e baixa estoque
    for (const item of resumo.itens) {
      if (item.quantidade > item.produto.estoque) {
        throw new Error(`Estoque insuficiente para ${item.produto.descricao}.`);
      }
    }

    const venda = {
      id: DB.proximoId("vendas"),
      data: new Date().toISOString(),
      carrinho: false,
      total: resumo.total,
      idCliente,
    };
    DB.tabela("vendas").push(venda);

    for (const item of resumo.itens) {
      DB.tabela("vendaItens").push({
        id: DB.proximoId("vendaItens"),
        quantidade: item.quantidade,
        preco: item.detalhes.precoEfetivo,
        idVenda: venda.id,
        idProduto: item.produto.id,
      });
      item.produto.estoque -= item.quantidade;
    }

    // cria a entrega da venda (status PENDENTE)
    DB.tabela("entregas").push({
      id: DB.proximoId("entregas"),
      idVenda: venda.id,
      idCliente,
      idEntregador: null,
      status: "PENDENTE",
    });

    View.esvaziar(carrinho);
    View.sincronizar(idCliente, carrinho);
    DB.salvar();
    return venda;
  },

  // ---------- Vendas / Relatorios ----------
  vendaListar() {
    return DB.tabela("vendas");
  },
  listarTodas() {
    return DB.tabela("vendas").map((v) => View._detalharVenda(v));
  },
  listarPorCliente(idCliente) {
    return DB.tabela("vendas")
      .filter((v) => v.idCliente === idCliente)
      .map((v) => View._detalharVenda(v));
  },
  _detalharVenda(venda) {
    const itens = DB.tabela("vendaItens")
      .filter((i) => i.idVenda === venda.id)
      .map((i) => ({
        ...i,
        produto: View.produtoPorId(i.idProduto),
      }));
    const cliente = DB.tabela("clientes").find((c) => c.id === venda.idCliente);
    return { ...venda, itens, cliente };
  },

  // ---------- Favoritos ----------
  favoritar(idCliente, idProduto) {
    const tab = DB.tabela("favoritos");
    if (!tab.some((f) => f.idCliente === idCliente && f.idProduto === idProduto)) {
      tab.push({ id: DB.proximoId("favoritos"), idCliente, idProduto });
      DB.salvar();
    }
  },
  desfavoritar(idCliente, idProduto) {
    const tab = DB.tabela("favoritos");
    const i = tab.findIndex((f) => f.idCliente === idCliente && f.idProduto === idProduto);
    if (i >= 0) {
      tab.splice(i, 1);
      DB.salvar();
    }
  },
  listarProdutosFavoritos(idCliente) {
    const ids = DB.tabela("favoritos")
      .filter((f) => f.idCliente === idCliente)
      .map((f) => f.idProduto);
    return DB.tabela("produtos").filter((p) => ids.includes(p.id));
  },

  // ---------- Entregadores / Entregas ----------
  entregadorCadastrar(nome, fone, login, senha, senha2) {
    nome = (nome || "").trim();
    login = (login || "").trim();
    if (!nome || !fone || !login || !senha) throw new Error("Preencha todos os campos.");
    if (senha.length < 4) throw new Error("A senha deve ter no mínimo 4 caracteres.");
    if (senha !== senha2) throw new Error("As senhas não conferem.");
    if (DB.tabela("entregadores").some((e) => e.login === login)) {
      throw new Error("Login de entregador já existe.");
    }
    const ent = { id: DB.proximoId("entregadores"), nome, fone, login, senha };
    DB.tabela("entregadores").push(ent);
    DB.salvar();
    return ent;
  },
  entregadorListar() {
    return DB.tabela("entregadores");
  },
  entregaListarPedidos() {
    // garante que toda venda tenha uma entrega
    View._garantirEntregas();
    return DB.tabela("entregas").map((e) => View._detalharEntrega(e));
  },
  entregaAlocar(idVenda, idEntregador) {
    const e = DB.tabela("entregas").find((x) => x.idVenda === idVenda);
    if (!e) throw new Error("Entrega não encontrada.");
    e.idEntregador = Number(idEntregador);
    e.status = "ALOCADA";
    DB.salvar();
  },
  entregaListarParaEntregador(idEntregador) {
    View._garantirEntregas();
    return DB.tabela("entregas")
      .filter((e) => e.idEntregador === idEntregador && e.status !== "PENDENTE")
      .map((e) => View._detalharEntrega(e));
  },
  entregaAvancarStatus(idEntrega, idEntregador) {
    const ordem = ["PENDENTE", "ALOCADA", "EM_TRANSPORTE", "ENTREGUE"];
    const e = DB.tabela("entregas").find((x) => x.id === idEntrega);
    if (!e) throw new Error("Entrega não encontrada.");
    if (e.idEntregador !== idEntregador) throw new Error("Entrega não é sua.");
    const i = ordem.indexOf(e.status);
    if (i < ordem.length - 1) e.status = ordem[i + 1];
    DB.salvar();
  },
  entregaAcompanharCliente(idCliente) {
    View._garantirEntregas();
    return DB.tabela("entregas")
      .filter((e) => e.idCliente === idCliente)
      .map((e) => View._detalharEntrega(e));
  },
  _garantirEntregas() {
    const entregas = DB.tabela("entregas");
    let mudou = false;
    for (const v of DB.tabela("vendas")) {
      if (!entregas.some((e) => e.idVenda === v.id)) {
        entregas.push({
          id: DB.proximoId("entregas"),
          idVenda: v.id,
          idCliente: v.idCliente,
          idEntregador: null,
          status: "PENDENTE",
        });
        mudou = true;
      }
    }
    if (mudou) DB.salvar();
  },
  _detalharEntrega(entrega) {
    const venda = DB.tabela("vendas").find((v) => v.id === entrega.idVenda);
    const cliente = DB.tabela("clientes").find((c) => c.id === entrega.idCliente);
    const entregador = DB.tabela("entregadores").find((e) => e.id === entrega.idEntregador);
    return { ...entrega, venda, cliente, entregador };
  },

  // ---------- Admin util ----------
  garantirAdminPadrao() {
    if (!DB.tabela("administradores").some((a) => a.login === "admin")) {
      DB.tabela("administradores").push({ id: DB.proximoId("administradores"), login: "admin", senha: "admin123" });
      DB.salvar();
    }
  },
  resetarBanco() {
    DB.resetar();
    localStorage.removeItem("petshopif_carrinhos");
  },
};
