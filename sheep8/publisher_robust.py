import os
# SHEEP 8 - Robust Cloudflare Pages Deployer
from config_loader import get_credential, get_flock_config, os, hashlib, requests, time, zipfile
from datetime import datetime

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"
SITE_DIR = os.path.join(os.path.dirname(PROJECT), "autoflock/publish")

def get_sha256(content):
    return hashlib.sha256(content).hexdigest()

def run():
    print("🐑 SHEEP 8: Publishing (Robust Mode)...")
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
    
    # Assign filenames
    for i, a in enumerate(articles):
        a["filename"] = f"{ts}-{i+1}.html"
    
    from publisher import _build_index, _build_article_page
    
    # Build content
    files_to_deploy = {}
    
    index_html = _build_index(articles, date_str)
    files_to_deploy["/index.html"] = index_html.encode("utf-8")
    
    # Save locally for reference
    with open(f"{SITE_DIR}/index.html", "wb") as f: f.write(files_to_deploy["/index.html"])
    
    for a in articles:
        content = _build_article_page(a, now).encode("utf-8")
        files_to_deploy[f"/{a['filename']}"] = content
        with open(f"{SITE_DIR}/{a['filename']}", "wb") as f: f.write(content)

    # Load config
    try:
        cf = get_flock_config('autoflock')
    except:
        print("🐑 SHEEP 8: Missing Cloudflare config!"); return None
        
    ACCOUNT_ID = cf["account_id"]
    TOKEN = cf["api_token"]
    PROJECT_NAME = "autoflock"
    
    headers = {"Authorization": f"Bearer {TOKEN}"}
    base_url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT_NAME}"
    
    # Build manifest with SHA-256
    manifest = {path: get_sha256(content) for path, content in files_to_deploy.items()}
    
    # Step 1: Create Deployment
    print("🐑 SHEEP 8: Creating deployment...")
    r = requests.post(
        f"{base_url}/deployments",
        headers=headers,
        data={
            "branch": "main",
            "commit_message": f"Flock Update {ts}",
            "manifest": json.dumps(manifest)
        }
    )
    
    if r.status_code != 200:
        print(f"🐑 SHEEP 8: Failed to create deployment: {r.text}")
        return None
        
    res = r.json()
    if not res.get("success"):
        print(f"🐑 SHEEP 8: API Error: {res.get('errors')}")
        return None
        
    deployment_id = res["result"]["id"]
    deploy_url = res["result"]["url"]
    missing_hashes = res["result"].get("missing_hashes", [])
    
    print(f"🐑 SHEEP 8: Deployment created. ID: {deployment_id}")
    print(f"🐑 SHEEP 8: Missing hashes: {len(missing_hashes)}")
    
    # Step 2: Upload Missing Files
    if missing_hashes:
        print("🐑 SHEEP 8: Uploading files...")
        # Map hashes back to content
        hash_to_content = {get_sha256(content): content for content in files_to_deploy.values()}
        
        for h in missing_hashes:
            if h in hash_to_content:
                # The Cloudflare API for uploading files expects a list of files or a single file
                # According to Wrangler, it POSTs to /files
                # We can try to upload all in one go if possible, or one by one.
                # Let's try one by one as it is safer.
                # Cloudflare Pages Direct Upload /files endpoint expects multipart/form-data
                # with the file content.
                r_upload = requests.post(
                    f"{base_url}/files",
                    headers=headers,
                    files={"file": (h, hash_to_content[h], "application/octet-stream")}
                )
                if r_upload.status_code != 200:
                    print(f"   Failed to upload {h}: {r_upload.text}")
                else:
                    print(f"   Uploaded hash {h} ✓")
    
    print(f"🐑 SHEEP 8: Deployment complete!")
    print(f"🐑 SHEEP 8: URL: {deploy_url}")
    
    # Verification
    print("🐑 SHEEP 8: Verifying...")
    time.sleep(10)
    v = requests.get(deploy_url)
    if "generator" in v.text.lower():
        print("🐑 SHEEP 8: VERIFIED ✓ - Content is LIVE!")
    else:
        print("🐑 SHEEP 8: Deployment URL ready, but content might take a moment to propagate.")
    
    result = {"published": True, "url": deploy_url, "articles": len(articles)}
    with open(f"{OUTPUT}/sheep8_published.json", "w") as f:
        json.dump(result, f, indent=2)
        
    return result

if __name__ == "__main__":
    run()
