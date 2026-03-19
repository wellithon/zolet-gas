import os
import glob
import re

def slugify(value):
    import unicodedata
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

# Generate the 6 footer pages for the root
footer_keywords = [
    "disk gás cascavel", 
    "comprar gás cascavel", 
    "gás próximo", 
    "entrega de gás", 
    "botijão ultragaz", 
    "galão de água cascavel"
]

with open('index.html', 'r', encoding='utf-8') as f:
    base_html = f.read()

sitemap_entries = []

for kw in footer_keywords:
    slug = slugify(kw)
    filename = f"{slug}.html"
    url = f"https://www.zoletsgas.com.br/{slug}"
    
    page = base_html
    title_kw = kw.title()
    desc_str = f"{title_kw} com entrega rápida e preço justo. Somos a Zolet's Gás, revenda autorizada Ultragaz. Peça agora pelo WhatsApp (45) 99920-8741."
    
    page = re.sub(r'<title>.*?</title>', f'<title>{title_kw} | Zolet\'S Gás - Entrega Rápida</title>', page, 1)
    page = re.sub(r'<meta name="description" content="[^"]+">', f'<meta name="description" content="{desc_str}">', page, 1)
    page = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="{url}">', page)
    page = re.sub(r'<meta property="og:url" content="[^"]+">', f'<meta property="og:url" content="{url}">', page)
    page = re.sub(r'"name": "Zolet\'S Gás - Disk Gás Cascavel"', f'"name": "{title_kw} - Zolet\'S Gás"', page)
    
    page = re.sub(r'<h1[^>]*>.*?</h1>', f'<h1 style="color: var(--cor-fundo);">{title_kw} | Zolet\'S Gás</h1>', page, 1)
    hero_p = f"""<p style="font-size: 1.2em; max-width: 800px; margin: 0 auto 30px;">
                    Procurando por <strong>{kw}</strong>? Você encontrou o lugar certo! Somos uma revenda de gás autorizada 
                    <strong>Ultragaz</strong> com entrega em todos os bairros. Botijão, galão de água 20L, 
                    mangueiras e registros. <strong>Gás próximo de você</strong>, com segurança e preço justo!
                </p>"""
    page = re.sub(r'<p style="font-size: 1.2em; max-width: 800px; margin: 0 auto 30px;">.*?</p>', hero_p, page, 1, flags=re.DOTALL)
    
    # Active Link
    page = page.replace('class="nav-link-futuristic active-nav-link"', 'class="nav-link-futuristic"')
    page = page.replace('href="index.html" class="nav-link-futuristic"', 'href="index.html" class="nav-link-futuristic active-nav-link"')

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(page)
        
    sitemap_entries.append(f'  <url>\n    <loc>{url}</loc>\n    <lastmod>2026-03-17</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.75</priority>\n  </url>')

# Generate the 6 footer pages for EVERY BAIRRO (59 * 6 = 354 pages)
# Because the user explicitly asked: "e cria um html para cada um também!" ... "para todas as paginas e deixar relacionada a cada bairro"
bairros_files = glob.glob('bairro-*.html')

for filepath in bairros_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract neighborhood name
    match = re.search(r'<title>Disk Gás (.*?) \|', content)
    bairro = match.group(1).strip() if match else ""
    bairro_slug = slugify(bairro)
    
    local_keywords = [
        f"disk gás {bairro}", 
        f"comprar gás {bairro}", 
        f"gás próximo ao {bairro}", 
        f"entrega de gás {bairro}", 
        f"botijão ultragaz {bairro}", 
        f"galão de água {bairro}"
    ]
    
    for kw in local_keywords:
        slug = slugify(kw)
        filename = f"{slug}.html"
        url = f"https://www.zoletsgas.com.br/{slug}"
        
        page = content
        title_kw = kw.title()
        desc_str = f"{title_kw} com entrega rápida. Somos a Zolet's Gás, revenda autorizada Ultragaz. Peça agora pelo WhatsApp (45) 99920-8741."
        
        page = re.sub(r'<title>.*?</title>', f'<title>{title_kw} | Zolet\'S Gás - Entrega Rápida</title>', page, 1)
        page = re.sub(r'<meta name="description" content="[^"]+">', f'<meta name="description" content="{desc_str}">', page, 1)
        page = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="{url}">', page)
        page = re.sub(r'<meta property="og:url" content="[^"]+">', f'<meta property="og:url" content="{url}">', page)
        page = re.sub(r'"name": ".*?"', f'"name": "{title_kw} - Zolet\'S Gás"', page, 1)
        
        page = re.sub(r'<h1[^>]*>.*?</h1>', f'<h1 style="color: var(--cor-fundo);">{title_kw} | Zolet\'S Gás</h1>', page, 1)
        
        # WhatsApp URL replacement
        import urllib.parse
        def repl_wa(m):
            full_url = m.group(0)
            if '?text=' in full_url:
                base, qs = full_url.split('?text=')
                decoded = urllib.parse.unquote(qs)
                # Keep the generic whatsapp approach for these exact pages, just passing the keyword
                decoded = f"[Google] Olá! Gostaria de falar sobre: {kw}"
                encoded = urllib.parse.quote(decoded)
                return f"{base}?text={encoded}"
            return full_url
            
        page = re.sub(r'https://wa\.me/[^\s"\'\`]+', repl_wa, page)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(page)
            
        sitemap_entries.append(f'  <url>\n    <loc>{url}</loc>\n    <lastmod>2026-03-17</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.70</priority>\n  </url>')

# Append to sitemap
with open('sitemap.xml', 'r', encoding='utf-8') as f:
    sitemap = f.read()

sitemap = sitemap.replace('</urlset>', '\n'.join(sitemap_entries) + '\n</urlset>')

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap)

print("Generated 360 Footer SEO pages!")
