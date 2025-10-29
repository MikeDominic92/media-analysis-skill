#!/usr/bin/env python3
"""
Media Analysis Orchestrator
Routes files to appropriate analyzer (Gemini, OCR, or both)
"""

import os
import sys
from pathlib import Path


def analyze_file(file_path):
    """
    Main entry point for file analysis
    Routes to Gemini, OCR, or both based on file type
    """
    file_path = Path(file_path)
    ext = file_path.suffix.lower()

    print(f"[*] Analyzing: {file_path.name}")
    print(f"[*] File type: {ext}")

    if ext in ['.pdf', '.png', '.jpg', '.jpeg', '.bmp', '.tiff']:
        # Route to Gemini first, fallback to OCR if needed
        print(f"[*] Document/Image file detected")
        print(f"[*] Will use: Gemini AI (primary) + PaddleOCR (fallback)")
        print(f"[!] Gemini analyzer not yet implemented (Agent 2)")
        print(f"[!] OCR processor not yet implemented (Agent 3)")
        return {
            "status": "pending",
            "message": "Awaiting Agent 2 (Gemini) and Agent 3 (OCR) implementation",
            "file_type": "document/image",
            "analyzers": ["gemini", "ocr"]
        }

    elif ext in ['.mp3', '.wav', '.mp4', '.mov', '.avi', '.m4a']:
        # Audio/video: Gemini only
        print(f"[*] Audio/Video file detected")
        print(f"[*] Will use: Gemini AI (audio/video analysis)")
        print(f"[!] Gemini analyzer not yet implemented (Agent 2)")
        return {
            "status": "pending",
            "message": "Awaiting Agent 2 (Gemini) implementation",
            "file_type": "audio/video",
            "analyzers": ["gemini"]
        }

    else:
        return {
            "status": "error",
            "message": f"Unsupported file type: {ext}",
            "supported_types": [
                "Documents: .pdf",
                "Images: .png, .jpg, .jpeg, .bmp, .tiff",
                "Audio: .mp3, .wav, .m4a",
                "Video: .mp4, .mov, .avi"
            ]
        }


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python main.py <file_path>")
        print("\nSupported file types:")
        print("  Documents: PDF")
        print("  Images: PNG, JPG, JPEG, BMP, TIFF")
        print("  Audio: MP3, WAV, M4A")
        print("  Video: MP4, MOV, AVI")
        sys.exit(1)

    file_path = sys.argv[1]

    if not Path(file_path).exists():
        print(f"[!] Error: File not found: {file_path}")
        sys.exit(1)

    result = analyze_file(file_path)

    print(f"\n[*] Analysis result:")
    print(f"    Status: {result.get('status')}")
    print(f"    Message: {result.get('message')}")

    if result.get('status') == 'error':
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
