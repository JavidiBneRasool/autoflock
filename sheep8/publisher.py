import json, os, hashlib, zipfile, time, subprocess, shutil, urllib.parse, random, html, re
from datetime import datetime

HEADER_HTML = """
    <header class="ai-header">
        <style>
@font-face{{font-family:'JameelNoori';src:url('/fonts/JameelNooriNastaleeq.ttf') format('truetype')}}
            @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;700&display=swap');
            @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
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
@font-face{{font-family:'JameelNoori';src:url('/fonts/JameelNooriNastaleeq.ttf') format('truetype')}}
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

AUTOFLOCK_STYLE = """
:root {
  --brand-black: #050505;
  --brand-card: #0f0f11;
  --brand-panel: rgba(15, 15, 17, 0.72);
  --brand-border: #222225;
  --brand-green: #00e599;
  --brand-red: #ff4d4d;
  --brand-purple: #a855f7;
  --brand-blue: #3b82f6;
  --text-main: #e7e9ee;
  --text-muted: #9ca3af;
}
* { box-sizing: border-box; }
html { background: var(--brand-black); }
body {
  margin: 0;
  min-height: 100vh;
  background:
    radial-gradient(circle at 18% -10%, rgba(0,229,153,.11), transparent 28rem),
    radial-gradient(circle at 88% 8%, rgba(168,85,247,.10), transparent 30rem),
    var(--brand-black);
  color: var(--text-main);
  font-family: "Inter", system-ui, sans-serif;}
body.ur {{ font-family: "JameelNoori", "Inter", sans-serif; direction: rtl; line-height: 1.9; }}
  -webkit-font-smoothing: antialiased;
}
a { color: inherit; text-decoration: none; }
.mono { font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace; }
.topbar {
  position: sticky; top: 0; z-index: 50;
  border-bottom: 1px solid var(--brand-border);
  background: rgba(5,5,5,.84);
  backdrop-filter: blur(14px);
}
.nav-inner, .wrap { width: min(1180px, calc(100% - 32px)); margin: 0 auto; }
.nav-inner { height: 64px; display: flex; align-items: center; justify-content: space-between; gap: 24px; }
.brand { display: flex; align-items: center; gap: 12px; min-width: max-content; }
.bolt {
  width: 32px; height: 32px; border-radius: 6px; display: grid; place-items: center;
  background: var(--brand-green); color: #020403; font-weight: 900;
}
.brand-word { font-size: 1.25rem; font-weight: 800; letter-spacing: -.04em; }
.brand-word span { color: var(--brand-green); }
.live-pill {
  padding: 3px 8px; border-radius: 999px;
  background: rgba(0,229,153,.10); color: var(--brand-green);
  border: 1px solid rgba(0,229,153,.22); font-size: .72rem; font-weight: 700;
}
.nav-links { display: flex; gap: 28px; color: var(--text-muted); font-size: .86rem; }
.nav-links a:hover, .nav-links a.active { color: #fff; }
.search-row { display: flex; align-items: center; gap: 12px; }
.search-box {
  width: 250px; border: 1px solid var(--brand-border); background: var(--brand-card);
  color: var(--text-main); border-radius: 10px; padding: 9px 12px; outline: none;
}
.search-box:focus { border-color: var(--brand-green); }
.connect-btn {
  border: 0; border-radius: 10px; padding: 9px 14px; background: #fff; color: #050505;
  font-weight: 800; cursor: pointer;
}
.hero { padding: 48px 0 28px; }
.hero-grid { display: grid; grid-template-columns: minmax(0,2fr) minmax(280px,1fr); gap: 24px; }
.glass-card {
  background: var(--brand-panel);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,.08);
  transition: border-color .25s ease, transform .25s ease, box-shadow .25s ease;
}
.glass-card:hover {
  border-color: rgba(255,255,255,.20);
  transform: translateY(-2px);
  box-shadow: 0 18px 42px -24px rgba(0,229,153,.40);
}
.featured { position: relative; overflow: hidden; border-radius: 18px; padding: clamp(24px, 4vw, 36px); min-height: 360px; cursor: pointer; }
.feature-mark {
  position: absolute; right: 28px; top: 28px; color: var(--brand-green);
  font-size: 8rem; opacity: .12; line-height: 1;
}
.badge-row { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; margin-bottom: 18px; }
.badge {
  display: inline-flex; align-items: center; gap: 6px; border-radius: 6px; padding: 5px 9px;
  border: 1px solid currentColor; font-size: .72rem; font-weight: 800;
}
.badge.opportunity { color: var(--brand-green); background: rgba(0,229,153,.12); }
.badge.warning { color: var(--brand-red); background: rgba(255,77,77,.12); }
.badge.signal { color: var(--brand-purple); background: rgba(168,85,247,.12); }
.badge.terminal { color: var(--brand-blue); background: rgba(59,130,246,.12); }
.meta { color: #6b7280; font-size: .72rem; font-weight: 700; }
.featured h1 {
  max-width: 780px; margin: 0 0 18px; font-size: clamp(2rem, 5vw, 4rem);
  line-height: 1.02; letter-spacing: -.055em;
}
.featured:hover h1 { color: var(--brand-green); }
.summary { max-width: 660px; color: var(--text-muted); font-size: 1rem; line-height: 1.7; }
.feature-foot {
  margin-top: 28px; padding-top: 22px; border-top: 1px solid var(--brand-border);
  display: flex; align-items: center; justify-content: space-between; gap: 16px;
}
.source-dot { width: 24px; height: 24px; border-radius: 999px; background: #374151; }
.read-link { color: var(--brand-green); font-weight: 800; }
.side-stack { display: flex; flex-direction: column; gap: 24px; }
.status-card, .mini-signal { border-radius: 18px; padding: 24px; }
.kicker { color: #6b7280; font-size: .72rem; letter-spacing: .16em; text-transform: uppercase; margin: 0 0 18px; }
.stat-row { display: flex; justify-content: space-between; gap: 12px; margin-top: 14px; font-size: .9rem; }
.bar { height: 6px; border-radius: 999px; background: #1f2937; overflow: hidden; margin-top: 10px; }
.bar span { display: block; height: 100%; border-radius: 999px; }
.mini-signal { border-left: 4px solid var(--brand-purple); }
.mini-signal h3 { margin: 8px 0; font-size: 1.2rem; }
.tabs { padding: 8px 0 26px; display: flex; gap: 12px; overflow-x: auto; }
.tab {
  white-space: nowrap; border: 1px solid var(--brand-border); color: var(--text-muted);
  background: var(--brand-card); border-radius: 999px; padding: 9px 14px; font-weight: 700; font-size: .86rem;
}
.tab.active { background: #fff; color: #050505; border-color: #fff; }
.feed-grid { display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 24px; padding-bottom: 72px; }
.feed-card { border-radius: 14px; padding: 24px; min-height: 255px; display: flex; flex-direction: column; justify-content: space-between; }
.feed-card h2 { margin: 0 0 12px; font-size: 1.08rem; line-height: 1.35; }
.feed-card h2:hover { color: var(--accent, var(--brand-green)); }
.feed-card p { color: var(--text-muted); font-size: .9rem; line-height: 1.58; margin: 0; }
.card-foot { margin-top: 18px; padding-top: 16px; border-top: 1px solid var(--brand-border); display: flex; justify-content: space-between; gap: 12px; color: #6b7280; font-size: .75rem; }
.site-footer { border-top: 1px solid var(--brand-border); background: #000; padding: 56px 0 28px; }
.footer-grid { display: grid; grid-template-columns: 1.2fr repeat(3, 1fr); gap: 38px; margin-bottom: 38px; }
.site-footer h4 { margin: 0 0 14px; color: #fff; }
.site-footer p, .site-footer li { color: #6b7280; font-size: .88rem; line-height: 1.6; }
.site-footer ul { list-style: none; padding: 0; margin: 0; display: grid; gap: 9px; }
.newsletter { display: flex; }
.newsletter input { min-width: 0; flex: 1; background: var(--brand-card); color: #fff; border: 1px solid var(--brand-border); border-radius: 8px 0 0 8px; padding: 10px; }
.newsletter button { border: 0; background: var(--brand-green); color: #050505; font-weight: 900; padding: 0 14px; border-radius: 0 8px 8px 0; }
.footer-bottom { border-top: 1px solid var(--brand-border); padding-top: 22px; display: flex; justify-content: space-between; gap: 16px; color: #4b5563; font-size: .72rem; }
.article-page .wrap { padding: 44px 0 72px; }
.article-shell { border-radius: 18px; padding: clamp(22px, 5vw, 46px); }
.hero-img { width: 100%; max-height: 420px; object-fit: cover; border-radius: 14px; border: 1px solid var(--brand-border); margin-bottom: 28px; }
.article-body { color: var(--text-main); font-size: clamp(1rem, 2.4vw, 1.18rem); line-height: 1.86; }
.article-body h1, .article-body h2, .article-body h3 { color: #fff; letter-spacing: -.025em; }
.article-body a { color: var(--brand-green); }
.source-link { margin-top: 28px; padding-top: 18px; border-top: 1px solid var(--brand-border); color: var(--text-muted); }
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #050505; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 4px; }
@media (max-width: 920px) {
  .hero-grid, .feed-grid, .footer-grid { grid-template-columns: 1fr; }
  .nav-links, .search-row { display: none; }
}
@media (max-width: 560px) {
  .nav-inner, .wrap { width: min(100% - 20px, 1180px); }
  .featured { min-height: auto; }
  .feature-foot, .footer-bottom { align-items: flex-start; flex-direction: column; }
}
"""

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

def _slugify(value):
    import re
    slug = re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-")
    return slug[:100] or hashlib.md5(str(value).encode()).hexdigest()[:12]

def _escape(value):
    return html.escape(str(value or ""), quote=True)

def _clean_text(value, limit=180):
    text = str(value or "").replace("#", " ").replace("*", " ").replace("\n", " ")
    text = " ".join(text.split())
    return text[:limit].rstrip() + ("..." if len(text) > limit else "")

def _signal_type(article):
    text = f"{article.get('headline', '')} {article.get('category', '')}".lower()
    if "warning" in text or "risk" in text or "security" in text:
        return ("warning", "WARNING", "RISK REPORT", "var(--brand-red)")
    if "terminal" in text or "dev" in text or "github" in text:
        return ("terminal", "TERMINAL", "DEV", "var(--brand-blue)")
    if "signal" in text or "analysis" in text:
        return ("signal", "SIGNAL", "ANALYSIS", "var(--brand-purple)")
    return ("opportunity", "OPPORTUNITY", "STRATEGY", "var(--brand-green)")

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

    with open(f"{SITE_DIR}/style.css", "w", encoding="utf-8") as f:
        f.write(AUTOFLOCK_STYLE.strip() + "\n")

    # Generate Index Page
    index_html = _build_index(history[:12])
    with open(f"{SITE_DIR}/index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

    # Generate Article Pages (Regenerate All)
    for a in history:
        filename = a.get("filename", f"{_slugify(a.get('headline', 'article'))}.html")
        a["filename"] = filename
        content = _build_article_page(a)
        with open(f"{SITE_DIR}/{filename}", "w", encoding="utf-8") as f:
            f.write(content)

    print(f"🐑 SHEEP 8: {len(current_articles)} SEO-optimized articles published ✓")
    return {"published": True}

def _build_index(latest):
    latest = latest or []
    featured = latest[0] if latest else {}
    secondary = latest[1] if len(latest) > 1 else featured
    f_kind, f_label, f_meta, _ = _signal_type(featured)
    s_kind, s_label, _, _ = _signal_type(secondary)
    featured_url = _escape(featured.get("filename", "#"))
    featured_title = _escape(featured.get("headline", "Auto Flock Intelligence Network"))
    featured_summary = _escape(_clean_text(featured.get("body") or featured.get("summary"), 250))
    featured_source = _escape(featured.get("source", "Auto Flock Agent"))
    secondary_title = _escape(secondary.get("headline", "Autonomous signal engine online"))
    secondary_summary = _escape(_clean_text(secondary.get("body") or secondary.get("summary"), 120))
    secondary_source = _escape(secondary.get("source", "Auto Flock"))

    cards_html = ""
    for a in latest[1:]:
        kind, label, meta, accent = _signal_type(a)
        filename = _escape(a.get("filename", "#"))
        title = _escape(a.get("headline", "Untitled signal"))
        excerpt = _escape(_clean_text(a.get("body") or a.get("summary"), 165))
        source = _escape(a.get("source", "Auto Flock"))
        date = _escape(str(a.get("written_at", "") or a.get("published_at", "") or "Live")[:10])
        cards_html += f"""
            <article class="glass-card feed-card" style="--accent:{accent}" onclick="window.location.href='{filename}'">
                <div>
                    <div class="badge-row">
                        <span class="badge {kind}">{label}</span>
                        <span class="meta mono">{meta}</span>
                    </div>
                    <h2>{title}</h2>
                    <p>{excerpt}</p>
                </div>
                <div class="card-foot mono">
                    <span>{source}</span>
                    <span>{date}</span>
                </div>
            </article>"""

    return f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AUTO FLOCK | AI Intelligence Network</title>
    <meta name="google-site-verification" content="Dthc_OiAqsG2NxrZXLE_gE84PLsD4_fLmc71KGGgKQI" />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav class="topbar">
        <div class="nav-inner">
            <a class="brand" href="/">
                <span class="bolt">⚡</span>
                <span class="brand-word mono">AUTO<span>FLOCK</span></span>
                <span class="live-pill mono">v2.1 LIVE</span>
            </a>
            <div class="nav-links mono">
                <a class="active" href="/">Dashboard</a>
                <a href="#signals">Signals</a>
                <a href="#research">Research</a>
                <a href="#terminal">Terminal</a>
            </div>
            <div class="search-row">
                <input class="search-box" type="search" placeholder="Search intelligence..." oninput="filterCards(this.value)">
                <button class="connect-btn">Connect Wallet</button>
            </div>
        </div>
    </nav>

    <header class="wrap hero">
        <div class="hero-grid">
            <article class="glass-card featured" onclick="window.location.href='{featured_url}'">
                <div class="feature-mark">◆</div>
                <div class="badge-row">
                    <span class="badge {f_kind}">{f_label}</span>
                    <span class="meta mono">AI RESEARCH • LIVE</span>
                </div>
                <h1>{featured_title}</h1>
                <p class="summary">{featured_summary}</p>
                <div class="feature-foot">
                    <div style="display:flex;align-items:center;gap:10px">
                        <span class="source-dot"></span>
                        <span class="mono">{featured_source}</span>
                    </div>
                    <span class="read-link mono">Read Analysis →</span>
                </div>
            </article>

            <aside class="side-stack">
                <section class="glass-card status-card">
                    <p class="kicker mono">System Status</p>
                    <div class="stat-row"><span>Neural Net Load</span><strong class="mono" style="color:var(--brand-green)">98%</strong></div>
                    <div class="bar"><span style="width:98%;background:var(--brand-green)"></span></div>
                    <div class="stat-row"><span>Threat Level</span><strong class="mono" style="color:var(--brand-red)">HIGH</strong></div>
                    <div class="bar"><span style="width:75%;background:var(--brand-red)"></span></div>
                </section>
                <section class="glass-card mini-signal">
                    <span class="badge {s_kind}">{s_label}</span>
                    <h3>{secondary_title}</h3>
                    <p class="summary" style="font-size:.9rem">{secondary_summary}</p>
                    <span class="meta mono">{secondary_source}</span>
                </section>
            </aside>
        </div>
    </header>

    <section class="wrap tabs mono">
        <button class="tab active" onclick="filterCards('')">All Feeds</button>
        <button class="tab" onclick="filterCards('warning')">Warnings</button>
        <button class="tab" onclick="filterCards('opportunity')">Opportunities</button>
        <button class="tab" onclick="filterCards('terminal')">Terminal/Dev</button>
        <button class="tab" onclick="filterCards('security')">Automation/Sec</button>
    </section>

    <main class="wrap" id="signals">
        <div class="feed-grid" id="feedGrid">
            {cards_html}
        </div>
    </main>

    <footer class="site-footer">
        <div class="wrap">
            <div class="footer-grid">
                <div>
                    <span class="brand-word mono">AUTO<span>FLOCK</span></span>
                    <p>Autonomous Infrastructure for the AI Age. Real-time intelligence aggregation and risk analysis.</p>
                </div>
                <div><h4 class="mono">Platform</h4><ul><li>API Documentation</li><li>System Status</li><li>Pricing</li></ul></div>
                <div><h4 class="mono">Intelligence</h4><ul><li>Threat Reports</li><li>Market Signals</li><li>Research Papers</li></ul></div>
                <div><h4 class="mono">Newsletter</h4><div class="newsletter"><input type="email" placeholder="agent@auto.flock"><button>→</button></div></div>
            </div>
            <div class="footer-bottom mono">
                <span>© 2026 AI Flock Empire — Auto Flock Network</span>
                <span>SYSTEM STATUS: OPTIMAL • PROTOCOL: X-7 NEURAL</span>
            </div>
        </div>
    </footer>
    <script>
      function filterCards(query) {{
        const q = String(query || '').toLowerCase();
        document.querySelectorAll('.feed-card').forEach(card => {{
          card.style.display = card.innerText.toLowerCase().includes(q) ? '' : 'none';
        }});
      }}
    </script>
</body>
</html>"""

def _get_affiliate_block(category):
    c = category.lower()
    branding = "AI Infrastructure: Institutional-Grade Compute & Deployments"
    
    affiliates = [
        ("RunPod", "https://www.runpod.io/?ref=autoflock", "fa-solid fa-server"),
        ("Vast.ai", "https://vast.ai/?ref=autoflock", "fa-solid fa-microchip"),
        ("Railway", "https://railway.app?referralCode=autoflock", "fa-solid fa-train-subway"),
        ("DigitalOcean", "https://m.do.co/c/autoflock", "fa-solid fa-droplet"),
        ("Hostinger", "https://www.hostinger.com/autoflock", "fa-solid fa-hosting")
    ]
    
    links_html = "".join([f'''
        <a href="{url}" target="_blank" class="affiliate-card">
            <i class="{icon}"></i>
            <span>{name}</span>
        </a>''' for name, url, icon in affiliates])
    
    return f'''
    <div class="affiliate-container">
        <h4 class="affiliate-title">{branding}</h4>
        <div class="affiliate-grid">
            {links_html}
        </div>
    </div>
    '''

def _get_adsense_tag():
    try:
        with open(f"{PROJECT}/config/adsense.json", "r") as f:
            config = json.load(f)
            return config.get("script_tag", "")
    except:
        return ""


def _markdown_to_html(value):
    if not value: return ""
    # Ensure headers have a space after # for reliable parsing
    value = re.sub(r'^(#+)([A-Za-z0-9])', r'\1 \2', str(value), flags=re.MULTILINE)
    try:
        import markdown
        return markdown.markdown(value, extensions=['extra'])
    except Exception:
        paragraphs = [p.strip() for p in str(value).split("\n\n") if p.strip()]
        return "\n".join(f"<p>{html.escape(p)}</p>" for p in paragraphs)

def _build_article_page(a):
    body_html = _markdown_to_html(a.get('body', ''))
    affiliate_block = _get_affiliate_block(a.get('category', 'Default'))
    adsense = _get_adsense_tag()
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{a.get('headline', 'AutoFlock | AI Intelligence')}</title>
    <meta name="google-site-verification" content="Dthc_OiAqsG2NxrZXLE_gE84PLsD4_fLmc71KGGgKQI" />
    {a.get('meta', '')}
    {adsense}
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    <style>
@font-face{{font-family:'JameelNoori';src:url('/fonts/JameelNooriNastaleeq.ttf') format('truetype')}}
        .article-content {{ max-width: 850px; margin: 0 auto; padding: 2rem 1rem; }}
        .article-body {{ 
            font-size: 1.15rem; 
            line-height: 1.8; 
            color: var(--text-main); 
        }}
        .article-body h1, .article-body h2, .article-body h3 {{ 
            font-family: 'Space Grotesk', sans-serif; 
            color: #fff; 
            margin-top: 3rem;
            margin-bottom: 1.5rem;
            text-align: left;
        }}
        .article-body p {{ margin-bottom: 1.5rem; text-align: left; }}
        .article-body ul, .article-body ol {{ margin-bottom: 1.5rem; padding-left: 1.5rem; text-align: left; }}
        .article-body li {{ margin-bottom: 0.5rem; }}
        
        .article-body table {{
            width: 100%;
            border-collapse: collapse;
            margin: 2rem 0;
            background: rgba(255,255,255,0.02);
            border-radius: 8px;
            overflow: hidden;
        }}
        .article-body th, .article-body td {{
            padding: 1rem;
            border: 1px solid rgba(255,255,255,0.1);
            text-align: left;
        }}
        .article-body th {{
            background: rgba(255,255,255,0.05);
            color: #fff;
            font-weight: 700;
        }}
        
        /* Affiliate Grid Styles */
        .affiliate-container {{
            background: linear-gradient(145deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 100%);
            border: 1px solid rgba(0, 255, 255, 0.1);
            border-radius: 20px;
            padding: 2.5rem;
            margin: 4rem 0;
            backdrop-filter: blur(15px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            text-align: center;
        }}
        .affiliate-title {{
            color: #fff;
            margin-bottom: 2rem;
            font-size: 1.2rem;
            font-weight: 700;
            text-align: center;
            letter-spacing: 0.5px;
            font-family: 'Space Grotesk', sans-serif;
            text-transform: uppercase;
            opacity: 0.8;
        }}
        .affiliate-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 1.5rem;
        }}
        .affiliate-card {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 12px;
            text-decoration: none;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .affiliate-card:hover {{
            background: rgba(0, 255, 255, 0.05);
            border-color: rgba(0, 255, 255, 0.2);
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }}
        .affiliate-card i {{
            font-size: 2rem;
            color: #0ff;
        }}
        .affiliate-card span {{
            color: #fff;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            text-align: center;
        }}
        
        .hero-img {{
            width: 100%;
            height: 400px;
            object-fit: cover;
            border-radius: 16px;
            margin-bottom: 3rem;
            box-shadow: 0 15px 30px rgba(0,0,0,0.4);
            border: 1px solid var(--brand-border);
        }}
        .source-link {{
            margin-top: 4rem;
            padding-top: 2rem;
            border-top: 1px solid var(--brand-border);
            font-size: 0.85rem;
            color: var(--text-muted);
            text-align: center;
        }}
        .source-link a {{ color: var(--brand-green); text-decoration: none; font-weight: 600; }}
        
        @media (max-width: 768px) {{
            .hero-img {{ height: 250px; }}
            .affiliate-grid {{ grid-template-columns: repeat(2, 1fr); }}
        }}
    </style>
</head>
<body class="article-page dark">
    {HEADER_HTML}
    <main class="article-content">
        <article>
            <img src="{a['image_url']}" class="hero-img" alt="{a['headline']}">
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
