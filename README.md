# SteamCMD Server Downloader

This script automates the process of downloading and updating a server using SteamCMD.

## Requirements
- Python 3
- Windows 10/11

## Usage

1. Set the following environment variables:
  - `SERVER`: the path to the server installation directory
  - `USERNAME`: your Steam username
  - `PASSWORD`: your Steam password
  - `BETAPASSWORD`: the password for the beta branch of the server
  
  You can set these variables in the command line or in a .env file.
  You can find an example of .env file called `example.env`, edit the file and rename it to `.env`

2. Run the script:

3. The script will create a `SteamCMD` folder in the current directory, download and extract SteamCMD, and run the update command using the environment variables.

## Launching the server

You can use the `server.py` file to launch the server after the download script has completed.
Make sure you set the server varuables  in the .env file befire running the script.
