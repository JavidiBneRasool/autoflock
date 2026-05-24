import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AGENT_PATH = os.path.join(ROOT, "FlockHub", "agents", "monetizer", "monetizer.py")
os.system(f"{sys.executable} {AGENT_PATH} {os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}")
