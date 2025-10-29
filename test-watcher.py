"""
Test script for directory watcher
Verifies all components without actually starting the watcher
"""

import sys
from pathlib import Path

def test_imports():
    """Test all required imports"""
    print("[TEST] Checking imports...")
    try:
        import watchdog
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
        print("  [PASS] watchdog imported successfully")
    except ImportError as e:
        print(f"  [FAIL] watchdog import failed: {e}")
        return False

    try:
        import win32serviceutil
        import win32service
        import win32event
        import servicemanager
        print("  [PASS] pywin32 imported successfully")
    except ImportError as e:
        print(f"  [WARN] pywin32 not available (optional for service mode): {e}")

    return True

def test_paths():
    """Test all required paths"""
    print("\n[TEST] Checking paths...")

    incoming_dir = Path(r"C:\Users\sleep\Documents\tickets\incoming")
    if incoming_dir.exists():
        print(f"  [PASS] Incoming directory exists: {incoming_dir}")
    else:
        print(f"  [FAIL] Incoming directory not found: {incoming_dir}")
        return False

    skill_path = Path(r"C:\Users\sleep\.claude\skills\media-analysis\run.py")
    if skill_path.exists():
        print(f"  [PASS] Media analysis skill exists: {skill_path}")
    else:
        print(f"  [FAIL] Media analysis skill not found: {skill_path}")
        return False

    log_dir = Path(r"C:\Users\sleep\.claude\logs")
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)
        print(f"  [INFO] Created log directory: {log_dir}")
    else:
        print(f"  [PASS] Log directory exists: {log_dir}")

    return True

def test_script_syntax():
    """Test script syntax"""
    print("\n[TEST] Checking script syntax...")

    scripts = [
        "watch-incoming.py",
        "watch-incoming-service.py",
        "watcher-status.py"
    ]

    for script in scripts:
        script_path = Path(__file__).parent / script
        if not script_path.exists():
            print(f"  [FAIL] Script not found: {script}")
            return False

        try:
            import py_compile
            py_compile.compile(str(script_path), doraise=True)
            print(f"  [PASS] {script} syntax valid")
        except py_compile.PyCompileError as e:
            print(f"  [FAIL] {script} syntax error: {e}")
            return False

    return True

def test_configuration():
    """Test configuration values"""
    print("\n[TEST] Checking configuration...")

    try:
        # Import with hyphen-safe approach
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "watch_incoming",
            Path(__file__).parent / "watch-incoming.py"
        )
        watch_incoming = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(watch_incoming)

        supported_exts = watch_incoming.SUPPORTED_EXTS
        print(f"  [INFO] Supported extensions: {', '.join(supported_exts)}")

        incoming_dir = watch_incoming.INCOMING_DIR
        print(f"  [INFO] Monitoring directory: {incoming_dir}")

        skill_path = watch_incoming.SKILL_PATH
        print(f"  [INFO] Analysis script: {skill_path}")

        log_path = watch_incoming.LOG_PATH
        print(f"  [INFO] Log file: {log_path}")

        print("  [PASS] Configuration loaded successfully")
        return True
    except Exception as e:
        print(f"  [FAIL] Configuration test error: {e}")
        return False

def test_file_handler():
    """Test file handler class"""
    print("\n[TEST] Checking file handler...")

    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "watch_incoming",
            Path(__file__).parent / "watch-incoming.py"
        )
        watch_incoming = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(watch_incoming)

        handler = watch_incoming.IncomingFileHandler()
        print(f"  [PASS] IncomingFileHandler instantiated")
        print(f"  [INFO] Processing set initialized: {len(handler.processing)} items")
        return True
    except Exception as e:
        print(f"  [FAIL] File handler error: {e}")
        return False

def test_status_dashboard():
    """Test status dashboard"""
    print("\n[TEST] Checking status dashboard...")

    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "watcher_status",
            Path(__file__).parent / "watcher-status.py"
        )
        watcher_status = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(watcher_status)

        print("  [PASS] Status dashboard module loaded")

        # Try to display status (will show "No activity" if log doesn't exist)
        watcher_status.display_status()
        print("  [PASS] Status dashboard executed successfully")
        return True
    except Exception as e:
        print(f"  [FAIL] Status dashboard error: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("BMAD-EDI Directory Watcher - Component Test")
    print("="*60)

    tests = [
        ("Imports", test_imports),
        ("Paths", test_paths),
        ("Script Syntax", test_script_syntax),
        ("Configuration", test_configuration),
        ("File Handler", test_file_handler),
        ("Status Dashboard", test_status_dashboard)
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n[ERROR] Test '{name}' crashed: {e}")
            results.append((name, False))

    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {name}")

    print("="*60)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("\n[SUCCESS] All tests passed! Watcher is ready to use.")
        print("\nNext steps:")
        print("  1. Test manually: python run-watcher.bat")
        print("  2. Copy a test file to incoming folder")
        print("  3. Verify analysis triggers")
        print("  4. Install as service: install-watcher.bat (as Administrator)")
        return 0
    else:
        print("\n[WARNING] Some tests failed. Review errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
