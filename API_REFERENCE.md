# Media Analysis Skill - API Reference

**Version:** 1.0.0
**Last Updated:** 2025-10-29

Complete API documentation for developers integrating with the Media Analysis skill.

## Table of Contents

- [Core Modules](#core-modules)
  - [GeminiAnalyzer](#geminianalyzer)
  - [OCRProcessor](#ocrprocessor)
  - [TicketWorkflow](#ticketworkflow)
  - [ArchivalManager](#archivalmanager)
- [Data Structures](#data-structures)
- [Error Handling](#error-handling)
- [Examples](#examples)

---

## Core Modules

### GeminiAnalyzer

**Module:** `gemini_analyzer.py`

Browser automation for Google Gemini 2.5 Pro API via AI Studio.

#### Class: GeminiAnalyzer

```python
class GeminiAnalyzer:
    """Gemini 2.5 Pro media analyzer with browser automation"""

    def __init__(self, data_dir=None):
        """
        Initialize Gemini analyzer

        Args:
            data_dir (Path, optional): Directory for auth and cache.
                Defaults to ./data/

        Attributes:
            data_dir: Storage directory for authentication
            browser_state_dir: Browser session storage
            auth_info_file: Authentication status file
            browser: Playwright browser instance
            context: Browser context with saved state
            page: Active browser page
        """
```

#### Methods

##### initialize()

```python
async def initialize(self):
    """
    Initialize browser with saved authentication state

    Returns:
        None

    Raises:
        Exception: If browser fails to launch

    Example:
        analyzer = GeminiAnalyzer()
        await analyzer.initialize()
    """
```

##### authenticate()

```python
async def authenticate(self):
    """
    Launch browser for manual Google authentication

    Process:
        1. Opens Google AI Studio in browser
        2. Waits for user to sign in manually
        3. Saves authentication state to disk

    Returns:
        None

    Raises:
        Exception: If browser automation fails

    Example:
        analyzer = GeminiAnalyzer()
        await analyzer.initialize()
        if not analyzer.check_auth():
            await analyzer.authenticate()
    """
```

##### check_auth()

```python
def check_auth(self):
    """
    Check if user is authenticated

    Returns:
        bool: True if authenticated, False otherwise

    Example:
        analyzer = GeminiAnalyzer()
        if analyzer.check_auth():
            print("Already authenticated")
        else:
            print("Authentication required")
    """
```

##### analyze()

```python
async def analyze(self, file_path, system_prompt=None, query=None):
    """
    Analyze media file with Gemini 2.5 Pro

    Args:
        file_path (str|Path): Path to media file
        system_prompt (str, optional): System instructions.
            If None, loads from prompts/media-analysis.txt
        query (str, optional): Question to ask about the file.
            If None, uses default query based on media type

    Returns:
        dict: {
            "success": bool,
            "response": str,  # Gemini's analysis
            "confidence": float,  # 0.0-1.0
            "metadata": dict,  # Extracted structured data
            "error": str  # Only if success=False
        }

    Raises:
        FileNotFoundError: If file_path doesn't exist
        Exception: If Gemini analysis fails

    Example:
        analyzer = GeminiAnalyzer()
        await analyzer.initialize()
        result = await analyzer.analyze("ticket.pdf")
        if result["success"]:
            print(f"Confidence: {result['confidence']}")
            print(f"Analysis: {result['response']}")
    """
```

##### detect_media_type()

```python
def detect_media_type(self, file_path):
    """
    Detect media type from file extension

    Args:
        file_path (str|Path): Path to file

    Returns:
        str: Media type - "document", "image", "audio", "video", or "unknown"

    Example:
        analyzer = GeminiAnalyzer()
        media_type = analyzer.detect_media_type("ticket.pdf")
        # Returns: "document"
    """
```

##### cleanup()

```python
async def cleanup(self):
    """
    Close browser and cleanup resources

    Returns:
        None

    Example:
        analyzer = GeminiAnalyzer()
        await analyzer.initialize()
        # ... do work ...
        await analyzer.cleanup()
    """
```

#### Standalone Functions

##### extract_ticket_metadata()

```python
async def extract_ticket_metadata(file_path):
    """
    Extract EDI ticket metadata from file using Gemini

    High-level convenience function that handles initialization,
    authentication, and cleanup automatically.

    Args:
        file_path (str|Path): Path to ticket file

    Returns:
        dict: {
            "ticket_id": str,
            "customer_name": str,
            "company": str,
            "trading_partner": str,
            "transaction_type": str,  # "850 PO", "856 ASN", etc.
            "message_id": str,
            "severity": str,  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
            "issue_title": str,
            "root_cause": str,
            "recommended_actions": list[str],
            "analysis_confidence": float,  # 0.0-1.0
            "extraction_method": str,  # "gemini"
            "timestamp": str,  # ISO 8601 format
            "original_file": str  # Filename
        }

    Raises:
        FileNotFoundError: If file doesn't exist
        Exception: If extraction fails

    Example:
        metadata = await extract_ticket_metadata("ticket.pdf")
        print(f"Ticket ID: {metadata['ticket_id']}")
        print(f"Company: {metadata['company']}")
        print(f"Confidence: {metadata['analysis_confidence']}")
    """
```

---

### OCRProcessor

**Module:** `ocr_processor.py`

PaddleOCR integration for text extraction with advanced preprocessing.

#### Class: OCRProcessor

```python
class OCRProcessor:
    """PaddleOCR text extraction with preprocessing"""

    def __init__(self, data_dir=None):
        """
        Initialize PaddleOCR with English language support

        Args:
            data_dir (Path, optional): Directory for cache.
                Defaults to ./data/

        Attributes:
            data_dir: Cache directory
            cache_dir: OCR cache for processed images
            ocr: PaddleOCR instance (English only)
        """
```

#### Methods

##### extract_text()

```python
def extract_text(self, file_path, preprocess=True):
    """
    Extract text from image or PDF

    Args:
        file_path (str|Path): Path to file (PDF, PNG, JPG, JPEG, etc.)
        preprocess (bool): Apply image preprocessing for better accuracy.
            Default: True

    Returns:
        dict: {
            "success": bool,
            "confidence": float,  # Average confidence across all text
            "text": str,  # Extracted text (all pages combined)
            "structured_data": list,  # Raw OCR results per page
            "metadata": dict: {
                "pages": int,
                "total_chars": int,
                "file_type": str
            },
            "error": str  # Only if success=False
        }

    Example:
        ocr = OCRProcessor()
        result = ocr.extract_text("screenshot.png", preprocess=True)
        if result["success"]:
            print(f"Confidence: {result['confidence']:.2f}")
            print(f"Text: {result['text']}")
            print(f"Pages: {result['metadata']['pages']}")
    """
```

##### clear_cache()

```python
def clear_cache(self):
    """
    Clear OCR cache directory

    Removes all cached preprocessed images to free disk space.

    Returns:
        int: Number of files deleted

    Example:
        ocr = OCRProcessor()
        deleted = ocr.clear_cache()
        print(f"Deleted {deleted} cached files")
    """
```

##### _preprocess_image()

```python
def _preprocess_image(self, image_path):
    """
    Apply multi-stage preprocessing to improve OCR accuracy

    Internal method. Applies:
    - Grayscale conversion
    - Noise reduction
    - Contrast enhancement
    - Sharpening
    - Thresholding

    Args:
        image_path (str|Path): Path to image

    Returns:
        str: Path to preprocessed image in cache

    Note: This is an internal method. Use extract_text(preprocess=True) instead.
    """
```

##### _calculate_confidence()

```python
def _calculate_confidence(self, ocr_results):
    """
    Calculate average confidence from OCR results

    Args:
        ocr_results (list): Raw PaddleOCR results

    Returns:
        float: Average confidence (0.0-1.0)
    """
```

---

### TicketWorkflow

**Module:** `workflow.py`

BMAD-EDI Phase 0 workflow for automated ticket processing.

#### Class: TicketWorkflow

```python
class TicketWorkflow:
    """BMAD-EDI ticket processing workflow - Phase 0 Pre-Investigation Analysis"""

    def __init__(self):
        """
        Initialize ticket workflow

        Attributes:
            tickets_base: C:\Users\sleep\Documents\tickets\
            incoming_dir: tickets_base/incoming
            processing_dir: tickets_base/processing
            failed_dir: incoming_dir/failed
            log_file: tickets_base/media-analysis.log
        """
```

#### Methods

##### process_ticket()

```python
async def process_ticket(self, file_path):
    """
    Phase 0: Pre-Investigation Analysis

    Complete workflow:
    1. Extract metadata with Gemini 2.5 Pro
    2. Check confidence score
    3. Fallback to OCR if confidence < 0.70 (hybrid mode)
    4. Generate standardized filename
    5. Create processing/ticket_{id}/ folder
    6. Copy file to processing folder
    7. Save metadata.json
    8. Generate preliminary_analysis.md
    9. Remove file from incoming/
    10. Log processing details

    Args:
        file_path (str|Path): Path to ticket file in incoming/

    Returns:
        dict: {
            "success": bool,
            "confidence": float,
            "ticket_folder": str,  # Path to processing/ticket_{id}/
            "metadata": dict,  # Extracted metadata
            "extraction_method": str,  # "gemini" or "hybrid"
            "processing_time": float,  # Seconds
            "artifacts": dict: {
                "metadata_json": str,  # Path to metadata.json
                "analysis_md": str,  # Path to preliminary_analysis.md
                "processed_file": str  # Path to standardized file
            },
            "error": str  # Only if success=False
        }

    Raises:
        FileNotFoundError: If file doesn't exist
        Exception: If processing fails

    Example:
        workflow = TicketWorkflow()
        result = await workflow.process_ticket("incoming/ticket.pdf")

        if result["success"]:
            print(f"Ticket ID: {result['metadata']['ticket_id']}")
            print(f"Confidence: {result['confidence']:.2f}")
            print(f"Method: {result['extraction_method']}")
            print(f"Time: {result['processing_time']:.1f}s")
            print(f"Folder: {result['ticket_folder']}")
        else:
            print(f"Error: {result['error']}")
    """
```

##### _generate_filename()

```python
def _generate_filename(self, metadata, extension):
    """
    Generate standardized filename

    Format: YYYY-MM-DD_{ticket-id}_{company}_TradingPartner-{partner}_{transaction}.{ext}

    Args:
        metadata (dict): Extracted ticket metadata
        extension (str): File extension (e.g., ".pdf")

    Returns:
        str: Standardized filename

    Example:
        workflow = TicketWorkflow()
        filename = workflow._generate_filename(metadata, ".pdf")
        # Returns: "2025-10-29_13624970_AceHardware_TradingPartner-HomeDepot_856-ASN-Rejection.pdf"
    """
```

##### _generate_analysis_md()

```python
def _generate_analysis_md(self, metadata, output_file):
    """
    Generate preliminary_analysis.md from metadata

    Creates human-readable markdown report with:
    - Ticket overview
    - Issue summary
    - Root cause analysis
    - Recommended actions
    - Next steps
    - Extraction details

    Args:
        metadata (dict): Extracted metadata
        output_file (Path): Path to save markdown file

    Returns:
        None

    Side Effects:
        Writes preliminary_analysis.md to disk
    """
```

---

### ArchivalManager

**Module:** `archival.py`

Phase 7 artifact archival for resolved tickets.

#### Standalone Functions

##### archive_ticket()

```python
async def archive_ticket(ticket_id, webedi_id, company_name):
    """
    Archive resolved ticket with full context preservation

    Process:
    1. Locate ticket in processing/{ticket_id}/
    2. Generate resolution summary from templates
    3. Copy all artifacts to resolution/{company}/{ticket_id}/
    4. Preserve metadata, analysis, and resolution docs
    5. Update knowledge base index
    6. Clean up processing folder

    Args:
        ticket_id (str): Ticket ID (e.g., "13624970")
        webedi_id (str): WebEDI ticket reference (e.g., "WEB-456")
        company_name (str): Customer company name

    Returns:
        dict: {
            "success": bool,
            "archive_path": str,  # Path to archived folder
            "artifacts_archived": int,  # Number of files archived
            "summary_generated": bool,
            "error": str  # Only if success=False
        }

    Example:
        result = await archive_ticket(
            ticket_id="13624970",
            webedi_id="WEB-456",
            company_name="Ace Hardware"
        )

        if result["success"]:
            print(f"Archived to: {result['archive_path']}")
            print(f"Files: {result['artifacts_archived']}")
    """
```

---

## Data Structures

### Metadata Schema

Standard metadata extracted by `extract_ticket_metadata()`:

```python
{
    # Required Fields
    "ticket_id": str,              # Ticket number (e.g., "13624970")
    "customer_name": str,          # Contact name
    "company": str,                # Company name
    "trading_partner": str,        # EDI trading partner
    "transaction_type": str,       # EDI transaction (e.g., "850 PO", "856 ASN")
    "severity": str,               # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    "issue_title": str,            # Brief description

    # Analysis Fields
    "root_cause": str,             # Identified root cause
    "recommended_actions": [str],  # List of action items

    # Confidence & Method
    "analysis_confidence": float,  # 0.0-1.0
    "extraction_method": str,      # "gemini" or "hybrid"

    # Optional Fields (may be None)
    "message_id": str,             # EDI message ID
    "error_code": str,             # Specific error code
    "segment_info": str,           # EDI segment details

    # Metadata
    "timestamp": str,              # ISO 8601 timestamp
    "original_file": str,          # Original filename
    "processed_file": str          # Standardized filename (added by workflow)
}
```

### OCR Result Schema

Structure returned by `OCRProcessor.extract_text()`:

```python
{
    "success": bool,
    "confidence": float,           # 0.0-1.0
    "text": str,                   # Combined text from all pages
    "structured_data": [           # Raw OCR results per page
        [
            [                       # Per text block
                [[x1, y1], [x2, y2], [x3, y3], [x4, y4]],  # Bounding box
                ("detected text", confidence)               # Text + confidence
            ],
            ...
        ],
        ...
    ],
    "metadata": {
        "pages": int,              # Number of pages processed
        "total_chars": int,        # Total characters extracted
        "file_type": str           # File extension
    },
    "error": str                   # Only present if success=False
}
```

### Workflow Result Schema

Structure returned by `TicketWorkflow.process_ticket()`:

```python
{
    "success": bool,
    "confidence": float,           # Final confidence (Gemini or hybrid)
    "ticket_folder": str,          # Path to processing/ticket_{id}/
    "metadata": dict,              # Full metadata (see Metadata Schema)
    "extraction_method": str,      # "gemini" or "hybrid"
    "processing_time": float,      # Processing time in seconds
    "artifacts": {
        "metadata_json": str,      # Path to metadata.json
        "analysis_md": str,        # Path to preliminary_analysis.md
        "processed_file": str      # Path to standardized file
    },
    "error": str                   # Only present if success=False
}
```

---

## Error Handling

### Exception Types

All modules raise standard Python exceptions:

```python
# File not found
FileNotFoundError: Raised when input file doesn't exist

# General errors
Exception: Raised for processing errors, authentication failures, etc.

# Async errors
asyncio.TimeoutError: Raised when browser operations timeout
```

### Error Response Format

Functions return error information in dict:

```python
{
    "success": False,
    "error": "Error message describing what went wrong",
    "confidence": 0.0,
    # Other fields may be present with default/empty values
}
```

### Best Practices

```python
# Always check success flag
result = await analyzer.analyze(file_path)
if not result["success"]:
    print(f"Error: {result['error']}")
    return

# Use try-except for critical operations
try:
    metadata = await extract_ticket_metadata(file_path)
except FileNotFoundError:
    print(f"File not found: {file_path}")
except Exception as e:
    print(f"Extraction failed: {e}")
```

---

## Examples

### Example 1: Basic Media Analysis

```python
import asyncio
from gemini_analyzer import GeminiAnalyzer

async def analyze_file(file_path):
    analyzer = GeminiAnalyzer()
    await analyzer.initialize()

    try:
        result = await analyzer.analyze(file_path)
        if result["success"]:
            print(f"Analysis: {result['response']}")
            print(f"Confidence: {result['confidence']:.2f}")
        else:
            print(f"Error: {result['error']}")
    finally:
        await analyzer.cleanup()

# Run
asyncio.run(analyze_file("ticket.pdf"))
```

### Example 2: OCR Text Extraction

```python
from ocr_processor import OCRProcessor

def extract_text_from_image(image_path):
    ocr = OCRProcessor()
    result = ocr.extract_text(image_path, preprocess=True)

    if result["success"]:
        print(f"Extracted {result['metadata']['total_chars']} characters")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Text:\n{result['text']}")
    else:
        print(f"Error: {result['error']}")

# Run
extract_text_from_image("screenshot.png")
```

### Example 3: Complete Ticket Processing

```python
import asyncio
from workflow import TicketWorkflow

async def process_ticket(file_path):
    workflow = TicketWorkflow()
    result = await workflow.process_ticket(file_path)

    if result["success"]:
        print(f"Ticket ID: {result['metadata']['ticket_id']}")
        print(f"Company: {result['metadata']['company']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Method: {result['extraction_method']}")
        print(f"Processing time: {result['processing_time']:.1f}s")
        print(f"Artifacts saved to: {result['ticket_folder']}")
    else:
        print(f"Processing failed: {result['error']}")

# Run
asyncio.run(process_ticket("incoming/ticket.pdf"))
```

### Example 4: Hybrid Mode (Gemini + OCR)

```python
import asyncio
from gemini_analyzer import extract_ticket_metadata
from ocr_processor import OCRProcessor

async def hybrid_extraction(file_path):
    # Step 1: Try Gemini first
    print("[*] Extracting with Gemini...")
    metadata = await extract_ticket_metadata(file_path)

    # Step 2: Check confidence
    confidence = metadata.get("analysis_confidence", 0.0)
    print(f"[*] Gemini confidence: {confidence:.2f}")

    # Step 3: Fallback to OCR if low confidence
    if confidence < 0.70:
        print("[*] Low confidence - trying OCR...")
        ocr = OCRProcessor()
        ocr_result = ocr.extract_text(file_path, preprocess=True)

        if ocr_result["success"]:
            metadata["ocr_text"] = ocr_result["text"]
            metadata["ocr_confidence"] = ocr_result["confidence"]
            metadata["extraction_method"] = "hybrid"
            print(f"[+] OCR confidence: {ocr_result['confidence']:.2f}")

    return metadata

# Run
asyncio.run(hybrid_extraction("ticket.pdf"))
```

### Example 5: Batch Processing

```python
import asyncio
from pathlib import Path
from workflow import TicketWorkflow

async def process_batch(incoming_dir):
    workflow = TicketWorkflow()
    incoming = Path(incoming_dir)

    files = list(incoming.glob("*.pdf"))
    print(f"[*] Found {len(files)} files to process")

    results = []
    for file in files:
        print(f"\n[*] Processing: {file.name}")
        result = await workflow.process_ticket(file)
        results.append(result)

        if result["success"]:
            print(f"[+] Success: {result['metadata']['ticket_id']}")
        else:
            print(f"[!] Failed: {result['error']}")

    # Summary
    successful = sum(1 for r in results if r["success"])
    print(f"\n[*] Processed {len(results)} files")
    print(f"[+] Successful: {successful}")
    print(f"[!] Failed: {len(results) - successful}")

# Run
asyncio.run(process_batch("C:/Users/sleep/Documents/tickets/incoming"))
```

### Example 6: Custom Authentication Check

```python
from gemini_analyzer import GeminiAnalyzer

async def ensure_authenticated():
    analyzer = GeminiAnalyzer()

    if not analyzer.check_auth():
        print("[!] Not authenticated - starting authentication...")
        await analyzer.initialize()
        await analyzer.authenticate()
        print("[+] Authentication complete!")
    else:
        print("[+] Already authenticated")

# Run
import asyncio
asyncio.run(ensure_authenticated())
```

---

## Configuration

### Environment Variables

Optional configuration via environment variables:

```bash
# Ticket directories
TICKETS_BASE_DIR=C:\Users\sleep\Documents\tickets
INCOMING_DIR=${TICKETS_BASE_DIR}\incoming
PROCESSING_DIR=${TICKETS_BASE_DIR}\processing

# Logging
MEDIA_ANALYSIS_LOG=true
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR

# Processing options
AUTO_PROCESS_MEDIA=true
CONFIDENCE_THRESHOLD=0.70  # Trigger OCR fallback below this
```

### Prompt Customization

Edit prompts in `prompts/` directory:

**prompts/edi-specialist.txt:**
```
You are an EDI specialist analyzing customer support tickets.
Extract the following metadata...
```

**prompts/media-analysis.txt:**
```
Analyze this media file and provide insights...
```

---

## Performance Optimization

### Caching

OCR results are cached in `data/ocr_cache/`:
- Preprocessed images are cached to avoid re-processing
- Clear cache weekly: `ocr.clear_cache()`

### Parallel Processing

For batch processing, use asyncio.gather():

```python
async def process_parallel(files):
    workflow = TicketWorkflow()
    tasks = [workflow.process_ticket(f) for f in files]
    results = await asyncio.gather(*tasks)
    return results
```

### GPU Acceleration

Enable GPU for OCR (requires CUDA):

```python
ocr = PaddleOCR(
    use_angle_cls=True,
    lang='en',
    use_gpu=True  # Requires paddlepaddle-gpu
)
```

---

## Testing

### Unit Tests

```bash
# OCR tests
python test_ocr.py

# Phase 0 workflow
python test_phase0.py

# Archival workflow
python test_archival_workflow.py
```

### Integration Tests

```python
import asyncio
from workflow import TicketWorkflow

async def test_integration():
    workflow = TicketWorkflow()
    result = await workflow.process_ticket("test_ticket.pdf")
    assert result["success"], "Processing failed"
    assert result["confidence"] >= 0.70, "Low confidence"
    print("[+] Integration test passed!")

asyncio.run(test_integration())
```

---

## Changelog

### Version 1.0.0 (2025-10-29)
- Initial production release
- Gemini 2.5 Pro integration
- PaddleOCR integration
- Phase 0 workflow
- Phase 7 archival
- Complete API documentation

---

**Questions?** Refer to SKILL.md for additional details or check agent completion reports.
