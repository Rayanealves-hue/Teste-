"""Build the deploy-ready version of the simple 5-tab site.

Usage:  python3 tools/build_simple.py [--domain https://www.example.com]
Input:  classic-simple.html (the reviewed page)
Output: site-simple/  (upload the contents of this folder to the web host)
"""
import base64, hashlib, html, json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'classic-simple.html')
OUT = os.path.join(ROOT, 'site-simple')
DOMAIN = 'https://YOUR-DOMAIN.com'
if '--domain' in sys.argv:
    DOMAIN = sys.argv[sys.argv.index('--domain') + 1].rstrip('/')

s = open(SRC, encoding='utf-8').read()
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(os.path.join(OUT, 'assets', 'img'))

# ---- images: data URIs -> files (deduplicated)
saved = {}
names = {}
for m in re.finditer(r'<img[^>]*src="(data:image/[^"]+)"[^>]*alt="([^"]*)"', s):
    names.setdefault(hashlib.sha1(m.group(1).encode()).hexdigest(), m.group(2))


def save(uri):
    m = re.match(r'data:image/(png|jpe?g|gif|webp);base64,(.*)', uri, re.S)
    if not m:
        return uri
    raw = base64.b64decode(m.group(2))
    if len(raw) < 200:          # 1x1 placeholder: keep inline
        return uri
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

# ---- head pieces from the source
title = re.search(r'<title>(.*?)</title>', s).group(1)
desc = re.search(r'<meta name="description" content="([^"]*)">', s).group(1)
fonts = '\n'.join(re.findall(r'<link rel="preconnect"[^>]*>|<link href="https://fonts[^>]*>', s))
body = re.sub(r'<title>.*?</title>|<meta name="description"[^>]*>|<link rel="preconnect"[^>]*>|<link href="https://fonts[^>]*>', '', s).strip()

logo = next(v for v in saved.values() if v.endswith('.png'))
hero = re.search(r'<div class="hero">\s*<img src="([^"]+)"', body).group(1)

local = {
    "@context": "https://schema.org", "@type": "HomeAndConstructionBusiness",
    "name": "Classic Shed Builders LLC", "url": DOMAIN + '/', "logo": f"{DOMAIN}/{logo}", "image": f"{DOMAIN}/{hero}",
    "telephone": "+1-814-470-4494", "email": "caleb@ibyfax.com",
    "address": {"@type": "PostalAddress", "streetAddress": "110 Davidson Rd.", "addressLocality": "Liverpool",
                "addressRegion": "PA", "postalCode": "17045", "addressCountry": "US"},
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                                   "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                                   "opens": "09:00", "closes": "18:00"}],
}

doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Classic Shed Builders | Sheds, Garages &amp; Pavilions in Liverpool, PA</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{DOMAIN}/">
<link rel="icon" type="image/png" href="{logo}">
<meta name="theme-color" content="#26352D">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Classic Shed Builders">
<meta property="og:title" content="Classic Shed Builders | Sheds, Garages &amp; Pavilions">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{DOMAIN}/">
<meta property="og:image" content="{DOMAIN}/{hero}">
{fonts}
<link rel="stylesheet" href="assets/site.css">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}[hidden]{{display:none!important}}</style>
<script type="application/ld+json">{json.dumps(local, separators=(',', ':'))}</script>
</head>
<body>
{body}
<script src="assets/site.js"></script>
</body>
</html>
'''
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(doc)

nf = doc.replace('<main>', '<main>\n<section><div class="wrap"><h1>Page not found</h1><p class="lead" style="margin-top:14px">'
                 'The page you are looking for isn\'t here. <a href="/">Go to the home page</a> or call '
                 '<a class="tel" href="tel:+18144704494">814.470.4494</a>.</p></div></section>\n<div hidden>', 1)
nf = nf.replace('</main>', '</div>\n</main>', 1).replace('href="assets/', 'href="/assets/').replace('src="assets/', 'src="/assets/')
open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8').write(nf)

open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
open(os.path.join(OUT, 'sitemap.xml'), 'w').write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    f'  <url><loc>{DOMAIN}/</loc></url>\n</urlset>\n')
open(os.path.join(OUT, '_headers'), 'w').write('/assets/*\n  Cache-Control: public, max-age=2592000\n')

total = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(OUT) for f in fs)
print(f'images: {len(saved)} | total {total / 1e6:.1f} MB | domain {DOMAIN}')
