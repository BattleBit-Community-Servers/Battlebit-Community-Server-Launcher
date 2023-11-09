import subprocess
import os
import configparser
import shutil  # Import the shutil module

# Function to install SteamCMD
def install_steamcmd():
    try:
        print("Installing SteamCMD...")

        # Create a folder named 'steamcmd'
        os.makedirs("steamcmd", exist_ok=True)

        # Download SteamCMD installer
        subprocess.run(
            [
                "powershell",
                "Invoke-WebRequest",
                "-Uri",
                "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip",
                "-OutFile",
                "steamcmd/steamcmd.zip",
            ]
        )

        # Extract the downloaded ZIP file to the 'steamcmd' folder
        subprocess.run(
            [
                "powershell",
                "Expand-Archive",
                "-Path",
                "steamcmd/steamcmd.zip",
                "-DestinationPath",
                "steamcmd",
            ]
        )

        print("SteamCMD has been installed successfully.")
    except Exception as e:
        print(f"Error installing SteamCMD: {str(e)}")

# Function to read values from setup_config.ini
def read_config():
    config = configparser.ConfigParser()
    config.read("setup_config.ini")
    force_install_dir = config.get("Setup", "force_install_dir")
    username = config.get("Setup", "username")
    password = config.get("Setup", "password")
    steamcmd_path = config.get(
        "Setup", "steamcmd_path", fallback="steamcmd/steamcmd.exe"
    )
    return force_install_dir, username, password, steamcmd_path

# Update steamcmd_directory in setup_config.ini
def update_steamcmd_directory(steamcmd_directory):
    config = configparser.ConfigParser()
    config.read("setup_config.ini")
    config.set("ServerConfig", "steamcmd_directory", steamcmd_directory)
    with open("setup_config.ini", "w") as config_file:
        config.write(config_file)

# Install SteamCMD
install_steamcmd()

# Get the directory path of the 'steamcmd' folder
steamcmd_directory = os.path.abspath("steamcmd")

# Update the steamcmd_directory in setup_config.ini
update_steamcmd_directory(steamcmd_directory)

# Read values from setup_config.ini
force_install_dir, username, password, steamcmd_path = read_config()

# Define the content with user-provided values
file_content = f"""@ShutdownOnFailedCommand 1
@NoPromptForPassword 1
force_install_dir {force_install_dir}
login {username} {password}
app_update 671860 validate
quit
"""

# Specify the file path with the desired name
file_path = "steamcmd_script.txt"

# Write the content to the text file
with open(file_path, "w") as file:
    file.write(file_content)

print(f'The text file "{file_path}" has been generated with the specified contents.')

# Move the steamcmd_script.txt to the steamcmd folder
destination_path = os.path.join("steamcmd", file_path)
shutil.move(file_path, destination_path)

print(f'The "{file_path}" file has been moved to the "steamcmd" folder.')

print("The SteamCMD path has been updated in setup_config.ini.")