import json, os, urllib.parse, random, uuid, time

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = f"{PROJECT}/output"

# MUCH larger subject pool per category - prevents repeats
SUBJECTS = {
    "World": ["united nations assembly", "global summit meeting", "international flags", "world leaders handshake", "diplomatic conference", "global trade port", "international court", "world economic forum", "g20 summit", "climate conference"],
    "Politics": ["parliament session", "election voting booth", "political campaign rally", "white house exterior", "senate hearing room", "supreme court building", "protest march", "government press briefing", "political debate podium", "polling station"],
    "India": ["mumbai gateway", "delhi india gate", "taj mahal sunrise", "jaipur pink city", "kerala houseboat", "varanasi ghats", "himalayan mountains", "goa beach sunset", "bengaluru tech park", "chennai marina"],
    "Business": ["wall street bull", "stock exchange trading", "corporate boardroom", "startup office space", "shipping container port", "bank vault interior", "financial chart display", "retail store interior", "factory production line", "business handshake"],
    "Technology": ["fiber optic cables", "robot arm factory", "silicon chip macro", "data center servers", "quantum computer lab", "vr headset display", "autonomous car sensor", "drone aerial view", "satellite in orbit", "smartphone circuit"],
    "Science": ["hubble telescope", "dna double helix", "particle accelerator", "mars rover surface", "microscope bacteria", "chemical reaction", "space station earth", "fossil excavation", "brain mri scan", "volcano eruption"],
    "Sports": ["olympic stadium", "soccer goal net", "basketball dunk", "cricket stadium", "tennis serve", "swimming race", "formula 1 track", "marathon finish line", "skiing downhill", "boxing ring"],
    "Entertainment": ["movie premiere red carpet", "concert crowd lights", "theater stage empty", "film director chair", "recording studio mic", "broadway marquee", "circus tent", "ballet performance", "opera house interior", "award statue"],
    "Health": ["hospital emergency room", "surgical theater", "pharmacy shelves", "dna sequencing machine", "medical team discussion", "vaccine vial closeup", "stethoscope heart", "xray film light", "ambulance lights", "rehabilitation center"],
    "Middle East": ["dubai burj khalifa", "istanbul blue mosque", "cairo pyramids", "riyadh skyline", "doha corniche", "muscat grand mosque", "abu dhabi louvre", "petra jordan", "beirut mediterranean", "jerusalem old city"],
    "War News": ["military command center", "fighter jet formation", "naval aircraft carrier", "soldier silhouette sunset", "tank column desert", "peace negotiations table", "radar installation", "military drone flight", "armored vehicle convoy", "war room strategy map"],
    "Markets": ["gold bullion bars", "stock ticker display", "commodities trading floor", "bitcoin physical coin", "forex chart screen", "bond certificate", "real estate skyline", "oil rig platform", "agriculture harvest", "mineral extraction"],
    "Crypto": ["bitcoin mining farm", "crypto coins gold", "ethereum logo", "blockchain digital node", "cryptocurrency trading", "digital wallet app", "nft gallery", "altcoins display", "decentralized finance", "binary code glow"],
    "Artificial Intelligence": ["humanoid robot face", "neural network brain", "ai coding screen", "future city cyborg", "machine learning nodes", "automated drone swarm", "intelligent robot arm", "artificial intelligence glow", "server chip ai", "virtual assistant hologram"],
    "Engineering": ["blueprint architecture", "suspension bridge construction", "jet engine turbine", "massive dam gears", "civil engineering site", "robotic assembly line", "space rocket engine", "mechanical clockwork", "industrial lathe", "high-tech lab"],
    "Ranking Superpower": ["global power map", "statue of liberty", "great wall china", "kremlin building", "london big ben", "world flag circle", "eiffel tower night", "tokyo neon skyline", "washington dc mall", "european union flags"],
}

def get_image_url(headline, category, index):
    # Pick subject based on index to guarantee variety across articles
    subjects_list = SUBJECTS.get(category, ["breaking news", "journalism", "reporting"])
    subject = subjects_list[index % len(subjects_list)]
    
    # Multiple unique identifiers
    unique_id = uuid.uuid4().hex[:8]
    seed = hash(f"{headline}{unique_id}{index}") % 999999
    
    prompt = f"professional photojournalism photo of {subject}, sharp focus, dramatic lighting, national geographic style, ref:{unique_id}"
    encoded = urllib.parse.quote(prompt)
    
    # Using LoremFlickr for more reliable keyword-based random images
    # This avoids the redirect issues of Unsplash and guarantees variety
    clean_keyword = urllib.parse.quote(subject.replace(" ", ","))
    timestamp = int(time.time())
    
    return {
        "unsplash": f"https://picsum.photos/seed/{seed}/1200/630",
        "pollinations": f"https://image.pollinations.ai/prompt/{encoded}?width=800&height=600&nologo=true&seed={seed}&model=turbo"
    }

def run():
    print("🐑 SHEEP 5: Headlines & Unique Images...")
    try:
        with open(f"{OUTPUT}/sheep3_compliance.json") as f:
            articles = json.load(f)
    except FileNotFoundError:
        print("🐑 SHEEP 5: No input!"); return None
    
    passed = [a for a in articles if a["decision"] == "PASS"]
    
    results = []
    seen_headlines = set()
    
    for i, article in enumerate(passed):
        title = article["title"][:70]
        # Pivot to 'Signal' framing (The Purple Cow)
        best = f"🔮 SIGNAL: {title} — Analysis"
        if i % 3 == 0:
            best = f"📈 OPPORTUNITY: {title} — Strategy"
        elif i % 3 == 1:
            best = f"🚨 WARNING: {title} — Risk Report"
        
        if best in seen_headlines:
            best = f"🧠 INTELLIGENCE: {title} — Deep Dive"
        seen_headlines.add(best)
        
        image_urls = get_image_url(best, article["category"], i)
        
        results.append({
            "category": article["category"],
            "headline": best,
            "image_url": image_urls["unsplash"],  # Primary: Unsplash (reliable)
            "image_fallback": image_urls["pollinations"],  # Backup
            "article": article
        })
    
    with open(f"{OUTPUT}/sheep5_headlines.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"🐑 SHEEP 5: {len(results)} headlines with Unsplash images ready ✓")
    return results

if __name__ == "__main__":
    run()
