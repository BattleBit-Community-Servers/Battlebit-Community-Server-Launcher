import os
from dotenv import load_dotenv
from main.scripts import create_file, download_and_extract

print("created by jellisy")

# Check for the presence of .env file
if os.path.isfile('.env'):
    # Load the environment variables
    load_dotenv()
    
    # Create the update.txt file
    create_file()
    
    # Download and extract the SteamCMD files, then execute the update.txt script
    download_and_extract()
else:
    print('\033[91m.env file not found, please create or edit the .env file first!\033[0m')
