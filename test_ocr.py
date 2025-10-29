"""
Test script for OCR processor module
Tests basic functionality and image preprocessing
"""

import sys
from pathlib import Path
from ocr_processor import OCRProcessor, extract_text


def test_initialization():
    """Test OCR processor initialization"""
    print("[+] Testing OCR processor initialization...")
    try:
        processor = OCRProcessor()
        print("[+] SUCCESS: OCR processor initialized")
        print(f"[+] Data directory: {processor.data_dir}")
        print(f"[+] Cache directory: {processor.cache_dir}")
        return True
    except Exception as e:
        print(f"[!] FAILED: {e}")
        return False


def test_cache_management():
    """Test cache management functions"""
    print("\n[+] Testing cache management...")
    try:
        processor = OCRProcessor()

        # Get cache stats
        stats = processor.get_cache_stats()
        print(f"[+] Cache files: {stats['file_count']}")
        print(f"[+] Cache size: {stats['total_size_mb']:.2f} MB")

        # Clear cache
        cleared = processor.clear_cache()
        print(f"[+] Cleared {cleared} cache files")

        print("[+] SUCCESS: Cache management working")
        return True
    except Exception as e:
        print(f"[!] FAILED: {e}")
        return False


def test_text_extraction(image_path):
    """Test text extraction from image"""
    print(f"\n[+] Testing text extraction from: {image_path}")

    if not Path(image_path).exists():
        print(f"[!] Image not found: {image_path}")
        return False

    try:
        result = extract_text(image_path)

        if result["success"]:
            print(f"[+] SUCCESS: Text extracted")
            print(f"[+] Confidence: {result['confidence']:.2%}")
            print(f"[+] Pages: {result['metadata']['pages']}")
            print(f"[+] Characters: {result['metadata']['total_chars']}")
            print("\n--- Extracted Text (first 200 chars) ---")
            print(result["text"][:200])
            return True
        else:
            print(f"[!] FAILED: {result.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"[!] EXCEPTION: {e}")
        return False


def test_preprocessing():
    """Test image preprocessing pipeline"""
    print("\n[+] Testing preprocessing pipeline...")
    try:
        processor = OCRProcessor()

        # Create a simple test image
        import cv2
        import numpy as np

        # Create a test image with text
        img = np.ones((300, 600, 3), dtype=np.uint8) * 255
        cv2.putText(img, "Test Image", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)

        test_path = processor.cache_dir / "test_input.png"
        cv2.imwrite(str(test_path), img)

        # Preprocess it
        processed_path = processor._preprocess_image(str(test_path))

        if Path(processed_path).exists():
            print(f"[+] SUCCESS: Preprocessing created: {processed_path}")
            return True
        else:
            print("[!] FAILED: Preprocessed image not created")
            return False
    except Exception as e:
        print(f"[!] EXCEPTION: {e}")
        return False


def test_structured_data():
    """Test structured data extraction"""
    print("\n[+] Testing structured data extraction...")
    try:
        processor = OCRProcessor()

        # Create a test image with key-value pairs
        import cv2
        import numpy as np

        img = np.ones((400, 600, 3), dtype=np.uint8) * 255
        cv2.putText(img, "Name: John Doe", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(img, "Email: john@example.com", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(img, "Phone = 555-1234", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        test_path = processor.cache_dir / "test_kv.png"
        cv2.imwrite(str(test_path), img)

        # Extract structured data
        result = processor.extract_structured_data(str(test_path))

        if result["success"]:
            print(f"[+] SUCCESS: Structured data extracted")
            print(f"[+] Key-value pairs found: {len(result['key_value_pairs'])}")
            for key, value in result['key_value_pairs'].items():
                print(f"    {key}: {value}")
            return True
        else:
            print("[!] FAILED: Could not extract structured data")
            return False
    except Exception as e:
        print(f"[!] EXCEPTION: {e}")
        return False


def run_all_tests(test_image=None):
    """Run all tests"""
    print("="*60)
    print("OCR Processor Test Suite")
    print("="*60)

    results = []

    # Basic tests
    results.append(("Initialization", test_initialization()))
    results.append(("Cache Management", test_cache_management()))
    results.append(("Preprocessing", test_preprocessing()))
    results.append(("Structured Data", test_structured_data()))

    # Optional image test
    if test_image and Path(test_image).exists():
        results.append(("Text Extraction", test_text_extraction(test_image)))

    # Summary
    print("\n" + "="*60)
    print("Test Results Summary")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name}")

    print(f"\nPassed: {passed}/{total}")

    return passed == total


if __name__ == "__main__":
    test_image = sys.argv[1] if len(sys.argv) > 1 else None
    success = run_all_tests(test_image)
    sys.exit(0 if success else 1)
