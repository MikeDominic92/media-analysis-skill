#!/usr/bin/env python3
"""
Test Phase 0 - BMAD-EDI Workflow Integration
Agent 6 - Verification Script

Tests Phase 0 pre-investigation analysis workflow
"""

import asyncio
import json
from pathlib import Path
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from workflow import TicketWorkflow


async def test_phase0():
    """Test Phase 0 workflow with sample file"""
    print("=" * 80)
    print("PHASE 0 TEST - BMAD-EDI Workflow Integration")
    print("=" * 80)

    # Check if test file exists in incoming
    tickets_dir = Path(r"C:\Users\sleep\Documents\tickets")
    incoming_dir = tickets_dir / "incoming"

    print(f"\n[*] Checking incoming directory: {incoming_dir}")

    if not incoming_dir.exists():
        print(f"[!] Incoming directory does not exist: {incoming_dir}")
        print(f"[*] Creating directory...")
        incoming_dir.mkdir(parents=True, exist_ok=True)

    # Look for any PDF files in incoming
    pdf_files = list(incoming_dir.glob("*.pdf"))

    if not pdf_files:
        print(f"\n[!] No PDF files found in incoming directory")
        print(f"[*] Please place a ticket PDF file in: {incoming_dir}")
        print(f"\nUsage:")
        print(f"  1. Copy a ticket PDF to: {incoming_dir}")
        print(f"  2. Run: python test_phase0.py")
        print(f"  OR")
        print(f"  python test_phase0.py <path-to-ticket-pdf>")
        return False

    # Use first PDF file found
    test_file = pdf_files[0]
    print(f"[+] Found test file: {test_file.name}")

    # Initialize workflow
    print(f"\n[*] Initializing Phase 0 workflow...")
    workflow = TicketWorkflow()

    # Process ticket
    print(f"\n[PHASE 0] Processing ticket file...")
    print("-" * 80)

    result = await workflow.process_ticket(test_file)

    print("-" * 80)

    # Check results
    if result["success"]:
        print(f"\n[SUCCESS] Phase 0 Complete!")
        print(f"\nResults:")
        print(f"  Ticket Folder: {result['ticket_folder']}")
        print(f"  Confidence: {result['confidence']:.2%}")
        print(f"  Extraction Method: {result['extraction_method'].upper()}")

        # Verify artifacts
        print(f"\n[*] Verifying artifacts...")
        ticket_folder = Path(result['ticket_folder'])

        # Check metadata.json
        metadata_file = ticket_folder / "metadata.json"
        if metadata_file.exists():
            print(f"  [+] metadata.json exists")
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            print(f"      - Ticket ID: {metadata.get('ticket_id', 'N/A')}")
            print(f"      - Company: {metadata.get('company', 'N/A')}")
            print(f"      - Trading Partner: {metadata.get('trading_partner', 'N/A')}")
            print(f"      - Transaction: {metadata.get('transaction_type', 'N/A')}")
            print(f"      - Severity: {metadata.get('severity', 'N/A')}")
        else:
            print(f"  [X] metadata.json missing")

        # Check preliminary_analysis.md
        analysis_file = ticket_folder / "preliminary_analysis.md"
        if analysis_file.exists():
            print(f"  [+] preliminary_analysis.md exists")
            with open(analysis_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"      - Size: {len(content)} bytes")
        else:
            print(f"  [X] preliminary_analysis.md missing")

        # Check processed file
        processed_file = ticket_folder / metadata.get('processed_file', '')
        if processed_file.exists():
            print(f"  [+] Processed file exists: {processed_file.name}")
        else:
            print(f"  [X] Processed file missing")

        # Success criteria check
        print(f"\n[*] Success Criteria Check:")
        checks = [
            ("Metadata extraction confidence > 0.85", result['confidence'] > 0.85),
            ("metadata.json created", metadata_file.exists()),
            ("preliminary_analysis.md created", analysis_file.exists()),
            ("File moved to processing", processed_file.exists()),
            ("Original file removed from incoming", not test_file.exists())
        ]

        passed = 0
        for criterion, status in checks:
            status_str = "[+]" if status else "[X]"
            print(f"  {status_str} {criterion}")
            if status:
                passed += 1

        print(f"\n[*] Passed: {passed}/{len(checks)} checks")

        if passed == len(checks):
            print(f"\n[SUCCESS] All success criteria met!")
            print(f"\n[READY FOR ANALYST]")
            print(f"  Analyst can now review: {ticket_folder}")
            return True
        else:
            print(f"\n[WARNING] Some success criteria not met")
            return False

    else:
        print(f"\n[FAILED] Phase 0 Failed")
        print(f"Error: {result['error']}")
        if result.get('failed_path'):
            print(f"Failed file location: {result['failed_path']}")
        return False


async def test_with_custom_file(file_path):
    """Test with a specific file"""
    file_path = Path(file_path)

    if not file_path.exists():
        print(f"[!] File not found: {file_path}")
        return False

    print(f"[*] Testing with file: {file_path.name}")

    workflow = TicketWorkflow()
    result = await workflow.process_ticket(file_path)

    if result["success"]:
        print(f"\n[SUCCESS] Phase 0 Complete!")
        print(f"Ticket Folder: {result['ticket_folder']}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"Extraction Method: {result['extraction_method'].upper()}")
        return True
    else:
        print(f"\n[FAILED] Phase 0 Failed")
        print(f"Error: {result['error']}")
        return False


async def main():
    """Main test entry point"""
    if len(sys.argv) > 1:
        # Test with custom file
        file_path = sys.argv[1]
        success = await test_with_custom_file(file_path)
    else:
        # Test with file from incoming directory
        success = await test_phase0()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
