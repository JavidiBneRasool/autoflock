import json, os, random, re
from datetime import datetime
from slugify import slugify

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"

def generate_seo_meta(headline, summary, image_url):
    return f"""
    <!-- SEO & Social Meta Tags -->
    <title>{headline} | Auto Flock Intelligence</title>
    <meta name="description" content="{summary[:160]}">
    <meta property="og:title" content="{headline}">
    <meta property="og:description" content="{summary[:160]}">
    <meta property="og:image" content="{image_url}">
    <meta property="og:type" content="article">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{headline}">
    <meta name="twitter:description" content="{summary[:160]}">
    <meta name="twitter:image" content="{image_url}">
    """

def run():
    print("🐑 SHEEP 6: Expert Analyst Writing...")
    try:
        with open(f"{OUTPUT}/sheep5_headlines.json") as f:
            headlines = json.load(f)
    except FileNotFoundError:
        print("🐑 SHEEP 6: No input!"); return None
    
    articles = []
    for item in headlines:
        h = item["headline"]
        a = item["article"]
        iu = item["image_url"]
        
        # SLUG GENERATION: Replace cryptic dates with human-readable slugs
        clean_headline = h.split(":", 1)[-1].split("—")[0].strip()
        slug = slugify(clean_headline)
        filename = f"{slug}.html"
        
        summary_text = a.get('summary', 'Detailed analysis pending.')
        
        # EXPERT ANALYST PROMPT LOGIC (Simulated for this script structure)
        # We transform the summary into a 'Contrarian Deep Dive'
        body = f"""# {h}

*Auto Flock Senior Analyst | {datetime.now().strftime('%B %d, %Y')}*

---

## 🎯 The Intelligence Signal
{summary_text}

## ⚡ Why This Matters (The Macro View)
While most outlets report the 'what', our intelligence engine focuses on the 'why'. This development in {a.get('category')} isn't just a news item; it's a structural pivot. 

## ⚖️ The Contrarian Perspective
Industry consensus suggests a linear impact, but our data indicates a potential 'Black Swan' ripple effect. If {a.get('category')} continues this trajectory, we expect {a.get('source')} readers to face a significant volatility spike.

## 📈 Strategic Alpha
• **Immediate Action:** Audit your {a.get('category')} exposure.
• **Long-term Play:** Position for the inevitable technical correction.
"""
        
        articles.append({
            "category": item["category"],
            "headline": h,
            "slug": slug,
            "filename": filename,
            "meta": generate_seo_meta(h, summary_text, iu),
            "image_url": iu,
            "body": body,
            "source": a["source"],
            "source_url": a["url"],
            "written_at": datetime.now().isoformat()
        })
    
    with open(f"{OUTPUT}/sheep6_articles.json", "w") as f:
        json.dump(articles, f, indent=2)
    
    print(f"🐑 SHEEP 6: {len(articles)} analyst reports written with SEO slugs ✓")
    return articles

if __name__ == "__main__":
    run()
