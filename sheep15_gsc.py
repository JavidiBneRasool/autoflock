import json, os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from config_loader import get_credential

PROJECT = os.path.dirname(os.path.abspath(__file__))
OUTPUT = f"{PROJECT}/output"
BASE_URL = "https://autoflock.cutbar.in"

def run():
    print("🐑 SHEEP 15: Google Indexing API Force-Push...")
    
    # Load credentials from Vault
    info = get_credential("google_indexing_key", flock="autoflock")
    if not info:
        print("❌ GSC Key missing in Vault. Skipping.")
        return

    try:
        with open(f"{OUTPUT}/sheep7_audited.json", "r") as f:
            articles = json.load(f)
    except:
        print("🐑 SHEEP 15: No new articles to index.")
        return

    # SCOPES for Indexing API
    SCOPES = ["https://www.googleapis.com/auth/indexing"]
    
    try:
        credentials = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
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
    except Exception as e:
        print(f"   ❌ GSC Error: {e}")

if __name__ == "__main__":
    run()
