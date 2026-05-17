# AUTOFLOCK - 3-Hour Automation Script
import time
import subprocess
import sys
import os
from datetime import datetime

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(PROJECT_DIR, "logs", "auto_run.log")

def run_sync():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] 🤖 Starting 3-Hour Autoflock Sync...")
    
    with open(LOG_FILE, "a") as log:
        log.write(f"\n--- SYNC START: {timestamp} ---\n")
        try:
            # Run the master sync script
            result = subprocess.run(
                ["bash", "sync.sh"],
                cwd=PROJECT_DIR,
                capture_output=True,
                text=True
            )
            log.write(result.stdout)
            if result.stderr:
                log.write(f"\nERRORS:\n{result.stderr}")
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Sync Complete.")
        except Exception as e:
            log.write(f"CRITICAL ERROR: {str(e)}")
            print(f"❌ Critical Error: {str(e)}")
        log.write(f"\n--- SYNC END ---\n")

if __name__ == "__main__":
    os.makedirs(os.path.join(PROJECT_DIR, "logs"), exist_ok=True)
    print("🚀 Autoflock 1-Hour Automation Started.")
    print(f"📝 Logging to: {LOG_FILE}")
    
    run_sync()
