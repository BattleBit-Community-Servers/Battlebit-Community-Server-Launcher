@echo off
echo Python is installed.

if exist requirements.txt (
    echo Installing Python packages from requirements.txt...
    python3 -m pip install -r requirements.txt
) else (
    echo requirements.txt not found. Skipping package installation.
)

echo Running download.py...
python3 download.py
pause
