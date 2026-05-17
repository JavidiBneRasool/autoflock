# MASTER ORCHESTRATOR - Full Pipeline
import subprocess, sys, json, os

HOME = os.path.expanduser("~")
PROJECT = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(PROJECT, "output")
LOGS = os.path.join(PROJECT, "logs")

os.makedirs(OUTPUT, exist_ok=True)
os.makedirs(LOGS, exist_ok=True)

SHEEP = [
    ("Sheep 1 (Scout)", "sheep1/scout.py"),
    ("Sheep 2 (Verifier)", "sheep2/verifier.py"),
    ("Sheep 3 (Compliance)", "sheep3/compliance.py"),
    ("Sheep 4 (Designer)", "sheep4/designer.py"),
    ("Sheep 5 (Headlines)", "sheep5/headline_writer.py"),
    ("Sheep 6 (Writer)", "sheep6/suspense_writer.py"),
    ("Sheep 7 (Auditor)", "sheep7/auditor.py"),
    ("Sheep 11 (Translator)", "sheep11/translator.py"),
    ("Sheep 13 (Monetizer)", "sheep13/monetizer.py"),
        ("Cleanup (Delete old deployments)", "sheep8/cleanup_deployments.py"),
    ("Sheep 8 (Publisher)", "sheep8/publisher.py"),
    ("Sheep 9 (Reporter)", "sheep9/reporter.py"),
    ("Sheep 10 (Social)", "sheep10/social_poster.py"),
    ("Sheep 12 (Indexer)", "sheep12/indexer.py"),
    ("Sheep 14 (SEO)", "sheep14_seo.py"),
    ("Sheep 15 (GSC Indexer)", "sheep15_gsc.py"),
]

print("""
╔════════════════════════════════╗
║   🤖 AUTOFLOCK AI AGENT     ║
║   10 Sources • Social Hub   ║
╚════════════════════════════════╝
""")

for name, script in SHEEP:
    print(f"\n{'='*40}")
    print(f"RUNNING {name}...")
    print(f"{'='*40}")
    
    result = subprocess.run([sys.executable, f"{PROJECT}/{script}"], capture_output=True, text=True, cwd=PROJECT)
    print(result.stdout)
    if result.returncode != 0:
        print(f"⚠ {name} ERROR: {result.stderr}")

print("\n✅ ORCHESTRATOR FINISHED")
