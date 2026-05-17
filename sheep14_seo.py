import json, os, datetime

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLISH_DIR = f"{PROJECT}/publish"
SITEMAP_FILE = f"{PROJECT}/sitemap.xml"
BASE_URL = "https://autoflock.cutbar.in"

def generate_sitemap():
    print("🐑 SHEEP 14: Updating Sitemap & SEO Index...")
    
    articles = []
    # Scan publish directory for html files (excluding index.html)
    for f in os.listdir(PUBLISH_DIR):
        if f.endswith(".html") and f != "index.html":
            articles.append(f)
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # Add Home
    xml.append(f'  <url><loc>{BASE_URL}/</loc><changefreq>hourly</changefreq><priority>1.0</priority></url>')
    
    # Add Articles
    for art in articles:
        xml.append(f'  <url><loc>{BASE_URL}/{art}</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>')
    
    xml.append('</urlset>')
    
    with open(SITEMAP_FILE, "w") as f:
        f.write("\n".join(xml))
    
    print(f"✅ Sitemap updated with {len(articles)} URLs.")

    # ROBOTS.TXT
    with open(f"{PROJECT}/robots.txt", "w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml")
    
    print("✅ robots.txt generated.")

if __name__ == "__main__":
    generate_sitemap()
