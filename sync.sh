#!/bin/bash

# AUTOFLOCK MASTER SYNC SCRIPT - ROBUST VERSION
# This script runs the full AI automation pipeline and pushes updates to the web.

set -euo pipefail

PROJECT_DIR="$(pwd)"
# Set Git Identity if not configured (crucial for GitHub Actions)
if [ -z "$(git config user.name || true)" ]; then
  git config --global user.name "Flock Agent"
  git config --global user.email "agent@cutbar.in"
fi
cd "$PROJECT_DIR"

fail() {
  echo "------------------------------------------"
  echo "❌ SYNC FAILED: $1"
  echo "------------------------------------------"
  exit 1
}

echo "------------------------------------------"
echo "🤖 Starting Autoflock Sync: $(date)"
echo "------------------------------------------"

# 0. Ensure a clean state and update from remote
echo "🔄 Step 0: Syncing with GitHub (Main)..."
# Discard any changes to tracked files that might block pull (usually publish/*)
# But we want to keep local changes if they are new articles... 
# Actually, the pipeline generates new files. 
# Best practice: Commit what we have, then pull rebase.

git add .
if ! git diff --cached --quiet; then
  git commit -m "Pre-sync checkpoint: $(date +'%Y-%m-%d %H:%M')" || echo "Commit failed, continuing anyway..."
fi

echo "📥 Pulling latest changes..."
git pull --rebase -X theirs origin main || {
  echo "Rebase failed. Trying to abort and force sync..."
  git rebase --abort || true
  git fetch origin main
  git reset --hard origin/main
}

# 1. Run the Orchestrator (Scout -> Writer -> Social Poster)
echo "🐑 Step 1: Running AI Pipeline & Social Posting..."
# We use a timeout to prevent hanging forever
timeout 1800 python3 run_flock.py || fail "AI pipeline failed or timed out"

# 2. Add, Commit, and Push to GitHub (Triggers Cloudflare Web Update)
echo "🚀 Step 2: Syncing to Web (GitHub/Cloudflare)..."
git add .
if git diff --cached --quiet; then
  echo "No changes to commit"
else
  git commit -m "Autoflock Update: $(date +'%Y-%m-%d %H:%M')" || echo "Commit failed"
fi

echo "📤 Pushing to GitHub..."
if ! git push origin main; then
  echo "Push failed. Attempting one last rebase and push..."
  git pull --rebase -X theirs origin main || {
    echo "Rebase still failed. Aborting rebase before exit."
    git rebase --abort || true
    fail "Final rebase failed"
  }
  git push origin main || fail "Final push failed"
fi

echo "------------------------------------------"
echo "✅ SYNC COMPLETE: Your AI tools are live!"
echo "🌐 URL: https://autoflock.cutbar.in"
echo "------------------------------------------"

# Keep only latest 150 article files
if [ -d "$PROJECT_DIR/publish" ]; then
  cd "$PROJECT_DIR/publish"
  ls -t *.html 2>/dev/null | grep -v index.html | tail -n +151 | xargs rm -f 2>/dev/null || true
  cd "$PROJECT_DIR"
fi
