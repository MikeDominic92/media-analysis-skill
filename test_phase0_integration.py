#!/usr/bin/env python3
"""
Phase 0 Integration Test Script
Tests complete Phase 0 → Phase 1 workflow

Agent 6 - BMAD-EDI Workflow Integration Specialist
"""

import asyncio
import json
import shutil
import tempfile
from pathlib import Path
from datetime import datetime
import sys

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from workflow import TicketWorkflow


class Phase0IntegrationTest:
    """Test Phase 0 integration with BMAD-EDI workflow"""

    def __init__(self):
        self.test_dir = Path(tempfile.mkdtemp(prefix="phase0_test_"))
        self.tickets_base = self.test_dir / "tickets"
        self.incoming_dir = self.tickets_base / "incoming"
        self.processing_dir = self.tickets_base / "processing"

        # Create test directories
        self.incoming_dir.mkdir(parents=True, exist_ok=True)
        self.processing_dir.mkdir(parents=True, exist_ok=True)

        print(f"[*] Test directory: {self.test_dir}")

    def create_test_ticket_file(self):
        """Create a test ticket file"""
        test_file = self.incoming_dir / "test_ticket_13620086.txt"
        content = """
        Ticket #13620086
        Customer: Jody Bridge
        Company: Singtech Inc
        Trading Partner: Staples
        Issue: i28 label setup required for Staples partner
        Transaction Type: i28 Label Setup
        Severity: MEDIUM

        Customer needs help configuring i28 label template for Staples.
        This is their first time setting up labels for this partner.
        """
        test_file.write_text(content, encoding='utf-8')
        print(f"[+] Created test file: {test_file}")
        return test_file

    async def test_phase0_execution(self):
        """Test 1: Phase 0 execution"""
        print("\n" + "="*70)
        print("TEST 1: Phase 0 Execution")
        print("="*70)

        test_file = self.create_test_ticket_file()

        # Create workflow instance (use test directory)
        workflow = TicketWorkflow()
        # Override directories for testing
        workflow.tickets_base = self.tickets_base
        workflow.incoming_dir = self.incoming_dir
        workflow.processing_dir = self.processing_dir
        workflow.failed_dir = self.incoming_dir / "failed"
        workflow.failed_dir.mkdir(exist_ok=True)

        # Run Phase 0
        print("\n[*] Running Phase 0 analysis...")
        result = await workflow.process_ticket(test_file)

        # Check results
        if result["success"]:
            print(f"[+] Phase 0 SUCCESS")
            print(f"[+] Ticket folder: {result['ticket_folder']}")
            print(f"[+] Confidence: {result['confidence']:.2f}")
            print(f"[+] Extraction method: {result['extraction_method']}")
            return True, result
        else:
            print(f"[!] Phase 0 FAILED: {result.get('error')}")
            return False, result

    def test_metadata_json_structure(self, ticket_folder):
        """Test 2: Verify metadata.json structure"""
        print("\n" + "="*70)
        print("TEST 2: Metadata JSON Structure")
        print("="*70)

        metadata_file = Path(ticket_folder) / "metadata.json"

        if not metadata_file.exists():
            print(f"[!] FAILED: metadata.json not found")
            return False

        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        # Required fields for Phase 1 consumption
        required_fields = [
            "ticket_id",
            "company",
            "trading_partner",
            "transaction_type",
            "severity",
            "issue_title",
            "confidence",
            "timestamp",
            "original_file",
            "processed_file"
        ]

        missing_fields = []
        for field in required_fields:
            if field not in metadata:
                missing_fields.append(field)

        if missing_fields:
            print(f"[!] FAILED: Missing fields: {missing_fields}")
            return False

        print("[+] All required fields present")
        print(f"[+] Ticket ID: {metadata.get('ticket_id')}")
        print(f"[+] Company: {metadata.get('company')}")
        print(f"[+] Trading Partner: {metadata.get('trading_partner')}")
        print(f"[+] Confidence: {metadata.get('confidence')}")

        return True

    def test_preliminary_analysis_markdown(self, ticket_folder):
        """Test 3: Verify preliminary_analysis.md exists"""
        print("\n" + "="*70)
        print("TEST 3: Preliminary Analysis Markdown")
        print("="*70)

        analysis_file = Path(ticket_folder) / "preliminary_analysis.md"

        if not analysis_file.exists():
            print(f"[!] FAILED: preliminary_analysis.md not found")
            return False

        content = analysis_file.read_text(encoding='utf-8')

        # Check for key sections
        required_sections = [
            "# Preliminary Analysis",
            "## Ticket Overview",
            "## Issue Summary",
            "## Root Cause",
            "## Recommended Actions",
            "## Next Steps"
        ]

        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)

        if missing_sections:
            print(f"[!] FAILED: Missing sections: {missing_sections}")
            return False

        print("[+] All required sections present")
        print(f"[+] File size: {len(content)} characters")

        return True

    def test_standardized_filename(self, ticket_folder):
        """Test 4: Verify standardized filename format"""
        print("\n" + "="*70)
        print("TEST 4: Standardized Filename")
        print("="*70)

        ticket_folder = Path(ticket_folder)
        files = list(ticket_folder.glob("*.txt"))

        if not files:
            print(f"[!] FAILED: No processed file found")
            return False

        processed_file = files[0]
        filename = processed_file.name

        # Expected format: YYYY-MM-DD_TicketID_Company_TradingPartner-Name_Transaction.ext
        print(f"[*] Filename: {filename}")

        # Basic checks
        parts = filename.rsplit('.', 1)[0].split('_')
        if len(parts) < 4:
            print(f"[!] FAILED: Filename format incorrect (expected 4+ parts)")
            return False

        # Check date format (YYYY-MM-DD)
        date_part = parts[0]
        try:
            datetime.strptime(date_part, "%Y-%m-%d")
            print(f"[+] Date format valid: {date_part}")
        except ValueError:
            print(f"[!] FAILED: Invalid date format: {date_part}")
            return False

        # Check ticket ID
        ticket_id = parts[1]
        if not ticket_id.isdigit():
            print(f"[!] WARNING: Ticket ID not numeric: {ticket_id}")

        print(f"[+] Ticket ID: {ticket_id}")
        print(f"[+] Company: {parts[2]}")
        print(f"[+] Filename format valid")

        return True

    def test_file_cleanup(self):
        """Test 5: Verify original file removed from incoming/"""
        print("\n" + "="*70)
        print("TEST 5: File Cleanup")
        print("="*70)

        incoming_files = list(self.incoming_dir.glob("*.*"))

        # Should only have failed/ subfolder if it exists, no ticket files
        ticket_files = [f for f in incoming_files if f.is_file()]

        if ticket_files:
            print(f"[!] FAILED: Files still in incoming/: {ticket_files}")
            return False

        print("[+] incoming/ folder cleaned (original file removed)")
        return True

    def test_phase1_consumption(self, ticket_folder):
        """Test 6: Simulate Phase 1 metadata consumption"""
        print("\n" + "="*70)
        print("TEST 6: Phase 1 Metadata Consumption")
        print("="*70)

        metadata_file = Path(ticket_folder) / "metadata.json"

        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            # Simulate Phase 1 Analyst consuming metadata
            print("[*] Phase 1 Analyst loading metadata...")

            # Extract fields Phase 1 needs
            ticket_id = metadata.get("ticket_id", "UNKNOWN")
            company = metadata.get("company", "UNKNOWN")
            customer_name = metadata.get("customer_name", "N/A")
            trading_partner = metadata.get("trading_partner", "UNKNOWN")
            transaction_type = metadata.get("transaction_type", "N/A")
            severity = metadata.get("severity", "NORMAL")
            issue_title = metadata.get("issue_title", "No issue title")
            confidence = metadata.get("confidence", 0.0)

            # Generate Phase 1 output (copy-paste ready format)
            phase1_output = f"""
================================================================================
TICKET: {company} - {issue_title}
================================================================================

[Phase 0 Status: METADATA PRE-EXTRACTED]
[Confidence: {confidence:.2f}]

Extraction Phase:

• Customer Name: {customer_name}
• Company Name: {company}
• Trading Partner: {trading_partner}
• Document Types: {transaction_type}
• Error/Issue: {issue_title}
• Priority: {severity}

Ticket ID: {ticket_id}
"""

            print(phase1_output)
            print("[+] Phase 1 successfully consumed Phase 0 metadata")
            return True

        except Exception as e:
            print(f"[!] FAILED: {str(e)}")
            return False

    def cleanup(self):
        """Clean up test directory"""
        print("\n" + "="*70)
        print("CLEANUP")
        print("="*70)

        try:
            shutil.rmtree(self.test_dir)
            print(f"[+] Test directory removed: {self.test_dir}")
        except Exception as e:
            print(f"[!] Cleanup failed: {str(e)}")

    async def run_all_tests(self):
        """Run all integration tests"""
        print("\n")
        print("="*70)
        print("PHASE 0 INTEGRATION TEST SUITE")
        print("="*70)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        results = {}

        # Test 1: Phase 0 execution
        success, result = await self.test_phase0_execution()
        results["phase0_execution"] = success

        if not success:
            print("\n[!] Phase 0 execution failed - cannot continue tests")
            self.cleanup()
            return results

        ticket_folder = result.get("ticket_folder")

        # Test 2: Metadata JSON structure
        results["metadata_json"] = self.test_metadata_json_structure(ticket_folder)

        # Test 3: Preliminary analysis markdown
        results["analysis_markdown"] = self.test_preliminary_analysis_markdown(ticket_folder)

        # Test 4: Standardized filename
        results["standardized_filename"] = self.test_standardized_filename(ticket_folder)

        # Test 5: File cleanup
        results["file_cleanup"] = self.test_file_cleanup()

        # Test 6: Phase 1 consumption
        results["phase1_consumption"] = self.test_phase1_consumption(ticket_folder)

        # Summary
        print("\n" + "="*70)
        print("TEST RESULTS SUMMARY")
        print("="*70)

        total_tests = len(results)
        passed_tests = sum(1 for v in results.values() if v)
        failed_tests = total_tests - passed_tests

        for test_name, passed in results.items():
            status = "[+] PASS" if passed else "[!] FAIL"
            print(f"{status} - {test_name}")

        print()
        print(f"Total: {total_tests} tests")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print()

        if failed_tests == 0:
            print("[+] ALL TESTS PASSED")
            print("[+] Phase 0 integration verified successfully")
        else:
            print(f"[!] {failed_tests} TEST(S) FAILED")
            print("[!] Review failures above")

        print()
        print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)

        # Cleanup
        self.cleanup()

        return results


async def main():
    """Main entry point"""
    print("\n[*] Initializing Phase 0 Integration Test Suite...")
    print("[*] This will test the complete Phase 0 → Phase 1 workflow")
    print()

    test_suite = Phase0IntegrationTest()
    results = await test_suite.run_all_tests()

    # Exit code based on results
    if all(results.values()):
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure


if __name__ == "__main__":
    asyncio.run(main())
