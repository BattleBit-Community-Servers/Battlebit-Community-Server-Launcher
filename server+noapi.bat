@echo off
echo Python is installed.

if exist requirements.txt (
    echo Installing Python packages from requirements.txt...
    python -m pip install -r requirements.txt
) else (
    echo requirements.txt not found. Skipping package installation.
)

echo Running server.py...
python server.py
pause