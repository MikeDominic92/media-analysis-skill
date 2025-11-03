#!/usr/bin/env python3
"""
Media Analysis Orchestrator
Routes files to appropriate analyzer (Gemini, OCR, or both)

ROUTING LOGIC:
- Documents/Images (PDF, PNG, JPG, etc.): PaddleOCR PRIMARY
- Audio/Video (MP3, MP4, WAV, etc.): Gemini 2.5 Pro ONLY

Integration Complete: Phase 0 BMAD-EDI Workflow
"""

import asyncio
import os
import sys
from pathlib import Path

# Import the complete workflow implementation
from workflow import TicketWorkflow


def analyze_file(file_path):
    """
    Main entry point for file analysis
    Routes to Gemini, OCR, or both based on file type

    This is a synchronous wrapper around the async workflow
    """
    file_path = Path(file_path)
    ext = file_path.suffix.lower()

    print(f"[*] Analyzing: {file_path.name}")
    print(f"[*] File type: {ext}")

    # Determine routing
    if ext in ['.pdf', '.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif']:
        print(f"[*] Document/Image file detected")
        print(f"[*] Routing to: PaddleOCR (PRIMARY)")
        analyzer_type = "document"
    elif ext in ['.mp3', '.wav', '.m4a', '.mp4', '.mov', '.avi', '.webm']:
        print(f"[*] Audio/Video file detected")
        print(f"[*] Routing to: Gemini 2.5 Pro (ONLY)")
        analyzer_type = "audio_video"
    else:
        print(f"[!] Unsupported file type: {ext}")
        return {
            "status": "error",
            "message": f"Unsupported file type: {ext}",
            "supported_types": {
                "documents": [".pdf", ".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif"],
                "audio_video": [".mp3", ".wav", ".m4a", ".mp4", ".mov", ".avi", ".webm"]
            }
        }

    # Execute workflow (async)
    try:
        workflow = TicketWorkflow()
        result = asyncio.run(workflow.process_ticket(file_path))

        if result.get("success"):
            return {
                "status": "success",
                "message": f"Phase 0 analysis complete",
                "ticket_id": result.get("ticket_id", "UNKNOWN"),
                "ticket_folder": result.get("ticket_folder"),
                "metadata_file": result.get("metadata_file"),
                "analysis_file": result.get("analysis_file"),
                "confidence": result.get("confidence", 0.0),
                "extraction_method": result.get("extraction_method"),
                "file_type": analyzer_type
            }
        else:
            return {
                "status": "error",
                "message": result.get("error", "Unknown error"),
                "file_type": analyzer_type
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Processing failed: {str(e)}",
            "file_type": analyzer_type
        }


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python main.py <file_path>")
        print("\nSupported file types:")
        print("  Documents (PaddleOCR): PDF, PNG, JPG, JPEG, BMP, TIFF, GIF")
        print("  Audio/Video (Gemini): MP3, WAV, M4A, MP4, MOV, AVI, WEBM")
        print("\nExample:")
        print("  python main.py C:/Users/sleep/Documents/tickets/incoming/ticket.pdf")
        sys.exit(1)

    file_path = sys.argv[1]

    if not Path(file_path).exists():
        print(f"[!] Error: File not found: {file_path}")
        sys.exit(1)

    result = analyze_file(file_path)

    print(f"\n{'='*60}")
    print(f"[*] ANALYSIS RESULT")
    print(f"{'='*60}")
    print(f"Status: {result.get('status').upper()}")

    if result.get('status') == 'success':
        print(f"Ticket ID: {result.get('ticket_id')}")
        print(f"Confidence: {result.get('confidence', 0.0):.2f}")
        print(f"Extraction Method: {result.get('extraction_method', 'unknown').upper()}")
        print(f"Ticket Folder: {result.get('ticket_folder')}")
        print(f"\nGenerated Files:")
        print(f"  - Metadata: {result.get('metadata_file')}")
        print(f"  - Analysis: {result.get('analysis_file')}")
        print(f"\n[SUCCESS] Phase 0 Pre-Investigation Analysis Complete")
        sys.exit(0)
    else:
        print(f"Error: {result.get('message')}")
        if result.get('supported_types'):
            print(f"\nSupported types:")
            for category, types in result['supported_types'].items():
                print(f"  {category}: {', '.join(types)}")
        print(f"\n[FAILED] Analysis Failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
