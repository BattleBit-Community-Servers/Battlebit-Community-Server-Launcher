import subprocess
import configparser
import sys
import datetime


def get_server_configuration(config_file):
    try:
        # Read server configuration from the config file
        config = configparser.ConfigParser()
        config.read(config_file)

        if "Server Configuration" in config:
            server_config = config["Server Configuration"]
            executable_path = server_config.get("ExecutablePath")
            working_directory = server_config.get("WorkingDirectory")

            if not executable_path or not working_directory:
                print(
                    "Error: 'ExecutablePath' or 'WorkingDirectory' not found in the config file."
                )
                return None, None

            return executable_path, working_directory
        else:
            print("Error: 'Server Configuration' section not found in the config file.")
            return None, None
    except configparser.Error as e:
        print(f"ConfigParser Error: {e}")
        return None, None


def get_arguments_from_config(config_file):
    try:
        # Read arguments from the specified INI file
        config = configparser.ConfigParser()
        config.read(config_file)

        if "Server Settings" in config:
            settings = config["Server Settings"]
            return [f"-{key}={value}" for key, value in settings.items()]
        else:
            print("Error: 'Server Settings' section not found in the config file.")
            return []
    except configparser.Error as e:
        print(f"ConfigParser Error: {e}")
        return []


def generate_log_filename(log_location):
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{log_location}\\log_{current_time}.txt"


def main():
    try:
        # Specify the path to your config file
        config_file = "config.ini"

        # Get the executable path and working directory from the config file
        executable_path, working_directory = get_server_configuration(config_file)

        if not executable_path or not working_directory:
            sys.exit(1)

        # Read the log location from the config file
        config = configparser.ConfigParser()
        config.read(config_file)
        log_location = config.get("Server Settings", "LogLocation")

        # Generate the log filename using the log location
        log_filename = generate_log_filename(log_location)

        # Build the command to start the executable
        cmd = [
            executable_path,
            "-batchmode",
            "-nographics",
            "-logFile",
            log_filename,
        ] + get_arguments_from_config(config_file)

        # If cmd list only contains the executable, it means an error occurred
        if len(cmd) == 1:
            print("Exiting due to errors.")
            sys.exit(1)

        # Use subprocess.Popen to run the command with the specified working directory
        process = subprocess.Popen(cmd, cwd=working_directory)

        # Wait for the process to complete
        process.wait()

        if process.returncode != 0:
            print(f"Subprocess Error: Command exited with code {process.returncode}")
            sys.exit(1)

    except KeyboardInterrupt:
        print("KeyboardInterrupt: Stopping the executable...")
        sys.exit(0)


if __name__ == "__main__":
    main()
