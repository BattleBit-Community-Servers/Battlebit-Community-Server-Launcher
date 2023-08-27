import subprocess
from dotenv import load_dotenv
import os
import sys

load_dotenv()

# List of common server variables
common_server_vars = [
    "SERVER_NAME",
    "SERVER_PORT",
    "SERVER_HZ",
    "SERVER_ANTICHEAT",
    "SERVER_MAX_PING",
    "SERVER_VOXEL_MODE",
    "SERVER_FIXED_SIZE",
    "SERVER_FIRST_GAMEMODE",
    "SERVER_FIRST_MAP",
]

# List of server variables specific to -api
api_server_vars = [
    "SERVER_API_ENDPOINT",
]

# Check if the script is run with -api flag
use_api = "-api" in sys.argv

# Choose the appropriate set of server variables
if use_api:
    server_vars = common_server_vars + api_server_vars
else:
    server_vars = common_server_vars

args = []
for var in server_vars:
    args.append(f"-{var.split('_', 1)[1].replace('_', '')}={os.getenv(var)}")

args.insert(0, os.getenv("SERVER_PATH"))
args.append("-batchmode")
args.append("-nographics")

try:
    subprocess.run(args)
except KeyboardInterrupt:
    pass
