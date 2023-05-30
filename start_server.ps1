$python_path = (Get-Command python -ErrorAction SilentlyContinue)
if ($null -eq $python_path) {
    Write-Host "Python is not installed."
    Write-Host "Downloading Python..."
    $url = "https://www.python.org/ftp/python/3.11.3/python-3.11.3-amd64.exe"
    $output = "$env:TEMP\python-3.11.3-amd64.exe"
    Invoke-WebRequest -Uri $url -OutFile $output
    Write-Host "Python installer has been downloaded to $output"
    Write-Host "Launching Python installer..."
    Start-Process -Wait -FilePath $output
    Write-Host "Please ensure Python was installed correctly and added to PATH before continuing."
    Read-Host -Prompt "Press Enter to continue"
} else {
    Write-Host "Python is installed."
}
Write-Host "Running server.py..."
python server.py
Read-Host -Prompt "Press Enter to exit"
