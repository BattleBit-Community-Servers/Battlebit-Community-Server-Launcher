import os
import tempfile
import urllib.request
import zipfile
import subprocess


def create_file():
    server = os.getenv("SERVER")
    username = os.getenv("USERNAMER")
    password = os.getenv("PASSWORD")
    appid = os.getenv("APPID")
    betapassword = os.getenv("BETAPASSWORD")
    branch = os.getenv("BRANCH")

    content = f"""// update battlebit server
    @ShutdownOnFailedCommand 1
    @NoPromptForPassword 1
    force_install_dir {server}
    login {username} {password}
    app_update {appid} -beta {branch}"""

    if betapassword:
        content += f" {betapassword}"

    content += " validate\nquit"

    folder_name = "SteamCMD"
    os.makedirs(folder_name, exist_ok=True)
    file_name = os.path.join(folder_name, "update.txt")

    with open(file_name, "w") as file:
        file.write(content)


def download_and_extract():
    folder_name = "SteamCMD"
    file_name = "update.txt"

    url = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"
    temp_dir = tempfile.mkdtemp()
    download_location = os.path.join(temp_dir, "steamcmd.zip")
    urllib.request.urlretrieve(url, download_location)

    with zipfile.ZipFile(download_location, "r") as zip_ref:
        zip_ref.extractall(folder_name)

    os.remove(download_location)
    steamcmd_path = os.path.join(folder_name, "steamcmd.exe")
    subprocess.run([steamcmd_path, "+runscript", file_name])
