#!/usr/bin/env python3
"""
BMAD-EDI Workflow Integration - Phase 0 Implementation
Handles Phase 0 pre-investigation analysis

ROUTING LOGIC:
- Documents (PDF, PNG, JPG, etc.): PaddleOCR PRIMARY
- Audio/Video (MP3, MP4, etc.): Gemini 2.5 Pro ONLY

Agent 6 - BMAD-EDI Workflow Integration Specialist
Modified for PaddleOCR-first approach
"""

import asyncio
import json
import shutil
import re
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

    def _parse_metadata_from_text(self, text):
        """
        Parse ticket metadata from OCR-extracted text

        Looks for patterns like:
        - Ticket #XXXXXXX
        - Customer: Name
        - Company: Name
        - Trading Partner: Name
        - etc.
        """
        metadata = {
            "ticket_id": "UNKNOWN",
            "customer_name": "Unknown",
            "company": "Unknown",
            "trading_partner": "Unknown",
            "transaction_type": "Unknown",
            "message_id": "N/A",
            "severity": "NORMAL",
            "issue_title": "Issue extracted from OCR",
            "root_cause": "Pending investigation",
            "recommended_actions": []
        }

        # Extract ticket number (#XXXXXXX or Ticket: XXXXXXX)
        ticket_patterns = [
            r'#(\d{7,8})',
            r'Ticket[:\s#]+(\d{7,8})',
            r'Case[:\s#]+(\d{7,8})',
        ]
        for pattern in ticket_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                metadata["ticket_id"] = match.group(1)
                break

        # Extract customer/company name
        customer_patterns = [
            r'Customer[:\s]+([^\n]+)',
            r'From[:\s]+([^\n]+)',
            r'Requester[:\s]+([^\n]+)',
        ]
        for pattern in customer_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                metadata["customer_name"] = match.group(1).strip()
                break

        # Extract company
        company_patterns = [
            r'Company[:\s]+([^\n]+)',
            r'Organization[:\s]+([^\n]+)',
        ]
        for pattern in company_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                metadata["company"] = match.group(1).strip()
                break

        # Extract trading partner
        partner_patterns = [
            r'Trading Partner[:\s]+([^\n]+)',
            r'Partner[:\s]+([^\n]+)',
            r'Vendor[:\s]+([^\n]+)',
        ]
        for pattern in partner_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                metadata["trading_partner"] = match.group(1).strip()
                break

        # Extract transaction type (850, 810, 856, etc.)
        transaction_patterns = [
            r'(850|810|856|997|940|945|947|204|210|214|990)\s*(PO|Invoice|ASN|FA|Warehouse|Shipment|Status|Carrier|Freight)?',
            r'Transaction[:\s]+(\d{3})',
        ]
        for pattern in transaction_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                trans_code = match.group(1)
                trans_type = match.group(2) if match.lastindex > 1 else ""
                metadata["transaction_type"] = f"{trans_code} {trans_type}".strip()
                break

        # Extract severity keywords
        if re.search(r'\b(urgent|critical|emergency|down)\b', text, re.IGNORECASE):
            metadata["severity"] = "HIGH"
        elif re.search(r'\b(important|priority|asap)\b', text, re.IGNORECASE):
            metadata["severity"] = "MEDIUM"

        # Extract issue title (first line with "error", "issue", "problem", etc.)
        issue_patterns = [
            r'(Error[:\s]+[^\n]+)',
            r'(Issue[:\s]+[^\n]+)',
            r'(Problem[:\s]+[^\n]+)',
            r'(Subject[:\s]+[^\n]+)',
        ]
        for pattern in issue_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                metadata["issue_title"] = match.group(1).strip()
                break

        return metadata

    async def process_ticket(self, file_path):
        """
        Phase 0: Pre-Investigation Analysis with PaddleOCR PRIMARY for documents

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

        # Determine file type
        ext = file_path.suffix.lower()
        is_audio_video = ext in ['.mp3', '.wav', '.m4a', '.mp4', '.mov', '.avi', '.webm']
        is_document = ext in ['.pdf', '.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif']

        try:
            # ROUTING LOGIC: PaddleOCR for documents, Gemini for audio/video
            if is_document:
                # Step 1: Extract text with PaddleOCR (PRIMARY for documents)
                self._log("[*] Document detected - using PaddleOCR as primary engine...")
                ocr = OCRProcessor()
                ocr_result = ocr.extract_text(str(file_path), preprocess=True)

                if not ocr_result.get("success"):
                    error_msg = f"OCR extraction failed: {ocr_result.get('error', 'Unknown error')}"
                    self._log(error_msg, "ERROR")
                    return {
                        "success": False,
                        "error": error_msg
                    }

                # Parse OCR text to extract metadata
                ocr_text = ocr_result.get("text", "")
                self._log(f"[*] PaddleOCR extracted {len(ocr_text)} characters")

                # Extract metadata from OCR text
                metadata = self._parse_metadata_from_text(ocr_text)
                metadata["ocr_text"] = ocr_text
                metadata["ocr_confidence"] = ocr_result.get("confidence", 0.0)
                metadata["confidence"] = ocr_result.get("confidence", 0.0)
                extraction_method = "paddleocr_primary"
                confidence = metadata["confidence"]
                self._log(f"[*] PaddleOCR confidence: {confidence:.2f}")

            elif is_audio_video:
                # Step 1: Extract metadata with Gemini (ONLY for audio/video)
                self._log("[*] Audio/video detected - using Gemini 2.5 Pro...")
                metadata = await extract_ticket_metadata(str(file_path))

                # Check if extraction was successful
                if not isinstance(metadata, dict):
                    raise Exception(f"Invalid metadata format: {type(metadata)}")

                confidence = metadata.get("confidence", metadata.get("analysis_confidence", 0.0))
                extraction_method = "gemini"
                self._log(f"[*] Gemini confidence: {confidence:.2f}")

            else:
                error_msg = f"Unsupported file type: {ext}"
                self._log(error_msg, "ERROR")
                return {
                    "success": False,
                    "error": error_msg,
                    "supported_types": {
                        "documents": [".pdf", ".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif"],
                        "audio_video": [".mp3", ".wav", ".m4a", ".mp4", ".mov", ".avi", ".webm"]
                    }
                }

            metadata["extraction_method"] = extraction_method

            # Step 2: Generate standardized filename
            new_filename = self._generate_filename(metadata, file_path.suffix)
            self._log(f"[*] Generated filename: {new_filename}")

            # Step 3: Create processing folder
            ticket_id = metadata.get("ticket_id", "UNKNOWN")
            ticket_folder = self.processing_dir / f"ticket_{ticket_id}"
            ticket_folder.mkdir(exist_ok=True)

            # Step 4: Copy file to processing folder
            new_file_path = ticket_folder / new_filename
            try:
                shutil.copy2(file_path, new_file_path)
                self._log(f"[+] File copied to: {new_file_path}")
            except Exception as e:
                self._log(f"[!] File copy failed: {str(e)}", "ERROR")
                raise

            # Step 5: Save metadata JSON
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

            # Step 6: Generate preliminary analysis
            analysis_file = ticket_folder / "preliminary_analysis.md"
            self._generate_analysis_md(metadata_to_save, analysis_file)
            self._log(f"[+] Analysis saved: {analysis_file}")

            # Step 7: Remove from incoming (optional - comment out if you want to keep originals)
            # file_path.unlink()
            # self._log(f"[+] Original file removed from incoming")

            self._log(f"[SUCCESS] Phase 0 complete: {ticket_folder}")

            return {
                "success": True,
                "ticket_id": ticket_id,
                "ticket_folder": str(ticket_folder),
                "metadata_file": str(metadata_file),
                "analysis_file": str(analysis_file),
                "confidence": confidence,
                "extraction_method": extraction_method
            }

        except Exception as e:
            self._log(f"[ERROR] Processing failed: {str(e)}", "ERROR")

            # Move to failed folder
            failed_path = self.failed_dir / file_path.name
            try:
                shutil.copy2(file_path, failed_path)
                self._log(f"[*] File copied to failed folder: {failed_path}")
            except:
                pass

            # Create error report
            error_report = {
                "error": str(e),
                "file": file_path.name,
                "timestamp": datetime.now().isoformat()
            }
            error_file = self.failed_dir / f"{file_path.stem}_error.json"
            with open(error_file, 'w') as f:
                json.dump(error_report, f, indent=2)

            return {
                "success": False,
                "error": str(e),
                "failed_path": str(failed_path),
                "error_file": str(error_file)
            }

    def _generate_filename(self, metadata, extension):
        """Generate standardized filename"""
        date = datetime.now().strftime("%Y-%m-%d")
        ticket_id = metadata.get("ticket_id", "UNKNOWN")
        company = metadata.get("company", "Unknown").replace(" ", "")
        partner = metadata.get("trading_partner", "Unknown").replace(" ", "")
        transaction = metadata.get("transaction_type", "").replace(" ", "-")

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

        extraction_method = metadata.get('extraction_method', 'unknown').upper()
        if extraction_method == "PADDLEOCR_PRIMARY":
            extraction_label = "PADDLEOCR (PRIMARY)"
        else:
            extraction_label = extraction_method

        content = f"""# Preliminary Analysis - Ticket {metadata.get('ticket_id', 'UNKNOWN')}

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} UTC
**Extraction Method:** {extraction_label}
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

        if metadata.get('extraction_method') == 'paddleocr_primary':
            content += f"- PaddleOCR confidence: {confidence:.2f}\n"
            content += f"- Characters extracted: {len(metadata.get('ocr_text', ''))}\n"
            content += f"- Preprocessing: 5-stage pipeline applied\n"
        elif metadata.get('extraction_method') == 'gemini':
            content += f"- Gemini 2.5 Pro confidence: {confidence:.2f}\n"
            content += f"- Analysis method: Multimodal (audio/video)\n"

        content += f"- Original file: {metadata.get('original_file', 'N/A')}\n"
        content += f"- Processed file: {metadata.get('processed_file', 'N/A')}\n"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)


async def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: python workflow_paddleocr_primary.py <file_path>")
        print("\nSupported file types:")
        print("  Documents (PaddleOCR): PDF, PNG, JPG, JPEG, BMP, TIFF, GIF")
        print("  Audio/Video (Gemini): MP3, WAV, M4A, MP4, MOV, AVI, WEBM")
        print("\nExample: python workflow_paddleocr_primary.py C:/Users/sleep/Documents/tickets/incoming/ticket.pdf")
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
