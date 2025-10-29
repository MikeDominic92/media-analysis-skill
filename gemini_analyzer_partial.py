#!/usr/bin/env python3
"""
Gemini 2.5 Pro Media Analyzer
Browser automation for Google AI Studio
Handles: PDFs, images, audio, video

Migrated from google-ai-studio skill for reusable media analysis
"""
import asyncio
import json
import re
import time
from pathlib import Path
from patchright.async_api import async_playwright


class GeminiAnalyzer:
    """Gemini 2.5 Pro media analyzer with browser automation"""

    def __init__(self, data_dir=None):
        """Initialize Gemini analyzer with browser automation"""
        self.data_dir = Path(data_dir) if data_dir else Path(__file__).parent / "data"
        self.browser_state_dir = self.data_dir / "browser_state"
        self.auth_info_file = self.data_dir / "auth_info.json"

        # Ensure directories exist
        self.data_dir.mkdir(exist_ok=True)
        self.browser_state_dir.mkdir(exist_ok=True)

        # Browser components
        self.browser = None
        self.context = None
        self.page = None
        self.playwright_instance = None

    async def initialize(self):
        """Initialize browser with saved state"""
        self.playwright_instance = await async_playwright().start()

        # Launch browser
        self.browser = await self.playwright_instance.chromium.launch(
            headless=False,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )

        # Load saved browser state if exists
        state_file = self.browser_state_dir / "state.json"
        if state_file.exists():
            self.context = await self.browser.new_context(
                storage_state=str(state_file)
            )
        else:
            self.context = await self.browser.new_context()

        self.page = await self.context.new_page()

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
