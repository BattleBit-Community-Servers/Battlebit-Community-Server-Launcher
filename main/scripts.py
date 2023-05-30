import os
import tempfile
import urllib.request
import zipfile
import subprocess

def create_file():
    """Creates a file update.txt in the SteamCMD folder with the commands to be executed."""
    # Environment variables
    server = os.getenv("SERVER")
    username = os.getenv("USERNAMER")
    password = os.getenv("PASSWORD")
    beta_password = os.getenv("BETAPASSWORD")

    # File content
    content = f'''// update battlebit server
    //
    @ShutdownOnFailedCommand 1
    @NoPromptForPassword 1
    force_install_dir {server}
    login {username} {password}
    app_update 1611740 -beta community-server -betapassword {beta_password} validate
    quit'''

    # Directory name
    folder_name = "SteamCMD"

    # Check and create directory if it doesn't exist
    os.makedirs(folder_name, exist_ok=True)

    # File name and location
    file_name = os.path.join(folder_name, "update.txt")

    # Write content to file
    with open(file_name, "w") as file:
        file.write(content)


def download_and_extract():
    """Downloads a zip file, extracts it to the SteamCMD directory and runs the SteamCMD update.txt script."""
    # Directory and file names
    folder_name = "SteamCMD"
    file_name = "update.txt"

    # URL to download the zip file from
    url = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"

    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    # Download location
    download_location = os.path.join(temp_dir, "steamcmd.zip")

    # Download the zip file
    urllib.request.urlretrieve(url, download_location)

    # Extract the zip file
    with zipfile.ZipFile(download_location, 'r') as zip_ref:
        zip_ref.extractall(folder_name)

    # Remove the downloaded zip file
    os.remove(download_location)

    # Path to the SteamCMD executable
    steamcmd_path = os.path.join(folder_name, "steamcmd.exe")

    # Run the SteamCMD script
    subprocess.run([steamcmd_path, "+runscript", file_name])
