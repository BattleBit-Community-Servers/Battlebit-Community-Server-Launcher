import os
import tempfile
import urllib.request
import zipfile
import subprocess

def create_file():
    # File content
    content = '''// update battlebit server
    //
    @ShutdownOnFailedCommand 1
    @NoPromptForPassword 1
    force_install_dir {server}
    login {usernamer} {password}
    app_update 1611740 -beta community-server -betapassword {betapassword} validate
    quit'''.format(
        server=os.environ.get("SERVER"),
        usernamer=os.environ.get("USERNAMER"),
        password=os.environ.get("PASSWORD"),
        betapassword=os.environ.get("BETAPASSWORD")
    )

    # File name and location
    folder_name = "SteamCMD"
    file_name = os.path.join(folder_name, "update.txt")

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Write to file
    with open(file_name, "w") as file:
        file.write(content)

def download_and_extract():
    # Creating a temporary directory
    temp_dir = tempfile.mkdtemp()
    folder_name = "SteamCMD"
    file_name = os.path.join(folder_name, "update.txt")

    # Download the file from `url` and save it locally under `file_name`:
    url = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"
    file_name = os.path.join(temp_dir, "steamcmd.zip")
    urllib.request.urlretrieve(url, file_name)

    # Extract the zip file
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall(folder_name)

    # Remove the zip file
    os.remove(file_name)

    # Launch SteamCMD.exe
    steamcmd_path = os.path.join(folder_name, "steamcmd.exe")
    subprocess.run([steamcmd_path, "+runscript", "update.txt"])
