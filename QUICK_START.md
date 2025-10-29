# Media Analysis - Quick Start Guide

**Status:** Structurally complete, dependencies need installation

**Time to Production:** 15 minutes

---

## 1. Install Dependencies (10 minutes)

```bash
cd C:\Users\sleep\.claude\skills\media-analysis
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -r requirements.txt
```

**Expected:** Installation completes without errors

---

## 2. Authenticate Gemini (2 minutes)

```bash
cd C:\Users\sleep\.claude\skills\media-analysis
python gemini_analyzer.py auth
```

**Expected:** Chrome opens, you log in, "Authentication successful" message

---

## 3. Verify Installation (1 minute)

```bash
cd C:\Users\sleep\.claude\skills\media-analysis
python test_integration.py
```

**Expected Output:**
```
============================================================
INTEGRATION TEST SUMMARY
============================================================
Total Tests: 26
Passed: 26
Failed: 0
Success Rate: 100.0%
============================================================
```

---

## 4. Test Processing (2 minutes)

```bash
cd C:\Users\sleep\.claude\skills\media-analysis
python run.py "C:\Users\sleep\Documents\tickets\incoming\test_hook.pdf"
```

**Expected:** JSON output with structured analysis

---

## 5. Usage

### Analyze Any File

```bash
python run.py <file_path>
```

**Supported Formats:**
- PDF documents
- Images (PNG, JPG, JPEG, GIF, BMP, TIFF)
- Audio files (MP3, WAV, M4A, FLAC)
- Video files (MP4, AVI, MOV, MKV)

### Example: Analyze Customer Attachment

```bash
python run.py "C:\Users\sleep\Documents\tickets\incoming\customer_attachment.pdf"
```

### Output Format

```json
{
  "file": "customer_attachment.pdf",
  "file_type": "application/pdf",
  "timestamp": "2025-10-29T14:15:00",
  "analysis": {
    "summary": "EDI 850 Purchase Order...",
    "key_findings": [...],
    "entities": {...},
    "recommendations": [...]
  },
  "ocr_text": "extracted text if image...",
  "metadata": {...}
}
```

---

## Troubleshooting

### Issue: "No module named 'patchright'"

**Solution:** Run step 1 (install dependencies)

### Issue: "Gemini authentication failed"

**Solution:** Run step 2 (authenticate Gemini)

### Issue: Tests failing

**Check:**
```bash
venv\Scripts\python.exe -c "import patchright; import cv2; import paddleocr; print('Dependencies OK')"
```

If error, reinstall dependencies:
```bash
venv\Scripts\python.exe -m pip install -r requirements.txt --force-reinstall
```

---

## Integration with Claude Code

### Automatic File Detection

When you drop a file in `C:\Users\sleep\Documents\tickets\incoming\`, it will:
1. Be detected by file-context.sh hook
2. Appear in Claude Code context
3. Be analyzed automatically (if configured)

### Manual Analysis in Claude Code

Say to Claude:
```
"Analyze this file: C:\path\to\file.pdf"
```

Claude will use the media-analysis skill automatically.

---

## Next Steps

1. **Install dependencies** (step 1 above)
2. **Authenticate Gemini** (step 2 above)
3. **Run tests** to verify (step 3 above)
4. **Test with real EDI document** (step 4 above)
5. **Integrate with /bmadedi workflow**

---

## Documentation

- **Full Test Report:** `TEST_RESULTS.md`
- **Test Execution Guide:** `RUN_TESTS.md`
- **Verification Checklist:** `VERIFICATION_CHECKLIST.md`
- **Agent 9 Report:** `AGENT9_REPORT.md`
- **Integration Guide:** `INTEGRATION_VERIFICATION.md`
- **Usage Guide:** `USAGE.md`
- **Hooks Guide:** `HOOKS_INTEGRATION.md`

---

## Support

**Test Scripts:**
- `test_integration.py` - Full integration test suite
- `test_performance.py` - Performance benchmarking

**Quick Status Check:**
```bash
python test_integration.py 2>&1 | tail -10
```

---

**Last Updated:** 2025-10-29
**Status:** Ready for deployment (after step 1)
