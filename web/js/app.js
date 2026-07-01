// app.js — UI e roteamento (equivale ao index.py + Templates/*.py do Streamlit).

// ---------------------------------------------------------------------------
// Estado global da aplicacao (equivale ao st.session_state)
// ---------------------------------------------------------------------------
const estado = {
  usuario: null,
  carrinho: {},
  telaLogin: "login", // login | cadastro | entregador
  paginaLoja: "produtos",
  paginaAdmin: "dashboard",
  filtroCategoria: "todas",
};

const app = document.getElementById("app");

// ---------------------------------------------------------------------------
// Utilitarios
// ---------------------------------------------------------------------------
function esc(txt) {
  const div = document.createElement("div");
  div.textContent = txt == null ? "" : String(txt);
  return div.innerHTML;
}

function real(v) {
  return "$" + Number(v).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function dataBr(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  const loc = localeAtual();
  return d.toLocaleDateString(loc) + " " + d.toLocaleTimeString(loc, { hour: "2-digit", minute: "2-digit" });
}

// Pluralizacao consciente de idioma: plural(n, ptSing, ptPlu, enSing, enPlu)
function plural(n, ptSing, ptPlu, enSing, enPlu) {
  if (I18N.lang === "pt") return `${n} ${n === 1 ? ptSing : ptPlu}`;
  return `${n} ${n === 1 ? enSing : enPlu}`;
}

function toast(msg, tipo = "sucesso", icone = "") {
  const area = document.getElementById("toast-area");
  const el = document.createElement("div");
  el.className = "toast " + tipo;
  el.innerHTML = `<span>${icone || (tipo === "erro" ? "⚠️" : "✅")}</span><span>${esc(t(msg))}</span>`;
  area.appendChild(el);
  setTimeout(() => {
    el.style.opacity = "0";
    el.style.transition = "opacity .3s ease";
    setTimeout(() => el.remove(), 300);
  }, 2800);
}

function fotoProduto(id) {
  const src = View.produtoCaminhoFoto(id);
  return `<img src="${src}" alt="Foto" onerror="this.parentNode.innerHTML='<span class=\\'icone\\'>🐾</span>'" />`;
}

function setBodyClasse(cls) {
  document.body.className = cls || "";
}

// Botao flutuante de troca de idioma (presente em todas as telas)
function garantirBotaoIdioma() {
  let b = document.getElementById("btn-idioma");
  if (!b) {
    b = document.createElement("button");
    b.id = "btn-idioma";
    b.className = "btn-idioma";
    document.body.appendChild(b);
    b.onclick = () => { I18N.toggle(); render(); };
  }
  b.innerHTML = I18N.lang === "pt" ? "🌐 EN" : "🌐 PT";
  b.title = I18N.lang === "pt" ? "Translate to English" : "Traduzir para Português";
}

// ---------------------------------------------------------------------------
// Roteamento principal
// ---------------------------------------------------------------------------
function render() {
  View.garantirAdminPadrao();
  garantirBotaoIdioma();
  document.documentElement.lang = I18N.lang === "pt" ? "pt-BR" : "en";

  if (!estado.usuario) return telaLogin();
  if (estado.usuario.admin) return telaAdmin();
  if (estado.usuario.tipo === "entregador") return telaEntregador();
  return telaLoja();
}

function sair() {
  estado.usuario = null;
  estado.carrinho = {};
  estado.telaLogin = "login";
  estado.paginaLoja = "produtos";
  estado.paginaAdmin = "dashboard";
  render();
}

// ===========================================================================
// TELA DE LOGIN / CADASTRO / ENTREGADOR
// ===========================================================================
function telaLogin() {
  setBodyClasse("tela-login");
  const modo = estado.telaLogin;

  let banner, corpo, rodape;
  if (modo === "cadastro") {
    banner = [t("CRIAR CONTA"), t("Cadastre-se no Pet Shop IF")];
    corpo = formCadastro();
    rodape = rodapeSimples(t("Já possui uma conta?"), t("Entrar"), () => { estado.telaLogin = "login"; render(); });
  } else if (modo === "entregador") {
    banner = [t("SOU ENTREGADOR"), t("Cadastre-se para realizar entregas")];
    corpo = formEntregador();
    rodape = rodapeSimples(t("Já tem cadastro de entregador?"), t("Entrar"), () => { estado.telaLogin = "login"; render(); });
  } else {
    banner = [t("BEM-VINDO(A)"), t("Entre na sua conta Pet Shop IF")];
    corpo = formLogin();
    rodape = `
      <div class="login-divider"></div>
      <p class="login-rodape">${t("Não tem conta?")}</p>
      <div class="login-extra">
        <button class="btn-secundario" id="ir-cadastro">${t("Abrir conta")}</button>
        <button class="btn-secundario" id="ir-entregador">${t("Sou entregador")}</button>
      </div>`;
  }

  app.innerHTML = `
    <div class="login-wrap">
      <div class="login-top">
        <div class="icone">🐾</div>
        <h1>${banner[0]}</h1>
        <p>${banner[1]}</p>
      </div>
      <div id="login-msg"></div>
      ${corpo}
      ${rodape}
    </div>`;

  if (modo === "login") {
    document.getElementById("form-login").onsubmit = (e) => {
      e.preventDefault();
      const u = View.autenticar(campo("login-email"), campo("login-senha"));
      if (!u) return msgErro("E-mail/login ou senha inválidos.");
      estado.usuario = u;
      estado.carrinho = {};
      if (!u.admin && u.tipo === "cliente") View.carregar(u.id, estado.carrinho);
      render();
      const oi = I18N.lang === "pt" ? `Bem-vindo(a), ${u.nome}!` : `Welcome, ${u.nome}!`;
      toast(oi, "sucesso", "🐾");
    };
    document.getElementById("ir-cadastro").onclick = () => { estado.telaLogin = "cadastro"; render(); };
    document.getElementById("ir-entregador").onclick = () => { estado.telaLogin = "entregador"; render(); };
  } else if (modo === "cadastro") {
    document.getElementById("form-cadastro").onsubmit = (e) => {
      e.preventDefault();
      try {
        const c = View.abrirConta(campo("cad-nome"), campo("cad-email"), campo("cad-fone"), campo("cad-senha"), campo("cad-senha2"));
        const m = I18N.lang === "pt"
          ? `Conta criada! Seu ID de cliente é ${c.id}. Faça login.`
          : `Account created! Your customer ID is ${c.id}. Please sign in.`;
        msgSucesso(m);
      } catch (err) { msgErro(err.message); }
    };
  } else {
    document.getElementById("form-entregador").onsubmit = (e) => {
      e.preventDefault();
      try {
        const en = View.entregadorCadastrar(campo("ent-nome"), campo("ent-fone"), campo("ent-login"), campo("ent-senha"), campo("ent-senha2"));
        const m = I18N.lang === "pt"
          ? `Cadastro feito! Entre com o login '${en.login}'.`
          : `Registration complete! Sign in with the login '${en.login}'.`;
        msgSucesso(m);
      } catch (err) { msgErro(err.message); }
    };
  }
}

function campo(id) { return document.getElementById(id).value; }
function msgErro(m) { document.getElementById("login-msg").innerHTML = `<div class="msg-erro">${esc(t(m))}</div>`; }
function msgSucesso(m) { document.getElementById("login-msg").innerHTML = `<div class="msg-sucesso-box">${esc(m)}</div>`; }

function rodapeSimples(texto, botao, onclick) {
  const id = "rodape-btn-" + Math.random().toString(36).slice(2);
  setTimeout(() => { const b = document.getElementById(id); if (b) b.onclick = onclick; }, 0);
  return `
    <div class="login-divider"></div>
    <p class="login-rodape">${texto}</p>
    <div class="login-extra"><button class="btn-secundario" id="${id}">${botao}</button></div>`;
}

function formLogin() {
  return `
    <form class="login-form" id="form-login">
      <label>${t("E-mail ou login")}</label>
      <input id="login-email" placeholder="${t("Digite seu e-mail ou login")}" required />
      <label>${t("Senha")}</label>
      <input id="login-senha" type="password" placeholder="${t("Digite sua senha")}" required />
      <button class="btn-primario" type="submit">${t("ENTRAR")}</button>
    </form>`;
}

function formCadastro() {
  return `
    <form class="login-form" id="form-cadastro">
      <label>${t("Nome completo")}</label><input id="cad-nome" placeholder="${t("Seu nome")}" required />
      <label>${t("E-mail")}</label><input id="cad-email" type="email" placeholder="seu@email.com" required />
      <label>${t("Telefone")}</label><input id="cad-fone" placeholder="${t("(00) 00000-0000")}" required />
      <label>${t("Senha")}</label><input id="cad-senha" type="password" placeholder="${t("Mínimo 4 caracteres")}" required />
      <label>${t("Confirmar senha")}</label><input id="cad-senha2" type="password" placeholder="${t("Repita a senha")}" required />
      <button class="btn-primario" type="submit">${t("CRIAR CONTA")}</button>
    </form>`;
}

function formEntregador() {
  return `
    <form class="login-form" id="form-entregador">
      <label>${t("Nome completo")}</label><input id="ent-nome" placeholder="${t("Seu nome")}" required />
      <label>${t("Telefone")}</label><input id="ent-fone" placeholder="${t("(00) 00000-0000")}" required />
      <label>${t("Login")}</label><input id="ent-login" placeholder="${t("Crie um login de acesso")}" required />
      <label>${t("Senha")}</label><input id="ent-senha" type="password" placeholder="${t("Mínimo 4 caracteres")}" required />
      <label>${t("Confirmar senha")}</label><input id="ent-senha2" type="password" placeholder="${t("Repita a senha")}" required />
      <button class="btn-primario" type="submit">${t("CADASTRAR")}</button>
    </form>`;
}

// ===========================================================================
// LOJA DO CLIENTE
// ===========================================================================
const PAGINAS_LOJA = [
  ["produtos", "Produtos"],
  ["favoritos", "Favoritos"],
  ["carrinho", "Carrinho"],
  ["compras", "Compras"],
  ["perfil", "Perfil"],
];

function telaLoja() {
  setBodyClasse("");
  const menu = PAGINAS_LOJA.map(
    ([id, lbl]) => `<button class="nav-item ${estado.paginaLoja === id ? "ativo" : ""}" data-pag="${id}">${t(lbl)}</button>`
  ).join("");

  let conteudo = "";
  switch (estado.paginaLoja) {
    case "produtos": conteudo = paginaProdutos(); break;
    case "favoritos": conteudo = paginaFavoritos(); break;
    case "carrinho": conteudo = paginaCarrinho(); break;
    case "compras": conteudo = paginaCompras(); break;
    case "perfil": conteudo = paginaPerfil(); break;
  }

  app.innerHTML = `
    <div class="navbar navbar-loja">
      <div class="nav-logo">🐾 Pet Shop IF</div>
      <div class="nav-menu">${menu}</div>
      <button class="nav-sair" id="btn-sair">${t("Sair")}</button>
    </div>
    <div class="container">${conteudo}</div>`;

  document.querySelectorAll(".nav-item").forEach((b) => {
    b.onclick = () => { estado.paginaLoja = b.dataset.pag; render(); };
  });
  document.getElementById("btn-sair").onclick = sair;

  ligarEventosLoja();
}

function mapaCategorias() {
  const m = {};
  View.categoriaListar().forEach((c) => (m[c.id] = c.descricao));
  return m;
}

function htmlPreco(det) {
  if (det.emPromocao) {
    return `
      <div>
        <span class="preco-cheio riscado">${real(det.precoBase)}</span>
        <div class="preco-promo-linha">
          <span class="preco-oferta">${real(det.precoEfetivo)}</span>
          <span class="badge-off">-${det.percentual.toFixed(0)}%</span>
        </div>
      </div>`;
  }
  return `<div><span class="preco-cheio">${real(det.precoBase)}</span></div>`;
}

function htmlEstoque(estoque) {
  if (estoque <= 3) {
    const txt = I18N.lang === "pt" ? `Últimas ${estoque} unidades` : `Only ${estoque} left`;
    return `<p class="estoque-linha baixo">${txt}</p>`;
  }
  return `<p class="estoque-linha">${t("Em estoque")}</p>`;
}

function cardProduto(produto, cats, favIds) {
  const det = View.produtoPrecoDetalhes(produto);
  const ehFav = favIds.has(produto.id);
  const cat = tCat(cats[produto.idCategoria] || "");
  const nome = tProd(produto);
  return `
    <div class="card-produto">
      <div class="card-foto">
        ${fotoProduto(produto.id)}
        <button class="btn-fav ${ehFav ? "ativo" : ""}" data-fav="${produto.id}" title="${ehFav ? t("Removido dos favoritos.") : t("Adicionado aos favoritos!")}">${ehFav ? "♥" : "♡"}</button>
      </div>
      <div class="card-corpo">
        <div class="card-titulo" title="${esc(nome)}">${esc(nome)}</div>
        <div><span class="cat-chip">${esc(cat)}</span></div>
        ${htmlPreco(det)}
        ${htmlEstoque(produto.estoque)}
      </div>
      <div class="card-rodape">
        <button class="btn-comprar" data-add="${produto.id}">${t("🛒 Adicionar")}</button>
      </div>
    </div>`;
}

function paginaProdutos() {
  const cats = mapaCategorias();
  const favIds = new Set(View.listarProdutosFavoritos(estado.usuario.id).map((p) => p.id));
  const lista = View.categoriaListar();
  let produtos = View.produtosDisponiveisVenda();

  if (estado.filtroCategoria !== "todas") {
    produtos = produtos.filter((p) => p.idCategoria === Number(estado.filtroCategoria));
  }

  const opcoes =
    `<option value="todas">${t("Todas as categorias")}</option>` +
    lista.map((c) => `<option value="${c.id}" ${estado.filtroCategoria == c.id ? "selected" : ""}>${esc(tCat(c.descricao))}</option>`).join("");

  const n = produtos.length;
  const contador = `${n} ${n === 1 ? t("produto") : t("produtos")}`;
  const grid = produtos.length
    ? `<div class="grid-produtos">${produtos.map((p) => cardProduto(p, cats, favIds)).join("")}</div>`
    : `<div class="vazio"><span class="icone">🔍</span>${t("Nenhum produto encontrado com esse filtro.")}</div>`;

  return `
    <div class="loja-topo">
      <span class="eyebrow">${t("Catálogo")}</span>
      <h2>${t("Produtos disponíveis")}</h2>
      <p>${t("Escolha com carinho o melhor para o seu pet")}</p>
    </div>
    <div class="loja-filtro">
      <div class="campo">
        <label>${t("Filtrar por categoria")}</label>
        <select id="filtro-cat">${opcoes}</select>
      </div>
      <span class="loja-contador">📦 ${contador}</span>
    </div>
    ${grid}`;
}

function paginaFavoritos() {
  const cats = mapaCategorias();
  const favs = View.listarProdutosFavoritos(estado.usuario.id);
  const favIds = new Set(favs.map((p) => p.id));
  if (!favs.length) {
    return `<div class="vazio"><span class="icone">🤍</span>${t("Você ainda não favoritou nenhum produto.")}</div>`;
  }
  return `
    <p class="section-title">${t("Meus favoritos")}</p>
    <div class="grid-produtos">${favs.map((p) => cardProduto(p, cats, favIds)).join("")}</div>`;
}

function paginaCarrinho() {
  const resumo = View.montarResumo(estado.carrinho);
  if (!resumo.itens.length) {
    return `<div class="vazio"><span class="icone">🛒</span>${t("Seu carrinho está vazio.")}<br/><br/>
      <button class="btn-mini solido" id="ir-produtos">${t("Ver produtos")}</button></div>`;
  }
  const itens = resumo.itens
    .map(
      (it) => `
      <div class="item-carrinho">
        <div class="item-foto">${fotoProduto(it.produto.id)}</div>
        <div class="item-info">
          <div class="nome">${esc(tProd(it.produto))}</div>
          <div class="sub">${real(it.detalhes.precoEfetivo)} ${t("cada")}${it.detalhes.emPromocao ? " · " + t("promoção") : ""}</div>
        </div>
        <div class="item-qtd">
          <button data-menos="${it.produto.id}">−</button>
          <span>${it.quantidade}</span>
          <button data-mais="${it.produto.id}">+</button>
        </div>
        <div class="item-subtotal">${real(it.subtotal)}</div>
        <button class="btn-remover" data-rem="${it.produto.id}" title="${t("Excluir")}">🗑️</button>
      </div>`
    )
    .join("");
  return `
    <p class="section-title">${t("Meu carrinho")}</p>
    <div class="card">
      ${itens}
      <div class="resumo-total"><span>${t("Total")}</span><span class="valor">${real(resumo.total)}</span></div>
      <div class="acoes-carrinho">
        <button class="btn-secundario" id="esvaziar">${t("Esvaziar")}</button>
        <button class="btn-primario" id="finalizar" style="margin-top:0">${t("Finalizar compra")}</button>
      </div>
    </div>`;
}

function paginaCompras() {
  const vendas = View.listarPorCliente(estado.usuario.id).sort((a, b) => b.id - a.id);
  const entregas = {};
  View.entregaAcompanharCliente(estado.usuario.id).forEach((e) => (entregas[e.idVenda] = e));
  if (!vendas.length) {
    return `<div class="vazio"><span class="icone">📦</span>${t("Você ainda não fez nenhuma compra.")}</div>`;
  }
  const labelStatus = {
    PENDENTE: t("Aguardando alocação"),
    ALOCADA: t("Entregador a caminho"),
    EM_TRANSPORTE: t("Em transporte"),
    ENTREGUE: t("Entregue"),
  };
  return `<p class="section-title">${t("Minhas compras")}</p>` + vendas
    .map((v) => {
      const ent = entregas[v.id];
      const itens = v.itens
        .map((i) => `<div class="pedido-item"><span>${i.quantidade}× ${esc(i.produto ? tProd(i.produto) : t("Produto removido"))}</span><span>${real(i.preco * i.quantidade)}</span></div>`)
        .join("");
      const statusBadge = ent
        ? `<span class="badge badge-status badge-${ent.status}">${labelStatus[ent.status]}</span>`
        : "";
      return `
        <div class="pedido">
          <div class="pedido-topo">
            <div><span class="num">${t("Pedido")} #${v.id}</span> <span class="data">${dataBr(v.data)}</span></div>
            ${statusBadge}
          </div>
          <div class="pedido-corpo">
            ${itens}
            <div class="pedido-total"><span>${t("Total")}</span><span class="valor">${real(v.total)}</span></div>
          </div>
        </div>`;
    })
    .join("");
}

function paginaPerfil() {
  const c = View.clienteListar().find((x) => x.id === estado.usuario.id);
  if (!c) return `<div class="vazio">${t("Cliente não encontrado.")}</div>`;
  return `
    <p class="section-title">${t("Meu perfil")}</p>
    <div class="form-box perfil-box">
      <h4>${t("Dados da conta")}</h4>
      <div class="form-grid full">
        <div class="campo-form"><label>${t("Nome")}</label><input id="perfil-nome" value="${esc(c.nome)}" /></div>
        <div class="campo-form"><label>${t("E-mail")}</label><input id="perfil-email" value="${esc(c.email)}" /></div>
        <div class="campo-form"><label>${t("Telefone")}</label><input id="perfil-fone" value="${esc(c.fone)}" /></div>
        <div class="campo-form"><label>${t("Senha")}</label><input id="perfil-senha" type="password" value="${esc(c.senha)}" /></div>
      </div>
      <div class="btns-linha">
        <button class="btn-add" id="salvar-perfil">${t("Salvar alterações")}</button>
      </div>
    </div>`;
}

function ligarEventosLoja() {
  const id = estado.usuario.id;

  const filtro = document.getElementById("filtro-cat");
  if (filtro) filtro.onchange = () => { estado.filtroCategoria = filtro.value; render(); };

  document.querySelectorAll("[data-add]").forEach((b) => {
    b.onclick = () => {
      try {
        View.adicionar(estado.carrinho, Number(b.dataset.add), 1);
        View.sincronizar(id, estado.carrinho);
        toast("Produto adicionado ao carrinho!", "sucesso", "🛒");
        render();
      } catch (e) { toast(e.message, "erro"); }
    };
  });

  document.querySelectorAll("[data-fav]").forEach((b) => {
    b.onclick = () => {
      const pid = Number(b.dataset.fav);
      const favs = new Set(View.listarProdutosFavoritos(id).map((p) => p.id));
      if (favs.has(pid)) { View.desfavoritar(id, pid); toast("Removido dos favoritos.", "sucesso", "🤍"); }
      else { View.favoritar(id, pid); toast("Adicionado aos favoritos!", "sucesso", "❤️"); }
      render();
    };
  });

  document.querySelectorAll("[data-mais]").forEach((b) => {
    b.onclick = () => {
      try { View.adicionar(estado.carrinho, Number(b.dataset.mais), 1); View.sincronizar(id, estado.carrinho); render(); }
      catch (e) { toast(e.message, "erro"); }
    };
  });
  document.querySelectorAll("[data-menos]").forEach((b) => {
    b.onclick = () => {
      const pid = Number(b.dataset.menos);
      const atual = estado.carrinho[pid] || 0;
      if (atual <= 1) delete estado.carrinho[pid];
      else estado.carrinho[pid] = atual - 1;
      View.sincronizar(id, estado.carrinho);
      render();
    };
  });
  document.querySelectorAll("[data-rem]").forEach((b) => {
    b.onclick = () => { View.removerItem(estado.carrinho, Number(b.dataset.rem)); View.sincronizar(id, estado.carrinho); render(); };
  });

  const esvaziar = document.getElementById("esvaziar");
  if (esvaziar) esvaziar.onclick = () => { View.esvaziar(estado.carrinho); View.sincronizar(id, estado.carrinho); render(); };

  const finalizar = document.getElementById("finalizar");
  if (finalizar) finalizar.onclick = () => {
    try {
      const v = View.finalizarCompra(id, estado.carrinho);
      const m = I18N.lang === "pt" ? `Compra finalizada! Pedido #${v.id}` : `Order placed! Order #${v.id}`;
      toast(m, "sucesso", "🎉");
      estado.paginaLoja = "compras";
      render();
    } catch (e) { toast(e.message, "erro"); }
  };

  const irProdutos = document.getElementById("ir-produtos");
  if (irProdutos) irProdutos.onclick = () => { estado.paginaLoja = "produtos"; render(); };

  const salvar = document.getElementById("salvar-perfil");
  if (salvar) salvar.onclick = () => {
    try {
      View.clienteAtualizar(id, campo("perfil-nome"), campo("perfil-email"), campo("perfil-fone"), campo("perfil-senha"));
      estado.usuario.nome = campo("perfil-nome");
      toast("Perfil atualizado!", "sucesso");
      render();
    } catch (e) { toast(e.message, "erro"); }
  };
}

// ===========================================================================
// PAINEL DO ENTREGADOR
// ===========================================================================
function telaEntregador() {
  setBodyClasse("tela-entregador");
  const id = estado.usuario.id;
  const entregas = View.entregaListarParaEntregador(id);
  const labelStatus = { ALOCADA: t("Iniciar transporte"), EM_TRANSPORTE: t("Marcar como entregue"), ENTREGUE: t("Entregue") };
  const saudacao = I18N.lang === "pt" ? `Olá, ${esc(estado.usuario.nome)} 🛵` : `Hi, ${esc(estado.usuario.nome)} 🛵`;

  const linhas = entregas.length
    ? entregas
        .map((e) => `
        <tr>
          <td class="col-destaque">#${e.venda ? e.venda.id : "?"}</td>
          <td>${esc(e.cliente ? e.cliente.nome : "-")}</td>
          <td>${real(e.venda ? e.venda.total : 0)}</td>
          <td><span class="badge badge-status badge-${e.status}">${t(e.status.replace("_", " "))}</span></td>
          <td class="direita">
            ${e.status !== "ENTREGUE" ? `<button class="btn-mini solido" data-avancar="${e.id}">${labelStatus[e.status]}</button>` : "✓"}
          </td>
        </tr>`)
        .join("")
    : `<tr><td colspan="5" style="text-align:center;color:#aaa;padding:2rem">${t("Nenhuma entrega alocada para você ainda.")}</td></tr>`;

  app.innerHTML = `
    <div class="navbar navbar-admin">
      <div class="nav-logo">🐾 <span class="col"><span>Pet Shop IF</span><small>${t("Painel Entregador")}</small></span></div>
      <div class="nav-menu"></div>
      <button class="nav-sair" id="btn-sair">${t("Sair")}</button>
    </div>
    <div class="container container-admin">
      <div class="admin-hero"><h2>${saudacao}</h2><p>${t("Suas entregas alocadas")}</p></div>
      <div class="card">
        <div class="card-titulo-sec">${t("Minhas entregas")}</div>
        <table class="tabela">
          <thead><tr><th>${t("Pedido")}</th><th>${t("Cliente")}</th><th>${t("Total")}</th><th>${t("Status")}</th><th class="direita">${t("Ação")}</th></tr></thead>
          <tbody>${linhas}</tbody>
        </table>
      </div>
    </div>`;

  document.getElementById("btn-sair").onclick = sair;
  document.querySelectorAll("[data-avancar]").forEach((b) => {
    b.onclick = () => {
      try { View.entregaAvancarStatus(Number(b.dataset.avancar), id); toast("Status atualizado!", "sucesso"); render(); }
      catch (e) { toast(e.message, "erro"); }
    };
  });
}

// ===========================================================================
// PAINEL ADMIN
// ===========================================================================
const PAGINAS_ADMIN = [
  ["dashboard", "Início"],
  ["clientes", "Clientes"],
  ["categorias", "Categorias"],
  ["produtos", "Produtos"],
  ["promocoes", "Promoções"],
  ["vendas", "Vendas"],
  ["entregas", "Entregas"],
];

function telaAdmin() {
  setBodyClasse("tela-admin");
  const menu = PAGINAS_ADMIN.map(
    ([id, lbl]) => `<button class="nav-item ${estado.paginaAdmin === id ? "ativo" : ""}" data-pag="${id}">${t(lbl)}</button>`
  ).join("");

  let conteudo = "";
  switch (estado.paginaAdmin) {
    case "dashboard": conteudo = adminDashboard(); break;
    case "clientes": conteudo = adminClientes(); break;
    case "categorias": conteudo = adminCategorias(); break;
    case "produtos": conteudo = adminProdutos(); break;
    case "promocoes": conteudo = adminPromocoes(); break;
    case "vendas": conteudo = adminVendas(); break;
    case "entregas": conteudo = adminEntregas(); break;
  }

  app.innerHTML = `
    <div class="navbar navbar-admin">
      <div class="nav-logo">🐾 <span class="col"><span>Pet Shop IF</span><small>${t("Painel Admin")}</small></span></div>
      <div class="nav-menu">${menu}</div>
      <button class="nav-sair" id="btn-sair">${t("Sair")}</button>
    </div>
    <div class="container container-admin">${conteudo}</div>`;

  document.querySelectorAll(".nav-item").forEach((b) => {
    b.onclick = () => { estado.paginaAdmin = b.dataset.pag; render(); };
  });
  document.getElementById("btn-sair").onclick = sair;

  ligarEventosAdmin();
}

function adminDashboard() {
  const produtos = View.produtoListar();
  const clientes = View.clienteListar();
  const vendas = View.vendaListar();
  const faturamento = vendas.reduce((s, v) => s + v.total, 0);
  const baixoEstoque = produtos.filter((p) => p.estoque <= 3);
  const ultimas = View.listarTodas().sort((a, b) => b.id - a.id).slice(0, 5);

  const linhasVendas = ultimas.length
    ? ultimas.map((v) => `<tr><td class="col-destaque">#${v.id}</td><td>${esc(v.cliente ? v.cliente.nome : "-")}</td><td>${dataBr(v.data)}</td><td class="direita col-destaque">${real(v.total)}</td></tr>`).join("")
    : `<tr><td colspan="4" style="text-align:center;color:#aaa;padding:1.5rem">${t("Nenhuma venda ainda.")}</td></tr>`;

  const unid = (n) => I18N.lang === "pt" ? `${n} un.` : `${n} left`;
  const linhasEstoque = baixoEstoque.length
    ? baixoEstoque.map((p) => `<tr><td>${esc(tProd(p))}</td><td class="direita"><span class="badge">${unid(p.estoque)}</span></td></tr>`).join("")
    : `<tr><td colspan="2" style="text-align:center;color:#aaa;padding:1.5rem">${t("Estoque saudável 🎉")}</td></tr>`;

  return `
    <div class="admin-hero"><h2>${t("Painel administrativo")}</h2><p>${t("Visão geral do Pet Shop IF")}</p></div>
    <div class="stat-grid">
      <div class="stat"><div class="label">${t("Produtos")}</div><div class="valor">${produtos.length}</div></div>
      <div class="stat"><div class="label">${t("Clientes")}</div><div class="valor">${clientes.length}</div></div>
      <div class="stat"><div class="label">${t("Vendas")}</div><div class="valor">${vendas.length}</div></div>
      <div class="stat"><div class="label">${t("Faturamento")}</div><div class="valor">${real(faturamento)}</div></div>
    </div>
    <div class="card">
      <div class="card-titulo-sec">${t("Últimas vendas")}</div>
      <table class="tabela"><thead><tr><th>${t("Pedido")}</th><th>${t("Cliente")}</th><th>${t("Data")}</th><th class="direita">${t("Total")}</th></tr></thead><tbody>${linhasVendas}</tbody></table>
    </div>
    <div class="card">
      <div class="card-titulo-sec">${t("Estoque baixo (≤ 3)")}</div>
      <table class="tabela"><thead><tr><th>${t("Produto")}</th><th class="direita">${t("Estoque")}</th></tr></thead><tbody>${linhasEstoque}</tbody></table>
    </div>`;
}

function adminClientes() {
  const clientes = View.clienteListar();
  const linhas = clientes
    .map((c) => `
      <tr>
        <td>${c.id}</td><td>${esc(c.nome)}</td><td>${esc(c.email)}</td><td>${esc(c.fone)}</td>
        <td class="direita"><button class="btn-mini perigo" data-del-cliente="${c.id}">${t("Excluir")}</button></td>
      </tr>`)
    .join("");
  return `
    <div class="admin-hero"><h2>${t("Clientes")}</h2><p>${plural(clientes.length, "cliente cadastrado", "clientes cadastrados", "customer registered", "customers registered")}</p></div>
    <div class="form-box">
      <h4>${t("Novo cliente")}</h4>
      <div class="form-grid">
        <div class="campo-form"><label>${t("Nome")}</label><input id="cli-nome" /></div>
        <div class="campo-form"><label>${t("E-mail")}</label><input id="cli-email" /></div>
        <div class="campo-form"><label>${t("Telefone")}</label><input id="cli-fone" /></div>
        <div class="campo-form"><label>${t("Senha")}</label><input id="cli-senha" /></div>
      </div>
      <div class="btns-linha"><button class="btn-add" id="add-cliente">${t("Adicionar cliente")}</button></div>
    </div>
    <div class="card">
      <table class="tabela"><thead><tr><th>ID</th><th>${t("Nome")}</th><th>${t("E-mail")}</th><th>${t("Telefone")}</th><th class="direita">${t("Ações")}</th></tr></thead><tbody>${linhas}</tbody></table>
    </div>`;
}

function adminCategorias() {
  const cats = View.categoriaListar();
  const linhas = cats
    .map((c) => `
      <tr>
        <td>${c.id}</td>
        <td><input class="edit-cat" data-id="${c.id}" value="${esc(c.descricao)}" style="border:1px solid #eee;border-radius:8px;padding:.35rem .6rem;width:100%" /></td>
        <td class="direita">
          <button class="btn-mini" data-save-cat="${c.id}">${t("Salvar")}</button>
          <button class="btn-mini perigo" data-del-cat="${c.id}">${t("Excluir")}</button>
        </td>
      </tr>`)
    .join("");
  return `
    <div class="admin-hero"><h2>${t("Categorias")}</h2><p>${plural(cats.length, "categoria", "categorias", "category", "categories")}</p></div>
    <div class="form-box">
      <h4>${t("Nova categoria")}</h4>
      <div class="form-grid"><div class="campo-form"><label>${t("Descrição")}</label><input id="cat-desc" /></div></div>
      <div class="btns-linha"><button class="btn-add" id="add-cat">${t("Adicionar categoria")}</button></div>
    </div>
    <div class="card">
      <table class="tabela"><thead><tr><th>ID</th><th>${t("Descrição")}</th><th class="direita">${t("Ações")}</th></tr></thead><tbody>${linhas}</tbody></table>
    </div>`;
}

function adminProdutos() {
  const cats = View.categoriaListar();
  const mapa = mapaCategorias();
  const produtos = View.produtoListar();
  const opts = cats.map((c) => `<option value="${c.id}">${esc(tCat(c.descricao))}</option>`).join("");
  const linhas = produtos
    .map((p) => `
      <tr>
        <td>${p.id}</td><td>${esc(tProd(p))}</td><td>${esc(tCat(mapa[p.idCategoria] || "-"))}</td>
        <td>${real(p.preco)}</td><td>${p.estoque}</td>
        <td class="direita"><button class="btn-mini perigo" data-del-prod="${p.id}">${t("Excluir")}</button></td>
      </tr>`)
    .join("");
  return `
    <div class="admin-hero"><h2>${t("Produtos")}</h2><p>${plural(produtos.length, "produto", "produtos", "product", "products")} ${t("no catálogo")}</p></div>
    <div class="form-box">
      <h4>${t("Novo produto")}</h4>
      <div class="form-grid">
        <div class="campo-form"><label>${t("Descrição")}</label><input id="prod-desc" /></div>
        <div class="campo-form"><label>${t("Categoria")}</label><select id="prod-cat">${opts}</select></div>
        <div class="campo-form"><label>${t("Preço")}</label><input id="prod-preco" type="number" step="0.01" min="0" /></div>
        <div class="campo-form"><label>${t("Estoque")}</label><input id="prod-estoque" type="number" min="0" /></div>
      </div>
      <div class="btns-linha">
        <button class="btn-add" id="add-prod">${t("Adicionar produto")}</button>
        <button class="btn-mini" id="reajustar">${t("Reajustar preços (%)")}</button>
      </div>
    </div>
    <div class="card">
      <table class="tabela"><thead><tr><th>ID</th><th>${t("Descrição")}</th><th>${t("Categoria")}</th><th>${t("Preço")}</th><th>${t("Estoque")}</th><th class="direita">${t("Ações")}</th></tr></thead><tbody>${linhas}</tbody></table>
    </div>`;
}

function adminPromocoes() {
  const cats = View.categoriaListar();
  const mapa = mapaCategorias();
  const promos = View.promocaoListar();
  const opts = cats.map((c) => `<option value="${c.id}">${esc(tCat(c.descricao))}</option>`).join("");
  const hoje = new Date().toISOString().slice(0, 10);
  const linhas = promos.length
    ? promos.map((p) => {
        const ativa = p.dataInicio <= hoje && hoje <= p.dataFim;
        return `<tr>
          <td>${p.id}</td><td>${esc(tCat(mapa[p.idCategoria] || "-"))}</td><td>${p.percentual.toFixed(0)}%</td>
          <td>${p.dataInicio}</td><td>${p.dataFim}</td>
          <td><span class="badge badge-status badge-${ativa ? "ENTREGUE" : "PENDENTE"}">${ativa ? t("Ativa") : t("Inativa")}</span></td>
          <td class="direita"><button class="btn-mini perigo" data-del-promo="${p.id}">${t("Excluir")}</button></td>
        </tr>`;
      }).join("")
    : `<tr><td colspan="7" style="text-align:center;color:#aaa;padding:1.5rem">${t("Nenhuma promoção.")}</td></tr>`;
  return `
    <div class="admin-hero"><h2>${t("Promoções")}</h2><p>${t("Descontos por categoria")}</p></div>
    <div class="form-box">
      <h4>${t("Nova promoção")}</h4>
      <div class="form-grid">
        <div class="campo-form"><label>${t("Categoria")}</label><select id="promo-cat">${opts}</select></div>
        <div class="campo-form"><label>${t("Percentual (%)")}</label><input id="promo-perc" type="number" min="1" max="90" /></div>
        <div class="campo-form"><label>${t("Data início")}</label><input id="promo-ini" type="date" value="${hoje}" /></div>
        <div class="campo-form"><label>${t("Data fim")}</label><input id="promo-fim" type="date" value="${hoje}" /></div>
      </div>
      <div class="btns-linha"><button class="btn-add" id="add-promo">${t("Adicionar promoção")}</button></div>
    </div>
    <div class="card">
      <table class="tabela"><thead><tr><th>ID</th><th>${t("Categoria")}</th><th>%</th><th>${t("Início")}</th><th>${t("Fim")}</th><th>${t("Status")}</th><th class="direita">${t("Ações")}</th></tr></thead><tbody>${linhas}</tbody></table>
    </div>`;
}

function adminVendas() {
  const vendas = View.listarTodas().sort((a, b) => b.id - a.id);
  const total = vendas.reduce((s, v) => s + v.total, 0);
  const linhas = vendas.length
    ? vendas.map((v) => `
        <tr>
          <td class="col-destaque">#${v.id}</td>
          <td>${esc(v.cliente ? v.cliente.nome : "-")}</td>
          <td>${dataBr(v.data)}</td>
          <td>${plural(v.itens.reduce((s, i) => s + i.quantidade, 0), "item", "itens", "item", "items")}</td>
          <td class="direita col-destaque">${real(v.total)}</td>
        </tr>`).join("")
    : `<tr><td colspan="5" style="text-align:center;color:#aaa;padding:1.5rem">${t("Nenhuma venda registrada.")}</td></tr>`;
  return `
    <div class="admin-hero"><h2>${t("Vendas")}</h2><p>${t("Relatório de vendas — total:")} <strong>${real(total)}</strong></p></div>
    <div class="card">
      <table class="tabela"><thead><tr><th>${t("Pedido")}</th><th>${t("Cliente")}</th><th>${t("Data")}</th><th>${t("Itens")}</th><th class="direita">${t("Total")}</th></tr></thead><tbody>${linhas}</tbody></table>
    </div>`;
}

function adminEntregas() {
  const pedidos = View.entregaListarPedidos().sort((a, b) => b.idVenda - a.idVenda);
  const entregadores = View.entregadorListar();
  const optsEnt = entregadores.map((e) => `<option value="${e.id}">${esc(e.nome)}</option>`).join("");
  const linhas = pedidos.length
    ? pedidos.map((e) => {
        const acao =
          e.status === "PENDENTE"
            ? `<select class="sel-ent" data-venda="${e.idVenda}" style="border:1px solid #eee;border-radius:8px;padding:.3rem">${optsEnt}</select>
               <button class="btn-mini solido" data-alocar="${e.idVenda}">${t("Alocar")}</button>`
            : `<span class="badge">${esc(e.entregador ? e.entregador.nome : "-")}</span>`;
        return `<tr>
          <td class="col-destaque">#${e.idVenda}</td>
          <td>${esc(e.cliente ? e.cliente.nome : "-")}</td>
          <td>${real(e.venda ? e.venda.total : 0)}</td>
          <td><span class="badge badge-status badge-${e.status}">${t(e.status.replace("_", " "))}</span></td>
          <td class="direita">${acao}</td>
        </tr>`;
      }).join("")
    : `<tr><td colspan="5" style="text-align:center;color:#aaa;padding:1.5rem">${t("Nenhum pedido para entrega.")}</td></tr>`;
  return `
    <div class="admin-hero"><h2>${t("Entregas")}</h2><p>${t("Aloque entregadores aos pedidos")}</p></div>
    <div class="card">
      <table class="tabela"><thead><tr><th>${t("Pedido")}</th><th>${t("Cliente")}</th><th>${t("Total")}</th><th>${t("Status")}</th><th class="direita">${t("Alocação")}</th></tr></thead><tbody>${linhas}</tbody></table>
    </div>`;
}

function ligarEventosAdmin() {
  const on = (id, fn) => { const el = document.getElementById(id); if (el) el.onclick = fn; };

  // Clientes
  on("add-cliente", () => {
    try {
      if (!campo("cli-nome") || !campo("cli-email")) throw new Error("Preencha nome e e-mail.");
      View.clienteInserir(campo("cli-nome"), campo("cli-email"), campo("cli-fone"), campo("cli-senha") || "1234");
      toast("Cliente adicionado!", "sucesso"); render();
    } catch (e) { toast(e.message, "erro"); }
  });
  document.querySelectorAll("[data-del-cliente]").forEach((b) => {
    b.onclick = () => { if (confirm(t("Excluir cliente?"))) { View.clienteExcluir(Number(b.dataset.delCliente)); toast("Cliente excluído.", "sucesso"); render(); } };
  });

  // Categorias
  on("add-cat", () => {
    try { View.categoriaInserir(campo("cat-desc")); toast("Categoria adicionada!", "sucesso"); render(); }
    catch (e) { toast(e.message, "erro"); }
  });
  document.querySelectorAll("[data-save-cat]").forEach((b) => {
    b.onclick = () => {
      const inp = document.querySelector(`.edit-cat[data-id="${b.dataset.saveCat}"]`);
      try { View.categoriaAtualizar(Number(b.dataset.saveCat), inp.value); toast("Categoria atualizada!", "sucesso"); render(); }
      catch (e) { toast(e.message, "erro"); }
    };
  });
  document.querySelectorAll("[data-del-cat]").forEach((b) => {
    b.onclick = () => { try { View.categoriaExcluir(Number(b.dataset.delCat)); toast("Categoria excluída.", "sucesso"); render(); } catch (e) { toast(e.message, "erro"); } };
  });

  // Produtos
  on("add-prod", () => {
    try {
      View.produtoInserir(campo("prod-desc"), campo("prod-preco"), campo("prod-estoque"), campo("prod-cat"));
      toast("Produto adicionado!", "sucesso"); render();
    } catch (e) { toast(e.message, "erro"); }
  });
  on("reajustar", () => {
    const p = prompt(t("Percentual de reajuste (ex.: 10 para +10%, -5 para -5%):"));
    if (p === null || p === "") return;
    try { View.produtoReajustarPercentual(Number(p)); toast("Preços reajustados!", "sucesso"); render(); }
    catch (e) { toast(e.message, "erro"); }
  });
  document.querySelectorAll("[data-del-prod]").forEach((b) => {
    b.onclick = () => { if (confirm(t("Excluir produto?"))) { View.produtoExcluir(Number(b.dataset.delProd)); toast("Produto excluído.", "sucesso"); render(); } };
  });

  // Promocoes
  on("add-promo", () => {
    try {
      View.promocaoInserir(campo("promo-cat"), campo("promo-perc"), campo("promo-ini"), campo("promo-fim"));
      toast("Promoção adicionada!", "sucesso"); render();
    } catch (e) { toast(e.message, "erro"); }
  });
  document.querySelectorAll("[data-del-promo]").forEach((b) => {
    b.onclick = () => { View.promocaoExcluir(Number(b.dataset.delPromo)); toast("Promoção excluída.", "sucesso"); render(); };
  });

  // Entregas
  document.querySelectorAll("[data-alocar]").forEach((b) => {
    b.onclick = () => {
      const sel = document.querySelector(`.sel-ent[data-venda="${b.dataset.alocar}"]`);
      try { View.entregaAlocar(Number(b.dataset.alocar), Number(sel.value)); toast("Entregador alocado!", "sucesso"); render(); }
      catch (e) { toast(e.message, "erro"); }
    };
  });
}

// ---------------------------------------------------------------------------
// Inicializacao
// ---------------------------------------------------------------------------
render();
