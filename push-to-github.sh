#!/bin/bash

# BMAD-EDI Media Analysis - GitHub Push Script
# Agent 10: Git Operations Specialist

echo "[*] Pushing BMAD-EDI Media Analysis Skill to GitHub..."
echo ""

# Add remote
echo "[1/3] Adding remote origin..."
git remote add origin https://github.com/MikeDominic92/bmad-media-analysis-skill.git

# Push to GitHub
echo "[2/3] Pushing to GitHub..."
git push -u origin master

# Show status
echo "[3/3] Verifying push..."
git remote -v
echo ""
echo "[+] Repository URL: https://github.com/MikeDominic92/bmad-media-analysis-skill"
echo "[+] Commit pushed successfully!"
