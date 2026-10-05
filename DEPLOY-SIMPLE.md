# Classic Shed Builders: site simples (5 abas), guia para colocar no ar

**Prévia aprovada:** https://claude.ai/artifact/JLmKCa1m8H8M6Bdwe7mWxm
**Abas:** Home · Buildings · Rent to Own & Financing · Delivery & Warranty · Contact / Where to Buy

## 1. O que vai para a hospedagem

Suba **o conteúdo da pasta `site-simple/`** (não a pasta em si) para a raiz do site:

```
site-simple/
├── index.html        ← o site (5 abas numa página só)
├── 404.html          ← página de erro
├── robots.txt
├── sitemap.xml
├── _headers          ← cache das imagens (Cloudflare Pages / Netlify)
└── assets/
    ├── site.css
    ├── site.js
    └── img/          ← 15 imagens (logo + fotos)
```

O site é **estático** (HTML, CSS e JS). Não precisa de banco de dados, PHP nem WordPress. Tamanho total: cerca de 4,8 MB.

## 2. Antes de subir

1. **Domínio** registrado **no nome da Classic Shed Builders LLC** (contrato, itens 4.1 e 5.1).
2. **Gerar a pasta com o domínio certo.** O endereço entra no sitemap, no robots e nos dados para o Google:
   ```bash
   python3 tools/build_simple.py --domain https://www.DOMINIO-DO-CLIENTE.com
   ```
   (Só precisa de Python 3. O arquivo de entrada é `classic-simple.html`.)
3. **Testar no computador:** `cd site-simple && python3 -m http.server 8000` e abrir http://localhost:8000.

## 3. Onde subir

**Cloudflare Pages (recomendado, gratuito; é o que a Receita do cliente pede no item 15)**
1. Criar a conta Cloudflare no nome do cliente.
2. Workers & Pages → Create → Pages → **Upload assets** → arrastar o conteúdo de `site-simple/` → Deploy.
3. Custom domains → adicionar o domínio e seguir as instruções de DNS.

**Netlify:** arrastar a pasta `site-simple/` em app.netlify.com/drop e ligar o domínio.

**Hostinger, cPanel ou outra hospedagem:** enviar o conteúdo de `site-simple/` para `public_html/` pelo gerenciador de arquivos ou por FTP. Nessas hospedagens o `_headers` não tem efeito e pode ser ignorado.

## 4. Depois de no ar

- [ ] Abrir o site no celular e no computador e conferir as 5 abas, o menu de três risquinhos, a galeria (setas, miniaturas e tela cheia) e o carrossel de avaliações.
- [ ] Tocar no telefone 814.470.4494 no celular e confirmar que abre a ligação.
- [ ] Google Search Console: verificar o domínio e enviar `https://DOMINIO/sitemap.xml`.
- [ ] Google Business Profile **no nome do cliente**: endereço 110 Davidson Rd., Liverpool, PA 17045, telefone 814.470.4494 e o link do site.
- [ ] (Opcional) Google Analytics na conta do cliente: colar o código no `<head>` do `index.html`.

## 5. Formulário de orçamento

O botão **"Prepare my request"** monta o pedido na tela, e o visitante copia e manda para caleb@ibyfax.com ou lê por telefone. **Nenhum e-mail é enviado automaticamente.**

Para receber os pedidos direto no e-mail, ligue o formulário a um serviço como Formspree, Netlify Forms ou Cloudflare Worker, na conta do cliente. Antes disso, é preciso o Caleb confirmar qual e-mail recebe os orçamentos.

## 6. Pendências com o cliente (não impedem o lançamento)

- Confirmar as 7 avaliações do Facebook (Matt, Rob, "Beaver Springs, PA").
- Confirmar o horário das lojas (seg–sáb, 9h–18h).
- Confirmar as fotos da galeria e da foto principal.
- Confirmar o raio de entrega grátis: "PA + 50 milhas" (tabelas) ou "250 milhas" (folheto).
- Aprovar o logo oval.
- Confirmar o e-mail que recebe os orçamentos do site.
