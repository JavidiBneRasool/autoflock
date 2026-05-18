import json, os

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"

# Branding Gate Configuration
BRAND_NAME = "Auto Flock Intelligence"
SIGNAL_KEYWORDS = ["SIGNAL", "OPPORTUNITY", "WARNING"]

PLACEHOLDERS = ["TODO", "[HOOK]", "[REVEAL]", "fact one"]

def run():
    print("🐑 SHEEP 7: Auditing (Branding + Substance Gate)...")
    try:
        with open(f"{OUTPUT}/sheep6_articles.json", "r") as f:
            articles = json.load(f)
    except FileNotFoundError:
        print("🐑 SHEEP 7: No draft!"); return None
    
    clean = []
    for article in articles:
        body = article.get("body", "")
        headline = article.get("headline", "") or article.get("title", "")
        
        errors = []
        
        # 1. Substance Check
        if len(body) < 300:
            errors.append("TOO_SHORT")
        
        # 2. Branding Check
        if BRAND_NAME.lower() not in body.lower():
            errors.append("MISSING_BRAND")
            
        # 3. Signal Presence Check
        if not any(k.upper() in headline.upper() or k.upper() in body.upper() for k in SIGNAL_KEYWORDS):
            errors.append("MISSING_SIGNAL")

        # Placeholder Check
        if any(p.lower() in body.lower() for p in PLACEHOLDERS):
            errors.append("PLACEHOLDER_FOUND")
        
        article["errors"] = len(errors)
        article["error_list"] = errors
        article["clean"] = len(errors) == 0
        
        if article["clean"]:
            clean.append(article)
        else:
            print(f"   [FAILURE] {headline[:40]}... Errors: {errors}")
    
    with open(f"{OUTPUT}/sheep7_audited.json", "w") as f:
        json.dump(clean, f, indent=2)
    
    print(f"🐑 SHEEP 7: {len(clean)} clean, {len(articles)-len(clean)} with errors ✓")
    return clean

if __name__ == "__main__":
    run()
