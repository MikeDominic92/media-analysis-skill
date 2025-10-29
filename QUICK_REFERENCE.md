# Quick Reference - BMAD-EDI Media Analysis Skill

**One-page cheat sheet for common tasks**

---

## Installation (One-Time)

```bash
# Windows
install.bat

# Or manual:
pip install -r requirements.txt
patchright install chrome
python gemini_analyzer.py auth
```

---

## Essential Commands

### Analysis

```bash
# Analyze single file
python run.py <file_path>

# Process ticket (Phase 0)
python workflow.py <file_path>

# Archive ticket (Phase 7)
python archival.py <ticket_id> <webedi_id> <company_name>
```

### Authentication

```bash
# Authenticate
python gemini_analyzer.py auth

# Check status
python gemini_analyzer.py auth --check
```

### Testing

```bash
# Quick system check
python status.py

# Verify OCR
python verify_ocr.py

# Test Phase 0
python test_phase0.py

# Test everything
python test_all.py
```

### Monitoring

```bash
# View logs (Windows)
type C:\Users\sleep\Documents\tickets\media-analysis.log

# Live logs (PowerShell)
Get-Content C:\Users\sleep\Documents\tickets\media-analysis.log -Wait -Tail 20

# System status
python status.py

# Watcher status
python watcher-status.py
```

### Directory Watcher

```bash
# Start watcher
python watch-incoming.py

# Check status
python watcher-status.py

# Install as service (Windows)
install-watcher.bat
```

---

## File Locations

### Core Scripts
```
C:\Users\sleep\.claude\skills\media-analysis\
├── run.py (venv wrapper)
├── main.py (orchestrator)
├── gemini_analyzer.py (Gemini)
├── ocr_processor.py (OCR)
├── workflow.py (Phase 0)
├── archival.py (Phase 7)
└── requirements.txt
```

### Directories
```
C:\Users\sleep\Documents\tickets\
├── incoming/     (drop files here)
├── processing/   (active tickets)
├── archived/     (resolved tickets)
└── media-analysis.log
```

### Configuration
```
media-analysis/
├── prompts/edi-specialist.txt
├── prompts/media-analysis.txt
├── data/auth_info.json (gitignored)
├── data/browser_state/ (gitignored)
└── data/ocr_cache/ (gitignored)
```

---

## Supported File Types (14)

**Documents:** PDF
**Images:** PNG, JPG, JPEG, BMP, TIFF
**Audio:** MP3, WAV, M4A
**Video:** MP4, MOV, AVI

---

## Workflow

```
incoming/ → Media Analysis → processing/ticket_{id}/ → Analyst → PM →
Investigator → NotebookLM → Documentation → archived/{year}/{month}/
```

---

## Confidence Scores

- **HIGH (≥ 0.85):** Auto-accept, proceed to Analyst
- **MEDIUM (0.70-0.84):** Accept with review flag
- **LOW (< 0.70):** OCR fallback triggered (hybrid mode)

---

## Troubleshooting

### Authentication Failed
```bash
# Clear and re-auth
rm -rf data/browser_state/
python gemini_analyzer.py auth
```

### OCR Not Working
```bash
pip install paddleocr==2.7.0 --force-reinstall
python verify_ocr.py
```

### Low Confidence
- Check file quality (resolution, clarity)
- Review preliminary_analysis.md
- Hybrid mode auto-triggers (< 0.70)

### Files Not Processing
```bash
# Check logs
type C:\Users\sleep\Documents\tickets\media-analysis.log

# Manual process
python workflow.py <file_path>

# Check watcher
python watcher-status.py
```

---

## Phase 0: Pre-Investigation Analysis

### What It Does

1. Detects file type
2. Routes to appropriate analyzer (Gemini/OCR/Hybrid)
3. Extracts EDI metadata (ticket ID, company, partner, etc.)
4. Generates standardized filename
5. Creates metadata.json + preliminary_analysis.md
6. Moves file to processing/ticket_{id}/

### Time Savings

- Manual: 15-20 minutes
- Automated: 6-11 minutes
- **Saved: 7-9 minutes per ticket (50-64% faster)**

### Analyst Action

Review `metadata.json` and `preliminary_analysis.md` before investigation.

---

## Phase 7: Artifact Archival

### What It Does

1. Creates archive structure: archived/{year}/{month}/{ticket_id}/
2. Copies artifacts: metadata.json, preliminary_analysis.md, original file
3. Generates documentation from templates
4. Preserves complete ticket context

### Command

```bash
python archival.py <ticket_id> <webedi_id> <company_name>
```

---

## Maintenance

### Weekly

```bash
# Clear OCR cache (saves disk space)
rm -rf data/ocr_cache/*

# Review logs
type C:\Users\sleep\Documents\tickets\media-analysis.log
```

### Monthly

- Review confidence score trends
- Check processing times
- Update prompts if needed
- Plan improvements

---

## Performance Targets

- **Processing time:** < 90 seconds
- **Confidence:** ≥ 85%
- **Success rate:** ≥ 95%
- **Time savings:** 7-9 minutes/ticket

---

## Key Documentation

- **README.md** - User guide
- **SKILL.md** - Technical reference
- **DEPLOYMENT_GUIDE.md** - Deployment steps
- **QUICK_REFERENCE.md** - This file
- **CHANGELOG.md** - Version history
- **PROJECT_SUMMARY.md** - Executive summary

---

## Support

### Quick Checks

```bash
python status.py              # System status
python verify_ocr.py          # OCR verification
python test_phase0.py         # Phase 0 test
python test_all.py            # All tests
```

### Logs

```
C:\Users\sleep\Documents\tickets\media-analysis.log
```

### Testing

```
test_phase0.py               # Phase 0 workflow
verify_ocr.py                # OCR setup
test_archival_workflow.py    # Phase 7
test-watcher.py              # Watcher
```

---

## Environment Variables (Optional)

Create `.env` file:

```bash
INCOMING_DIR=C:\Users\sleep\Documents\tickets\incoming
PROCESSING_DIR=C:\Users\sleep\Documents\tickets\processing
WATCHER_INTERVAL=5
AUTO_PROCESS_MEDIA=true
MEDIA_ANALYSIS_LOG=true
```

---

## Git Commands

### Initial Commit

```bash
git init
git add .
git commit -m "Initial commit: BMAD-EDI Media Analysis Skill v1.0.0"
```

### Create Repository

```bash
# On GitHub, create new repository
git remote add origin <repository-url>
git push -u origin main
```

---

## Quick Status Check

```bash
python status.py
```

**Expected Output:**
- All dependencies: OK
- Authentication: OK
- Directories: OK
- Recent activity: Stats shown
- System Ready: YES

---

## Getting Started (30 seconds)

```bash
# 1. Install
install.bat

# 2. Authenticate
python gemini_analyzer.py auth

# 3. Test
python test_phase0.py

# 4. Done!
```

---

## Common Workflows

### New Ticket Arrives

1. File dropped in `incoming/`
2. Watcher detects (or manual: `python workflow.py <file>`)
3. Analysis runs automatically
4. Review `metadata.json` + `preliminary_analysis.md`
5. Proceed with investigation

### Archive Resolved Ticket

```bash
python archival.py 13624970 WEB-456 "Company Name"
```

### Check System Health

```bash
python status.py
```

---

**Version:** 1.0.0
**Updated:** 2025-10-29
**Print this page for desk reference**
