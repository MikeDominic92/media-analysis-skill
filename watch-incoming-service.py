"""
Windows service wrapper for directory watcher
Runs as background service
"""

import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import subprocess
from pathlib import Path

class WatchIncomingService(win32serviceutil.ServiceFramework):
    _svc_name_ = "BMadEdiWatcher"
    _svc_display_name_ = "BMAD-EDI Incoming Folder Watcher"
    _svc_description_ = "Monitors incoming tickets folder and auto-analyzes media files"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.process = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        if self.process:
            self.process.terminate()

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.main()

    def main(self):
        watcher_path = Path(__file__).parent / "watch-incoming.py"
        self.process = subprocess.Popen([sys.executable, str(watcher_path)])

        # Wait for stop signal
        win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(WatchIncomingService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(WatchIncomingService)