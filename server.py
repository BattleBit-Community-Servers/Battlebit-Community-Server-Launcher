import subprocess
from dotenv import load_dotenv
import os
import sys

load_dotenv()
server_vars = [
    "SERVER_NAME","SERVER_PORT","SERVER_HZ","SERVER_ANTICHEAT","SERVER_MAX_PING","SERVER_VOXEL_MODE","SERVER_API_ENDPOINT","SERVER_FIXED_SIZE","SERVER_FIRST_GAMEMODE","SERVER_FIRST_MAP"]

args = []
for var in server_vars:
    args.append(f"-{var.split('_', 1)[1].replace('_','')}={os.getenv(var)}")

args.insert(0, os.getenv("SERVER_PATH"))
args.append("-batchmode")
args.append("-nographics")

try:
    subprocess.run(args)
except KeyboardInterrupt:
    pass
