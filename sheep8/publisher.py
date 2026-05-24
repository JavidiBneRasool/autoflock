import json, os, hashlib, zipfile, time, subprocess, shutil, urllib.parse, random, html, re
from datetime import datetime

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
body.light-mode {
  --brand-black: #ffffff;
  --brand-card: #f9fafb;
  --brand-panel: rgba(255, 255, 255, 0.9);
  --brand-border: #e5e7eb;
  --text-main: #111827;
  --text-muted: #4b5563;
}

@font-face {
  font-family: 'JameelNoori';
  src: url('/fonts/JameelNooriNastaleeq.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

* { box-sizing: border-box; }
html { background: var(--brand-black); }
body {
  margin: 0;
  min-height: 100vh;
  background: var(--brand-black);
  color: var(--text-main);
  font-family: Inter, system-ui, sans-serif;
  -webkit-font-smoothing: antialiased;
  transition: all 0.3s ease;
  font-size: 18px;
}

/* Force Nastaleeq for Urdu */
[dir="rtl"], body.ur, body.ur * { 
  font-family: 'JameelNoori', serif !important; 
  line-height: 2 !important;
  text-align: right !important;
}

a { color: inherit; text-decoration: none; }
.mono { font-family: "JetBrains Mono", ui-monospace, monospace; }
.wrap { width: min(1180px, calc(100% - 32px)); margin: 0 auto; }

.hero { padding: 48px 0 28px; }
.hero-grid { display: grid; grid-template-columns: minmax(0,2fr) minmax(280px,1fr); gap: 24px; }
.glass-card {
  background: var(--brand-panel);
  backdrop-filter: blur(12px);
  border: 1px solid var(--brand-border);
  transition: all .25s ease;
}
.glass-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
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
.meta { color: var(--text-muted); font-size: .72rem; font-weight: 700; }
.featured h1 {
  max-width: 780px; margin: 0 0 18px; font-size: 2rem;
  line-height: 1.1; letter-spacing: -.03em;
}
.featured:hover h1 { color: var(--brand-green); }
.summary { max-width: 660px; color: var(--text-muted); font-size: 0.95rem; line-height: 1.6; }
.feature-foot {
  margin-top: 28px; padding-top: 22px; border-top: 1px solid var(--brand-border);
  display: flex; align-items: center; justify-content: space-between; gap: 16px;
}
.read-link { color: var(--brand-green); font-weight: 800; }
.side-stack { display: flex; flex-direction: column; gap: 24px; }
.status-card, .mini-signal { border-radius: 18px; padding: 24px; }
.kicker { color: var(--text-muted); font-size: .72rem; letter-spacing: .16em; text-transform: uppercase; margin: 0 0 18px; }
.stat-row { display: flex; justify-content: space-between; gap: 12px; margin-top: 14px; font-size: .9rem; }
.bar { height: 6px; border-radius: 999px; background: rgba(0,0,0,0.2); overflow: hidden; margin-top: 10px; }
.bar span { display: block; height: 100%; border-radius: 999px; }

.feed-grid { display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 24px; padding-bottom: 72px; }
.feed-card { border-radius: 14px; padding: 24px; min-height: 255px; display: flex; flex-direction: column; justify-content: space-between; cursor: pointer; }
.feed-card h2 { margin: 0 0 12px; font-size: 1.15rem; line-height: 1.35; color: var(--text-main); }
.feed-card p { color: var(--text-muted); font-size: .9rem; line-height: 1.58; margin: 0; }
.card-foot { margin-top: 18px; padding-top: 16px; border-top: 1px solid var(--brand-border); display: flex; justify-content: space-between; gap: 12px; color: var(--text-muted); font-size: .75rem; }

.article-content { max-width: 800px; margin: 0 auto; padding: 2rem 1.5rem; }
.article-body { font-size: 1.1rem; line-height: 1.7; color: var(--text-main); }
.article-body h1, .article-body h2, .article-body h3 { font-family: inherit; color: var(--text-main); margin-top: 2.5rem; margin-bottom: 1.2rem; font-weight: 700; }
.article-body p { margin-bottom: 1.2rem; }

.affiliate-container { background: var(--brand-panel); border: 1px solid var(--brand-border); border-radius: 16px; padding: 2rem; margin: 3.5rem 0; backdrop-filter: blur(10px); text-align: center; }
.affiliate-title { color: var(--text-main); margin-bottom: 1.8rem; font-size: 1.2rem; font-weight: 700; font-family: 'Space Grotesk', sans-serif; text-transform: uppercase; opacity: 0.8; }
.affiliate-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 1.2rem; }
.affiliate-card { background: rgba(255, 255, 255, 0.03); border: 1px solid var(--brand-border); border-radius: 12px; padding: 1.2rem; display: flex; flex-direction: column; align-items: center; gap: 10px; text-decoration: none; transition: all 0.3s ease; }
.affiliate-card:hover { background: rgba(0, 255, 255, 0.05); border-color: rgba(0, 255, 255, 0.2); transform: translateY(-3px); }
.affiliate-card i { font-size: 1.8rem; color: #0ff; }
.affiliate-card span { color: var(--text-main); font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }

.hero-img { width: 100%; height: 400px; object-fit: cover; border-radius: 12px; margin-bottom: 2.5rem; box-shadow: 0 10px 30px rgba(0,0,0,0.2); border: 1px solid var(--brand-border); }
.source-link { margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid var(--brand-border); font-size: 0.85rem; color: var(--text-muted); text-align: center; }
.source-link a { color: var(--brand-green); text-decoration: none; font-weight: 600; }

@media (max-width: 920px) {
  .hero-grid, .feed-grid { grid-template-columns: 1fr; }
}
@media (max-width: 768px) {
    .hero-img { height: 220px; }
    .affiliate-grid { grid-template-columns: repeat(2, 1fr); }
    .article-body { font-size: 1.05rem; }
}
"""

HEADER_HTML = """
    <header class="ai-header">
        <style>
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
            .ai-nav-tools { display: flex; align-items: center; gap: 1rem; }
            .theme-btn, .lang-btn {
                background: rgba(0, 255, 255, 0.05); color: #fff;
                border: 1px solid rgba(0, 255, 255, 0.1); padding: 0.4rem 0.7rem; border-radius: 8px; cursor: pointer; font-size: 0.75rem;
                transition: all 0.2s ease;
            }
            .lang-btn.active { border-color: #0ff; color: #0ff; }
            @media (max-width: 640px) { .ai-tagline { display: none; } }
        </style>
        <div class="ai-header-content">
            <a href="/" class="ai-logo">
                <div class="ai-logo-text">Auto <span>Flock</span></div>
                <div class="ai-tagline">Autonomous Journalism for the Agentic Era</div>
            </a>
            <div class="ai-nav-tools">
                <a href="/about.html" class="lang-btn" style="text-decoration:none; display:flex; align-items:center;">About</a>
                <button class="theme-btn" id="themeToggle" onclick="toggleTheme()">🌙</button>
                <div class="lang-toggle" style="display:flex; gap:0.5rem;">
                    <button class="lang-btn active" id="btn-en" onclick="setLang('en')">EN</button>
                    <button class="lang-btn" id="btn-ur" onclick="setLang('ur')">UR</button>
                </div>
            </div>
        </div>
    </header>
"""

COMMON_JS = """
    <script>
        let TRANSLATIONS = {};
        fetch('/translations.json').then(r => r.json()).catch(()=>{ }).then(data => { if(data) TRANSLATIONS = data; applyLang(); });

        function toggleTheme() {
            document.body.classList.toggle('light-mode');
            const isLight = document.body.classList.contains('light-mode');
            localStorage.setItem('theme', isLight ? 'light' : 'dark');
            document.getElementById('themeToggle').innerText = isLight ? '☀️' : '🌙';
        }

        async function applyLang() {
            const lang = localStorage.getItem('lang') || 'en';
            document.documentElement.lang = lang;
            document.body.classList.toggle('ur', lang === 'ur');
            const btnEn = document.getElementById('btn-en');
            const btnUr = document.getElementById('btn-ur');
            if(btnEn) btnEn.classList.toggle('active', lang === 'en');
            if(btnUr) btnUr.classList.toggle('active', lang === 'ur');
            
            if(lang === 'ur') {
                document.documentElement.dir = 'rtl';
            } else {
                document.documentElement.dir = 'ltr';
            }

            const nodes = document.querySelectorAll('[data-trans]');
            if (lang === 'en') {
                nodes.forEach(el => {
                    if (el.hasAttribute('data-original')) {
                        el.innerHTML = el.getAttribute('data-original');
                    }
                });
                return;
            }

            for(let el of nodes) {
                const key = el.getAttribute('data-trans');
                const originalText = el.getAttribute('data-original') || el.innerText;
                if (!originalText || originalText.length < 2) continue;
                
                if (TRANSLATIONS[lang] && TRANSLATIONS[lang][key]) {
                    el.innerHTML = TRANSLATIONS[lang][key];
                } else {
                    try {
                        const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=${lang}&dt=t`;
                        const res = await fetch(url, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                            body: `q=${encodeURIComponent(originalText)}`
                        });
                        const data = await res.json();
                        let translated = '';
                        if(data && data[0]) {
                            data[0].forEach(part => { if(part[0]) translated += part[0]; });
                        }
                        if(translated) {
                            if(!TRANSLATIONS[lang]) TRANSLATIONS[lang] = {};
                            TRANSLATIONS[lang][key] = translated;
                            el.innerHTML = translated;
                        }
                    } catch(e) {
                        console.error('Translation failed:', e);
                        el.innerHTML = originalText;
                    }
                }
            }
        }

        function setLang(lang) {
            localStorage.setItem('lang', lang);
            applyLang();
        }

        window.onload = function() {
            if (localStorage.getItem('theme') === 'light') {
                document.body.classList.add('light-mode');
                document.getElementById('themeToggle').innerText = '☀️';
            }
            applyLang();
        }
    </script>
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
        <p class="ai-footer-text" data-trans="footer_copy">© 2026 AI Flock Empire — Auto Flock Network | Autonomous Infrastructure</p>
        <div class="ai-footer-bottom">System Status: Optimal • Protocol: X-7 Neural</div>
    </footer>
"""

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
    
    # Ensure font exists
    font_dir = f"{SITE_DIR}/fonts"
    os.makedirs(font_dir, exist_ok=True)
    font_src = os.path.expanduser("~/storage/downloads/Jameel Noori Nastaleeq Regular.ttf")
    if os.path.exists(font_src):
        shutil.copy(font_src, f"{font_dir}/JameelNooriNastaleeq.ttf")

    # Sync translations
    trans_src = f"{OUTPUT}/translations.json"
    if os.path.exists(trans_src):
        shutil.copy(trans_src, f"{SITE_DIR}/translations.json")
    
    try:
        with open(f"{OUTPUT}/sheep7_audited.json", "r") as f:
            current_articles = json.load(f)
    except:
        print("🐑 SHEEP 8: No articles!"); return None
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    
    current_articles = [_normalize_autoflock_article(a) for a in current_articles]
    history = current_articles + history
    history = history[:150]
    
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

    shutil.copy("/data/data/com.termux/files/home/projects/media/shared/styles/global.css", f"{SITE_DIR}/style.css")

    # Generate Index Page
    index_html = _build_index(history[:12])
    with open(f"{SITE_DIR}/index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

    # Generate About Page
    try:
        manifesto_path = os.path.join(os.path.dirname(PROJECT), "FlockHub", "manifesto.md")
        if os.path.exists(manifesto_path):
            with open(manifesto_path, "r") as f:
                manifesto_md = f.read()
            about_page = _build_article_page({
                "headline": "About Our Intelligence Network",
                "body": manifesto_md,
                "category": "Manifesto",
                "source": "FlockHub Agent",
                "source_url": "/",
                "image_url": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1200&q=80"
            })
            with open(f"{SITE_DIR}/about.html", "w", encoding="utf-8") as f:
                f.write(about_page)
    except Exception as e:
        print(f"⚠ About Page Error: {e}")

    # Generate Article Pages
    for a in history:
        filename = a.get("filename", f"{_slugify(a.get('headline', 'article'))}.html")
        a["filename"] = filename
        content = _build_article_page(a)
        with open(f"{SITE_DIR}/{filename}", "w", encoding="utf-8") as f:
            f.write(content)

    print(f"🐑 SHEEP 8: {len(history)} articles published with new design ✓")
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
        
        attr_hl = title.replace('"', '&quot;')
        attr_ex = excerpt.replace('"', '&quot;')
        
        cards_html += f"""
            <article class="glass-card feed-card" style="--accent:{accent}" onclick="window.location.href='{filename}'">
                <div>
                    <div class="badge-row">
                        <span class="badge {kind}">{label}</span>
                        <span class="meta mono">{meta}</span>
                    </div>
                    <h2 data-trans="{attr_hl}" data-original="{attr_hl}">{title}</h2>
                    <p data-trans="{attr_ex}" data-original="{attr_ex}">{excerpt}</p>
                </div>
                <div class="card-foot mono">
                    <span>{source}</span>
                    <span>{date}</span>
                </div>
            </article>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AUTO FLOCK | AI Intelligence Network</title>
    <meta name="google-site-verification" content="Dthc_OiAqsG2NxrZXLE_gE84PLsD4_fLmc71KGGgKQI" />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    {HEADER_HTML}

    <header class="wrap hero">
        <div class="hero-grid">
            <article class="glass-card featured" onclick="window.location.href='{featured_url}'">
                <div class="feature-mark">◆</div>
                <div class="badge-row">
                    <span class="badge {f_kind}">{f_label}</span>
                    <span class="meta mono">AI RESEARCH • LIVE</span>
                </div>
                <h1 data-trans="{featured_title}" data-original="{featured_title}">{featured_title}</h1>
                <p class="summary" data-trans="{featured_summary}" data-original="{featured_summary}">{featured_summary}</p>
                <div class="feature-foot">
                    <div style="display:flex;align-items:center;gap:10px">
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
                    <h3 data-trans="{secondary_title}" data-original="{secondary_title}">{secondary_title}</h3>
                    <p class="summary" data-trans="{secondary_summary}" data-original="{secondary_summary}" style="font-size:.9rem">{secondary_summary}</p>
                    <span class="meta mono">{secondary_source}</span>
                </section>
            </aside>
        </div>
    </header>

    <main class="wrap" id="signals">
        <div class="feed-grid" id="feedGrid">
            {cards_html}
        </div>
    </main>

    {FOOTER_HTML}
    {COMMON_JS}
</body>
</html>"""

def _get_affiliate_block(category):
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

def _markdown_to_html(value):
    if not value: return ""
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
    
    # Process body_html to wrap segments in translation tags
    def wrap_trans(m):
        tag, inner = m.group(1), m.group(2)
        if not inner.strip() or len(inner) < 2: return m.group(0)
        attr = inner.replace('"', '&quot;')
        return f'<{tag} data-trans="{attr}" data-original="{attr}">{inner}</{tag}>'
    
    translated_body = re.sub(r'<(p|h[1-6]|li|th|td|figcaption)\b[^>]*>(.*?)</\1>', wrap_trans, body_html, flags=re.DOTALL|re.IGNORECASE)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{a.get('headline', 'AutoFlock | AI Intelligence')}</title>
    <meta name="google-site-verification" content="Dthc_OiAqsG2NxrZXLE_gE84PLsD4_fLmc71KGGgKQI" />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body class="article-page">
    {HEADER_HTML}
    <main class="article-content">
        <article>
            <img src="{a['image_url']}" class="hero-img" alt="{a['headline']}">
            <div class="article-body">
                {translated_body}
                {affiliate_block}
            </div>
            <div class="source-link">
                Source: <a href="{a['source_url']}" target="_blank">{a['source']}</a>
            </div>
        </article>
    </main>
    {FOOTER_HTML}
    {COMMON_JS}
</body>
</html>"""

if __name__ == "__main__":
    run()
