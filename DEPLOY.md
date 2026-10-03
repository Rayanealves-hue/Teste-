# Classic Shed Builders: guia para colocar o site no ar

## 1. O que está no pacote

| Arquivo / pasta | Para que serve |
|---|---|
| `dist/` | **O site pronto.** É esta pasta que vai para a hospedagem: 62 páginas, mais a página 404, as imagens, `robots.txt` e `sitemap.xml` |
| `dist/assets/site.css` e `dist/assets/site.js` | Estilo e funções: menu, configurador de preço, formulário e avaliações |
| `dist/assets/img/` | Todas as imagens (50 arquivos) |
| `classic-shed-builders.html` | Versão de revisão num arquivo só. É o link enviado para aprovação. **Não é para subir.** |
| `tools/build_static.py` | Gera a pasta `dist/` a partir da versão de revisão. Use quando o domínio estiver definido ou depois de qualquer alteração |

O site é **estático** (HTML, CSS e JS). Não precisa de banco de dados nem de PHP. Funciona em qualquer hospedagem estática. Recomendamos **Cloudflare Pages**, que é o que a Receita do cliente pede no item 15 ("static Cloudflare stack") e é gratuito.

## 2. Antes de subir

1. **Domínio:** precisa estar registrado **no nome da Classic Shed Builders LLC** (contrato, itens 4.1 e 5.1).
2. **Gerar o pacote com o domínio certo.** O sitemap, o robots e os links canônicos usam o domínio:
   ```bash
   python3 tools/build_static.py --domain https://www.DOMINIO-DO-CLIENTE.com
   ```
   (Precisa de Python 3. Para recomprimir as imagens, precisa também do Pillow: `pip install pillow`.)
3. **Testar no computador:** `cd dist && python3 -m http.server 8000` e abrir http://localhost:8000. Abrir o `index.html` com dois cliques **não** funciona, porque os links começam com `/`.

## 3. Subir no Cloudflare Pages (recomendado)

**Opção A: arrastar a pasta (mais simples)**
1. Criar a conta Cloudflare **no nome do cliente** (contrato, item 5.1).
2. Workers & Pages → Create → Pages → **Upload assets**.
3. Nome do projeto: `classic-shed-builders`. Arrastar o **conteúdo** da pasta `dist/` e clicar em Deploy.
4. Custom domains → adicionar o domínio do cliente e seguir as instruções de DNS.

**Opção B: ligado ao GitHub (atualiza sozinho)**
1. Workers & Pages → Create → Pages → Connect to Git → repositório `rayanealves-hue/teste-`, branch `claude/open-create-html-rnalrx`.
2. Framework preset: **None**. Build command: *(vazio)*. Build output directory: **`dist`**.
3. A cada alteração: rodar `tools/build_static.py`, fazer commit da `dist/` e o Cloudflare publica sozinho.

**Outras hospedagens** (Netlify, Hostinger, cPanel): enviar o conteúdo de `dist/` para a pasta raiz do site (`public_html`). O arquivo `404.html` vira a página de erro. O `_redirects` só vale no Cloudflare e no Netlify.

## 4. Depois de no ar (contrato, item 1.3)

- [ ] Google Search Console: verificar o domínio e enviar `https://DOMINIO/sitemap.xml`
- [ ] Bing Webmaster Tools: importar do Search Console
- [ ] Google Analytics (GA4) **na conta do cliente**: colar o código no `<head>` e atualizar a página de Privacidade
- [ ] Google Business Profile: criar ou reivindicar, com o endereço 110 Davidson Rd., Liverpool, PA e o horário de seg–sáb, 9h–18h
- [ ] Colocar os links do Facebook e de "Leave a Google review" (os botões ficam escondidos até ter o link; procurar `-link-pending` no HTML)
- [ ] Testar o formulário de orçamento no celular e no computador

## 5. Formulário de orçamento: atenção

Hoje o formulário **abre o app de e-mail do visitante** com o pedido preenchido, para **caleb@ibyfax.com** (o e-mail do papel timbrado do Caleb). O visitante precisa apertar "Enviar". O contrato (item 1.2) pede entrega **por e-mail e fax**.

- **Falta confirmar com o Caleb:** para qual e-mail os pedidos devem ir (o jrmmcartney84@gmail.com não funciona) e se o Jason (717.460.8079) também recebe.
- Para o pedido chegar sem depender do app de e-mail, ligar o formulário a um serviço de formulários (Cloudflare Worker, Formspree ou similar) na conta do cliente. Isso é um custo de terceiro, pago pelo cliente (contrato, item 2.2).

## 6. O que ainda depende do cliente

| # | Item | Onde entra |
|---|---|---|
| 1 | E-mail que recebe os orçamentos | Formulário |
| 2 | Raio de entrega grátis: as tabelas dizem "PA + 50 milhas"; o folheto, escrito à mão, diz "250 milhas" | Delivery, FAQ e Home |
| 3 | Planilha do estoque e fotos originais | In Stock |
| 4 | Licença do Shed Suite no nome da Classic | Design & Price |
| 5 | Financiador e taxas | Financing |
| 6 | História da família, fotos da equipe e fotos aéreas do 110 Davidson Rd. | About |
| 7 | Lista de cidades atendidas | Service area |
| 8 | Fotos de 23 modelos | Páginas dos modelos |
| 9 | Links do Facebook e do Google | Reviews e Contact |
| 10 | Confirmar: as 7 avaliações do Facebook (Matt e Rob, "Beaver Springs, PA"), o "100% recommend", as fotos "Recently built" e a foto principal, e as 8 fotos novas dos modelos | Home, Reviews, Buildings |
| 11 | Aprovação de todos os textos (contrato, itens 1.2 e 3.3) | Todo o site |
