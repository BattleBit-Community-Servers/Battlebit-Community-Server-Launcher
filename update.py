import os
import subprocess
import configparser
import logging  # Import the logging module

# Create the 'logs' folder if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logging
log_file = os.path.join("logs", "update.log")
logging.basicConfig(filename=log_file, level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to log messages
def log(message):
    logging.info(message)
    print(message)

# Initialize a configparser object
config = configparser.ConfigParser()

# Path to your INI configuration file
ini_file_path = "setup_config.ini"  # Update with the actual path to your INI file

# Check if the INI file exists
if not os.path.exists(ini_file_path):
    error_message = f"Error: Config file {ini_file_path} not found."
    log(error_message)
    print(error_message)
    exit(1)

# Read the INI file
config.read(ini_file_path)

# Get the SteamCMD directory from the INI file
STEAMCMD_DIR = config.get("ServerConfig", "SteamCMD_Directory")

# Check if SteamCMD executable exists in the specified directory
steamcmd_executable = os.path.join(STEAMCMD_DIR, "steamcmd.exe")
if not os.path.exists(steamcmd_executable):
    error_message = "Error: SteamCMD executable not found in " + STEAMCMD_DIR
    log(error_message)
    print(error_message)
    exit(1)

# Define the path to your SteamCMD script
script_path = os.path.join(STEAMCMD_DIR, "steamcmd_script.txt")

# Log a message indicating the script execution
log("Executing SteamCMD with the script...")

# Run SteamCMD with the script
subprocess.run([steamcmd_executable, "+runscript", script_path], shell=True)

# Log a message indicating that SteamCMD has been executed
log("SteamCMD has been executed with the script.")
