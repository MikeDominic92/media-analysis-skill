# BMAD-EDI Directory Watcher

## Quick Links

- **Quick Start:** See `QUICKSTART_WATCHER.md`
- **Full Guide:** See `WATCHER_GUIDE.md`
- **Deliverables:** See `PHASE2_WATCHER_DELIVERABLES.md`
- **Deployment Summary:** See `WATCHER_DEPLOYMENT_SUMMARY.txt`

## One-Line Start

```bash
python watch-incoming.py
```

Or double-click: `run-watcher.bat`

## What It Does

Monitors `C:\Users\sleep\Documents\tickets\incoming\` for new files and automatically triggers media analysis.

## Supported Files

PDF, PNG, JPG, JPEG, BMP, TIFF, MP3, WAV, MP4, MOV, AVI

## Status Check

```bash
python watcher-status.py
```

## Test Suite

```bash
python test-watcher.py
```

## Service Installation (24/7 Mode)

Run as Administrator:
```bash
install-watcher.bat
```

## Logs

```
C:\Users\sleep\.claude\logs\watch-incoming.log
```

## Verification Status

**All Tests Passed:** 6/6
**Status:** Production-Ready
**Date:** 2025-10-29

## Components

1. `watch-incoming.py` - Main watcher
2. `watch-incoming-service.py` - Service wrapper
3. `watcher-status.py` - Status dashboard
4. `test-watcher.py` - Test suite
5. `install-watcher.bat` - Service installer
6. `run-watcher.bat` - Manual runner

## Documentation

- `WATCHER_GUIDE.md` - Comprehensive guide (9.1 KB)
- `QUICKSTART_WATCHER.md` - Quick start (5.3 KB)
- `PHASE2_WATCHER_DELIVERABLES.md` - Full report (13 KB)
- `WATCHER_DEPLOYMENT_SUMMARY.txt` - Deployment summary

## Integration

Part of BMAD-EDI media analysis integration:
- Phase 1: Media-analysis skill (COMPLETE)
- Phase 2: Directory watcher (COMPLETE - This)
- Phase 3: Investigation agent integration (NEXT)

## Support

Run tests: `python test-watcher.py`
Check status: `python watcher-status.py`
View logs: `type "C:\Users\sleep\.claude\logs\watch-incoming.log"`

---

**Ready for production use.**
