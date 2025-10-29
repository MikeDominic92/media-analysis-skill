@echo off
echo Installing BMAD-EDI Directory Watcher Service
echo.

REM Install service
python watch-incoming-service.py install

REM Start service
python watch-incoming-service.py start

echo.
echo Service installed and started successfully!
echo To stop: python watch-incoming-service.py stop
echo To remove: python watch-incoming-service.py remove
pause