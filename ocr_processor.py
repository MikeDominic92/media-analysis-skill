"""
PaddleOCR Text Extraction Processor
Handles text extraction from images and PDFs (English only)

Agent 3 - OCR Integration Specialist
BMAD-EDI Media Analysis Integration
"""

import os
import cv2
import numpy as np
from pathlib import Path
from PIL import Image
from paddleocr import PaddleOCR


class OCRProcessor:
    def __init__(self, data_dir=None):
        """Initialize PaddleOCR with English language support"""
        self.data_dir = data_dir or Path(__file__).parent / "data"
        self.cache_dir = self.data_dir / "ocr_cache"
        self.cache_dir.mkdir(exist_ok=True, parents=True)

        # Initialize PaddleOCR (English only)
        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang='en',
            show_log=False
        )

    def extract_text(self, file_path, preprocess=True):
        """
        Extract text from image or PDF

        Args:
            file_path: Path to file (PDF, PNG, JPG, JPEG)
            preprocess: Apply image preprocessing for better accuracy

        Returns:
            dict: {
                "success": bool,
                "confidence": float,
                "text": str,
                "structured_data": list,
                "metadata": dict
            }
        """
        file_path = Path(file_path)

        if not file_path.exists():
            return {
                "success": False,
                "error": f"File not found: {file_path}",
                "confidence": 0.0,
                "text": "",
                "structured_data": [],
                "metadata": {}
            }

        try:
            # Convert PDF to images if needed
            if file_path.suffix.lower() == '.pdf':
                images = self._pdf_to_images(file_path)
            else:
                images = [str(file_path)]

            # Extract text from each image
            all_text = []
            all_results = []

            for img_path in images:
                if preprocess:
                    img_path = self._preprocess_image(img_path)

                result = self.ocr.ocr(img_path, cls=True)
                text = self._parse_ocr_result(result)
                all_text.append(text)
                all_results.append(result)

            # Combine results
            combined_text = "\n\n".join(all_text)
            confidence = self._calculate_confidence(all_results)

            return {
                "success": True,
                "confidence": confidence,
                "text": combined_text,
                "structured_data": all_results,
                "metadata": {
                    "pages": len(images),
                    "total_chars": len(combined_text),
                    "file_type": file_path.suffix.lower()
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "confidence": 0.0,
                "text": "",
                "structured_data": [],
                "metadata": {}
            }

    def _pdf_to_images(self, pdf_path):
        """
        Convert PDF to images for OCR processing
        Returns list of image paths
        """
        try:
            from pdf2image import convert_from_path
        except ImportError:
            print("[!] pdf2image not installed. Run: pip install pdf2image")
            print("[!] Also ensure poppler is installed:")
            print("    Windows: choco install poppler")
            print("    Mac: brew install poppler")
            print("    Linux: apt-get install poppler-utils")
            return []

        try:
            images = convert_from_path(pdf_path)
            image_paths = []

            for i, img in enumerate(images):
                img_path = self.cache_dir / f"{Path(pdf_path).stem}_page_{i+1}.png"
                img.save(img_path)
                image_paths.append(str(img_path))

            return image_paths
        except Exception as e:
            print(f"[!] Error converting PDF: {e}")
            return []

    def _preprocess_image(self, img_path):
        """
        Preprocess image for better OCR accuracy
        - Enhance contrast
        - Upscale if low resolution
        - Denoise
        - Binarize
        """
        img = cv2.imread(str(img_path))

        if img is None:
            print(f"[!] Could not read image: {img_path}")
            return str(img_path)

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)

        # Denoise
        denoised = cv2.fastNlMeansDenoising(enhanced)

        # Binarize (Otsu's method)
        _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Upscale if needed (< 300 DPI equivalent)
        h, w = binary.shape
        if h < 1000 or w < 1000:
            scale = 2.0
            binary = cv2.resize(binary, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

        # Save preprocessed image
        processed_path = self.cache_dir / f"processed_{Path(img_path).name}"
        cv2.imwrite(str(processed_path), binary)

        return str(processed_path)

    def _parse_ocr_result(self, result):
        """Parse PaddleOCR result into plain text"""
        if not result or not result[0]:
            return ""

        text_lines = []
        for line in result[0]:
            text_lines.append(line[1][0])  # Extract text from structure

        return "\n".join(text_lines)

    def _calculate_confidence(self, results):
        """
        Calculate overall confidence score
        Based on individual character confidences
        """
        if not results:
            return 0.0

        total_conf = 0.0
        count = 0

        for page_result in results:
            if page_result and page_result[0]:
                for line in page_result[0]:
                    conf = line[1][1]  # Confidence score
                    total_conf += conf
                    count += 1

        return total_conf / count if count > 0 else 0.0

    def extract_structured_data(self, file_path):
        """
        Extract structured data (tables, forms, key-value pairs)
        Uses layout analysis

        Returns:
            dict: {
                "success": bool,
                "tables": list,
                "key_value_pairs": dict,
                "layout": list
            }
        """
        # Advanced: Use PaddleOCR layout analysis
        # This is a placeholder for future enhancement
        result = self.extract_text(file_path, preprocess=True)

        if not result["success"]:
            return {
                "success": False,
                "tables": [],
                "key_value_pairs": {},
                "layout": []
            }

        # Simple key-value extraction from text
        key_value_pairs = self._extract_key_value_pairs(result["text"])

        return {
            "success": True,
            "tables": [],  # Future: implement table detection
            "key_value_pairs": key_value_pairs,
            "layout": result["structured_data"]
        }

    def _extract_key_value_pairs(self, text):
        """
        Extract key-value pairs from text
        Looks for patterns like "Key: Value" or "Key = Value"
        """
        key_value_pairs = {}
        lines = text.split("\n")

        for line in lines:
            # Pattern: "Key: Value" or "Key = Value"
            if ':' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    if key and value:
                        key_value_pairs[key] = value
            elif '=' in line:
                parts = line.split('=', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    if key and value:
                        key_value_pairs[key] = value

        return key_value_pairs

    def clear_cache(self):
        """Clear OCR cache directory"""
        count = 0
        for file in self.cache_dir.glob("*"):
            if file.is_file():
                file.unlink()
                count += 1
        return count

    def get_cache_size(self):
        """Get cache directory size in MB"""
        total_size = sum(f.stat().st_size for f in self.cache_dir.glob("*") if f.is_file())
        return total_size / (1024 * 1024)

    def get_cache_stats(self):
        """Get detailed cache statistics"""
        files = list(self.cache_dir.glob("*"))
        file_count = len([f for f in files if f.is_file()])
        total_size = sum(f.stat().st_size for f in files if f.is_file())

        return {
            "file_count": file_count,
            "total_size_mb": total_size / (1024 * 1024),
            "cache_dir": str(self.cache_dir)
        }


# Convenience functions
def extract_text(file_path):
    """Quick text extraction"""
    processor = OCRProcessor()
    return processor.extract_text(file_path)


def extract_from_image(image_path):
    """Image-specific extraction"""
    processor = OCRProcessor()
    return processor.extract_text(image_path, preprocess=True)


def extract_from_pdf(pdf_path):
    """PDF-specific extraction"""
    processor = OCRProcessor()
    return processor.extract_text(pdf_path, preprocess=True)


# CLI Testing interface
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python ocr_processor.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    print(f"[+] Extracting text from: {file_path}")
    result = extract_text(file_path)

    if result["success"]:
        print(f"[+] Success! Confidence: {result['confidence']:.2%}")
        print(f"[+] Pages: {result['metadata']['pages']}")
        print(f"[+] Total characters: {result['metadata']['total_chars']}")
        print("\n--- Extracted Text ---")
        print(result["text"])
    else:
        print(f"[!] Error: {result.get('error', 'Unknown error')}")
