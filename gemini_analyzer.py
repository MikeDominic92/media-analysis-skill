#!/usr/bin/env python3
"""
Gemini 2.5 Pro Media Analyzer
Browser automation for Google AI Studio
Handles: PDFs, images, audio, video

COMPLETE IMPLEMENTATION BY AGENT 2
Migrated from google-ai-studio skill
"""
import asyncio
import json
import re
from pathlib import Path
from patchright.async_api import async_playwright


class GeminiAnalyzer:
    """Gemini 2.5 Pro media analyzer with browser automation"""

    def __init__(self, data_dir=None):
        """Initialize Gemini analyzer"""
        self.data_dir = Path(data_dir) if data_dir else Path(__file__).parent / "data"
        self.browser_state_dir = self.data_dir / "browser_state"
        self.auth_info_file = self.data_dir / "auth_info.json"

        self.data_dir.mkdir(exist_ok=True)
        self.browser_state_dir.mkdir(exist_ok=True)

        self.browser = None
        self.context = None
        self.page = None
        self.playwright_instance = None

    async def initialize(self):
        """Initialize browser with saved state"""
        self.playwright_instance = await async_playwright().start()

        self.browser = await self.playwright_instance.chromium.launch(
            headless=False,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )

        state_file = self.browser_state_dir / "state.json"
        if state_file.exists():
            self.context = await self.browser.new_context(storage_state=str(state_file))
        else:
            self.context = await self.browser.new_context()

        self.page = await self.context.new_page()

    async def save_auth_state(self):
        """Save authentication state"""
        state_file = self.browser_state_dir / "state.json"
        await self.context.storage_state(path=str(state_file))
        with open(self.auth_info_file, 'w') as f:
            json.dump({"authenticated": True}, f)

    def check_auth(self):
        """Check if authenticated"""
        if not self.auth_info_file.exists():
            return False
        try:
            with open(self.auth_info_file, 'r') as f:
                auth = json.load(f)
                return auth.get('authenticated', False)
        except:
            return False

    async def authenticate(self):
        """Launch browser for authentication"""
        print("[AUTH] Opening Google AI Studio...")
        await self.page.goto("https://aistudio.google.com")
        print("[AUTH] Please sign in manually...")
        print("[AUTH] Press Enter when done...")
        input()
        await self.save_auth_state()
        print("[AUTH] Authentication saved!")

    async def analyze(self, file_path, system_prompt=None, query=None):
        """Analyze media file with Gemini 2.5 Pro"""
        media_type = self.detect_media_type(file_path)
        if not query:
            query = self._get_default_query(media_type)

        print(f"[*] Analyzing: {file_path}")
        print(f"[*] Media type: {media_type}")

        await self.page.goto("https://aistudio.google.com")
        await self.page.wait_for_load_state("networkidle")
        await asyncio.sleep(2)

        try:
            # Create new prompt
            for selector in ['button:has-text("Create new")', 'button:has-text("New prompt")']:
                try:
                    await self.page.click(selector, timeout=3000)
                    print("[+] Created prompt")
                    break
                except:
                    continue

            await asyncio.sleep(2)

            # Add system instructions
            if system_prompt:
                for selector in ['textarea[placeholder*="system"]', 'textarea[placeholder*="System"]']:
                    try:
                        await self.page.fill(selector, system_prompt, timeout=3000)
                        print("[+] Added system instructions")
                        break
                    except:
                        continue

            # Upload file
            file_input = await self.page.query_selector('input[type="file"]')
            if file_input:
                await file_input.set_input_files(file_path)
                print("[+] File uploaded")
            else:
                return {"success": False, "error": "No file input", "file_path": file_path, "media_type": media_type}

            await asyncio.sleep(3)

            # Enter prompt
            for selector in ['textarea[placeholder*="prompt"]', 'textarea[placeholder*="Prompt"]', 'textarea']:
                try:
                    await self.page.fill(selector, query, timeout=3000)
                    print("[+] Prompt entered")
                    break
                except:
                    continue

            # Submit
            for selector in ['button:has-text("Run")', 'button:has-text("Submit")']:
                try:
                    await self.page.click(selector, timeout=3000)
                    print("[+] Submitted")
                    break
                except:
                    continue

            # Wait for response
            print("[*] Waiting for response...")
            await asyncio.sleep(10)

            response_text = None
            for selector in ['[data-testid="response"]', '[role="article"]', '.response-content']:
                try:
                    element = await self.page.query_selector(selector)
                    if element:
                        response_text = await element.inner_text()
                        if response_text and len(response_text) > 50:
                            print("[+] Response extracted")
                            break
                except:
                    continue

            if not response_text:
                response_text = await self.page.inner_text('body')

            confidence = self.calculate_confidence(response_text)
            extracted_data = self._try_parse_json(response_text)

            return {
                "success": True,
                "confidence": confidence,
                "extracted_data": extracted_data,
                "raw_response": response_text,
                "file_path": file_path,
                "media_type": media_type
            }

        except Exception as e:
            return {"success": False, "error": str(e), "file_path": file_path, "media_type": media_type}

    async def extract_edi_metadata(self, file_path):
        """Extract EDI metadata from ticket files"""
        prompt_file = Path(__file__).parent / "prompts" / "edi-specialist.txt"
        if prompt_file.exists():
            with open(prompt_file, 'r', encoding='utf-8') as f:
                system_prompt = f.read()
        else:
            system_prompt = "You are an EDI Specialist AI."

        query = """Analyze this EDI support ticket:

1. Ticket ID (format: #XXXXXXX)
2. Customer Company Name
3. Trading Partner
4. Transaction Type (850 PO, 810 Invoice, 856 ASN, 997 FA, 824 Rejection, etc.)
5. Issue Title
6. Severity (HIGH, MEDIUM, NORMAL, LOW)
7. Message ID or Reference Number

Format:
Ticket ID: #XXXXXXX
Company: [Company Name]
Trading Partner: [Partner Name]
Transaction Type: [Type]
Message ID: [Reference]
Issue Title: [Brief description]
Severity: [Level]

Then provide:
- Brief issue summary
- Likely root cause
- Recommended next steps
"""

        result = await self.analyze(file_path, system_prompt, query)
        if not result.get("success"):
            return result

        response_text = result.get("raw_response", "")

        metadata = {
            "ticket_id": self._extract_field(response_text, r'Ticket ID[:\s]+#?(\d+)'),
            "company": self._extract_field(response_text, r'Company[:\s]+([^\n]+)'),
            "trading_partner": self._extract_field(response_text, r'Trading Partner[:\s]+([^\n]+)'),
            "transaction_type": self._extract_field(response_text, r'Transaction Type[:\s]+([^\n]+)'),
            "message_id": self._extract_field(response_text, r'Message ID[:\s]+([^\n]+)'),
            "issue_title": self._extract_field(response_text, r'Issue Title[:\s]+([^\n]+)'),
            "severity": self._extract_field(response_text, r'Severity[:\s]+(HIGH|MEDIUM|NORMAL|LOW)', default="NORMAL"),
            "root_cause": self._extract_section(response_text, r'(?:Likely )?Root Cause[:\s]*(.+?)(?=\n\w+:|$)', multiline=True),
            "recommended_actions": self._extract_list(response_text, r'Recommended (?:Next )?Steps?[:\s]*(.+?)(?=\n\w+:|$)', multiline=True)
        }

        metadata["confidence"] = result.get("confidence", 0.0)
        metadata["raw_response"] = response_text
        metadata["file_path"] = file_path

        return metadata

    def calculate_confidence(self, response_text):
        """Calculate confidence score 0.0-1.0"""
        if not response_text or len(response_text) < 50:
            return 0.0

        score = 0.0
        if len(response_text) > 100:
            score += 0.2
        if len(response_text) > 500:
            score += 0.1

        if re.search(r'Ticket ID[:\s]+', response_text, re.I):
            score += 0.15
        if re.search(r'Company[:\s]+', response_text, re.I):
            score += 0.1
        if re.search(r'Trading Partner[:\s]+', response_text, re.I):
            score += 0.1

        if '{' in response_text and '}' in response_text:
            score += 0.1

        error_terms = ['error', 'could not', 'unable', 'failed']
        if not any(term in response_text.lower() for term in error_terms):
            score += 0.1
        else:
            score -= 0.2

        return max(0.0, min(1.0, score))

    @staticmethod
    def detect_media_type(file_path):
        """Detect media type from file extension"""
        ext = Path(file_path).suffix.lower()
        media_types = {
            '.pdf': 'document', '.png': 'image', '.jpg': 'image', '.jpeg': 'image',
            '.mp3': 'audio', '.wav': 'audio', '.mp4': 'video', '.mov': 'video'
        }
        return media_types.get(ext, 'unknown')

    def _get_default_query(self, media_type):
        """Generate default query"""
        queries = {
            'document': "Analyze this document and extract key information.",
            'image': "Describe this image in detail.",
            'audio': "Transcribe this audio.",
            'video': "Analyze this video."
        }
        return queries.get(media_type, "Analyze this file.")

    def _try_parse_json(self, text):
        """Try to extract JSON"""
        try:
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
        except:
            pass
        return None

    def _extract_field(self, text, pattern, default=None):
        """Extract single field"""
        match = re.search(pattern, text, re.I)
        return match.group(1).strip() if match else default

    def _extract_section(self, text, pattern, multiline=False):
        """Extract multi-line section"""
        flags = re.I | re.DOTALL if multiline else re.I
        match = re.search(pattern, text, flags)
        return match.group(1).strip() if match else None

    def _extract_list(self, text, pattern, multiline=False):
        """Extract list items"""
        section = self._extract_section(text, pattern, multiline)
        if not section:
            return []
        items = re.split(r'\n\s*[-*\d+.]\s*', section)
        return [item.strip() for item in items if item.strip()]

    async def cleanup(self):
        """Cleanup browser resources"""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright_instance:
            await self.playwright_instance.stop()


async def analyze_file(file_path, system_prompt=None, query=None):
    """Quick analysis function"""
    analyzer = GeminiAnalyzer()
    await analyzer.initialize()
    try:
        if not analyzer.check_auth():
            await analyzer.authenticate()
        result = await analyzer.analyze(file_path, system_prompt, query)
        return result
    finally:
        await analyzer.cleanup()


async def extract_ticket_metadata(file_path):
    """EDI ticket metadata extraction"""
    analyzer = GeminiAnalyzer()
    await analyzer.initialize()
    try:
        if not analyzer.check_auth():
            await analyzer.authenticate()
        result = await analyzer.extract_edi_metadata(file_path)
        return result
    finally:
        await analyzer.cleanup()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Gemini 2.5 Pro Media Analyzer")
    parser.add_argument("command", choices=["auth", "analyze", "extract-edi"])
    parser.add_argument("--file", help="File path to analyze")
    parser.add_argument("--prompt", help="Analysis prompt")
    parser.add_argument("--system-prompt", help="System instructions")

    args = parser.parse_args()

    async def main():
        analyzer = GeminiAnalyzer()
        await analyzer.initialize()
        try:
            if args.command == "auth":
                if analyzer.check_auth():
                    print("[+] Already authenticated!")
                else:
                    await analyzer.authenticate()
            elif args.command == "analyze":
                if not args.file:
                    print("[!] Error: --file required")
                    return
                if not analyzer.check_auth():
                    print("[!] Not authenticated. Run 'auth' first.")
                    return
                result = await analyzer.analyze(args.file, args.system_prompt, args.prompt)
                print(json.dumps(result, indent=2))
            elif args.command == "extract-edi":
                if not args.file:
                    print("[!] Error: --file required")
                    return
                if not analyzer.check_auth():
                    print("[!] Not authenticated. Run 'auth' first.")
                    return
                result = await analyzer.extract_edi_metadata(args.file)
                print(json.dumps(result, indent=2))
        finally:
            await analyzer.cleanup()

    asyncio.run(main())
