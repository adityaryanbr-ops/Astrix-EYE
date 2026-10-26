@echo off
cd /d "%~dp0"
if exist ".venv\Scripts\pythonw.exe" (
    start "" ".venv\Scripts\pythonw.exe" astrix_eye.py %*
) else (
    start "" pythonw astrix_eye.py %*
)
