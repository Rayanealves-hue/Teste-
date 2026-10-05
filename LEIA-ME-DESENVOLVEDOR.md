# Classic Shed Builders: pacote para colocar o site no ar

**Site aprovado (prévia):** https://claude.ai/artifact/MNqPrJ995bMyHiS9P3XjYr
**Cliente:** Classic Shed Builders LLC, 110 Davidson Rd., Liverpool, PA 17045, 814.470.4494, caleb@ibyfax.com

---

## 1. Conteúdo do pacote

```
classic-shed-builders-site-final.zip
├── site/                     ← ESTA É A PASTA QUE VAI PARA O AR
│   ├── index.html            ← o site (uma página com seções e menu)
│   ├── 404.html              ← página de erro
│   ├── robots.txt
│   ├── sitemap.xml
│   ├── _headers              ← cache das imagens (Cloudflare Pages / Netlify)
│   └── assets/
│       ├── site.css
│       ├── site.js
│       └── img/              ← 14 imagens (logo + fotos)
├── classic-v3.html           ← arquivo-fonte aprovado (um arquivo só, com tudo dentro)
├── tools/build_site.py       ← gera a pasta site/ a partir do arquivo-fonte
└── LEIA-ME-DESENVOLVEDOR.md  ← este guia
```

- Site **100% estático** (HTML, CSS e JavaScript puro). Não precisa de banco de dados, PHP, WordPress nem Node.
- Tamanho total da pasta `site/`: cerca de 3,7 MB.
- Fontes: Google Fonts (Libre Baskerville e Montserrat), carregadas pelo `index.html`.
- Funciona em celular e computador, nos modos claro e escuro.

## 2. Antes de subir: colocar o domínio

O domínio entra no sitemap, no robots, no link canônico e nos dados para o Google. Rode, com Python 3:

```bash
python3 tools/build_site.py --domain https://www.DOMINIO-DO-CLIENTE.com
```

O script recria a pasta `site/` com o domínio certo. Sem esse passo, os arquivos ficam com `https://YOUR-DOMAIN.com`.

> O domínio, a hospedagem e todas as contas devem ser criados **no nome da Classic Shed Builders LLC** (contrato, itens 4.1 e 5.1).

**Teste local:** `cd site && python3 -m http.server 8000` e abrir http://localhost:8000. Abrir o `index.html` com dois cliques também funciona, mas o teste pelo servidor é o mais fiel.

## 3. Publicar (escolha uma opção)

### Opção A: Cloudflare Pages (recomendado, gratuito; é a stack pedida pelo cliente)
1. Criar a conta Cloudflare no nome do cliente.
2. **Workers & Pages → Create → Pages → Upload assets.**
3. Nome do projeto: `classic-shed-builders`. Arrastar o **conteúdo** da pasta `site/` e clicar em **Deploy**.
4. **Custom domains → Set up a domain**, informar o domínio e seguir as instruções de DNS.

### Opção B: Netlify
Arrastar a pasta `site/` em https://app.netlify.com/drop e depois ligar o domínio em *Domain settings*.

### Opção C: hospedagem tradicional (Hostinger, GoDaddy, cPanel)
Enviar o **conteúdo** de `site/` para a pasta `public_html/` pelo gerenciador de arquivos ou por FTP. Configurar `404.html` como página de erro, se o painel pedir. O `_headers` pode ser ignorado.

## 4. Formulário de orçamento: ação necessária

Hoje o botão **"Submit Form"** só monta o pedido na tela, para o visitante copiar e mandar. **Nenhum e-mail é enviado automaticamente.**

Para os pedidos chegarem direto no e-mail do cliente:
1. **Confirmar com o Caleb qual e-mail recebe os orçamentos.** Hoje o site mostra caleb@ibyfax.com.
2. Criar um formulário no **Formspree** (https://formspree.io), no **Netlify Forms** ou num **Cloudflare Worker**, na conta do cliente.
3. Em `assets/site.js`, no trecho `/* quote form */`, trocar a montagem do texto por um `fetch` para o endpoint do serviço. Os campos têm os ids `q-first`, `q-last`, `q-phone`, `q-email`, `q-zip`, `q-type` e `q-msg`.
4. Fazer um envio de teste e confirmar que chegou.

## 5. Depois de no ar: checklist

- [ ] Abrir no celular e no computador. Conferir o menu (três risquinhos), os botões "Get a Quote", o carrossel de fotos, o carrossel de avaliações, o "Learn More" dos cartões e o formulário.
- [ ] Tocar no telefone 814.470.4494 no celular e confirmar que abre a ligação.
- [ ] Conferir se o link **Location** abre o Google Maps no 110 Davidson Rd.
- [ ] **Google Search Console:** verificar o domínio e enviar `https://DOMINIO/sitemap.xml`.
- [ ] **Bing Webmaster Tools:** importar do Search Console.
- [ ] **Google Business Profile** no nome do cliente: endereço, telefone, horário e link do site.
- [ ] (Opcional) **Google Analytics 4** na conta do cliente: colar o código no `<head>` do `index.html`.
- [ ] Ativar HTTPS (o Cloudflare e o Netlify fazem isso sozinhos).

## 6. Como fazer alterações depois
- **Texto pequeno:** editar direto em `site/index.html`.
- **Alteração maior:** editar o `classic-v3.html` (arquivo-fonte) e rodar de novo `python3 tools/build_site.py --domain https://...`. A pasta `site/` é recriada inteira.

## 7. Pendências com o cliente (não impedem o lançamento)
| Item | Situação |
|---|---|
| E-mail que recebe os orçamentos | Confirmar com o Caleb |
| Raio de entrega grátis | As tabelas dizem "PA + 50 milhas" (é o que está no site); o folheto escrito à mão diz "250 milhas" |
| 7 avaliações do Facebook (Matt, Rob, "Beaver Springs, PA") | Confirmar que são clientes da Classic |
| Horário das lojas, seg–sáb, 9h–18h | Confirmar |
| Fotos (topo, galeria, garagem LP) | Confirmar que são construções da Classic |
| Links do Facebook e do Google Reviews | Pedir ao cliente, para botões futuros |
