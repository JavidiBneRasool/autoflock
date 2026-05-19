import json, os, hashlib, zipfile, time, subprocess, shutil, urllib.parse, random, html
from datetime import datetime

HEADER_HTML = """
    <header class="ai-header">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;700&display=swap');
            .ai-header {
                position: sticky; top: 0; z-index: 9999; width: 100%;
                background: rgba(5, 5, 5, 0.75); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
                border-bottom: 1px solid rgba(0, 255, 255, 0.15);
                font-family: 'Space Grotesk', sans-serif;
            }
            .ai-header-content {
                max-width: 1200px; margin: 0 auto; padding: 0.75rem 1.5rem;
                display: flex; justify-content: space-between; align-items: center;
            }
            .ai-logo { text-decoration: none; display: flex; flex-direction: column; }
            .ai-logo-text { font-size: 1.25rem; font-weight: 700; color: #fff; text-transform: uppercase; letter-spacing: -0.5px; }
            .ai-logo-text span { color: #0ff; text-shadow: 0 0 12px rgba(0, 255, 255, 0.4); }
            .ai-tagline { font-size: 0.65rem; color: rgba(255, 255, 255, 0.4); text-transform: uppercase; letter-spacing: 1.5px; margin-top: 2px; }
            .ai-status-pill {
                padding: 0.35rem 0.75rem; background: rgba(0, 255, 255, 0.05); border: 1px solid rgba(0, 255, 255, 0.1);
                border-radius: 100px; font-size: 0.7rem; color: #fff; font-weight: 500;
                display: flex; align-items: center; gap: 0.5rem;
            }
            @media (max-width: 640px) { .ai-tagline { display: none; } }
        </style>
        <div class="ai-header-content">
            <a href="/" class="ai-logo">
                <div class="ai-logo-text">Auto <span>Flock</span></div>
                <div class="ai-tagline">Autonomous Journalism for the Agentic Era</div>
            </a>
            <div class="ai-status-pill">
                <span style="color: #0ff;">🟢</span> Engine: Auto Flock Agent
            </div>
        </div>
    </header>
"""

FOOTER_HTML = """
    <footer class="ai-footer">
        <style>
            .ai-footer {
                padding: 4rem 1.5rem; background: #050505; border-top: 1px solid rgba(255, 255, 255, 0.05);
                font-family: 'Space Grotesk', sans-serif; text-align: center;
            }
            .ai-footer-logo { font-size: 1.1rem; font-weight: 700; color: #fff; text-transform: uppercase; margin-bottom: 0.5rem; }
            .ai-footer-logo span { color: #0ff; }
            .ai-footer-text { font-size: 0.8rem; color: rgba(255, 255, 255, 0.3); margin-bottom: 1.5rem; line-height: 1.6; }
            .ai-footer-bottom { font-size: 0.65rem; color: rgba(255, 255, 255, 0.15); text-transform: uppercase; letter-spacing: 2px; }
        </style>
        <div class="ai-footer-logo">Auto <span>Flock</span></div>
        <p class="ai-footer-text">© 2026 AI Flock Empire — Auto Flock Network | Autonomous Infrastructure</p>
        <div class="ai-footer-bottom">System Status: Optimal • Protocol: X-7 Neural</div>
    </footer>
"""

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"
SITE_DIR = os.path.join(PROJECT, "publish")
HISTORY_FILE = f"{PROJECT}/history.json"

def _pick_unique_image(headline, category, used_set):
    # (Simplified for now, Sheep 6 and 5 already handle images better)
    return "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80"

def _normalize_autoflock_article(article):
    replacements = {
        "NewsHour Intelligence": "Auto Flock Intelligence",
        "NewsHour Signal Engine": "Auto Flock Signal Engine",
        "NewsHour Flock": "Auto Flock",
        "https://newshour.cutbar.in": "https://autoflock.cutbar.in",
    }
    for key in ("body", "summary", "description"):
        value = article.get(key)
        if isinstance(value, str):
            for old, new in replacements.items():
                value = value.replace(old, new)
            article[key] = value
    return article

def run():
    print("🐑 SHEEP 8: Publishing Expert Signals...")
    os.makedirs(SITE_DIR, exist_ok=True)
    
    try:
        with open(f"{OUTPUT}/sheep7_audited.json", "r") as f:
            current_articles = json.load(f)
    except:
        print("🐑 SHEEP 8: No articles!"); return None
    
    # Load and Update History
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    
    current_articles = [_normalize_autoflock_article(a) for a in current_articles]
    history = current_articles + history
    history = history[:150]
    
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

    # Generate Index Page
    index_html = _build_index(history[:12])
    with open(f"{SITE_DIR}/index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

    # Generate Article Pages
    for a in current_articles:
        filename = a.get("filename", f"{datetime.now().strftime('%Y%m%d%H%M%S')}.html")
        content = _build_article_page(a)
        with open(f"{SITE_DIR}/{filename}", "w", encoding="utf-8") as f:
            f.write(content)

    print(f"🐑 SHEEP 8: {len(current_articles)} SEO-optimized articles published ✓")
    return {"published": True}

def _build_index(latest):
    articles_html = ""
    for a in latest:
        excerpt = a.get("body", "").split("---")[0].replace('#','').replace('*','').strip()[:140] + "..."
        filename = a.get("filename", "#")
        articles_html += f"""
            <div class="pro-card" onclick="window.location.href='{filename}'">
                <div class="tag">{a['category']}</div>
                <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 1.3rem;">{a['headline']}</h3>
                <p>{excerpt}</p>
                <div class="card-foot">
                    <span>{a['source']}</span>
                </div>
            </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Auto Flock | AI Intelligence Hub</title>
    <link rel="stylesheet" href="style.css">
</head>
<body class="dark-theme">
    {HEADER_HTML}
    <div class="container">
        <div class="pro-grid">
            {articles_html}
        </div>
    </div>
    {FOOTER_HTML}
</body>
</html>"""

def _get_affiliate_block(category):
    c = category.lower()
    if 'tech' in c or 'ai' in c:
        branding = "AI Infrastructure: Institutional-Grade Compute & Deployments"
        links = [
            ("RunPod", "https://www.runpod.io/?ref=autoflock"),
            ("Vast.ai", "https://vast.ai/?ref=autoflock"),
            ("Railway", "https://railway.app?referralCode=autoflock"),
            ("DigitalOcean", "https://m.do.co/c/autoflock"),
            ("Hostinger", "https://www.hostinger.com/autoflock")
        ]
    else:
        branding = "Autonomous Infrastructure: Optimize Your Stack"
        links = [("Auto Infrastructure", "#")]
    
    links_html = "".join([f'<a href="{url}" style="color:var(--accent-blue); margin: 0 10px; text-decoration:none;">{name}</a>' for name, url in links])
    
    return f'''
    <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 2rem; margin: 3rem 0; text-align: center; backdrop-filter: blur(10px);">
        <h4 style="color: #fff; margin-bottom: 1rem; font-size: 1.25rem;">{branding}</h4>
        <div>{links_html}</div>
    </div>
    '''

def _markdown_to_html(value):
    try:
        import markdown
        return markdown.markdown(value)
    except Exception:
        paragraphs = [p.strip() for p in str(value).split("\n\n") if p.strip()]
        return "\n".join(f"<p>{html.escape(p)}</p>" for p in paragraphs)

def _build_article_page(a):
    body_html = _markdown_to_html(a.get('body', ''))
    affiliate_block = _get_affiliate_block(a.get('category', 'Default'))
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {a.get('meta', '')}
    <link rel="stylesheet" href="style.css">
    <style>
        .article-body {{ font-size: 1.35rem; line-height: 1.9; color: rgba(255, 255, 255, 0.8); }}
        .article-body h1, .article-body h2, .article-body h3 {{ font-family: 'Space Grotesk', sans-serif; color: #fff; margin-top: 2.5rem; }}
    </style>
</head>
<body class="article-page dark-theme">
    {HEADER_HTML}
    <main class="container">
        <article class="pro-card-expanded">
            <img src="{a['image_url']}" class="hero-img">
            <div class="article-body">
                {body_html}
                {affiliate_block}
            </div>
            <div class="source-link">
                Source: <a href="{a['source_url']}" target="_blank">{a['source']}</a>
            </div>
        </article>
    </main>
    {FOOTER_HTML}
</body>
</html>"""

if __name__ == "__main__":
    run()
