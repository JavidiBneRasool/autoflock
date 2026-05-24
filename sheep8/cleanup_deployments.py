# Cleanup - Delete old Cloudflare deployments
import json, os, requests

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"

def run():
    print("🐑 Cleanup: Deleting old deployments...")
    try:
        with open(f"{PROJECT}/config/cloudflare.json") as f:
            cf = json.load(f)
        account_id = cf["account_id"]
        token = cf["api_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        pages_project = "autoflock"
        url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects/{pages_project}/deployments"
        
        total_deleted = 0
        while True:
            r = requests.get(url, headers=headers)
            if r.status_code != 200:
                print(f"   Error fetching deployments: {r.text}")
                break
                
            deployments = r.json().get("result", [])
            if len(deployments) <= 1:
                break
            
            # Keep the first one (latest), delete others on this page
            page_deleted = 0
            for dep in deployments[1:]:
                dep_id = dep["id"]
                del_r = requests.delete(f"{url}/{dep_id}", headers=headers)
                if del_r.status_code == 200:
                    page_deleted += 1
            
            total_deleted += page_deleted
            if page_deleted == 0: # Avoid infinite loop
                break
                
        print(f"   Cleaned {total_deleted} old deployments ✓")
    except Exception as e:
        print(f"   Cleanup skipped: {e}")

if __name__ == "__main__":
    run()
