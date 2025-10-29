"""
Quick verification script for OCR processor
Checks that module can be imported and basic functions work
"""

import sys
from pathlib import Path


def verify_import():
    """Verify module can be imported"""
    print("[+] Step 1: Verifying module import...")
    try:
        from ocr_processor import OCRProcessor, extract_text, extract_from_image
        print("[+] SUCCESS: All imports working")
        return True
    except ImportError as e:
        print(f"[!] FAILED: Import error - {e}")
        return False
    except Exception as e:
        print(f"[!] FAILED: Unexpected error - {e}")
        return False


def verify_initialization():
    """Verify processor can be initialized"""
    print("\n[+] Step 2: Verifying processor initialization...")
    try:
        from ocr_processor import OCRProcessor
        processor = OCRProcessor()
        print(f"[+] SUCCESS: Processor initialized")
        print(f"    Data dir: {processor.data_dir}")
        print(f"    Cache dir: {processor.cache_dir}")
        return True
    except Exception as e:
        print(f"[!] FAILED: {e}")
        return False


def verify_paddleocr():
    """Verify PaddleOCR is available"""
    print("\n[+] Step 3: Verifying PaddleOCR...")
    try:
        from paddleocr import PaddleOCR
        print("[+] SUCCESS: PaddleOCR available")
        return True
    except ImportError:
        print("[!] FAILED: PaddleOCR not installed")
        print("    Install: pip install paddleocr==2.7.0")
        return False
    except Exception as e:
        print(f"[!] FAILED: {e}")
        return False


def verify_opencv():
    """Verify OpenCV is available"""
    print("\n[+] Step 4: Verifying OpenCV...")
    try:
        import cv2
        print(f"[+] SUCCESS: OpenCV {cv2.__version__} available")
        return True
    except ImportError:
        print("[!] FAILED: OpenCV not installed")
        print("    Install: pip install opencv-python==4.8.1")
        return False
    except Exception as e:
        print(f"[!] FAILED: {e}")
        return False


def verify_pdf2image():
    """Verify pdf2image is available"""
    print("\n[+] Step 5: Verifying pdf2image...")
    try:
        import pdf2image
        print("[+] SUCCESS: pdf2image available")
        return True
    except ImportError:
        print("[!] WARNING: pdf2image not installed (PDF processing will fail)")
        print("    Install: pip install pdf2image==1.16.3")
        print("    Also install poppler system package")
        return False
    except Exception as e:
        print(f"[!] FAILED: {e}")
        return False


def verify_methods():
    """Verify key methods exist"""
    print("\n[+] Step 6: Verifying processor methods...")
    try:
        from ocr_processor import OCRProcessor
        processor = OCRProcessor()

        required_methods = [
            'extract_text',
            'extract_structured_data',
            'clear_cache',
            'get_cache_stats',
            '_preprocess_image',
            '_pdf_to_images',
            '_parse_ocr_result',
            '_calculate_confidence'
        ]

        missing = []
        for method in required_methods:
            if not hasattr(processor, method):
                missing.append(method)

        if missing:
            print(f"[!] FAILED: Missing methods: {missing}")
            return False
        else:
            print(f"[+] SUCCESS: All {len(required_methods)} methods present")
            return True
    except Exception as e:
        print(f"[!] FAILED: {e}")
        return False


def verify_cache_management():
    """Verify cache management works"""
    print("\n[+] Step 7: Verifying cache management...")
    try:
        from ocr_processor import OCRProcessor
        processor = OCRProcessor()

        # Get stats
        stats = processor.get_cache_stats()
        print(f"[+] Cache stats retrieved:")
        print(f"    Files: {stats['file_count']}")
        print(f"    Size: {stats['total_size_mb']:.2f} MB")

        # Clear cache
        cleared = processor.clear_cache()
        print(f"[+] Cache cleared: {cleared} files")

        print("[+] SUCCESS: Cache management working")
        return True
    except Exception as e:
        print(f"[!] FAILED: {e}")
        return False


def run_verification():
    """Run all verification steps"""
    print("="*70)
    print("OCR Processor Module - Verification Script")
    print("="*70)

    steps = [
        ("Import", verify_import),
        ("Initialization", verify_initialization),
        ("PaddleOCR", verify_paddleocr),
        ("OpenCV", verify_opencv),
        ("pdf2image", verify_pdf2image),
        ("Methods", verify_methods),
        ("Cache Management", verify_cache_management)
    ]

    results = []
    for name, func in steps:
        result = func()
        results.append((name, result))

    # Summary
    print("\n" + "="*70)
    print("Verification Summary")
    print("="*70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {name}")

    print(f"\nResult: {passed}/{total} checks passed")

    if passed == total:
        print("\n[+] ALL CHECKS PASSED - OCR processor ready for use")
        return True
    else:
        print(f"\n[!] {total - passed} checks failed - review errors above")
        return False


if __name__ == "__main__":
    success = run_verification()
    sys.exit(0 if success else 1)
