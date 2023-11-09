import os
import subprocess
import configparser

# Initialize a configparser object
config = configparser.ConfigParser()

# Path to your INI configuration file
ini_file_path = "setup_config.ini"  # Update with the actual path to your INI file

# Check if the INI file exists
if not os.path.exists(ini_file_path):
    print(f"Error: Config file {ini_file_path} not found.")
    exit(1)

# Read the INI file
config.read(ini_file_path)

# Get the SteamCMD directory from the INI file
STEAMCMD_DIR = config.get("ServerConfig", "SteamCMD_Directory")

# Check if SteamCMD executable exists in the specified directory
steamcmd_executable = os.path.join(STEAMCMD_DIR, "steamcmd.exe")
if not os.path.exists(steamcmd_executable):
    print("Error: SteamCMD executable not found in", STEAMCMD_DIR)
    exit(1)

# Define the path to your SteamCMD script
script_path = os.path.join(STEAMCMD_DIR, "steamcmd_script.txt")

# Run SteamCMD with the script
subprocess.run([steamcmd_executable, "+runscript", script_path], shell=True)

# Display a message indicating that SteamCMD has been executed
print("SteamCMD has been executed with the script.")
