import re
import os
import unicodedata

# O review apontou que a "nuvem de tags" (tag cloud) é considerada Black Hat SEO e vai contra as diretrizes do Google ("keyword stuffing"), além de poluir o rodapé das 65 páginas, contrariando o pedido do usuário para não causar poluição.
# A melhor alternativa proposta pelo Review e que cumpre perfeitamente as exigências do Google e do usuário é criar UMA PÁGINA ESPECÍFICA de "Pesquisas Populares / Áreas de Cobertura" e lincá-la discretamente no rodapé.
# Como o usuário pediu: "criar uma pagina igual a index.html para cada uma delas". Não faremos 8 mil páginas, mas podemos fazer UMA página de "Buscas de Gás" que contenha uma listagem LIMPA das intenções de busca, ou injetar as palavras nas meta-tags e schema, não no HTML visível.
# Mas a instrução do Review foi clara: "A better approach would be creating a dedicated "Áreas de Cobertura" (Coverage Areas) page or an HTML sitemap that organizes these terms cleanly without spamming every page's footer."

# We will create ONE highly-organized page called "pesquisas-populares.html"
# It will have a professional accordion or list format.
# Then we just add ONE link in the footer of all pages pointing to it: "Pesquisas Frequentes"

keywords = [
"Gás de cozinha entrega rápida", "Disk gás", "Gás 24 horas perto de mim", "Telefone de gás", "Pedir gás online", "Gás de cozinha pronta entrega",
"Número do gás", "Entrega de gás agora", "Gás entrega domicílio", "WhatsApp do gás", "Pedir gás pelo zap", "Gás entrega grátis",
"Telefone entrega de gás", "Moto gás rápido", "Gás de cozinha delivery", "Pedir botijão de gás agora", "Gás urgente", "Disk gás telefone",
"Zap do gás", "Pedir gás pelo aplicativo", "Entrega de gás 24h", "Telefone do disk gás", "Gás rápido em casa", "Pedido de gás online",
"Telefone depósito de gás", "Entrega de botijão agora", "Gás entrega imediata", "Como pedir gás pelo celular", "Site para pedir gás",
"Gás de cozinha entrega domingo", "Entrega de gás feriado", "Gás 24 horas telefone", "Pedir botijão rápido", "Telefone da entrega de gás",
"Gás disk entrega", "Botijão de gás entrega rápida", "Disk gás WhatsApp número", "Gás de cozinha delivery perto de mim", "Onde pedir gás agora",
"Chamar o gás", "Gás em domicílio telefone", "Entrega expressa de gás", "Gás de cozinha entrega noturna", "Disk gás aberto agora",
"Telefone botijão de gás entrega", "Gás para entrega imediata", "Pedir gás rápido", "Entrega de gás de cozinha telefone", "WhatsApp entrega de gás",
"Zap disk gás", "Pedir gás de cozinha pelo WhatsApp", "Gás entrega de madrugada", "Telefone do caminhão do gás", "Disk gás mais próximo",
"Pedir gás em casa", "Disk gás entrega 24 horas", "Gás de cozinha online entrega", "Número do telefone do gás", "Entrega botijão agora",
"Como comprar gás pela internet", "Gás de cozinha entrega rápida WhatsApp", "Telefone entrega gás 24h", "Disk gás entrega gratuita", "Pedir gás pelo app",
"Gás de cozinha disk entrega rápida", "Número do gás de cozinha", "Telefone para pedir botijão", "Gás entrega hoje", "Zap do depósito de gás",
"Disk gás telefone celular", "Entrega de gás de cozinha 24 horas", "Pedir gás rápido pelo zap", "Gás entrega domiciliar rápida", "Disk gás telefone fixo",
"Gás de cozinha entrega no bairro", "Telefone do gás perto de mim", "Disk gás 24hs telefone", "WhatsApp do caminhão do gás", "Pedir gás botijão",
"Telefone entrega botijão", "Disk gás rápido telefone", "Gás de cozinha entrega sábado", "Gás 24 horas entrega rápida", "Pedir botijão de gás entrega grátis",
"Telefone do gás 24 horas", "Entrega de gás por aplicativo", "Disk gás pelo WhatsApp", "Gás de cozinha entrega residencial", "Telefone da distribuidora de gás",
"Pedir gás pelo telefone agora", "Gás entrega rápida perto de mim", "WhatsApp para pedir gás de cozinha", "Disk gás entrega imediata", "Telefone do gás delivery",
"Gás de cozinha rápido e barato", "Pedir gás pelo WhatsApp telefone", "Entrega de gás agora telefone", "Disk gás pronto entrega", "Gás de cozinha entrega telefone WhatsApp",
"Telefone para comprar gás rápido", "Preço do gás de cozinha hoje", "Gás de cozinha mais barato", "Promoção de gás de cozinha", "Preço botijão de gás",
"Onde comprar gás barato", "Valor do gás de cozinha", "Menor preço do gás", "Comparar preço de gás", "Cupom de desconto gás", "Gás de cozinha em oferta",
"Tabela de preço do gás", "Valor da recarga de gás", "Onde o gás está mais barato", "Promoção de botijão de gás", "Gás de cozinha preço atualizado",
"Preço do gás hoje valor", "Gás mais barato perto de mim", "Quanto custa o gás de cozinha", "Gás preço promocional", "Melhor preço gás de cozinha",
"Gás de cozinha preço revenda", "Valor botijão de gás hoje", "Preço do gás de cozinha por estado", "Gás de cozinha barato para retirar", "Valor da carga de gás",
"Cupom para gás de cozinha", "Gás de cozinha preço na distribuidora", "Promoção gás de cozinha", "Preço do botijão de gás vazio", "Gás de cozinha preço médio",
"Onde achar gás barato hoje", "Preço de gás de cozinha", "Gás em promoção", "Valor atual do gás de cozinha", "Gás de cozinha menor valor",
"Preço do gás hoje na minha cidade", "Oferta de gás de cozinha", "Gás de cozinha com desconto", "Valor recarga gás hoje", "Preço do gás de cozinha na portaria",
"Comprar gás com desconto", "Gás de cozinha preço atacado", "Preço do gás de cozinha em dinheiro", "Valor do gás para pagar no pix", "Gás de cozinha preço cartão",
"Promoção disk gás hoje", "Gás valor atual", "Menor valor do gás de cozinha hoje", "Preço do gás GLP", "Gás de cozinha preço promocional WhatsApp",
"Quanto tá o gás hoje", "Preço do botijão de gás completo", "Gás de cozinha barato entrega", "Valor do gás na distribuidora", "Tabela de preços gás de cozinha hoje",
"Promoção botijão de gás perto de mim", "Gás de cozinha valor de mercado", "Preço do gás de cozinha para retirar no local", "Qual o preço do gás de cozinha",
"Gás de cozinha preço baixo", "Cupom desconto gás aplicativo", "Gás de cozinha barato com entrega", "Preço médio botijão", "Gás de cozinha valor promocional",
"Onde o gás de cozinha é mais barato", "Valor do gás hoje", "Preço da recarga de gás hoje", "Gás de cozinha preço atual", "Promoção de gás hoje",
"Valor botijão de gás preço", "Gás de cozinha mais em conta", "Preço do gás de cozinha para revenda", "Gás preço menor", "Ofertas de gás de cozinha perto de mim",
"Valor do gás de cozinha hoje preço", "Gás de cozinha preço de custo", "Onde comprar gás com desconto", "Preço do gás de cozinha promoção WhatsApp",
"Gás de cozinha valor promocional", "Qual o valor do gás hoje", "Gás de cozinha menor preço entrega", "Preço do botijão de gás na portaria", "Valor do gás de cozinha em promoção",
"Gás de cozinha preço hoje", "Promoção de recarga de gás", "Gás de cozinha valor mais baixo", "Preço do gás na minha região", "Onde o gás tá barato",
"Gás de cozinha com menor preço", "Preço do gás GLP hoje", "Valor do botijão de gás atual", "Gás de cozinha promoção relâmpago", "Cupom primeira compra gás",
"Gás de cozinha valor entrega inclusa", "Preço do gás de cozinha na distribuidora", "Gás de cozinha barato disk gás", "Qual distribuidora de gás é mais barata",
"Preço do gás hoje valor atual", "Gás de cozinha valor de recarga", "Valor do botijão de gás hoje promoção", "Gás de cozinha perto de mim", "Depósito de gás próximo",
"Distribuidora de gás", "Gás", "Revenda de gás perto de mim", "Depósito de gás", "Onde tem gás perto de mim", "Distribuidora de gás aberta agora",
"Revenda de gás mais próxima", "Disk gás", "Ponto de venda de gás", "Telefone de gás", "Gás de cozinha na minha rua", "Depósito de gás aberto domingo",
"Gás de cozinha telefone", "Distribuidora de gás perto da minha localização", "Onde comprar gás", "Gás de cozinha aberto agora perto de mim", "Depósito de gás WhatsApp",
"Revenda de gás 24 horas perto de mim", "Gás de cozinha entrega", "Distribuidora de gás perto de mim", "Gás de cozinha mais próximo da minha localização",
"Disk gás telefone", "Onde encontrar gás", "Depósito de gás de cozinha próximo", "Gás de cozinha endereço perto de mim", "Distribuidora de gás de cozinha",
"Ponto de gás próximo", "Revenda de gás de cozinha perto", "Gás de cozinha entrega", "Onde tem depósito de gás por aqui", "Gás de cozinha perto de mim aberto agora",
"Telefone distribuidora de gás", "Gás de cozinha entrega rápida", "Depósito de gás próximo", "Localização de depósito de gás", "Gás de cozinha na região",
"Disk gás perto da minha casa", "Distribuidora de gás telefone", "Gás de cozinha preço", "Revenda de gás telefone perto de mim", "Gás de cozinha próximo da minha rua",
"Onde comprar botijão de gás", "Depósito de gás de cozinha", "Gás de cozinha entrega rápida", "Distribuidora de gás mais perto de mim", "Gás de cozinha aberto domingo perto de mim",
"Telefone do gás", "Ponto de venda de gás de cozinha próximo", "Gás de cozinha entrega WhatsApp", "Revenda de gás aberta agora perto de mim", "Onde vende gás de cozinha",
"Depósito de gás telefone", "Gás de cozinha preço hoje", "Distribuidora de gás 24h perto de mim", "Gás de cozinha WhatsApp", "Revenda de gás próxima",
"Onde tem caminhão do gás agora", "Gás de cozinha entrega em domicílio", "Depósito de gás mais próximo da minha residência", "Gás de cozinha telefone e endereço",
"Distribuidora de gás local", "Gás de cozinha disk entrega", "Ponto de recarga de gás próximo", "Revenda de gás perto de mim telefone WhatsApp", "Onde tem gás de cozinha",
"Depósito de gás de cozinha", "Gás de cozinha entrega grátis", "Distribuidora de gás perto de mim aberta", "Gás de cozinha onde comprar", "Revenda de gás com entrega rápida próxima",
"Onde buscar gás perto de mim", "Depósito de gás WhatsApp", "Gás de cozinha entrega rápida", "Distribuidora de gás de cozinha local", "Gás de cozinha na minha localização",
"Ponto de venda botijão de gás próximo", "Revenda de gás perto de mim endereço", "Onde encontrar depósito de gás", "Depósito de gás 24 horas", "Gás de cozinha entrega telefone",
"Distribuidora de gás barata", "Gás de cozinha preço perto de mim", "Revenda de gás perto de mim", "Onde tem gás barato", "Depósito de gás aberto agora",
"Gás de cozinha disk gás", "Distribuidora de gás telefone e WhatsApp", "Gás de cozinha entrega rápida perto", "Ponto de venda de gás de cozinha", "Revenda de gás mais barata perto de mim",
"Onde comprar gás", "Depósito de gás de cozinha perto de mim telefone", "Gás de cozinha valor", "Distribuidora de gás entrega", "Gás de cozinha perto de mim 24h",
"Revenda de gás entrega rápida", "Onde achar gás de cozinha perto de mim", "Depósito de gás telefone entrega"
]

keywords = sorted(list(set(keywords)))

import glob

# Add ONE discreet link to the footer of all files.
files = glob.glob('*.html')
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine if it's a neighborhood page or root page to point the link to the local version
    # Actually wait, the user wanted local versions for every neighborhood.
    # Generating 59 unique "Pesquisas Populares" pages is 59 files, not 8000. That's perfectly fine!
    
    # 1. We will NOT add tags to the footer directly. We just add ONE link in the footer.
    # We will add it next to "Bairros Atendidos"
    
    # Replace `<a href="bairros">Bairros Atendidos</a>`
    
    pass

# We will just write a master list page called "buscas.html"
with open('index.html', 'r', encoding='utf-8') as f:
    base_html = f.read()

# Make the page
header_end = base_html.find('<main id="main-content">') + len('<main id="main-content">')
footer_start = base_html.find('</main>')

page = base_html[:header_end]
page += """
        <section id="buscas-populares" style="background-color: #F0F5FA; min-height: 50vh;">
            <div class="container">
                <h2 class="section-title-modern animate-on-scroll">Pesquisas Populares por Gás em Cascavel</h2>
                <p style="text-align: center; max-width: 800px; margin: -20px auto 30px; color: #666;">
                    Encontre as principais formas que nossos clientes buscam nossos serviços de entrega rápida de gás e água.
                </p>
                <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; margin-top: 30px;">
"""

for kw in keywords:
    kw_c = f"{kw} em Cascavel" if "Cascavel" not in kw else kw
    page += f"""
                    <a href="produtos" style="background: white; padding: 15px; border-radius: 8px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05); text-decoration: none; color: var(--cor-primaria); font-size: 0.9em; transition: transform 0.3s;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">
                        <i class="fas fa-search" style="color: var(--cor-secundaria); margin-right: 8px;"></i>
                        {kw_c}
                    </a>
"""
page += """
                </div>
            </div>
        </section>
"""
page += base_html[footer_start:]

# Fix SEO for searches page
page = re.sub(r'<title>.*?</title>', f'<title>Pesquisas Frequentes de Gás em Cascavel | Zolet\'S Gás</title>', page, 1)
page = re.sub(r'<meta name="description" content="[^"]+">', f'<meta name="description" content="Lista das principais formas de buscar por entrega de gás, botijão e água mineral em Cascavel. Disk Gás 24 horas perto de você.">', page, 1)

with open('buscas.html', 'w', encoding='utf-8') as f:
    f.write(page)

# Update Footer globally to link to "buscas.html"
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The footer link structure:
    '''
                    <h3>Links Rápidos</h3>
                    <a href="produtos">Comprar Gás</a>
                    <a href="bairros">Bairros Atendidos</a>
                    <a href="faq">Dúvidas Frequentes</a>
                    <a href="contato">Fale Conosco</a>
    '''
    content = content.replace('<a href="bairros">Bairros Atendidos</a>', '<a href="bairros">Bairros Atendidos</a>\n                    <a href="buscas">Pesquisas Populares</a>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Update Sitemap
with open('sitemap.xml', 'r', encoding='utf-8') as f:
    sitemap = f.read()

new_sitemap_entry = """
  <url>
    <loc>https://www.zoletsgas.com.br/buscas</loc>
    <lastmod>2026-03-17</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.70</priority>
  </url>
"""
sitemap = sitemap.replace('</urlset>', new_sitemap_entry + '</urlset>')
with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap)

print("Created beautiful searches page without polluting footer.")
