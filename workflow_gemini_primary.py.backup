#!/usr/bin/env python3
"""
BMAD-EDI Workflow Integration - Phase 0 Implementation
Handles Phase 0 pre-investigation analysis

Agent 6 - BMAD-EDI Workflow Integration Specialist
Complete implementation of automated metadata extraction
"""

import asyncio
import json
import shutil
from pathlib import Path
from datetime import datetime
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gemini_analyzer import GeminiAnalyzer, extract_ticket_metadata
from ocr_processor import OCRProcessor


class TicketWorkflow:
    """BMAD-EDI ticket processing workflow - Phase 0 Pre-Investigation Analysis"""

    def __init__(self):
        # Working directory: C:\Users\sleep\Documents\tickets\
        self.tickets_base = Path(r"C:\Users\sleep\Documents\tickets")
        self.incoming_dir = self.tickets_base / "incoming"
        self.processing_dir = self.tickets_base / "processing"
        self.failed_dir = self.incoming_dir / "failed"

        # Create directories if needed
        self.incoming_dir.mkdir(exist_ok=True, parents=True)
        self.processing_dir.mkdir(exist_ok=True, parents=True)
        self.failed_dir.mkdir(exist_ok=True, parents=True)

        self.log_file = self.tickets_base / "media-analysis.log"

    def _log(self, message, level="INFO"):
        """Log message to file and console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)

        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + "\n")
        except:
            pass  # Don't fail if logging fails

    async def process_ticket(self, file_path):
        """
        Phase 0: Pre-Investigation Analysis

        Args:
            file_path: Path to ticket file in incoming/

        Returns:
            dict: Processing results with metadata
        """
        file_path = Path(file_path)
        self._log(f"[PHASE 0] Processing: {file_path.name}")

        if not file_path.exists():
            error_msg = f"File not found: {file_path}"
            self._log(error_msg, "ERROR")
            return {
                "success": False,
                "error": error_msg
            }

        try:
            # Step 1: Extract metadata with Gemini
            self._log("[*] Extracting metadata with Gemini 2.5 Pro...")
            metadata = await extract_ticket_metadata(str(file_path))

            # Check if extraction was successful
            if not isinstance(metadata, dict):
                raise Exception(f"Invalid metadata format: {type(metadata)}")

            # Step 2: Check confidence
            confidence = metadata.get("confidence", metadata.get("analysis_confidence", 0.0))
            self._log(f"[*] Extraction confidence: {confidence:.2f}")

            # Step 3: Fallback to OCR if low confidence
            extraction_method = "gemini"
            if confidence < 0.70:
                self._log("[*] Low confidence - trying OCR fallback...")
                try:
                    ocr = OCRProcessor()
                    ocr_result = ocr.extract_text(str(file_path))

                    if ocr_result.get("success"):
                        # Merge OCR text into metadata
                        metadata["ocr_text"] = ocr_result.get("text", "")
                        metadata["ocr_confidence"] = ocr_result.get("confidence", 0.0)
                        extraction_method = "hybrid"

                        # Re-calculate confidence as average
                        gemini_conf = confidence
                        ocr_conf = ocr_result.get("confidence", 0.0)
                        confidence = (gemini_conf + ocr_conf) / 2.0
                        metadata["confidence"] = confidence
                        self._log(f"[*] Hybrid confidence: {confidence:.2f}")
                except Exception as e:
                    self._log(f"[!] OCR fallback failed: {str(e)}", "WARNING")

            metadata["extraction_method"] = extraction_method

            # Step 4: Generate standardized filename
            new_filename = self._generate_filename(metadata, file_path.suffix)
            self._log(f"[*] Generated filename: {new_filename}")

            # Step 5: Create processing folder
            # Use ticket_id as folder name for simplicity
            ticket_id = metadata.get("ticket_id", "UNKNOWN")
            ticket_folder = self.processing_dir / f"ticket_{ticket_id}"
            ticket_folder.mkdir(exist_ok=True)

            # Step 6: Move/copy file to processing folder
            new_file_path = ticket_folder / new_filename
            try:
                shutil.copy2(file_path, new_file_path)
                self._log(f"[+] File copied to: {new_file_path}")
            except Exception as e:
                self._log(f"[!] File copy failed: {str(e)}", "ERROR")
                raise

            # Step 7: Save metadata JSON
            metadata_file = ticket_folder / "metadata.json"
            metadata_to_save = {
                **metadata,
                "timestamp": datetime.now().isoformat(),
                "original_file": file_path.name,
                "processed_file": new_filename,
                "confidence": confidence
            }

            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata_to_save, f, indent=2, ensure_ascii=False)
            self._log(f"[+] Metadata saved: {metadata_file}")

            # Step 8: Generate preliminary analysis
            analysis_file = ticket_folder / "preliminary_analysis.md"
            self._generate_analysis_md(metadata_to_save, analysis_file)
            self._log(f"[+] Analysis saved: {analysis_file}")

            # Step 9: Remove from incoming (only if successful)
            try:
                file_path.unlink()
                self._log(f"[+] Original file removed from incoming: {file_path}")
            except Exception as e:
                self._log(f"[!] Could not remove original file: {str(e)}", "WARNING")

            self._log(f"[+] Phase 0 complete: {ticket_folder}")

            return {
                "success": True,
                "ticket_folder": str(ticket_folder),
                "metadata": metadata_to_save,
                "confidence": confidence,
                "extraction_method": extraction_method
            }

        except Exception as e:
            error_msg = f"Phase 0 failed: {str(e)}"
            self._log(error_msg, "ERROR")

            # Move to failed folder
            try:
                failed_path = self.failed_dir / file_path.name
                # If file still exists in incoming
                if file_path.exists():
                    shutil.move(str(file_path), str(failed_path))
                    self._log(f"[!] File moved to failed: {failed_path}")

                # Create error report
                error_file = self.failed_dir / f"{file_path.stem}_error.txt"
                with open(error_file, 'w', encoding='utf-8') as f:
                    f.write(f"Phase 0 Failed: {datetime.now()}\n")
                    f.write(f"File: {file_path.name}\n")
                    f.write(f"Error: {str(e)}\n")

                    import traceback
                    f.write("\nTraceback:\n")
                    f.write(traceback.format_exc())
            except Exception as move_error:
                self._log(f"[!] Failed to move file to failed folder: {str(move_error)}", "ERROR")

            return {
                "success": False,
                "error": error_msg,
                "failed_path": str(self.failed_dir / file_path.name) if file_path else None
            }

    def _generate_filename(self, metadata, extension):
        """Generate standardized filename from metadata"""
        date = datetime.now().strftime("%Y-%m-%d")
        ticket_id = metadata.get("ticket_id", "UNKNOWN")

        # Clean company name
        company = metadata.get("company", "Unknown")
        company = company.replace(" ", "").replace(",", "").replace(".", "")
        if len(company) > 30:
            company = company[:30]

        # Clean trading partner
        partner = metadata.get("trading_partner", "Unknown")
        partner = partner.replace(" ", "").replace(",", "").replace(".", "")
        if len(partner) > 30:
            partner = partner[:30]

        # Clean transaction type
        transaction = metadata.get("transaction_type", "")
        transaction = transaction.replace(" ", "-").replace(",", "")
        if len(transaction) > 40:
            transaction = transaction[:40]

        # Build filename
        if transaction:
            filename = f"{date}_{ticket_id}_{company}_TradingPartner-{partner}_{transaction}{extension}"
        else:
            filename = f"{date}_{ticket_id}_{company}_TradingPartner-{partner}{extension}"

        # Ensure filename is valid (remove invalid characters)
        invalid_chars = '<>:"|?*'
        for char in invalid_chars:
            filename = filename.replace(char, "")

        return filename

    def _generate_analysis_md(self, metadata, output_file):
        """Generate preliminary analysis markdown"""
        confidence = metadata.get("confidence", 0.0)
        confidence_label = "HIGH" if confidence >= 0.85 else "MEDIUM" if confidence >= 0.70 else "LOW"

        content = f"""# Preliminary Analysis - Ticket {metadata.get('ticket_id', 'UNKNOWN')}

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} UTC
**Extraction Method:** {metadata.get('extraction_method', 'unknown').upper()}
**Confidence:** {confidence:.2f} ({confidence_label})

## Ticket Overview
- **Customer:** {metadata.get('customer_name', 'N/A')}
- **Company:** {metadata.get('company', 'N/A')}
- **Trading Partner:** {metadata.get('trading_partner', 'N/A')}
- **Transaction:** {metadata.get('transaction_type', 'N/A')}
- **Message ID:** {metadata.get('message_id', 'N/A')}
- **Severity:** {metadata.get('severity', 'NORMAL')}

## Issue Summary
{metadata.get('issue_title', 'No issue title extracted')}

## Root Cause
{metadata.get('root_cause', 'Root cause analysis pending')}

## Recommended Actions
"""

        actions = metadata.get('recommended_actions', [])
        if isinstance(actions, list) and actions:
            for i, action in enumerate(actions, 1):
                content += f"{i}. {action}\n"
        else:
            content += "No specific actions extracted. Analyst review required.\n"

        content += """
## Next Steps
- Analyst to review and verify extraction accuracy
- PM-Investigator to check trading partner specifications
- Investigator to query NotebookLM for similar cases

## Extraction Details
"""

        if metadata.get('extraction_method') == 'hybrid':
            content += f"- Gemini confidence: {metadata.get('analysis_confidence', 0.0):.2f}\n"
            content += f"- OCR confidence: {metadata.get('ocr_confidence', 0.0):.2f}\n"
            content += f"- Combined confidence: {confidence:.2f}\n"
        else:
            content += f"- Confidence: {confidence:.2f}\n"

        content += f"- Original file: {metadata.get('original_file', 'N/A')}\n"
        content += f"- Processed file: {metadata.get('processed_file', 'N/A')}\n"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)


async def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: python workflow.py <file_path>")
        print("Example: python workflow.py C:/Users/sleep/Documents/tickets/incoming/ticket.pdf")
        sys.exit(1)

    file_path = sys.argv[1]

    workflow = TicketWorkflow()
    result = await workflow.process_ticket(file_path)

    if result["success"]:
        print(f"\n[SUCCESS] Phase 0 Complete")
        print(f"Ticket Folder: {result['ticket_folder']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Extraction Method: {result['extraction_method']}")
        sys.exit(0)
    else:
        print(f"\n[FAILED] Phase 0 Failed")
        print(f"Error: {result['error']}")
        if result.get('failed_path'):
            print(f"File moved to: {result['failed_path']}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
