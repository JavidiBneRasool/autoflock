# SHEEP 12 - Google Indexing API Integration
import json, os, time, urllib.request, urllib.error

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"
KEY_FILE = f"{PROJECT}/config/google_indexing_key.json"
BASE_URL = "https://autoflock.cutbar.in"
DOMAIN = "autoflock.cutbar.in"

def verify_sitemap(filename):
    path = f"{PROJECT}/{filename}"
    url = f"{BASE_URL}/{filename}"
    if os.path.exists(path) and os.path.getsize(path) > 0:
        print(f"   ✓ Sitemap ready: {url}")
        return True
    print(f"   ! Sitemap missing or empty: {path}")
    return False

def submit_indexnow(urls):
    key = os.environ.get("BING_INDEXNOW_KEY") or os.environ.get("INDEXNOW_KEY")
    if not key or not urls:
        print("   ! IndexNow key missing or no URLs. Skipping IndexNow.")
        return
    payload = {
        "host": DOMAIN,
        "key": key,
        "keyLocation": f"{BASE_URL}/{key}.txt",
        "urlList": urls[:100],
    }
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=20) as response:
            print(f"   ✓ IndexNow response: {response.status}")
    except Exception as e:
        print(f"   ! IndexNow failed: {e}")

def run():
    print("🐑 SHEEP 12: Activating News Signal Engine...")
    
    verify_sitemap("sitemap.xml")
    verify_sitemap("news-sitemap.xml")
    recent_urls = _recent_urls()
    submit_indexnow(recent_urls)

    if not os.path.exists(KEY_FILE):
        print("   ! Google Indexing key not found. Skipping API.")
    else:
        try:
            _run_api_indexing(recent_urls)
        except Exception as e:
            print(f"   ! Indexing API failed: {e} (Continuing with other signals)")

def _recent_urls():
    try:
        with open(f"{PROJECT}/history.json") as f:
            history = json.load(f)
            articles = history[:5]
    except Exception:
        return []
    urls = []
    for article in articles:
        filename = article.get('filename', '').replace('.html', '')
        if filename:
            urls.append(f"{BASE_URL}/{filename}")
    return urls

def _run_api_indexing(urls):
    if not urls:
        print("   ! No recent URLs available for Google Indexing API.")
        return
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import Request
    except Exception as e:
        print(f"   ! google-auth missing. Install google-auth to enable GSC indexing: {e}")
        return
    scopes = ['https://www.googleapis.com/auth/indexing']
    credentials = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=scopes)
    credentials.refresh(Request())
    access_token = credentials.token
    
    endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
    for url in urls:
        print(f"   API Indexing: {url}")
        payload = {"url": url, "type": "URL_UPDATED"}
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
        try:
            req = urllib.request.Request(endpoint, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
            urllib.request.urlopen(req, timeout=20).close()
        except Exception:
            pass

if __name__ == "__main__":
    run()
