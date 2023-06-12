import subprocess
import os

folder_name = "SteamCMD"
steamcmd_path = os.path.join(folder_name, "steamcmd.exe")
subprocess.run([steamcmd_path, "+runscript", "update.txt"])
