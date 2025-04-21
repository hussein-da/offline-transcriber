@echo off
echo Installiere FFmpeg fuer Offline-Transcriber...
powershell -Command "Start-Process PowerShell -ArgumentList '-ExecutionPolicy Bypass -File setup_ffmpeg.ps1' -Verb RunAs"
echo.
echo Wenn die Installation abgeschlossen ist, starte ein neues Terminal und versuche es erneut.
echo.
pause 