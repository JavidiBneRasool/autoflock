import json, os, datetime

PROJECT = os.path.dirname(os.path.abspath(__file__))
PUBLISH_DIR = f"{PROJECT}/publish"
SITEMAP_FILE = f"{PROJECT}/sitemap.xml"
NEWS_SITEMAP_FILE = f"{PROJECT}/news-sitemap.xml"
BASE_URL = "https://autoflock.cutbar.in"

def generate_sitemap():
    print("🐑 SHEEP 14: Updating Sitemap & SEO Index...")
    
    articles = []
    # Scan publish directory for html files (excluding index.html)
    if not os.path.exists(PUBLISH_DIR):
        os.makedirs(PUBLISH_DIR, exist_ok=True)

    for f in os.listdir(PUBLISH_DIR):
        if f.endswith(".html") and f != "index.html":
            articles.append(f)
    articles.sort(key=lambda name: os.path.getmtime(os.path.join(PUBLISH_DIR, name)), reverse=True)
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # Add Home
    xml.append(f'  <url><loc>{BASE_URL}/</loc><changefreq>hourly</changefreq><priority>1.0</priority></url>')
    
    # Add Articles
    for art in articles:
        xml.append(f'  <url><loc>{BASE_URL}/{art}</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>')
    
    xml.append('</urlset>')
    
    with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(xml))
    
    print(f"✅ Sitemap updated with {len(articles)} URLs.")

    news_xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    news_xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">')
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    for art in articles[:1000]:
        title = art.replace(".html", "").replace("-", " ").title()
        news_xml.append(f'  <url><loc>{BASE_URL}/{art}</loc><news:news><news:publication><news:name>AutoFlock</news:name><news:language>en</news:language></news:publication><news:publication_date>{today}</news:publication_date><news:title>{title}</news:title></news:news></url>')
    news_xml.append('</urlset>')
    with open(NEWS_SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(news_xml))
    print(f"✅ News sitemap updated with {min(len(articles), 1000)} URLs.")

    # ROBOTS.TXT
    with open(f"{PROJECT}/robots.txt", "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\nSitemap: {BASE_URL}/news-sitemap.xml\n")
    
    print("✅ robots.txt generated.")

if __name__ == "__main__":
    generate_sitemap()
