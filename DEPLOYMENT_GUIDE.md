# Deployment Guide - BMAD-EDI Media Analysis Skill

**Version:** 1.0.0
**Date:** 2025-10-29
**Status:** Production Ready

---

## Overview

This guide provides step-by-step instructions for deploying the Media Analysis Skill to production. The deployment process is designed to be completed in 30-60 minutes.

---

## Pre-Deployment Checklist

### System Requirements

- [ ] Windows 10/11 OR Linux OR macOS
- [ ] Python 3.8 or higher
- [ ] 2GB RAM minimum (4GB recommended)
- [ ] 1GB free disk space
- [ ] Internet connection for authentication
- [ ] Google account for Gemini AI Studio access

### Dependencies

- [ ] Python 3.8+
- [ ] pip package manager
- [ ] Virtual environment support
- [ ] Chrome browser (auto-installed by Patchright)

---

## Installation Steps

### Step 1: Verify Prerequisites

```bash
# Check Python version
python --version
# Should show: Python 3.8.0 or higher

# Check pip
pip --version

# Navigate to skill directory
cd C:\Users\sleep\.claude\skills\media-analysis
```

**Expected Result:** Python 3.8+ and pip installed and accessible.

---

### Step 2: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# This installs:
# - patchright==1.55.2 (browser automation)
# - paddlepaddle==2.6.0 (ML framework)
# - paddleocr==2.7.0 (OCR engine)
# - opencv-python==4.8.1 (image processing)
# - Pillow==10.1.0 (image handling)
# - python-dotenv==1.0.0 (config management)
# - watchdog==3.0.0 (file monitoring)
# - pdf2image==1.16.3 (PDF conversion)
# - pywin32==306 (Windows service)
```

**Expected Result:** All packages installed without errors.

**Troubleshooting:**
- If paddlepaddle fails on Windows, use: `pip install paddlepaddle==2.6.0 -i https://pypi.tuna.tsinghua.edu.cn/simple`
- If pywin32 fails on non-Windows, it's optional (skip it)

---

### Step 3: Install Browser for Gemini

```bash
# Install Chrome for browser automation
patchright install chrome
```

**Expected Result:** Chrome browser installed in Patchright cache.

---

### Step 4: Authenticate with Google AI Studio

```bash
# Run authentication
python gemini_analyzer.py auth

# Browser will open automatically
# Sign in with your Google account
# Press Enter when authentication is complete
```

**Expected Result:**
- Browser opens to Google AI Studio
- Sign-in successful
- Authentication saved to `data/auth_info.json`
- Message: "Authentication successful!"

**Troubleshooting:**
- If browser doesn't open: Check firewall settings
- If authentication fails: Clear `data/browser_state/` and retry
- If "Google AI Studio not available": Check VPN or region settings

---

### Step 5: Verify OCR Installation

```bash
# Run OCR verification
python verify_ocr.py
```

**Expected Result:**
```
[NB] OCR Verification Started
[+] PaddleOCR loaded successfully
[+] Test image processed
[+] Text extraction working
[+] Confidence: 0.95
[+] OCR verification PASSED
```

**Troubleshooting:**
- If "PaddleOCR not found": Reinstall with `pip install paddleocr==2.7.0`
- If models downloading: Wait for completion (300MB, one-time)
- If confidence < 0.70: Expected for first run (models warming up)

---

### Step 6: Test Phase 0 Workflow

```bash
# Run Phase 0 integration test
python test_phase0.py
```

**Expected Result:**
```
[NB] Testing Phase 0 Workflow
[+] Test file created
[+] Metadata extracted
[+] Confidence: 0.87
[+] File organized correctly
[+] Artifacts generated
[+] Phase 0 test PASSED
```

**Troubleshooting:**
- If "File not found": Check `C:\Users\sleep\Documents\tickets\incoming\` exists
- If "Low confidence": Review `preliminary_analysis.md` for details
- If "Processing failed": Check logs in `media-analysis.log`

---

### Step 7: Update BMAD-EDI Configuration

This is the ONLY manual step required.

**File:** `C:\Users\sleep\.claude\commands\bmadedi.md`

**Add to "Phase 0: Pre-Investigation Analysis (Analyst)" section:**

```markdown
### Media File Auto-Analysis

When ticket files are media (PDF, images, audio, video):

1. Files dropped in `incoming/` are auto-detected
2. Media analysis skill processes them:
   - Gemini 2.5 Pro multimodal analysis
   - PaddleOCR text extraction (fallback)
   - Confidence scoring (0.0-1.0 scale)
3. Extracts EDI metadata automatically:
   - Ticket ID
   - Company name
   - Trading partner
   - Transaction type
   - Message ID
   - Severity
   - Issue summary
4. Generates artifacts:
   - `metadata.json` (structured data)
   - `preliminary_analysis.md` (human-readable)
5. Standardizes filename: `{TICKET_ID}_{COMPANY}_{SHORT_DESC}.{ext}`
6. Moves to `processing/ticket_{id}/`

**Time Savings:** 7-9 minutes per ticket (50-64% faster)

**Analyst Action:** Review `metadata.json` + `preliminary_analysis.md` before investigation.
```

**Estimated Time:** 5 minutes

---

### Step 8: Configure Directory Watcher (Optional)

For 24/7 automatic processing:

```bash
# Start watcher
python watch-incoming.py

# Or install as Windows service
install-watcher.bat

# Check status
python watcher-status.py
```

**Expected Result:**
- Watcher running in background
- Files automatically processed when dropped in `incoming/`
- Status shows: "Watcher active, monitoring incoming/"

**Note:** This is optional. You can manually run `python workflow.py <file>` instead.

---

### Step 9: Test End-to-End Workflow

```bash
# Create test ticket file
echo "Test Ticket #12345 - Company ABC - EDI 850 Purchase Order Error" > C:\Users\sleep\Documents\tickets\incoming\test_ticket.txt

# Wait 10 seconds (if watcher running) or manually process:
python workflow.py C:\Users\sleep\Documents\tickets\incoming\test_ticket.txt

# Verify results
dir C:\Users\sleep\Documents\tickets\processing\ticket_*

# Check metadata
type C:\Users\sleep\Documents\tickets\processing\ticket_12345\metadata.json

# Check analysis
type C:\Users\sleep\Documents\tickets\processing\ticket_12345\preliminary_analysis.md
```

**Expected Result:**
- Ticket processed successfully
- Folder created: `processing/ticket_12345/`
- Files present: `metadata.json`, `preliminary_analysis.md`, original file
- Standardized filename applied
- Confidence score >= 0.70

---

### Step 10: Verify Hook Integration

```bash
# Check file-context.sh hook (if using)
cat C:\Users\sleep\.claude\hooks\file-context.sh | grep "media-analysis"

# Expected: Media file detection logic present
```

**Expected Result:** Hook contains media file detection and auto-processing logic.

---

## Production Rollout

### Timeline

- **Preparation:** 30 minutes (Steps 1-6)
- **Configuration:** 5 minutes (Step 7)
- **Testing:** 15 minutes (Steps 8-10)
- **Total:** 50 minutes

### Rollout Strategy

**Week 1: Pilot**
- Deploy to 1-2 analysts
- Process 10-20 tickets manually
- Collect feedback
- Monitor confidence scores

**Week 2: Expansion**
- Deploy to full team
- Enable directory watcher (optional)
- Monitor processing times
- Document edge cases

**Week 3: Optimization**
- Tune confidence thresholds if needed
- Update prompts based on patterns
- Train team on workflow
- Establish best practices

---

## Monitoring & Maintenance

### Daily Checks

```bash
# View recent logs
Get-Content C:\Users\sleep\Documents\tickets\media-analysis.log -Tail 50

# Check watcher status (if enabled)
python watcher-status.py

# Verify authentication
python gemini_analyzer.py auth --check
```

### Weekly Maintenance

```bash
# Clear OCR cache (saves disk space)
Remove-Item -Recurse -Force C:\Users\sleep\.claude\skills\media-analysis\data\ocr_cache\*

# Rotate logs (if large)
Move-Item C:\Users\sleep\Documents\tickets\media-analysis.log C:\Users\sleep\Documents\tickets\logs\media-analysis_$(Get-Date -Format 'yyyy-MM-dd').log

# Review confidence trends
# (Manual review of metadata.json files)
```

### Monthly Reviews

- Review confidence score trends
- Analyze processing times
- Identify common failure patterns
- Update prompts if needed
- Check for Gemini API updates

---

## Success Metrics

### Key Performance Indicators

**Processing Speed:**
- Target: < 90 seconds per file
- Baseline: 15-20 minutes manual extraction
- Expected: 6-11 minutes automated

**Accuracy:**
- Target: >= 85% confidence score
- Fallback: OCR hybrid mode for < 0.70
- Success rate: >= 95%

**Time Savings:**
- Per ticket: 7-9 minutes saved
- Daily (10 tickets): 70-90 minutes saved
- Annual: 300-390 hours saved

**Adoption:**
- Week 1: 10% of tickets
- Week 2: 50% of tickets
- Week 3+: 90% of tickets

---

## Troubleshooting Guide

### Issue: Authentication Expired

**Symptoms:**
- "Not authenticated" errors
- "Please run: python gemini_analyzer.py auth"

**Solution:**
```bash
python gemini_analyzer.py auth
# Re-authenticate in browser
```

---

### Issue: Low Confidence Scores

**Symptoms:**
- Confidence < 0.70
- OCR fallback triggered frequently

**Solution:**
1. Check file quality (resolution, clarity)
2. Review `preliminary_analysis.md` for clues
3. Manually verify metadata.json
4. Consider updating prompts if pattern emerges

---

### Issue: Files Not Processing

**Symptoms:**
- Files stuck in incoming/
- No metadata.json generated

**Solution:**
```bash
# Check logs
Get-Content C:\Users\sleep\Documents\tickets\media-analysis.log -Tail 100

# Verify watcher status
python watcher-status.py

# Manual processing
python workflow.py C:\Users\sleep\Documents\tickets\incoming\<file>
```

---

### Issue: Watcher Service Crashed

**Symptoms:**
- `watcher-status.py` shows "Not running"
- Files not auto-processing

**Solution:**
```bash
# Restart watcher
python watch-incoming.py

# Or reinstall service (Windows)
install-watcher.bat
```

---

### Issue: OCR Errors

**Symptoms:**
- "PaddleOCR error" in logs
- Text extraction fails

**Solution:**
```bash
# Reinstall OCR
pip install paddleocr==2.7.0 --force-reinstall

# Clear cache
Remove-Item -Recurse -Force C:\Users\sleep\.claude\skills\media-analysis\data\ocr_cache\*

# Verify
python verify_ocr.py
```

---

## Rollback Procedures

### If Critical Issues Arise

**Immediate Actions:**
1. Stop directory watcher: `python watcher-status.py --stop`
2. Disable auto-processing in bmadedi.md
3. Revert to manual ticket extraction
4. Document failure mode
5. Review logs for root cause

**Recovery Steps:**
1. Fix identified issue
2. Run verification tests
3. Re-deploy to single analyst (pilot)
4. Monitor for 24 hours
5. Resume full deployment if stable

**Backup Strategy:**
- Original files preserved in `incoming/` until verified
- Metadata archived in `processing/ticket_{id}/`
- Logs retained for forensic analysis

---

## Post-Deployment Tasks

### Training

**Analyst Training (30 minutes):**
- Review `metadata.json` format
- Understand `preliminary_analysis.md` structure
- Learn confidence score interpretation
- Practice manual override procedures

**Documentation Specialist Training (15 minutes):**
- Phase 7 archival workflow
- Template usage
- Artifact preservation

### Documentation Updates

**Update bmadedi.md:**
- [x] Phase 0 media analysis section (Step 7)
- [ ] Analyst agent prompt enhancements
- [ ] Documentation Specialist archival procedures

**Create Team Resources:**
- [ ] One-page quick reference card
- [ ] Confidence score interpretation guide
- [ ] Troubleshooting flowchart
- [ ] FAQ document

---

## Next Steps After Deployment

### Short Term (Week 1-2)

1. Collect analyst feedback
2. Monitor confidence scores
3. Document edge cases
4. Tune prompts if needed
5. Establish baseline metrics

### Medium Term (Month 1-3)

1. Analyze time savings data
2. Calculate ROI
3. Identify improvement opportunities
4. Plan Phase 2 enhancements
5. Consider additional file types

### Long Term (Quarter 2+)

1. Multi-language support
2. Batch processing capabilities
3. GPU acceleration for OCR
4. Real-time dashboard
5. Integration with Zendesk API

---

## Support Contacts

### Technical Issues
- Check documentation: `SKILL.md`, `README.md`
- Review logs: `media-analysis.log`
- Run verification: `verify_ocr.py`, `test_phase0.py`

### Enhancement Requests
- Document in BMAD-EDI backlog
- Include use case and expected benefit
- Prioritize based on impact

---

## Appendix A: File Locations

**Core Scripts:**
- `C:\Users\sleep\.claude\skills\media-analysis\`

**Configuration:**
- `C:\Users\sleep\.claude\commands\bmadedi.md`
- `C:\Users\sleep\.claude\hooks\file-context.sh`

**Data Directories:**
- `C:\Users\sleep\Documents\tickets\incoming\`
- `C:\Users\sleep\Documents\tickets\processing\`
- `C:\Users\sleep\Documents\tickets\resolution\`
- `C:\Users\sleep\Documents\tickets\archived\`

**Logs:**
- `C:\Users\sleep\Documents\tickets\media-analysis.log`

---

## Appendix B: Verification Commands

```bash
# Full system check
python verify_ocr.py && python test_phase0.py && python test_archival_workflow.py

# Authentication status
python gemini_analyzer.py auth --check

# Watcher status
python watcher-status.py

# Process single file
python workflow.py <file_path>

# View logs (Windows PowerShell)
Get-Content C:\Users\sleep\Documents\tickets\media-analysis.log -Wait -Tail 20

# Clear cache
Remove-Item -Recurse -Force C:\Users\sleep\.claude\skills\media-analysis\data\ocr_cache\*
```

---

## Appendix C: Configuration Reference

**Environment Variables (.env - optional):**
```bash
INCOMING_DIR=C:\Users\sleep\Documents\tickets\incoming
PROCESSING_DIR=C:\Users\sleep\Documents\tickets\processing
WATCHER_INTERVAL=5
AUTO_PROCESS_MEDIA=true
MEDIA_ANALYSIS_LOG=true
```

**Confidence Thresholds:**
- HIGH: >= 0.85 (auto-accept)
- MEDIUM: 0.70-0.84 (accept with review flag)
- LOW: < 0.70 (trigger OCR fallback)

---

**Deployment Complete!**

After completing all steps, the Media Analysis Skill will be fully operational and integrated into the BMAD-EDI workflow. Expect 50-64% faster ticket extraction and 300-390 hours saved annually.

---

**Document Version:** 1.0.0
**Last Updated:** 2025-10-29
**Next Review:** 2025-11-29
