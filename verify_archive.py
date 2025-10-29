"""
Archive Verification Script
Verifies completeness of resolution archive including Phase 0 artifacts

Part of BMAD-EDI v4.0 Documentation Specialist workflow
"""

import os
import json
from pathlib import Path
from datetime import datetime


class ArchiveVerifier:
    """Verify resolution archive completeness"""

    def __init__(self, webedi_id, company_name):
        self.webedi_id = webedi_id
        self.company_name = company_name
        self.tickets_dir = Path.home() / "Documents" / "tickets"
        self.resolution_dir = self.tickets_dir / "resolution"
        self.folder_name = f"{webedi_id}_{company_name.replace(' ', '_')}"
        self.archive_path = self.resolution_dir / self.folder_name

    def verify(self):
        """
        Verify archive completeness

        Returns:
            dict: Verification results with issues and recommendations
        """
        print(f"\n[*] Verifying archive: {self.archive_path}")
        print()

        results = {
            "archive_exists": False,
            "structure_valid": False,
            "phase0_complete": False,
            "investigation_complete": False,
            "customer_response_complete": False,
            "summary_complete": False,
            "issues": [],
            "warnings": [],
            "recommendations": []
        }

        # Check if archive folder exists
        if not self.archive_path.exists():
            results["issues"].append(f"Archive folder does not exist: {self.archive_path}")
            print(f"[X] Archive folder not found")
            return results

        results["archive_exists"] = True
        print(f"[+] Archive folder exists")

        # Verify folder structure
        structure_checks = self._verify_structure()
        results["structure_valid"] = structure_checks["valid"]
        results["issues"].extend(structure_checks["issues"])
        results["warnings"].extend(structure_checks["warnings"])

        # Verify Phase 0 artifacts
        phase0_checks = self._verify_phase0()
        results["phase0_complete"] = phase0_checks["complete"]
        results["issues"].extend(phase0_checks["issues"])
        results["warnings"].extend(phase0_checks["warnings"])

        # Verify investigation artifacts
        investigation_checks = self._verify_investigation()
        results["investigation_complete"] = investigation_checks["complete"]
        results["issues"].extend(investigation_checks["issues"])
        results["warnings"].extend(investigation_checks["warnings"])

        # Verify customer response
        response_checks = self._verify_customer_response()
        results["customer_response_complete"] = response_checks["complete"]
        results["issues"].extend(response_checks["issues"])
        results["warnings"].extend(response_checks["warnings"])

        # Verify summary files
        summary_checks = self._verify_summary()
        results["summary_complete"] = summary_checks["complete"]
        results["issues"].extend(summary_checks["issues"])
        results["warnings"].extend(summary_checks["warnings"])

        # Generate recommendations
        results["recommendations"] = self._generate_recommendations(results)

        # Print summary
        self._print_summary(results)

        return results

    def _verify_structure(self):
        """Verify folder structure"""
        print("\n[*] Checking folder structure...")

        expected_dirs = [
            "ticket_original",
            "analysis",
            "customer_response",
            "verification"
        ]

        issues = []
        warnings = []
        valid = True

        for dir_name in expected_dirs:
            dir_path = self.archive_path / dir_name
            if not dir_path.exists():
                issues.append(f"Missing directory: {dir_name}/")
                print(f"    [X] {dir_name}/ - MISSING")
                valid = False
            else:
                print(f"    [+] {dir_name}/ - OK")

        return {
            "valid": valid,
            "issues": issues,
            "warnings": warnings
        }

    def _verify_phase0(self):
        """Verify Phase 0 artifacts"""
        print("\n[*] Checking Phase 0 artifacts...")

        required_files = {
            "metadata.json": "ticket_original/metadata.json",
            "preliminary_analysis.md": "analysis/preliminary_analysis.md"
        }

        issues = []
        warnings = []
        complete = True

        for file_type, file_path in required_files.items():
            full_path = self.archive_path / file_path
            if not full_path.exists():
                issues.append(f"Missing Phase 0 file: {file_path}")
                print(f"    [X] {file_type} - MISSING")
                complete = False
            else:
                # Validate file content
                if file_type == "metadata.json":
                    validation = self._validate_metadata(full_path)
                    if not validation["valid"]:
                        warnings.extend(validation["warnings"])
                        print(f"    [!] {file_type} - OK (with warnings)")
                    else:
                        print(f"    [+] {file_type} - OK")
                else:
                    print(f"    [+] {file_type} - OK")

        # Check for original ticket file
        original_files = list((self.archive_path / "ticket_original").glob("*"))
        original_files = [f for f in original_files if f.suffix in ['.pdf', '.png', '.jpg', '.jpeg', '.mp3', '.mp4', '.wav', '.mov']]

        if not original_files:
            warnings.append("No original ticket file found (expected PDF, image, audio, or video)")
            print(f"    [!] Original ticket file - MISSING (not critical)")
        else:
            print(f"    [+] Original ticket file - OK ({original_files[0].name})")

        return {
            "complete": complete,
            "issues": issues,
            "warnings": warnings
        }

    def _validate_metadata(self, metadata_path):
        """Validate metadata.json content"""
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            required_fields = [
                "ticket_id",
                "extraction_method",
                "confidence",
                "timestamp"
            ]

            warnings = []
            valid = True

            for field in required_fields:
                if field not in metadata:
                    warnings.append(f"metadata.json missing field: {field}")
                    valid = False

            # Check confidence score
            if "confidence" in metadata:
                confidence = metadata["confidence"]
                if confidence < 0.7:
                    warnings.append(f"Low confidence score: {confidence:.2f} (expected >= 0.7)")

            return {
                "valid": valid,
                "warnings": warnings
            }

        except json.JSONDecodeError:
            return {
                "valid": False,
                "warnings": ["metadata.json is not valid JSON"]
            }
        except Exception as e:
            return {
                "valid": False,
                "warnings": [f"Error reading metadata.json: {str(e)}"]
            }

    def _verify_investigation(self):
        """Verify investigation artifacts"""
        print("\n[*] Checking investigation artifacts...")

        expected_files = [
            "analysis/investigation_report.md"
        ]

        issues = []
        warnings = []
        complete = True

        for file_path in expected_files:
            full_path = self.archive_path / file_path
            if not full_path.exists():
                warnings.append(f"Missing investigation file: {file_path}")
                print(f"    [!] {file_path} - MISSING (may not be created yet)")
            else:
                print(f"    [+] {file_path} - OK")

        return {
            "complete": complete,
            "issues": issues,
            "warnings": warnings
        }

    def _verify_customer_response(self):
        """Verify customer response"""
        print("\n[*] Checking customer response...")

        expected_files = [
            "customer_response/response_final.md"
        ]

        issues = []
        warnings = []
        complete = True

        for file_path in expected_files:
            full_path = self.archive_path / file_path
            if not full_path.exists():
                warnings.append(f"Missing customer response: {file_path}")
                print(f"    [!] {file_path} - MISSING (may not be created yet)")
            else:
                print(f"    [+] {file_path} - OK")

        return {
            "complete": complete,
            "issues": issues,
            "warnings": warnings
        }

    def _verify_summary(self):
        """Verify summary files"""
        print("\n[*] Checking summary files...")

        expected_files = {
            "resolution_summary.md": "Resolution summary",
            "phase0_metrics.json": "Phase 0 metrics"
        }

        issues = []
        warnings = []
        complete = True

        for file_name, file_desc in expected_files.items():
            full_path = self.archive_path / file_name
            if not full_path.exists():
                issues.append(f"Missing summary file: {file_name}")
                print(f"    [X] {file_desc} - MISSING")
                complete = False
            else:
                print(f"    [+] {file_desc} - OK")

        return {
            "complete": complete,
            "issues": issues,
            "warnings": warnings
        }

    def _generate_recommendations(self, results):
        """Generate recommendations based on verification results"""
        recommendations = []

        if not results["archive_exists"]:
            recommendations.append("Run archival.py to create archive structure")

        if not results["structure_valid"]:
            recommendations.append("Re-run archival.py to create missing directories")

        if not results["phase0_complete"]:
            recommendations.append("Check if Phase 0 analysis was completed for this ticket")
            recommendations.append("Verify processing/[ticket-id]/ folder contains Phase 0 artifacts")

        if not results["investigation_complete"]:
            recommendations.append("Investigation report may not be saved yet (expected during Phase 5)")

        if not results["customer_response_complete"]:
            recommendations.append("Customer response may not be saved yet (expected during Phase 6)")

        if not results["summary_complete"]:
            recommendations.append("Re-run archival.py to generate missing summary files")

        if results["warnings"]:
            recommendations.append("Review warnings and update affected files if needed")

        return recommendations

    def _print_summary(self, results):
        """Print verification summary"""
        print("\n" + "=" * 80)
        print("VERIFICATION SUMMARY")
        print("=" * 80)

        # Overall status
        all_critical_ok = (
            results["archive_exists"] and
            results["structure_valid"] and
            results["phase0_complete"] and
            results["summary_complete"]
        )

        if all_critical_ok:
            print("\n[+] Archive verification PASSED")
        else:
            print("\n[X] Archive verification FAILED")

        # Issues
        if results["issues"]:
            print(f"\n[!] Critical Issues ({len(results['issues'])}):")
            for issue in results["issues"]:
                print(f"    - {issue}")

        # Warnings
        if results["warnings"]:
            print(f"\n[!] Warnings ({len(results['warnings'])}):")
            for warning in results["warnings"]:
                print(f"    - {warning}")

        # Recommendations
        if results["recommendations"]:
            print(f"\n[*] Recommendations:")
            for i, rec in enumerate(results["recommendations"], 1):
                print(f"    {i}. {rec}")

        print("\n" + "=" * 80)


def main():
    """CLI interface for archive verification"""
    import sys

    if len(sys.argv) < 3:
        print("Usage: python verify-archive.py <webedi_id> <company_name>")
        print("\nExample:")
        print('  python verify-archive.py WEB-456 "Ace Hardware"')
        print("\nDescription:")
        print("  Verifies completeness of resolution archive including Phase 0 artifacts")
        print("  Checks folder structure, Phase 0 files, investigation files, and summaries")
        sys.exit(1)

    webedi_id = sys.argv[1]
    company_name = sys.argv[2]

    verifier = ArchiveVerifier(webedi_id, company_name)
    results = verifier.verify()

    # Exit with appropriate code
    if results["issues"]:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
