import subprocess
import os
import configparser
import shutil
import logging

# Create the 'logs' folder if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logging
LOG_FILE = os.path.join("logs", "setup.log")
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def install_steamcmd():
    """
    Install SteamCMD by downloading and extracting it.
    """
    try:
        logging.info("Installing SteamCMD...")
        os.makedirs("steamcmd", exist_ok=True)

        # Download SteamCMD installer
        subprocess.run([
            "powershell", "Invoke-WebRequest",
            "-Uri", "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip",
            "-OutFile", "steamcmd/steamcmd.zip"
        ])

        # Extract the downloaded ZIP file
        subprocess.run([
            "powershell", "Expand-Archive",
            "-Path", "steamcmd/steamcmd.zip",
            "-DestinationPath", "steamcmd"
        ])

        logging.info("SteamCMD has been installed successfully.")
    except Exception as e:
        logging.error(f"Error installing SteamCMD: {str(e)}")

def read_config():
    """
    Read values from setup_config.ini file.
    """
    config = configparser.ConfigParser()
    config.read("setup_config.ini")
    force_install_dir = config.get("Setup", "force_install_dir")
    username = config.get("Setup", "username")
    password = config.get("Setup", "password")
    steamcmd_path = config.get("Setup", "steamcmd_path", fallback="steamcmd/steamcmd.exe")
    return force_install_dir, username, password, steamcmd_path

def update_steamcmd_directory(steamcmd_directory):
    """
    Update steamcmd_directory in setup_config.ini file.
    """
    config = configparser.ConfigParser()
    config.read("setup_config.ini")
    config.set("ServerConfig", "steamcmd_directory", steamcmd_directory)
    with open("setup_config.ini", "w") as config_file:
        config.write(config_file)

install_steamcmd()

steamcmd_directory = os.path.abspath("steamcmd")
update_steamcmd_directory(steamcmd_directory)

force_install_dir, username, password, steamcmd_path = read_config()

file_content = f"""@ShutdownOnFailedCommand 1
@NoPromptForPassword 1
force_install_dir {force_install_dir}
login {username} {password}
app_update 671860 validate
quit
"""

FILE_PATH = "steamcmd_script.txt"

with open(FILE_PATH, "w") as file:
    file.write(file_content)

logging.info(f'The text file "{FILE_PATH}" has been generated with the specified contents.')

destination_path = os.path.join("steamcmd", FILE_PATH)
shutil.move(FILE_PATH, destination_path)

logging.info(f'The "{FILE_PATH}" file has been moved to the "steamcmd" folder.')
logging.info("The SteamCMD path has been updated in setup_config.ini.")
