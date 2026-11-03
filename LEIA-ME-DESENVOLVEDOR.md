# Classic Shed Builders: pacote para colocar o site no ar

**Site aprovado (prévia):** https://claude.ai/artifact/MNqPrJ995bMyHiS9P3XjYr
**Cliente:** Classic Shed Builders LLC, oficina 110 Davidson Rd., Liverpool, PA 17045 (não é loja), 814.470.4494, classicstructurespa@gmail.com
**Domínio:** https://classicshedbuilders.com (registro A → 45.55.170.20)

---

## 1. Conteúdo do pacote

```
classic-shed-builders-site-final.zip
├── site/                     ← ESTA É A PASTA QUE VAI PARA O AR
│   ├── index.html            ← início
│   ├── rent-to-own.html      ← rent to own, com a tabela de preços mensais
│   ├── delivery.html         ← entrega, remoção do galpão antigo, preparo do terreno
│   ├── warranty.html         ← garantia vitalícia
│   ├── about.html            ← sobre nós (texto do Caleb)
│   ├── faq.html              ← perguntas frequentes
│   ├── price-lists.html      ← tabelas de preços em texto: estilos, itens inclusos, preços, opções e especificações
│   ├── contact.html          ← contato e formulário de orçamento
│   ├── thank-you.html        ← página de agradecimento depois do formulário (noindex)
│   ├── privacy.html          ← política de privacidade
│   ├── 404.html              ← página de erro
│   ├── robots.txt
│   ├── sitemap.xml
│   ├── _headers              ← cache das imagens (Cloudflare Pages / Netlify)
│   └── assets/
│       ├── site.css
│       ├── site.js
│       └── img/              ← 24 imagens (logo e fotos)
├── classic-v3.html           ← arquivo-fonte (um arquivo só, com todas as páginas dentro)
├── tools/build_site.py       ← gera a pasta site/ a partir do arquivo-fonte
└── LEIA-ME-DESENVOLVEDOR.md  ← este guia
```

- Site **100% estático** (HTML, CSS e JavaScript puro). Não precisa de banco de dados, PHP, WordPress nem Node.
- Tamanho total da pasta `site/`: cerca de 5,7 MB. Os links entre páginas são relativos (`rent-to-own.html`, `index.html#types`).
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

O formulário fica em `contact.html` e já está pronto para um serviço de formulário. **Os pedidos devem chegar em classicstructurespa@gmail.com.**

- Enquanto `data-endpoint` estiver vazio, o botão **"Submit Form"** só monta o pedido na tela para o visitante copiar. Nenhum e-mail é enviado.
- Com o endereço preenchido, o site envia os dados por `POST` (FormData, com `Accept: application/json`) e, se a resposta for OK, abre `thank-you.html`.

Passos:
1. Criar o formulário no **Formspree** (https://formspree.io) na conta do cliente, com destino classicstructurespa@gmail.com. Pode ser outro serviço que aceite POST e responda 200.
2. Em `classic-v3.html`, trocar `data-endpoint=""` por `data-endpoint="https://formspree.io/f/SEU-ID"` e rodar o build de novo. Também dá para editar direto em `site/contact.html`.
3. Os campos enviados são `first_name`, `last_name`, `phone`, `email`, `zip`, `building` e `message`.
4. Fazer um envio de teste e confirmar que chegou e que abriu a página de agradecimento.

## 5. Depois de no ar: checklist

- [ ] Abrir no celular e no computador. Conferir o menu (três risquinhos), as 10 páginas, os botões "Get a Quote" (o do cartão já escolhe o prédio no formulário), o carrossel de fotos, o carrossel de avaliações, a tabela de preços do Rent to Own e o formulário.
- [ ] Tocar no telefone 814.470.4494 no celular e confirmar que abre a ligação.
- [ ] Conferir se `www.classicshedbuilders.com` redireciona para `https://classicshedbuilders.com` (um endereço principal, o outro redirecionando).
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
| Endereços das lojas (retail) | O 110 Davidson Rd é a oficina, não loja. Pedir os endereços ao Caleb |
| Texto pelo 814.470.4494 | Confirmar se recebe SMS, para pôr o botão "Text us" |
| Prédios em estoque | Pedir lista e fotos para uma página de estoque |
| Vídeo de entrega | Pedir vídeos ou fotos de entrega |
| FAQ | Rascunho enviado ao Caleb. Só publicar depois que ele aprovar |
| Links do Facebook e do Google | Aguardando o Facebook liberar a troca do nome para Classic |
| Responsável pelo site | Sam, 814.299.3885 |
