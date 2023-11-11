import subprocess
import configparser
import sys
import datetime


def get_server_configuration(config_file):
    """
    Read server configuration from the config file.
    """
    try:
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
    """
    Read arguments from the specified INI file.
    """
    try:
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
    """
    Generate a log filename using the current time and log location.
    """
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{log_location}\\log_{current_time}.txt"


def main():
    """
    Main function to execute the script.
    """
    try:
        config_file = "config.ini"

        executable_path, working_directory = get_server_configuration(config_file)
        if not executable_path or not working_directory:
            sys.exit(1)

        config = configparser.ConfigParser()
        config.read(config_file)
        log_location = config.get("Server Settings", "LogLocation")

        log_filename = generate_log_filename(log_location)

        cmd = [
            executable_path,
            "-batchmode",
            "-nographics",
            "-logFile",
            log_filename,
        ] + get_arguments_from_config(config_file)

        if len(cmd) == 1:
            print("Exiting due to errors.")
            sys.exit(1)

        process = subprocess.Popen(cmd, cwd=working_directory)
        process.wait()

        if process.returncode != 0:
            print(f"Subprocess Error: Command exited with code {process.returncode}")
            sys.exit(1)

    except KeyboardInterrupt:
        print("KeyboardInterrupt: Stopping the executable...")
        sys.exit(0)


if __name__ == "__main__":
    main()
