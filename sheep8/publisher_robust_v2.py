import os
# SHEEP 8 - Robust Cloudflare Pages Deployer (v2)
from config_loader import get_credential, get_flock_config, os, hashlib, requests, time
from datetime import datetime

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"
SITE_DIR = os.path.join(os.path.dirname(PROJECT), "autoflock/publish")

def get_sha256(content):
    return hashlib.sha256(content).hexdigest()

def run():
    print("🐑 SHEEP 8: Publishing (Robust Mode v2)...")
    os.makedirs(OUTPUT, exist_ok=True)
    os.makedirs(SITE_DIR, exist_ok=True)
    
    try:
        with open(f"{OUTPUT}/sheep7_audited.json", "r") as f:
            articles = json.load(f)
    except:
        print("🐑 SHEEP 8: No articles!"); return None
    
    now = datetime.now()
    ts = now.strftime("%Y%m%d-%H%M%S")
    date_str = now.strftime("%B %d, %Y")
    
    for i, a in enumerate(articles):
        a["filename"] = f"{ts}-{i+1}.html"
    
    from publisher import _build_index, _build_article_page
    
    files_to_deploy = {}
    index_html = _build_index(articles, date_str)
    files_to_deploy["/index.html"] = index_html.encode("utf-8")
    
    for a in articles:
        content = _build_article_page(a, now).encode("utf-8")
        files_to_deploy[f"/{a['filename']}"] = content

    try:
        cf = get_flock_config('autoflock')
    except:
        print("🐑 SHEEP 8: Missing Cloudflare config!"); return None
        
    ACCOUNT_ID = cf["account_id"]
    TOKEN = cf["api_token"]
    PROJECT_NAME = "autoflock"
    
    headers = {"Authorization": f"Bearer {TOKEN}"}
    base_url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages"
    
    # Build manifest
    manifest = {path: get_sha256(content) for path, content in files_to_deploy.items()}
    
    # Step 1: Create Deployment
    print("🐑 SHEEP 8: Creating deployment...")
    r = requests.post(
        f"{base_url}/projects/{PROJECT_NAME}/deployments",
        headers=headers,
        files={
            "manifest": (None, json.dumps(manifest)),
            "branch": (None, "main")
        }
    )
    
    if r.status_code != 200:
        print(f"🐑 SHEEP 8: Failed: {r.text}")
        return None
        
    res = r.json()
    deployment_id = res["result"]["id"]
    deploy_url = res["result"]["url"]
    missing_hashes = res["result"].get("missing_hashes", [])
    
    print(f"🐑 SHEEP 8: Deployment {deployment_id} created. Missing {len(missing_hashes)} hashes.")
    
    # Step 2: Upload Files
    if missing_hashes:
        print("🐑 SHEEP 8: Uploading missing files...")
        hash_to_content = {get_sha256(content): content for content in files_to_deploy.values()}
        
        # We can upload multiple files in one request
        upload_files = {}
        for h in missing_hashes:
            if h in hash_to_content:
                upload_files[h] = (h, hash_to_content[h], "application/octet-stream")
        
        if upload_files:
            # The correct endpoint for uploading multiple files
            r_upload = requests.post(
                f"{base_url}/files",
                headers=headers,
                files=upload_files
            )
            if r_upload.status_code != 200:
                print(f"🐑 SHEEP 8: Upload failed: {r_upload.text}")
                return None
            print("   Upload successful ✓")
    
    print(f"🐑 SHEEP 8: LIVE at {deploy_url}")
    
    # Finalize locally
    with open(f"{SITE_DIR}/index.html", "wb") as f: f.write(files_to_deploy["/index.html"])
    for a in articles:
        with open(f"{SITE_DIR}/{a['filename']}", "wb") as f: f.write(files_to_deploy[f"/{a['filename']}"])
        
    return {"published": True, "url": deploy_url}

if __name__ == "__main__":
    run()
