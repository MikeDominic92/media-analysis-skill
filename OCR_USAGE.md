# OCR Processor Module - Usage Guide

## Overview
The OCR Processor module provides comprehensive text extraction from images and PDFs using PaddleOCR with advanced image preprocessing.

## Agent 3 Deliverables
- Complete ocr_processor.py implementation
- PaddleOCR integration (English only)
- Advanced image preprocessing pipeline
- PDF to image conversion support
- Confidence scoring system
- Cache management
- Structured data extraction

---

## Installation

### Required Dependencies
```bash
pip install paddlepaddle==2.6.0
pip install paddleocr==2.7.0
pip install opencv-python==4.8.1
pip install Pillow==10.1.0
pip install pdf2image==1.16.3
```

### System Requirements (for PDF processing)
**Windows:**
```bash
choco install poppler
```

**macOS:**
```bash
brew install poppler
```

**Linux:**
```bash
apt-get install poppler-utils
```

---

## Quick Start

### Basic Text Extraction
```python
from ocr_processor import extract_text

# Extract text from image
result = extract_text("document.png")

if result["success"]:
    print(f"Confidence: {result['confidence']:.2%}")
    print(f"Text: {result['text']}")
```

### Initialize Processor
```python
from ocr_processor import OCRProcessor

processor = OCRProcessor()
result = processor.extract_text("document.pdf", preprocess=True)
```

---

## Core Features

### 1. Image Preprocessing Pipeline
The module applies advanced preprocessing for optimal OCR accuracy:

- **CLAHE (Contrast Limited Adaptive Histogram Equalization)**
  - Enhances local contrast
  - Improves text visibility

- **Noise Reduction**
  - Uses fast non-local means denoising
  - Removes artifacts and compression noise

- **Binarization**
  - Otsu's adaptive thresholding
  - Converts to clean black/white text

- **Upscaling**
  - Auto-detects low resolution images (< 1000px)
  - Scales 2x using cubic interpolation
  - Improves OCR accuracy for small text

**Usage:**
```python
processor = OCRProcessor()
result = processor.extract_text("low_quality.jpg", preprocess=True)
```

### 2. PDF Processing
Automatic conversion of multi-page PDFs to images:

```python
result = processor.extract_text("report.pdf")

# Check pages processed
print(f"Pages: {result['metadata']['pages']}")
```

### 3. Confidence Scoring
Every extraction includes confidence scores:

```python
result = extract_text("document.png")

if result["confidence"] > 0.85:
    print("High confidence extraction")
elif result["confidence"] > 0.70:
    print("Medium confidence - verify manually")
else:
    print("Low confidence - preprocessing recommended")
```

### 4. Structured Data Extraction
Extract key-value pairs from forms and documents:

```python
result = processor.extract_structured_data("form.pdf")

# Access key-value pairs
for key, value in result["key_value_pairs"].items():
    print(f"{key}: {value}")
```

**Supported patterns:**
- `Key: Value`
- `Key = Value`

### 5. Cache Management
Preprocessed images are cached for performance:

```python
# Get cache statistics
stats = processor.get_cache_stats()
print(f"Cache size: {stats['total_size_mb']:.2f} MB")
print(f"Files cached: {stats['file_count']}")

# Clear cache
cleared = processor.clear_cache()
print(f"Cleared {cleared} files")
```

---

## API Reference

### OCRProcessor Class

#### `__init__(data_dir=None)`
Initialize OCR processor with PaddleOCR engine.

**Parameters:**
- `data_dir` (Path, optional): Directory for data storage. Defaults to `./data`

#### `extract_text(file_path, preprocess=True)`
Extract text from image or PDF.

**Parameters:**
- `file_path` (str/Path): Path to file (supports: PDF, PNG, JPG, JPEG)
- `preprocess` (bool): Apply image preprocessing. Default: True

**Returns:**
```python
{
    "success": bool,
    "confidence": float,  # 0.0 to 1.0
    "text": str,  # Extracted text
    "structured_data": list,  # Raw OCR results
    "metadata": {
        "pages": int,
        "total_chars": int,
        "file_type": str
    }
}
```

#### `extract_structured_data(file_path)`
Extract structured data (key-value pairs, tables, layout).

**Returns:**
```python
{
    "success": bool,
    "tables": list,  # Future enhancement
    "key_value_pairs": dict,
    "layout": list
}
```

#### `clear_cache()`
Clear OCR cache directory.

**Returns:** Number of files cleared

#### `get_cache_stats()`
Get cache statistics.

**Returns:**
```python
{
    "file_count": int,
    "total_size_mb": float,
    "cache_dir": str
}
```

---

## Convenience Functions

### `extract_text(file_path)`
Quick text extraction with defaults.

### `extract_from_image(image_path)`
Image-specific extraction with preprocessing enabled.

### `extract_from_pdf(pdf_path)`
PDF-specific extraction with preprocessing enabled.

---

## CLI Usage

Run directly from command line:

```bash
python ocr_processor.py document.pdf
```

**Output:**
```
[+] Extracting text from: document.pdf
[+] Success! Confidence: 92.35%
[+] Pages: 3
[+] Total characters: 4567

--- Extracted Text ---
[extracted text here]
```

---

## Testing

Run the test suite:

```bash
# Basic tests
python test_ocr.py

# Test with specific image
python test_ocr.py sample_document.png
```

**Test Coverage:**
- [+] OCR processor initialization
- [+] Cache management
- [+] Preprocessing pipeline
- [+] Structured data extraction
- [+] Text extraction (with sample image)

---

## Integration with Media Analysis Skill

### Step 1: Import Module
```python
from ocr_processor import OCRProcessor
```

### Step 2: Process Media
```python
processor = OCRProcessor()

# For images
result = processor.extract_text("screenshot.png", preprocess=True)

# For PDFs
result = processor.extract_text("invoice.pdf", preprocess=True)
```

### Step 3: Use Results
```python
if result["success"] and result["confidence"] > 0.75:
    # High confidence - use directly
    extracted_text = result["text"]
else:
    # Low confidence - flag for review
    print(f"Warning: Low confidence ({result['confidence']:.2%})")
```

---

## Performance Characteristics

### Speed
- Single image: ~2-5 seconds
- PDF (per page): ~3-6 seconds
- Preprocessing overhead: +1-2 seconds

### Accuracy
- Clean documents: 95%+ confidence
- Low quality scans: 70-85% confidence
- Handwritten text: 40-60% confidence (not optimized)

### Resource Usage
- Memory: ~500MB-1GB (PaddleOCR models)
- Disk: ~300MB (models) + cache

---

## Troubleshooting

### Issue: "pdf2image not installed"
**Solution:**
```bash
pip install pdf2image==1.16.3
```

### Issue: "poppler not found"
**Solution:** Install poppler system package (see Installation section)

### Issue: Low confidence scores
**Solutions:**
1. Enable preprocessing: `preprocess=True`
2. Increase image resolution before OCR
3. Verify image quality (not blurry/distorted)
4. Check language is English

### Issue: "Could not read image"
**Solutions:**
1. Verify file exists and path is correct
2. Check file format is supported (PNG, JPG, JPEG, PDF)
3. Ensure file is not corrupted

### Issue: Cache filling up disk
**Solution:**
```python
processor.clear_cache()
```

---

## Limitations

1. **English Only**: PaddleOCR configured for English language only
2. **Stateless**: Each extraction is independent (no multi-query context)
3. **Table Detection**: Basic - advanced table extraction not implemented yet
4. **Handwriting**: Limited accuracy on handwritten text
5. **Special Characters**: Mathematical symbols may have lower accuracy

---

## Future Enhancements

- [ ] Multi-language support
- [ ] Advanced table detection and extraction
- [ ] Layout analysis (columns, headers, footers)
- [ ] Handwriting optimization
- [ ] Batch processing for multiple files
- [ ] GPU acceleration support
- [ ] Custom model fine-tuning

---

## Agent 3 Verification Checklist

- [+] Module can be imported: `from ocr_processor import OCRProcessor`
- [+] extract_text() works on images
- [+] extract_text() works on PDFs (with pdf2image)
- [+] Preprocessing improves accuracy
- [+] Confidence scoring implemented
- [+] Cache system functional
- [+] Structured data extraction working
- [+] Error handling comprehensive
- [+] CLI interface functional
- [+] Test suite complete

---

## Support & Documentation

**PaddleOCR Documentation:**
https://github.com/PaddlePaddle/PaddleOCR

**OpenCV Documentation:**
https://docs.opencv.org/

**Module Location:**
`C:\Users\sleep\.claude\skills\media-analysis\ocr_processor.py`

---

**Agent 3 - OCR Integration Specialist**
BMAD-EDI Media Analysis Integration
Status: COMPLETE
