"""
Display watcher status and recent activity
"""

import json
from pathlib import Path
from datetime import datetime, timedelta

LOG_PATH = r"C:\Users\sleep\.claude\logs\watch-incoming.log"
STATUS_FILE = r"C:\Users\sleep\.claude\logs\watcher-status.json"

def parse_log():
    """Parse log file for statistics"""
    if not Path(LOG_PATH).exists():
        return None

    stats = {
        "total_files": 0,
        "success": 0,
        "failed": 0,
        "timeout": 0,
        "last_activity": None,
        "recent_files": []
    }

    with open(LOG_PATH, 'r') as f:
        for line in f:
            if "New file detected:" in line:
                stats["total_files"] += 1
                filename = line.split("New file detected:")[-1].strip()
                timestamp = line.split(" - ")[0]
                stats["recent_files"].append({
                    "file": filename,
                    "time": timestamp
                })
            elif "Analysis complete:" in line:
                stats["success"] += 1
            elif "Analysis failed:" in line:
                stats["failed"] += 1
            elif "Analysis timeout:" in line:
                stats["timeout"] += 1

        stats["last_activity"] = stats["recent_files"][-1]["time"] if stats["recent_files"] else None
        stats["recent_files"] = stats["recent_files"][-10:]  # Last 10

    return stats

def display_status():
    """Display watcher status"""
    stats = parse_log()

    if not stats:
        print("No watcher activity logged yet.")
        return

    print("="*60)
    print("BMAD-EDI Directory Watcher - Status Dashboard")
    print("="*60)
    print(f"Total Files Processed: {stats['total_files']}")
    print(f"Success: {stats['success']}")
    print(f"Failed: {stats['failed']}")
    print(f"Timeout: {stats['timeout']}")
    print(f"Last Activity: {stats['last_activity']}")
    print("\nRecent Files:")
    for item in stats["recent_files"]:
        print(f"  [{item['time']}] {item['file']}")
    print("="*60)

if __name__ == "__main__":
    display_status()