# SHEEP 10 - Multi-Platform Social Poster (Telegram + Facebook)
import json, os, requests, time, random, re
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"
HISTORY_FILE = f"{PROJECT}/history.json"
POSTED_FILE = f"{OUTPUT}/social_posted.json"
BASE_URL = "https://autoflock.cutbar.in"
TRACKING_PARAMS = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "fbclid", "gclid", "ref"}

def load_config():
    with open(f"{PROJECT}/config/social.json") as f:
        return json.load(f)

def _canonical_url(url):
    if not url: return ""
    parts = urlsplit(url.strip())
    query = urlencode([(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k.lower() not in TRACKING_PARAMS])
    path = parts.path.rstrip('/') or '/'
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, query, ''))

def _title_key(title):
    title = re.sub(r"[^a-z0-9 ]+", " ", (title or "").lower())
    return re.sub(r"\s+", " ", title).strip()

def _article_url(article):
    filename = article.get("filename", "")
    if filename: return f"{BASE_URL}/{filename}"
    return article.get("source_url") or article.get("url") or BASE_URL

def _load_posted():
    if not os.path.exists(POSTED_FILE): return []
    try:
        with open(POSTED_FILE) as f: return json.load(f)
    except: return []

def _load_published_articles():
    try:
        with open(HISTORY_FILE) as f:
            h = json.load(f)
            if h: return h
    except: pass
    return []

def generate_curiosity_hook(headline, category, source):
    # Curiosity Hook Logic: Why this matters + Bullet Points
    clean_h = headline.split(":", 1)[-1].split("—")[0].strip()
    return f"""🧠 SIGNAL: {clean_h}

Why this matters:
• Strategic pivot in {category} detected.
• Potential market ripple effect from {source}.
• Expert deep-dive inside.

Full Intelligence Report 👇"""

def post_to_telegram(bot_token, channel_id, headline, article_url, category, source):
    hook = generate_curiosity_hook(headline, category, source)
    post_text = f"<b>{hook}</b>\n🔗 {article_url}\n\n#Autoflock #AI #Intelligence"
    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": channel_id, "text": post_text, "parse_mode": "HTML"}
    try:
        r = requests.post(api_url, json=payload)
        data = r.json()
        if data.get("ok"):
            return True, "ok"
        return False, data.get("description", "Unknown error")
    except Exception as e: return False, str(e)

def post_to_facebook(page_id, access_token, headline, article_url, category, source):
    hook = generate_curiosity_hook(headline, category, source)
    message = f"{hook}\nRead more: {article_url}\n\n#Autoflock #AI #Automation"
    api_url = f"https://graph.facebook.com/{page_id}/feed"
    payload = {"message": message, "link": article_url, "access_token": access_token}
    try:
        r = requests.post(api_url, data=payload)
        if r.status_code == 200:
            return True, "ok"
        data = r.json()
        return False, data.get("error", {}).get("message", f"HTTP {r.status_code}")
    except Exception as e: return False, str(e)

def post_to_whatsapp(instance, token, number, headline, article_url, category, source):
    hook = generate_curiosity_hook(headline, category, source)
    message = f"*{hook}*\nRead more: {article_url}\n\n#Autoflock #AI #Automation"
    api_url = f"https://api.ultramsg.com/{instance}/messages/chat"
    payload = {"token": token, "to": number, "body": message}
    try:
        r = requests.post(api_url, data=payload)
        if r.status_code == 200:
            return True, "ok"
        return False, f"HTTP {r.status_code}: {r.text[:100]}"
    except Exception as e: return False, str(e)

def run():
    print("\n🐑 SHEEP 10: Posting Analyst Hooks to Social Hub...")
    config = load_config()
    bot_token = config.get("telegram_bot_token")
    channel_id = config.get("telegram_channel_id")
    fb_page_id = config.get("facebook_page_id")
    fb_access_token = config.get("facebook_access_token")
    wa_instance = config.get("whatsapp_instance")
    wa_token = config.get("whatsapp_token")
    wa_number = config.get("whatsapp_number")

    articles = _load_published_articles()
    if not articles:
        print("   ❌ No articles found in history!"); return None

    posted = _load_posted()
    posted_urls = {_canonical_url(item.get("source_url", "")) for item in posted}
    posted_titles = {_title_key(item.get("headline", "")) for item in posted}

    selected = []
    for a in articles:
        h = a.get("headline") or a.get("title") or ""
        su = _canonical_url(a.get("source_url") or a.get("url") or "")
        tk = _title_key(h)
        if su in posted_urls or tk in posted_titles: continue
        selected.append(a)
        posted_urls.add(su); posted_titles.add(tk)
        if len(selected) == 2: break

    if not selected:
        print("   ✅ No new social signals to send."); return []

    results = []
    for a in selected:
        h = a.get("headline") or a.get("title")
        au = _article_url(a)
        cat = a.get("category", "Tech")
        src = a.get("source", "Autoflock")
        print(f"\n📢 Posting: {h[:60]}...")

        platforms = {}
        
        # 1. Telegram
        if bot_token and channel_id:
            ok, err = post_to_telegram(bot_token, channel_id, h, au, cat, src)
            platforms["telegram"] = "✅" if ok else f"❌ ({err})"
            print(f"   - Telegram: {platforms['telegram']}")
        else:
            platforms["telegram"] = "⏩ (Skipped)"

        # 2. Facebook
        if fb_page_id and fb_access_token:
            ok, err = post_to_facebook(fb_page_id, fb_access_token, h, au, cat, src)
            platforms["facebook"] = "✅" if ok else f"❌ ({err})"
            print(f"   - Facebook: {platforms['facebook']}")
        else:
            platforms["facebook"] = "⏩ (Skipped)"

        # 3. WhatsApp
        if wa_instance and wa_token and wa_number:
            ok, err = post_to_whatsapp(wa_instance, wa_token, wa_number, h, au, cat, src)
            platforms["whatsapp"] = "✅" if ok else f"❌ ({err})"
            print(f"   - WhatsApp: {platforms['whatsapp']}")
        else:
            platforms["whatsapp"] = "⏩ (Skipped)"
        
        sent = "✅" in platforms.values()
        res = {"headline": h, "url": au, "success": sent, "platforms": platforms, "timestamp": time.time()}
        results.append(res); posted.insert(0, res)
        time.sleep(3)

    with open(POSTED_FILE, "w") as f: json.dump(posted[:300], f, indent=2)
    print("\n🐑 SHEEP 10: Digital Analyst Social Feed updated ✓")
    return results

if __name__ == "__main__":
    run()
