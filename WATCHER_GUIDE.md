# BMAD-EDI Directory Watcher Guide

## Overview
The Directory Watcher provides continuous monitoring of the incoming/ folder for new media files. When a supported file is detected, it automatically triggers the media-analysis skill for processing.

## Features
- [+] 24/7 continuous monitoring
- [+] Automatic file type detection
- [+] Duplicate processing prevention
- [+] File stability verification (waits for complete uploads)
- [+] Comprehensive logging
- [+] Windows service support
- [+] Status dashboard

## Installation

### Prerequisites
```bash
# Install dependencies
cd C:\Users\sleep\.claude\skills\media-analysis
pip install -r requirements.txt
```

### Manual Installation (Testing)
No installation needed. Run directly:
```bash
python run-watcher.bat
```

### Service Installation (Production)
Run as Administrator:
```bash
install-watcher.bat
```

## Usage

### Manual Mode (Testing)
```bash
# Start watcher in console
run-watcher.bat

# Stop with Ctrl+C
```

### Service Mode (Production)
```bash
# Start service
python watch-incoming-service.py start

# Stop service
python watch-incoming-service.py stop

# Check service status
python watch-incoming-service.py status

# Remove service
python watch-incoming-service.py remove
```

### Status Dashboard
```bash
# View watcher statistics
python watcher-status.py
```

Output:
```
============================================================
BMAD-EDI Directory Watcher - Status Dashboard
============================================================
Total Files Processed: 15
Success: 12
Failed: 2
Timeout: 1
Last Activity: 2025-10-29 14:23:45

Recent Files:
  [2025-10-29 14:23:45] customer_complaint.pdf
  [2025-10-29 14:18:32] voicemail_123.wav
  [2025-10-29 14:10:15] screenshot_error.png
============================================================
```

## Configuration

### Monitored Directory
Default: `C:\Users\sleep\Documents\tickets\incoming\`

To change:
1. Edit `watch-incoming.py`
2. Update `INCOMING_DIR` constant
3. Restart watcher

### Supported File Types
- Documents: .pdf
- Images: .png, .jpg, .jpeg, .bmp, .tiff
- Audio: .mp3, .wav
- Video: .mp4, .mov, .avi

To add new types:
1. Edit `watch-incoming.py`
2. Update `SUPPORTED_EXTS` set
3. Restart watcher

### Timeouts
- File stability wait: 10 seconds (configurable)
- Analysis timeout: 120 seconds (2 minutes)

To adjust:
1. Edit `watch-incoming.py`
2. Update timeout parameters in `_wait_for_file_ready()` and `_analyze_file()`
3. Restart watcher

## Log Files

### Main Log
Location: `C:\Users\sleep\.claude\logs\watch-incoming.log`

Format:
```
2025-10-29 14:23:45 - INFO - New file detected: customer_complaint.pdf
2025-10-29 14:23:47 - INFO - Starting analysis: customer_complaint.pdf
2025-10-29 14:24:12 - INFO - Analysis complete: customer_complaint.pdf
```

### Service Log
Location: Windows Event Viewer > Application Logs
Filter by Source: "BMadEdiWatcher"

## Troubleshooting

### Watcher Not Starting

**Symptom:** Script exits immediately

**Checks:**
```bash
# Verify incoming folder exists
dir "C:\Users\sleep\Documents\tickets\incoming\"

# Verify media-analysis skill exists
dir "C:\Users\sleep\.claude\skills\media-analysis\run.py"

# Check log file for errors
type "C:\Users\sleep\.claude\logs\watch-incoming.log"
```

**Solution:**
- Create missing directories
- Verify skill installation
- Check file permissions

### Files Not Being Processed

**Symptom:** Files copied but no analysis triggered

**Checks:**
```bash
# Check if file type is supported
# Supported: .pdf, .png, .jpg, .jpeg, .bmp, .tiff, .mp3, .wav, .mp4, .mov, .avi

# Check log file
type "C:\Users\sleep\.claude\logs\watch-incoming.log"

# Verify watcher is running
tasklist | findstr python
```

**Solution:**
- Verify file extension is supported
- Check log for error messages
- Restart watcher

### Analysis Failing

**Symptom:** Files detected but analysis fails

**Checks:**
```bash
# Test media-analysis skill directly
cd C:\Users\sleep\.claude\skills\media-analysis
python run.py "C:\path\to\test\file.pdf"

# Check log for specific error
type "C:\Users\sleep\.claude\logs\watch-incoming.log" | findstr ERROR
```

**Solution:**
- Fix media-analysis skill issues first
- Verify API credentials
- Check file integrity

### Service Not Installing

**Symptom:** Service installation fails

**Checks:**
```bash
# Verify running as Administrator
whoami /groups | findstr "S-1-5-32-544"

# Check pywin32 installation
python -c "import win32serviceutil"
```

**Solution:**
- Run as Administrator
- Reinstall pywin32: `pip install --force-reinstall pywin32`

### High CPU Usage

**Symptom:** Watcher consuming excessive resources

**Checks:**
```bash
# Check for file processing loop
type "C:\Users\sleep\.claude\logs\watch-incoming.log" | findstr "Already processing"

# Monitor process
tasklist /v | findstr python
```

**Solution:**
- Clear incoming folder of problematic files
- Restart watcher
- Increase file stability timeout

## Advanced Configuration

### Custom Event Handlers
Edit `watch-incoming.py` and extend `IncomingFileHandler`:

```python
def on_modified(self, event):
    """Handle file modification events"""
    # Custom logic here
    pass

def on_deleted(self, event):
    """Handle file deletion events"""
    # Custom logic here
    pass
```

### Multiple Folders
Create separate watcher instances:

```python
# watch-incoming-folder2.py
INCOMING_DIR = r"C:\path\to\folder2"
LOG_PATH = r"C:\Users\sleep\.claude\logs\watch-incoming-folder2.log"
```

### Email Notifications
Add email alerts on analysis completion:

```python
import smtplib
from email.mime.text import MIMEText

def _send_notification(self, file_path, success):
    msg = MIMEText(f"Analysis {'complete' if success else 'failed'}: {file_path.name}")
    msg['Subject'] = f"BMAD-EDI: File {'Processed' if success else 'Failed'}"
    msg['From'] = "watcher@bmad-edi.local"
    msg['To'] = "admin@bmad-edi.local"

    # Configure SMTP settings
    # smtp.send_message(msg)
```

## Performance Tuning

### Optimal Settings
- Small files (<10MB): Use defaults
- Large files (>100MB): Increase timeouts
- High volume: Consider batch processing

### Resource Limits
```python
# Limit concurrent processing
import threading

class IncomingFileHandler(FileSystemEventHandler):
    def __init__(self, max_concurrent=3):
        self.processing = set()
        self.semaphore = threading.Semaphore(max_concurrent)
```

## Integration with BMAD-EDI

### Workflow Integration
1. File arrives in incoming/ folder
2. Watcher detects file
3. Analysis triggered automatically
4. Results saved to analysis output folder
5. Investigation agent can access results

### Notification to Investigation Agent
Add webhook or file marker:

```python
def _notify_investigation_agent(self, file_path, result_path):
    """Create marker file for investigation agent"""
    marker = Path(result_path).with_suffix('.ready')
    marker.write_text(f"Analysis complete: {file_path.name}")
```

## Maintenance

### Log Rotation
Logs grow over time. Add rotation:

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    LOG_PATH,
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
```

### Cleanup Old Files
Add automatic cleanup:

```python
def cleanup_old_files(directory, days=30):
    """Remove files older than specified days"""
    cutoff = time.time() - (days * 86400)
    for file in Path(directory).iterdir():
        if file.stat().st_mtime < cutoff:
            file.unlink()
```

## Security Considerations

### File Validation
- File size limits enforced by media-analysis skill
- File type validation by extension
- No execution of uploaded files

### Access Control
- Watcher runs with current user permissions
- Service runs with SYSTEM account (if installed as service)
- Log files protected by filesystem permissions

### Malware Prevention
- Files scanned by media-analysis skill only
- No arbitrary code execution
- Sandboxed analysis environment

## FAQ

**Q: Can I monitor multiple folders?**
A: Yes, create separate watcher instances with different configurations.

**Q: What happens if watcher crashes?**
A: Service mode automatically restarts. Manual mode requires restart.

**Q: Can I process files already in the folder?**
A: No, only new files are processed. Run analysis manually for existing files.

**Q: How do I pause monitoring?**
A: Stop the watcher service or press Ctrl+C in manual mode.

**Q: Can I change file types while running?**
A: No, restart watcher after configuration changes.

**Q: Does it work on Linux/Mac?**
A: Yes, but service wrapper is Windows-only. Use systemd/launchd instead.

## Support

### Debug Mode
Enable verbose logging:
```python
# In watch-incoming.py
logging.basicConfig(level=logging.DEBUG)
```

### Contact
- Documentation: This file
- Issues: Log file analysis
- Updates: Check skill repository

## Version History

### v1.0 (2025-10-29)
- Initial release
- Basic directory monitoring
- Windows service support
- Status dashboard
- Comprehensive logging

## Next Steps

1. Test manual mode with sample files
2. Verify analysis triggers correctly
3. Install as service (if needed)
4. Configure log rotation
5. Set up monitoring alerts