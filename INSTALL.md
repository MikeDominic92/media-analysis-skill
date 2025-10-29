# Media Analysis Skill - Installation Guide

**Version:** 1.0.0
**Last Updated:** 2025-10-29

This guide provides step-by-step installation instructions for the BMAD-EDI Media Analysis skill.

## Prerequisites

### System Requirements
- **Operating System:** Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python:** 3.8 or higher
- **RAM:** 2GB minimum (4GB recommended)
- **Disk Space:** 500MB for dependencies and models
- **Internet:** Required for Gemini API and initial setup

### Software Requirements
- Python 3.8+ with pip
- Git (for cloning repositories)
- Chrome browser (installed automatically by Patchright)
- Google account (for Gemini authentication)

## Installation Steps

### Step 1: Navigate to Skills Directory

**Windows:**
```bash
cd C:\Users\sleep\.claude\skills\media-analysis
```

**Linux/Mac:**
```bash
cd ~/.claude/skills/media-analysis
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Expected output:**
```
Installing collected packages: patchright, paddlepaddle, paddleocr...
Successfully installed patchright-1.55.2 paddlepaddle-2.6.0 paddleocr-2.7.0...
```

**If errors occur:**
```bash
# Try upgrading pip first
pip install --upgrade pip

# Then retry installation
pip install -r requirements.txt --force-reinstall
```

### Step 3: Install Chrome for Gemini

```bash
patchright install chrome
```

**Expected output:**
```
Downloading Chromium...
Chromium downloaded successfully
```

**Troubleshooting:**
- If download fails, check internet connection
- Ensure sufficient disk space (~300MB)
- On Linux, may require: `sudo apt-get install libgbm1`

### Step 4: Authenticate with Google

```bash
python gemini_analyzer.py auth
```

**What happens:**
1. Chrome browser opens automatically
2. Navigate to Google AI Studio login page
3. Sign in with your Google account
4. Press Enter in terminal when done

**Expected output:**
```
[AUTH] Opening Google AI Studio...
[AUTH] Please sign in manually...
[AUTH] Press Enter when done...
[AUTH] Authentication saved!
```

**Authentication is stored in:**
- `data/auth_info.json`
- `data/browser_state/state.json`

**Troubleshooting:**
- If browser doesn't open, check firewall settings
- Ensure Google account has access to AI Studio
- Try incognito mode if login fails

### Step 5: Verify OCR Installation

```bash
python verify_ocr.py
```

**Expected output:**
```
[+] Testing OCR installation...
[+] PaddleOCR loaded successfully
[+] OCR test passed!
```

**If errors occur:**
```bash
# Reinstall PaddleOCR
pip uninstall paddleocr paddlepaddle
pip install paddlepaddle==2.6.0 paddleocr==2.7.0

# On Windows, may need Visual C++ redistributable
# Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe
```

### Step 6: Test Basic Functionality

```bash
# Create test directory structure
mkdir -p "C:\Users\sleep\Documents\tickets\incoming"

# Test with a sample file (if available)
python test_phase0.py
```

**Expected output:**
```
[*] Testing Phase 0 workflow...
[+] Processing test file...
[+] Metadata extracted successfully
[+] Confidence: 0.92
[+] All tests passed!
```

### Step 7: Configure Environment (Optional)

Create `.env` file in hooks directory:

**Windows:**
```bash
cd C:\Users\sleep\.claude\hooks
echo AUTO_PROCESS_MEDIA=true > .env
echo MEDIA_ANALYSIS_LOG=true >> .env
```

**Linux/Mac:**
```bash
cd ~/.claude/hooks
cat <<EOF > .env
AUTO_PROCESS_MEDIA=true
MEDIA_ANALYSIS_LOG=true
EOF
```

## Verification Checklist

After installation, verify the following:

- [ ] Python dependencies installed: `pip list | grep paddle`
- [ ] Chrome installed: `patchright --version`
- [ ] Authentication successful: `python gemini_analyzer.py auth --check`
- [ ] OCR working: `python verify_ocr.py`
- [ ] Directory structure exists: `ls C:\Users\sleep\Documents\tickets\`
- [ ] Test passes: `python test_phase0.py`

## Directory Structure Setup

The skill expects this directory structure:

```
C:\Users\sleep\Documents\tickets\
├── incoming/               # Place new tickets here
│   └── failed/            # Auto-created for failed extractions
├── processing/            # Active investigations
│   └── ticket_{id}/      # Per-ticket folders (auto-created)
├── resolution/            # Resolved tickets (organized by customer)
└── media-analysis.log     # Processing log
```

**Create directories:**
```bash
mkdir -p "C:\Users\sleep\Documents\tickets\incoming\failed"
mkdir -p "C:\Users\sleep\Documents\tickets\processing"
mkdir -p "C:\Users\sleep\Documents\tickets\resolution"
```

## Post-Installation Configuration

### 1. Test with Sample File

**Create a test PDF:**
```bash
# Download sample ticket (if available)
curl -o test_ticket.pdf https://example.com/sample-ticket.pdf

# Or use any existing PDF
python run.py test_ticket.pdf
```

### 2. Enable Directory Watcher (Optional)

**Windows:**
```bash
cd C:\Users\sleep\.claude\hooks
powershell .\watch-service.ps1 start
```

**Linux/Mac:**
```bash
cd ~/.claude/hooks
bash watch-control.sh start
```

### 3. Configure Logging

Edit `C:\Users\sleep\.claude\hooks\.env`:
```bash
# Enable detailed logging
MEDIA_ANALYSIS_LOG=true
LOG_LEVEL=DEBUG  # Options: DEBUG, INFO, WARNING, ERROR
```

## Troubleshooting Common Issues

### Issue 1: Import Errors

**Error:** `ModuleNotFoundError: No module named 'paddleocr'`

**Solution:**
```bash
pip install paddleocr==2.7.0 paddlepaddle==2.6.0 --force-reinstall
```

### Issue 2: Authentication Failed

**Error:** `[ERROR] Authentication failed`

**Solution:**
```bash
# Clear browser state
rm -rf data/browser_state/*
rm data/auth_info.json

# Re-authenticate
python gemini_analyzer.py auth
```

### Issue 3: Permission Denied

**Error:** `PermissionError: [Errno 13] Permission denied`

**Solution:**
```bash
# Windows: Run as Administrator
# Linux/Mac: Check directory permissions
chmod -R 755 ~/.claude/skills/media-analysis
```

### Issue 4: Chrome Not Found

**Error:** `Executable doesn't exist at...`

**Solution:**
```bash
# Reinstall Chrome
patchright uninstall chrome
patchright install chrome
```

### Issue 5: OCR Low Confidence

**Error:** Confidence scores consistently < 0.70

**Solution:**
- Check image quality (resolution, contrast)
- Enable preprocessing: `ocr.extract_text(file, preprocess=True)`
- Try hybrid mode (automatic if confidence < 0.70)

## Advanced Configuration

### Custom Prompts

Edit prompt files in `prompts/`:
- `edi-specialist.txt` - EDI metadata extraction
- `media-analysis.txt` - General analysis

### Performance Tuning

**For faster processing:**
```python
# In ocr_processor.py
self.ocr = PaddleOCR(
    use_angle_cls=True,
    lang='en',
    show_log=False,
    use_gpu=True  # If GPU available
)
```

### Multi-Language OCR

**English + Spanish:**
```python
self.ocr = PaddleOCR(lang='en', use_angle_cls=True)
self.ocr_es = PaddleOCR(lang='es', use_angle_cls=True)
```

## Uninstallation

To remove the skill:

```bash
# 1. Stop watcher (if running)
bash ~/.claude/hooks/watch-control.sh stop

# 2. Remove Python packages
pip uninstall patchright paddleocr paddlepaddle opencv-python

# 3. Remove skill directory
rm -rf ~/.claude/skills/media-analysis

# 4. Remove data directory (optional)
rm -rf ~/Documents/tickets
```

## Getting Help

If you encounter issues not covered here:

1. Check logs: `C:\Users\sleep\Documents\tickets\media-analysis.log`
2. Review error messages carefully
3. Verify all prerequisites are met
4. Consult SKILL.md for detailed API reference
5. Check agent completion reports for implementation details

## Next Steps

After successful installation:

1. Read SKILL.md for complete API reference
2. Review README.md for usage examples
3. Test with sample tickets
4. Configure automatic processing (optional)
5. Integrate with BMAD-EDI workflow

---

**Installation complete!** You're ready to use the media analysis skill.
