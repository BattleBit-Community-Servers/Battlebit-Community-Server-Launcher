from termcolor import colored
import os
from dotenv import load_dotenv
from main.scripts import create_file, download_and_extract

print("created by jellisy")

if os.path.isfile('.env'):
    load_dotenv()
    create_file()
    download_and_extract()
else:
    print(colored('.env file not found, please create or edit the .env file first!', 'red'))