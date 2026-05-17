import json, os, re

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"

# Digital Analyst Quality Gate Configuration
BRAND_NAME = "Auto Flock"
SEO_KEYWORDS = ["SIGNAL", "OPPORTUNITY", "WARNING"]
ALPHA_MARKERS = ["Why This Matters", "Macro View"]
NICHE_KEYWORDS = [
    "ai", "agent", "llm", "automation", "developer", "code", "api", "workflow", 
    "browser", "terminal", "robotics", "machine learning", "neural", "script", "devops"
]

PLACEHOLDERS = ["TODO", "[HOOK]", "[REVEAL]", "fact one"]

def run():
    print("🐑 SHEEP 7: Auditing (Digital Analyst Gate)...")
    try:
        with open(f"{OUTPUT}/sheep6_articles.json", "r") as f:
            articles = json.load(f)
    except FileNotFoundError:
        print("🐑 SHEEP 7: No draft!"); return None
    
    clean = []
    for article in articles:
        body = article.get("body", "")
        headline = article.get("headline", "") or article.get("title", "")
        errors = [p for p in PLACEHOLDERS if p.lower() in body.lower()]
        
        # 1. Readability Check
        if len(body) < 400:
            errors.append("READABILITY_FAIL")
        
        # 2. SEO Check
        if not any(k.upper() in headline.upper() for k in SEO_KEYWORDS):
            errors.append("SEO_FAIL")
            
        # 3. Alpha Check
        if not any(m.lower() in body.lower() for m in ALPHA_MARKERS):
            errors.append("ALPHA_FAIL")
            
        # 4. Keyword Density (Digital Analyst Score)
        # Using set for unique keywords found, or count for total occurrences.
        # Requirement: "Score < 8 mark as FAILURE". 
        # I'll use total occurrences of niche keywords for density.
        density_score = 0
        body_lower = body.lower()
        for kw in NICHE_KEYWORDS:
            density_score += len(re.findall(rf"\b{re.escape(kw)}\b", body_lower))
        
        if density_score < 8:
            errors.append("DENSITY_FAIL")
            
        # 5. Branding Check
        if BRAND_NAME.lower() not in body.lower():
            errors.append("BRAND_FAIL")
        
        # Preserve existing check for AI-Generated if it was important, 
        # but the prompt asked for these 5 specific upgrades.
        # Existing logic had: if "AI-Generated" not in body and BRAND_NAME not in body ... MISSING_TAG
        # I'll keep it as a safety check if not already covered.
        if "AI-Generated" not in body and BRAND_NAME not in body:
             if "BRAND_FAIL" not in errors: errors.append("MISSING_TAG")
        
        article["errors"] = len(errors)
        article["error_list"] = errors
        article["digital_analyst_score"] = density_score
        article["clean"] = len(errors) == 0
        
        # "don't include in sheep7_audited.json" if score < 8 (DENSITY_FAIL) or other fails.
        if article["clean"]:
            clean.append(article)
        else:
            print(f"   [FAILURE] {headline[:40]}... Score: {density_score} Errors: {errors}")
    
    with open(f"{OUTPUT}/sheep7_audited.json", "w") as f:
        json.dump(clean, f, indent=2)
    
    print(f"🐑 SHEEP 7: {len(clean)} clean, {len(articles)-len(clean)} with errors ✓")
    return clean

if __name__ == "__main__":
    run()
