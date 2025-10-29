# OCR Processor - Quick Start Guide

## 30-Second Quick Start

### 1. Import and Use
```python
from ocr_processor import extract_text

result = extract_text("document.pdf")
print(result["text"])
```

### 2. Check Confidence
```python
if result["confidence"] > 0.85:
    print("High confidence!")
```

### 3. Enable Preprocessing (Recommended)
```python
from ocr_processor import OCRProcessor

processor = OCRProcessor()
result = processor.extract_text("low_quality.jpg", preprocess=True)
```

---

## Common Use Cases

### Extract from Screenshot
```python
result = extract_text("screenshot.png")
```

### Extract from Multi-Page PDF
```python
result = extract_text("report.pdf")
print(f"Processed {result['metadata']['pages']} pages")
```

### Extract Key-Value Pairs (Forms)
```python
processor = OCRProcessor()
result = processor.extract_structured_data("form.pdf")

for key, value in result["key_value_pairs"].items():
    print(f"{key}: {value}")
```

### Manage Cache
```python
processor = OCRProcessor()

# Check cache size
stats = processor.get_cache_stats()
print(f"Cache: {stats['total_size_mb']:.2f} MB")

# Clear cache
processor.clear_cache()
```

---

## Result Structure

```python
{
    "success": True,              # Extraction successful?
    "confidence": 0.923,          # 0.0 to 1.0
    "text": "...",                # Extracted text
    "structured_data": [...],     # Raw OCR results
    "metadata": {
        "pages": 3,               # Number of pages
        "total_chars": 4567,      # Character count
        "file_type": ".pdf"       # File extension
    }
}
```

---

## Confidence Levels

| Score | Meaning | Action |
|-------|---------|--------|
| > 0.85 | High confidence | Use directly |
| 0.70-0.85 | Medium confidence | Verify if critical |
| < 0.70 | Low confidence | Manual review |

---

## CLI Usage

```bash
# Quick extraction
python ocr_processor.py document.pdf

# Verify installation
python verify_ocr.py

# Run tests
python test_ocr.py
```

---

## Installation (First Time)

```bash
# Install dependencies
pip install -r requirements.txt

# Install poppler (for PDF support)
# Windows: choco install poppler
# Mac: brew install poppler
# Linux: apt-get install poppler-utils
```

---

## Troubleshooting

### Low Confidence?
Enable preprocessing: `preprocess=True`

### PDF Error?
Install poppler system package

### Module Not Found?
```bash
pip install paddleocr==2.7.0
pip install opencv-python==4.8.1
pip install pdf2image==1.16.3
```

---

## Full Documentation

- **Complete Guide**: `OCR_USAGE.md`
- **API Reference**: `OCR_USAGE.md` (API Reference section)
- **Completion Report**: `AGENT3_COMPLETION_REPORT.md`

---

**Agent 3 - OCR Integration Specialist**
Quick Start Guide | BMAD-EDI Media Analysis Integration
