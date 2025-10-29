r"""
BMAD-EDI Incoming Folder Watcher
Monitors C:\Users\sleep\Documents\tickets\incoming\ for new files
Auto-triggers media analysis on supported file types
"""

import os
import sys
import time
import subprocess
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
INCOMING_DIR = r"C:\Users\sleep\Documents\tickets\incoming"
SKILL_PATH = r"C:\Users\sleep\.claude\skills\media-analysis\run.py"
LOG_PATH = r"C:\Users\sleep\.claude\logs\watch-incoming.log"

# Supported file extensions
SUPPORTED_EXTS = {'.pdf', '.png', '.jpg', '.jpeg', '.bmp', '.tiff',
                  '.mp3', '.wav', '.mp4', '.mov', '.avi'}

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler(sys.stdout)
    ]
)

class IncomingFileHandler(FileSystemEventHandler):
    """Handle file creation events in incoming folder"""

    def __init__(self):
        self.processing = set()  # Track files being processed

    def on_created(self, event):
        """Triggered when new file is created"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Check if supported file type
        if file_path.suffix.lower() not in SUPPORTED_EXTS:
            logging.info(f"Skipping unsupported file: {file_path.name}")
            return

        # Avoid duplicate processing
        if str(file_path) in self.processing:
            logging.warning(f"Already processing: {file_path.name}")
            return

        # Wait for file to be fully written
        if not self._wait_for_file_ready(file_path):
            logging.error(f"File not ready after waiting: {file_path.name}")
            return

        # Process file
        self.processing.add(str(file_path))
        logging.info(f"New file detected: {file_path.name}")

        try:
            self._analyze_file(file_path)
        finally:
            self.processing.discard(str(file_path))

    def _wait_for_file_ready(self, file_path, timeout=10):
        """
        Wait for file to be fully written
        Returns True if ready, False if timeout
        """
        start_time = time.time()
        last_size = -1

        while time.time() - start_time < timeout:
            try:
                current_size = file_path.stat().st_size
                if current_size == last_size and current_size > 0:
                    # Size stable, file ready
                    return True
                last_size = current_size
                time.sleep(0.5)
            except Exception as e:
                logging.warning(f"Error checking file size: {e}")
                time.sleep(0.5)

        return False

    def _analyze_file(self, file_path):
        """Run media analysis on file"""
        logging.info(f"Starting analysis: {file_path.name}")

        try:
            # Run analysis with timeout
            result = subprocess.run(
                [sys.executable, SKILL_PATH, str(file_path)],
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )

            if result.returncode == 0:
                logging.info(f"Analysis complete: {file_path.name}")
                logging.debug(f"Output: {result.stdout}")
            else:
                logging.error(f"Analysis failed: {file_path.name}")
                logging.error(f"Error: {result.stderr}")

        except subprocess.TimeoutExpired:
            logging.error(f"Analysis timeout: {file_path.name}")

        except Exception as e:
            logging.error(f"Analysis error: {file_path.name} - {e}")

def main():
    """Main watcher loop"""
    # Validate paths
    incoming_path = Path(INCOMING_DIR)
    if not incoming_path.exists():
        logging.error(f"Incoming directory not found: {INCOMING_DIR}")
        sys.exit(1)

    skill_path = Path(SKILL_PATH)
    if not skill_path.exists():
        logging.error(f"Media analysis skill not found: {SKILL_PATH}")
        sys.exit(1)

    # Create log directory
    log_dir = Path(LOG_PATH).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    # Start watching
    logging.info("="*60)
    logging.info("BMAD-EDI Incoming Folder Watcher - STARTED")
    logging.info(f"Monitoring: {INCOMING_DIR}")
    logging.info(f"Supported: {', '.join(SUPPORTED_EXTS)}")
    logging.info("="*60)

    event_handler = IncomingFileHandler()
    observer = Observer()
    observer.schedule(event_handler, INCOMING_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Watcher stopped by user")
        observer.stop()

    observer.join()

if __name__ == "__main__":
    main()