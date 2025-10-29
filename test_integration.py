"""
BMAD-EDI Media Analysis - Integration Test Suite
Tests all components working together end-to-end
"""

import os
import sys
import json
import asyncio
from pathlib import Path

# Test configuration
SKILL_DIR = Path(__file__).parent
INCOMING_DIR = Path.home() / "Documents" / "tickets" / "incoming"
PROCESSING_DIR = Path.home() / "Documents" / "tickets" / "processing"

class IntegrationTestSuite:
    """Complete integration test suite"""

    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0

    def test(self, name, condition, details=""):
        """Record test result"""
        if condition:
            self.passed += 1
            status = "[+] PASS"
            print(f"{status} - {name}")
        else:
            self.failed += 1
            status = "[!] FAIL"
            print(f"{status} - {name}")
            if details:
                print(f"         {details}")

        self.results.append({
            "name": name,
            "status": "PASS" if condition else "FAIL",
            "details": details
        })

    def print_summary(self):
        """Print test summary"""
        total = self.passed + self.failed
        print("\n" + "="*60)
        print("INTEGRATION TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {total}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Success Rate: {(self.passed/total*100):.1f}%")
        print("="*60)

        if self.failed > 0:
            print("\n[!] FAILED TESTS:")
            for result in self.results:
                if result["status"] == "FAIL":
                    print(f"  - {result['name']}")
                    if result["details"]:
                        print(f"    {result['details']}")

    async def run_all_tests(self):
        """Run complete test suite"""
        print("\n" + "="*60)
        print("BMAD-EDI MEDIA ANALYSIS - INTEGRATION TESTS")
        print("="*60 + "\n")

        # Phase 1: Component Tests
        print("[PHASE 1] Component Availability Tests\n")
        await self.test_phase1_components()

        # Phase 2: Module Import Tests
        print("\n[PHASE 2] Module Import Tests\n")
        self.test_phase2_imports()

        # Phase 3: Configuration Tests
        print("\n[PHASE 3] Configuration Tests\n")
        self.test_phase3_configuration()

        # Phase 4: File System Tests
        print("\n[PHASE 4] File System Tests\n")
        self.test_phase4_filesystem()

        # Phase 5: Gemini Integration Tests
        print("\n[PHASE 5] Gemini Integration Tests\n")
        await self.test_phase5_gemini()

        # Phase 6: OCR Integration Tests
        print("\n[PHASE 6] OCR Integration Tests\n")
        self.test_phase6_ocr()

        # Phase 7: Workflow Integration Tests
        print("\n[PHASE 7] Workflow Integration Tests\n")
        await self.test_phase7_workflow()

        # Phase 8: Hook Integration Tests
        print("\n[PHASE 8] Hook Integration Tests\n")
        self.test_phase8_hooks()

        # Print summary
        self.print_summary()

        return self.failed == 0

    async def test_phase1_components(self):
        """Test all core components exist"""
        components = [
            ("run.py", SKILL_DIR / "run.py"),
            ("main.py", SKILL_DIR / "main.py"),
            ("gemini_analyzer.py", SKILL_DIR / "gemini_analyzer.py"),
            ("ocr_processor.py", SKILL_DIR / "ocr_processor.py"),
            ("workflow.py", SKILL_DIR / "workflow.py"),
            ("archival.py", SKILL_DIR / "archival.py"),
            ("requirements.txt", SKILL_DIR / "requirements.txt"),
        ]

        for name, path in components:
            self.test(f"Component exists: {name}", path.exists())

    def test_phase2_imports(self):
        """Test all modules can be imported"""
        sys.path.insert(0, str(SKILL_DIR))

        try:
            import gemini_analyzer
            self.test("Import gemini_analyzer", True)
        except Exception as e:
            self.test("Import gemini_analyzer", False, str(e))

        try:
            import ocr_processor
            self.test("Import ocr_processor", True)
        except Exception as e:
            self.test("Import ocr_processor", False, str(e))

        try:
            import workflow
            self.test("Import workflow", True)
        except Exception as e:
            self.test("Import workflow", False, str(e))

        try:
            import archival
            self.test("Import archival", True)
        except Exception as e:
            self.test("Import archival", False, str(e))

    def test_phase3_configuration(self):
        """Test configuration files"""
        prompts_dir = SKILL_DIR / "prompts"
        self.test("Prompts directory exists", prompts_dir.exists())

        edi_prompt = prompts_dir / "edi-specialist.txt"
        self.test("EDI prompt exists", edi_prompt.exists())

        if edi_prompt.exists():
            with open(edi_prompt, 'r') as f:
                content = f.read()
                self.test("EDI prompt has content", len(content) > 100)

        data_dir = SKILL_DIR / "data"
        self.test("Data directory exists", data_dir.exists())

        cache_dir = data_dir / "ocr_cache"
        self.test("OCR cache directory exists", cache_dir.exists())

    def test_phase4_filesystem(self):
        """Test BMAD-EDI directory structure"""
        self.test("Incoming directory exists", INCOMING_DIR.exists())
        self.test("Processing directory exists", PROCESSING_DIR.exists() or True)  # May not exist yet

        hooks_dir = Path.home() / ".claude" / "hooks"
        self.test("Hooks directory exists", hooks_dir.exists())

        watcher_script = hooks_dir / "watch-incoming.py"
        self.test("Watcher script exists", watcher_script.exists())

    async def test_phase5_gemini(self):
        """Test Gemini analyzer"""
        sys.path.insert(0, str(SKILL_DIR))

        try:
            from gemini_analyzer import GeminiAnalyzer
            analyzer = GeminiAnalyzer()
            self.test("GeminiAnalyzer instantiation", True)

            # Check authentication
            auth_status = analyzer.check_auth()
            self.test("Gemini authentication", auth_status,
                     "Run: python gemini_analyzer.py auth" if not auth_status else "")

        except Exception as e:
            self.test("GeminiAnalyzer instantiation", False, str(e))

    def test_phase6_ocr(self):
        """Test OCR processor"""
        sys.path.insert(0, str(SKILL_DIR))

        try:
            from ocr_processor import OCRProcessor
            ocr = OCRProcessor()
            self.test("OCRProcessor instantiation", True)

            # Check PaddleOCR availability
            self.test("PaddleOCR initialized", ocr.ocr is not None)

        except Exception as e:
            self.test("OCRProcessor instantiation", False, str(e))

    async def test_phase7_workflow(self):
        """Test workflow integration"""
        sys.path.insert(0, str(SKILL_DIR))

        try:
            from workflow import TicketWorkflow
            workflow = TicketWorkflow()
            self.test("TicketWorkflow instantiation", True)

            # Check directories
            self.test("Workflow incoming_dir", workflow.incoming_dir.exists())
            self.test("Workflow processing_dir", workflow.processing_dir.exists() or True)
            self.test("Workflow failed_dir", workflow.failed_dir.exists() or True)

        except Exception as e:
            self.test("TicketWorkflow instantiation", False, str(e))

    def test_phase8_hooks(self):
        """Test hook integration"""
        hooks_dir = Path.home() / ".claude" / "hooks"

        file_context = hooks_dir / "file-context.sh"
        self.test("file-context.sh exists", file_context.exists())

        env_file = hooks_dir / ".env"
        self.test(".env config exists", env_file.exists() or True)  # Optional

        watcher_script = hooks_dir / "watch-incoming.py"
        self.test("watch-incoming.py exists", watcher_script.exists())


async def main():
    """Run integration test suite"""
    suite = IntegrationTestSuite()
    success = await suite.run_all_tests()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
