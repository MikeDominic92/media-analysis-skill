# Media Analysis - Test Execution Guide

Quick reference for running all tests on the media-analysis skill.

---

## Prerequisites

**Install Dependencies First:**
```bash
cd C:\Users\sleep\.claude\skills\media-analysis
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -r requirements.txt
```

**Expected Installation Time:** 5-10 minutes

---

## Test Suites

### 1. Integration Test Suite

**Purpose:** Verify all components work together correctly

**Command:**
```bash
cd C:\Users\sleep\.claude\skills\media-analysis
python test_integration.py
```

**What It Tests:**
- Component availability (7 tests)
- Module imports (4 tests)
- Configuration files (5 tests)
- File system structure (4 tests)
- Gemini integration (1 test)
- OCR processor (1 test)
- Workflow integration (3 tests)
- Hook integration (3 tests)

**Expected Result:** 26/26 tests pass (100%)

**Duration:** ~5 seconds

---

### 2. Performance Test Suite

**Purpose:** Measure processing speed and resource usage

**Command:**
```bash
cd C:\Users\sleep\.claude\skills\media-analysis
python test_performance.py
```

**What It Tests:**
- Startup time
- Memory baseline
- File I/O performance
- Directory scan speed
- JSON serialization
- Disk space availability
- CPU information

**Expected Result:** 7/7 tests pass (100%)

**Duration:** ~2 seconds

**Output:** Results saved to `performance_results.json`

---

### 3. Gemini Authentication Test

**Purpose:** Verify Gemini API access

**Command:**
```bash
cd C:\Users\sleep\.claude\skills\media-analysis
python gemini_analyzer.py auth
```

**What It Does:**
- Opens Chrome for Google authentication
- Saves session for future use
- Verifies API connectivity

**Expected Result:** "Authentication successful" message

**Duration:** 30 seconds (manual login required)

---

### 4. Live Processing Test

**Purpose:** Test end-to-end file processing

**Command:**
```bash
cd C:\Users\sleep\.claude\skills\media-analysis
python run.py "C:\Users\sleep\Documents\tickets\incoming\test_hook.pdf"
```

**What It Does:**
- Analyzes file with Gemini
- Extracts text with OCR (if image)
- Generates structured analysis
- Saves results

**Expected Result:** JSON output with analysis

**Duration:** 10-30 seconds (depends on file size and Gemini API)

---

## Quick Test Commands

### Run All Tests (After Dependency Installation)
```bash
cd C:\Users\sleep\.claude\skills\media-analysis
python test_integration.py && python test_performance.py
```

### Check Current Status
```bash
cd C:\Users\sleep\.claude\skills\media-analysis
python test_integration.py 2>&1 | grep -E "PASS|FAIL|Success"
```

### Verify Dependencies Installed
```bash
cd C:\Users\sleep\.claude\skills\media-analysis
venv\Scripts\python.exe -c "import patchright; import cv2; import paddleocr; print('All dependencies OK')"
```

---

## Test File Locations

**Test Scripts:**
- `C:\Users\sleep\.claude\skills\media-analysis\test_integration.py`
- `C:\Users\sleep\.claude\skills\media-analysis\test_performance.py`

**Test Files:**
- `C:\Users\sleep\Documents\tickets\incoming\test_hook.pdf`
- `C:\Users\sleep\Documents\tickets\incoming\test_verify.pdf`

**Test Results:**
- `C:\Users\sleep\.claude\skills\media-analysis\TEST_RESULTS.md` (detailed report)
- `C:\Users\sleep\.claude\skills\media-analysis\performance_results.json` (performance metrics)

---

## Troubleshooting

### Issue: "No module named 'patchright'"

**Solution:**
```bash
cd C:\Users\sleep\.claude\skills\media-analysis
venv\Scripts\python.exe -m pip install patchright==1.55.2
```

### Issue: "No module named 'cv2'"

**Solution:**
```bash
cd C:\Users\sleep\.claude\skills\media-analysis
venv\Scripts\python.exe -m pip install opencv-python
```

### Issue: "No module named 'paddleocr'"

**Solution:**
```bash
cd C:\Users\sleep\.claude\skills\media-analysis
venv\Scripts\python.exe -m pip install paddleocr
```

### Issue: "Virtual environment not found"

**Solution:**
```bash
cd C:\Users\sleep\.claude\skills\media-analysis
python -m venv venv
venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## Expected Test Results

### Before Dependency Installation

**Integration Tests:** 20/26 pass (76.9%)
- Component tests: 7/7 PASS
- Import tests: 1/4 FAIL (missing dependencies)
- Configuration tests: 5/5 PASS
- File system tests: 4/4 PASS
- Integration tests: 0/3 FAIL (missing dependencies)
- Hook tests: 3/3 PASS

**Performance Tests:** 6/7 pass (85.7%)
- Startup test: FAIL (missing dependencies)
- All other tests: PASS

### After Dependency Installation

**Integration Tests:** 26/26 pass (100%)
- All tests should pass

**Performance Tests:** 7/7 pass (100%)
- All tests should pass

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Media Analysis Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: windows-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'

    - name: Create virtual environment
      run: python -m venv venv

    - name: Install dependencies
      run: |
        venv\Scripts\python.exe -m pip install --upgrade pip
        venv\Scripts\python.exe -m pip install -r requirements.txt

    - name: Run integration tests
      run: python test_integration.py

    - name: Run performance tests
      run: python test_performance.py
```

---

## Test Development

### Adding New Tests to Integration Suite

Edit `test_integration.py` and add methods to `IntegrationTestSuite` class:

```python
async def test_phase9_custom(self):
    """Test custom functionality"""
    # Your test logic here
    self.test("Custom test name", condition, "error details")
```

Then add to `run_all_tests()`:
```python
print("\n[PHASE 9] Custom Tests\n")
await self.test_phase9_custom()
```

### Adding New Performance Tests

Edit `test_performance.py` and add methods to `PerformanceTestSuite` class:

```python
def measure_custom_metric(self):
    """Measure custom performance metric"""
    # Your measurement logic here
    self.results['custom_metric'] = {
        'value': measurement,
        'threshold': threshold,
        'passed': measurement < threshold
    }
```

Then add to `run_all_tests()`:
```python
print("[*] Testing custom metric...")
self.measure_custom_metric()
```

---

## Test Coverage

**Current Coverage:**
- Component structure: 100%
- Module imports: 100%
- Configuration: 100%
- File system: 100%
- Gemini integration: Basic (auth only)
- OCR integration: Basic (instantiation only)
- Workflow: Basic (instantiation only)
- Hooks: 100%
- Performance: 100%

**Not Yet Covered:**
- End-to-end file processing
- Error handling scenarios
- Edge cases (corrupt files, network failures)
- Concurrent processing
- Large file handling

**Future Test Additions:**
- E2E workflow test with real EDI document
- Error injection tests
- Load testing (multiple files)
- Stress testing (large files)
- Recovery testing (network interruption)

---

## Maintenance

**Regular Testing Schedule:**
- Run integration tests: After any code change
- Run performance tests: Weekly
- Run full E2E tests: Before each release
- Verify Gemini auth: Monthly (session expiry)

**Updating Tests:**
- Keep test files in sync with code changes
- Update expected results when behavior changes
- Add regression tests for any bugs found
- Document any test-specific configuration

---

**Last Updated:** 2025-10-29
**Maintained By:** BMAD-EDI Engineering Team
