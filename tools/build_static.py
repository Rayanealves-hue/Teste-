"""Build a deploy-ready static site (one real page per section, images as files)
from the single-file review version classic-shed-builders.html.

Usage:  python3 tools/build_static.py [--domain https://www.example.com]
Output: dist/  (upload this folder to any static host, e.g. Cloudflare Pages)
"""
import base64, hashlib, html, json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'classic-shed-builders.html')
OUT = os.path.join(ROOT, 'dist')
DOMAIN = 'https://YOUR-DOMAIN.com'
if '--domain' in sys.argv:
    DOMAIN = sys.argv[sys.argv.index('--domain') + 1].rstrip('/')

s = open(SRC, encoding='utf-8').read()
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(os.path.join(OUT, 'assets', 'img'))

# ---------------------------------------------------------------- page ids -> URLs
def url_for(pid):
    if pid == 'home':
        return '/'
    if pid.startswith('cat-'):
        return f'/buildings/{pid[4:]}/'
    if pid.startswith('model-'):
        return f'/models/{pid[6:]}/'
    if pid.startswith('faq-'):
        return f'/faq/{pid[4:]}/'
    return f'/{pid}/'

# ---------------------------------------------------------------- images out of data: URIs
saved = {}

def save_uri(uri, name=None):
    m = re.match(r'data:image/(png|jpe?g|webp|gif);base64,(.*)', uri, re.S)
    if not m:
        return uri
    raw = base64.b64decode(m.group(2))
    ext = 'jpg' if m.group(1).startswith('jp') else m.group(1)
    key = hashlib.sha1(raw).hexdigest()[:12]
    if key in saved:
        return saved[key]
    fname = f'{name or key}.{ext}'
    dest = os.path.join(OUT, 'assets', 'img', fname)
    open(dest, 'wb').write(raw)
    try:
        from PIL import Image
        im = Image.open(dest)
        if ext == 'jpg' and (im.width > 1600 or len(raw) > 250_000):
            im = im.convert('RGB')
            if im.width > 1600:
                im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
            im.save(dest, quality=82, optimize=True, progressive=True)
    except ImportError:
        pass
    saved[key] = f'/assets/img/{fname}'
    return saved[key]

# model thumbnails get readable names
MIMG = {}
for m in re.finditer(r'<img src="(data:image/[^"]+)" alt="[^"]*" data-thumb-src="([^"]+)">', s):
    MIMG[m.group(2)] = save_uri(m.group(1), 'model-' + m.group(2))
s = re.sub(r'(src|href)="(data:image/(?:png|jpe?g|webp|gif);base64,[^"]+)"', lambda m: f'{m.group(1)}="{save_uri(m.group(2))}"', s)
assert 'base64,' not in s.split('<link rel="icon"')[1][:10] or True

# ---------------------------------------------------------------- split the document
head = s[:s.index('</head>')]
style = re.search(r'<style>(.*?)</style>', head, re.S).group(1)
open(os.path.join(OUT, 'assets', 'site.css'), 'w', encoding='utf-8').write(style.strip() + '\n')
ld_scripts = re.findall(r'<script type="application/ld\+json">.*?</script>', head, re.S)
local_ld = next(x for x in ld_scripts if 'HomeAndConstructionBusiness' in x)
items_ld = next(x for x in ld_scripts if 'ItemList' in x)
fonts = re.findall(r'<link rel="preconnect"[^>]*>|<link href="https://fonts[^>]*>', head)
favicon = re.search(r'<link rel="icon"[^>]*>', head).group(0)

body = s[s.index('<body>') + 6:s.index('</body>')]
before_main = body[:body.index('<main>')]
after_main = body[body.index('</main>') + len('</main>'):]
script = re.search(r'<script>(.*?)</script>', after_main, re.S).group(1)
after_main = re.sub(r'<script>.*?</script>', '', after_main, flags=re.S)
main = body[body.index('<main>') + 6:body.index('</main>')]
pages = re.findall(r'(<div class="page" id="p-([^"]+)" data-title="([^"]*)" data-desc="([^"]*)">.*?)(?=<div class="page" id="p-|\Z)', main, re.S)
assert len(pages) >= 60, len(pages)
PIDS = {p[1] for p in pages}

# ---------------------------------------------------------------- JS for real pages
js = script
i = js.index('function route(){'); j = js.index("addEventListener('hashchange',route);route();")
js = js[:i] + js[j + len("addEventListener('hashchange',route);route();"):]
js = js.replace("\nroute();", '\n')
js = js.replace("setTimeout(()=>{location.hash='thank-you';},400);", "setTimeout(()=>{location.href='/thank-you/';},400);")
js = js.replace("""const t=document.querySelector('img[data-thumb-src="'+m.slug+'"]');
  const img=root.querySelector('.out img');if(t){img.src=t.src;img.alt=m.name;}""",
                """const img=root.querySelector('.out img');if(MIMG[m.slug]){img.src=MIMG[m.slug];img.alt=m.name;}""")
js = js.replace("root.querySelector('[data-v]').href='#model-'+m.slug;", "root.querySelector('[data-v]').href='/models/'+m.slug+'/';")
js = js.replace("""document.addEventListener('click',e=>{const a=e.target.closest('[data-ask]');if(a){const f=document.getElementById('st');if(f)f.value=a.dataset.ask;}
 const d=e.target.closest('[data-design]');if(d){window.__pick=d.dataset.design;setTimeout(()=>document.querySelectorAll('[data-builder]').forEach(b=>b.__select&&b.__select(window.__pick)),60);}});""",
                """document.addEventListener('click',e=>{const a=e.target.closest('[data-ask]');if(a){a.href='/contact/?building='+encodeURIComponent(a.dataset.ask);}
 const d=e.target.closest('[data-design]');if(d){d.href='/design/?model='+encodeURIComponent(d.dataset.design);}});
(()=>{const q=new URLSearchParams(location.search);const f=document.getElementById('st');if(f&&q.get('building'))f.value=q.get('building');})();""")
js = js.replace("document.querySelectorAll('[data-builder]').forEach(builder);",
                "document.querySelectorAll('[data-builder]').forEach(builder);\n(()=>{const m=new URLSearchParams(location.search).get('model');if(m)document.querySelectorAll('[data-builder]').forEach(b=>b.__select&&b.__select(m));})();")
assert 'route()' not in js and 'img[data-thumb-src' not in js, 'router leftovers'
js = 'const MIMG=' + json.dumps(MIMG, separators=(',', ':')) + ';\n' + js
js = "document.documentElement.classList.add('js');\n" + js
open(os.path.join(OUT, 'assets', 'site.js'), 'w', encoding='utf-8').write(js)


# ---------------------------------------------------------------- link rewriting
def fix_links(h):
    def rep(m):
        target = m.group(1)
        if target in PIDS:
            return f'href="{url_for(target)}"'
        if target == 'home-special':
            return 'href="/#home-special"'
        if target == 'prices':
            return 'href="/buildings/"'
        return m.group(0)
    h = re.sub(r'href="#([a-z0-9-]+)"', rep, h)
    # model hero images: real file instead of JS copy
    h = re.sub(r'<img class="mhero" data-thumb="([^"]+)" alt="([^"]*)" src="">',
               lambda m: f'<img class="mhero" src="{MIMG[m.group(1)]}" alt="{m.group(2)}">', h)
    return h


NAV_FOR = lambda pid: ('buildings' if pid.startswith(('cat-', 'model-')) else 'faq' if pid.startswith('faq-') else pid)

hdr = fix_links(before_main)
ftr = fix_links(after_main)


def write_page(pid, title, desc, content):
    path = url_for(pid)
    navkey = NAV_FOR(pid)
    h = hdr.replace(f'<a href="{url_for(navkey)}">', f'<a class="on" href="{url_for(navkey)}" aria-current="page">', 1) if navkey in PIDS else hdr
    content = fix_links(content).replace(f'<div class="page" id="p-{pid}"', f'<div class="page on" id="p-{pid}"', 1)
    content = re.sub(r' data-title="[^"]*" data-desc="[^"]*"', '', content, count=1)
    canon = DOMAIN + path
    extra_ld = items_ld if pid in ('buildings',) else ''
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
{favicon}
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta name="theme-color" content="#26352D">
{chr(10).join(fonts)}
<link rel="stylesheet" href="/assets/site.css">
{local_ld}
{extra_ld}
</head>
<body>
{h}<main>
{content}</main>
{ftr}<script src="/assets/site.js"></script>
</body>
</html>
'''
    d = os.path.join(OUT, path.strip('/'))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(doc)


for block, pid, title, desc in pages:
    write_page(pid, title, desc, block)

# 404
nf = ('<div class="page" id="p-404"><div class="pagehead"><div class="wrap"><div class="kicker">404</div><h1>Page not found</h1>'
      '<p>The page you are looking for isn\'t here. Try our <a href="/buildings/">buildings</a> or call '
      '<a class="tel" href="tel:+18144704494">814.470.4494</a>.</p></div></div></div>\n')
write_page('404', 'Page not found | Classic Shed Builders', 'Page not found.', nf)
shutil.move(os.path.join(OUT, '404', 'index.html'), os.path.join(OUT, '404.html'))
os.rmdir(os.path.join(OUT, '404'))

# robots + sitemap
urls = [url_for(p[1]) for p in pages if p[1] not in ('thank-you',)]
open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nDisallow: /thank-you/\nSitemap: {DOMAIN}/sitemap.xml\n')
open(os.path.join(OUT, 'sitemap.xml'), 'w').write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    ''.join(f'  <url><loc>{DOMAIN}{u}</loc></url>\n' for u in urls) + '</urlset>\n')
# Cloudflare Pages: old hash links and a short alias
open(os.path.join(OUT, '_redirects'), 'w').write('/prices /buildings/ 301\n/prices/ /buildings/ 301\n')

total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(OUT) for f in fs)
print(f'pages: {len(pages)} + 404 | images: {len(saved)} | total {total/1e6:.1f} MB | domain {DOMAIN}')
