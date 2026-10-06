"""Build the deploy-ready version of the Classic Shed Builders LLC site.

Usage:  python3 tools/build_site.py [--domain https://www.example.com]
Input:  classic-v3.html (the reviewed one-file site; its pages are <div class="page" data-page="...">)
Output: site/  (upload the contents of this folder to the web host)
        index.html, rent-to-own.html, delivery.html, warranty.html, about.html,
        contact.html, thank-you.html, privacy.html, 404.html
"""
import base64, hashlib, json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'classic-v3.html')
OUT = os.path.join(ROOT, 'site')
DOMAIN = 'https://YOUR-DOMAIN.com'
if '--domain' in sys.argv:
    DOMAIN = sys.argv[sys.argv.index('--domain') + 1].rstrip('/')
EMAIL = 'classicstructurespa@gmail.com'

s = open(SRC, encoding='utf-8').read()
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(os.path.join(OUT, 'assets', 'img'))

# ---- images: data URIs -> files (deduplicated)
saved = {}
names = {}
for m in re.finditer(r'<img[^>]*src="(data:image/[^"]+)"[^>]*alt="([^"]*)"', s):
    if m.group(2):
        names.setdefault(hashlib.sha1(m.group(1).encode()).hexdigest(), m.group(2))


def save(uri):
    m = re.match(r'data:image/(png|jpe?g|gif|webp);base64,(.*)', uri, re.S)
    if not m:
        return uri
    raw = base64.b64decode(m.group(2))
    key = hashlib.sha1(raw).hexdigest()[:10]
    if key in saved:
        return saved[key]
    ext = 'jpg' if m.group(1).startswith('jp') else m.group(1)
    label = re.sub(r'[^a-z0-9]+', '-', names.get(hashlib.sha1(uri.encode()).hexdigest(), '').lower()).strip('-')[:40] or 'image'
    fname = f'{label}-{key}.{ext}'
    open(os.path.join(OUT, 'assets', 'img', fname), 'wb').write(raw)
    saved[key] = f'assets/img/{fname}'
    return saved[key]


s = re.sub(r'src="(data:image/[^"]+)"', lambda m: f'src="{save(m.group(1))}"', s)

# ---- split CSS and JS into files
style = re.search(r'<style>(.*?)</style>', s, re.S).group(1)
open(os.path.join(OUT, 'assets', 'site.css'), 'w', encoding='utf-8').write(style.strip() + '\n')
s = re.sub(r'<style>.*?</style>', '', s, count=1, flags=re.S)
script = re.search(r'<script>(.*?)</script>', s, re.S).group(1)
open(os.path.join(OUT, 'assets', 'site.js'), 'w', encoding='utf-8').write(script.strip() + '\n')
s = re.sub(r'<script>.*?</script>', '', s, count=1, flags=re.S)

fonts = '\n'.join(re.findall(r'<link rel="preconnect"[^>]*>|<link href="https://fonts[^>]*>', s))
body = re.sub(r'<title>.*?</title>|<meta name="description"[^>]*>|<link rel="preconnect"[^>]*>|<link href="https://fonts[^>]*>', '', s).strip()

# ---- links: "#/page" -> page.html, "#/home/section" -> index.html#section
def fname(page):
    return 'index.html' if page in ('', 'home') else f'{page}.html'


def links(h):
    h = re.sub(r'(href|data-thanks)="#/([\w-]*)/([\w-]+)"', lambda m: f'{m.group(1)}="{fname(m.group(2))}#{m.group(3)}"', h)
    return re.sub(r'(href|data-thanks)="#/([\w-]*)"', lambda m: f'{m.group(1)}="{fname(m.group(2))}"', h)


body = links(body)
head_part, rest = body.split('<main id="top">', 1)
main_part, tail_part = rest.split('</main>', 1)
starts = [m.start() for m in re.finditer(r'<div class="page" data-page=', main_part)]
chunks = [main_part[a:b].strip() for a, b in zip(starts, starts[1:] + [len(main_part)])]
chunks = [re.sub(r'\s*<!-- =+ [\w -]+ =+ -->\s*$', '', c) for c in chunks]

logo = next(v for v in saved.values() if v.endswith('.png'))
hero = re.search(r'<img class="bg" src="([^"]+)"', body).group(1)
local = {
    "@context": "https://schema.org", "@type": "HomeAndConstructionBusiness",
    "name": "Classic Shed Builders LLC", "url": DOMAIN + '/', "logo": f"{DOMAIN}/{logo}", "image": f"{DOMAIN}/{hero}",
    "telephone": "+1-814-470-4494", "email": EMAIL,
    "address": {"@type": "PostalAddress", "streetAddress": "110 Davidson Rd.", "addressLocality": "Liverpool",
                "addressRegion": "PA", "postalCode": "17045", "addressCountry": "US"},
}


def page_doc(title, desc, url, content, extra_head='', prefix=''):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="{prefix}{logo}">
<meta name="theme-color" content="#26352D">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Classic Shed Builders LLC">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/{hero}">
{fonts}
<link rel="stylesheet" href="{prefix}assets/site.css">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}[hidden]{{display:none!important}}</style>{extra_head}
</head>
<body>
{head_part.strip()}
<main id="top">
{content}
</main>
{tail_part.strip()}
<script src="{prefix}assets/site.js"></script>
</body>
</html>
'''


sitemap = []
for c in chunks:
    a = re.match(r'<div class="page" data-page="([\w-]+)" data-title="([^"]+)" data-desc="([^"]+)"([^>]*)>', c)
    page, title, desc, more = a.groups()
    url = DOMAIN + '/' if page == 'home' else f'{DOMAIN}/{page}.html'
    extra = ''
    if 'data-noindex' in more:
        extra += '\n<meta name="robots" content="noindex">'
    else:
        sitemap.append(url)
    if page == 'home':
        extra += f'\n<script type="application/ld+json">{json.dumps(local, separators=(",", ":"))}</script>'
    open(os.path.join(OUT, fname(page)), 'w', encoding='utf-8').write(page_doc(title, desc, url, c, extra))

# ---- 404 (served from any folder, so every path is absolute)
home = next(c for c in chunks if 'data-page="home"' in c)
nf_content = ('<div class="page" data-page="404"><div class="phead"><div class="wrap"><p class="kicker">Error 404</p><h1>Page not found</h1>'
              '<p>The page you are looking for isn\'t here. <a href="/index.html" style="color:#fff;font-weight:700">Go to the home page</a> or call '
              '<a href="tel:+18144704494" style="color:#fff;font-weight:700">814.470.4494</a>.</p></div></div></div>')
nf = page_doc('Page not found | Classic Shed Builders LLC', 'Page not found.', DOMAIN + '/404.html', nf_content,
              '\n<meta name="robots" content="noindex">', prefix='/')
nf = re.sub(r'(href|src)="(assets/[^"]+|[\w-]+\.html(#[\w-]+)?)"', r'\1="/\2"', nf)
open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8').write(nf)

open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
open(os.path.join(OUT, 'sitemap.xml'), 'w').write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join(f'  <url><loc>{u}</loc></url>\n' for u in sitemap) + '</urlset>\n')
open(os.path.join(OUT, '_headers'), 'w').write('/assets/*\n  Cache-Control: public, max-age=2592000\n')

total = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(OUT) for f in fs)
print(f'pages: {len(chunks)} + 404 | images: {len(saved)} | total {total / 1e6:.1f} MB | domain {DOMAIN}')
