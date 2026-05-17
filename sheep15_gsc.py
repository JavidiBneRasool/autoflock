import json, os
from google.oauth2 import service_account
from googleapiclient.discovery import build

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"
KEY_FILE = f"{PROJECT}/config/google_indexing_key.json"
BASE_URL = "https://autoflock.cutbar.in"

def run():
    print("🐑 SHEEP 15: Google Indexing API Force-Push...")
    
    if not os.path.exists(KEY_FILE):
        print("❌ GSC Key missing. Skipping.")
        return

    try:
        with open(f"{OUTPUT}/sheep7_audited.json", "r") as f:
            articles = json.load(f)
    except:
        print("🐑 SHEEP 15: No new articles to index.")
        return

    # SCOPES for Indexing API
    SCOPES = ["https://www.googleapis.com/auth/indexing"]
    
    credentials = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
    service = build("indexing", "v3", credentials=credentials)

    for a in articles:
        url = f"{BASE_URL}/{a['filename']}"
        print(f"   Indexing: {url}")
        
        body = {
            "url": url,
            "type": "URL_UPDATED"
        }
        
        try:
            result = service.urlNotifications().publish(body=body).execute()
            print(f"   ✅ Success: {result.get('urlNotificationMetadata', {}).get('latestUpdate', {}).get('type')}")
        except Exception as e:
            print(f"   ❌ Failed: {str(e)}")

if __name__ == "__main__":
    run()
