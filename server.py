# server.py
import subprocess
from dotenv import load_dotenv
import os
import sys

load_dotenv()
server_vars = ["SERVER_PATH", "SERVER_NAME", "SERVER_PORT", "SERVER_HZ", "SERVER_SAVE_STATS", "SERVER_DYNAMIC_ROOMS", "SERVER_MAX_PLAYERS", "SERVER_PLAYERS_TO_START", "SERVER_FIRST_ROOM", "SERVER_DYNAMIC_FIRST_MAP", "SERVER_DYNAMIC_FIRST_GAMEMODE", "SERVER_DYNAMIC_FIRST_SIZE", "SERVER_DYNAMIC_FIXED_SIZE", "SERVER_BEGINNER_SERVER", "SERVER_DYNAMIC_MAX_SIZE", "SERVER_RCON_ENABLED", "SERVER_RCON_PASSWORD", "SERVER_REGION", "SERVER_TESTER_SERVER"]
args = []
for var in server_vars:
    args.append(f"-{var.split('_', 1)[1].replace('_','')}={os.getenv(var)}")

args.insert(0, os.getenv("SERVER_PATH"))
args.append("-batchmode")
args.append("-nographics")

folder_name = "SteamCMD"
steamcmd_path = os.path.join(folder_name, "steamcmd.exe")
if "-noupdate" not in sys.argv:
    subprocess.run([steamcmd_path, "+runscript", "update.txt"])
try:
    subprocess.run(args)
except KeyboardInterrupt:
    pass
