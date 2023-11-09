# BattleBit Remastered Server Setup Guide
Welcome to the BattleBit Remastered Server Setup Guide. This guide provides step-by-step instructions on how to set up and update your game server using SteamCMD.

### Get Support Here [Support Discord](https://discord.gg/5HVygFQJaja)

### Prerequisites

1.  **Python 3.12.0**: Make sure you have Python installed on your system. You can download Python from [python.org](https://www.python.org/downloads/).
2.  **`A Steam Account that Owns BattleBit Remastered`**
3.  **Server will only connect to master server `if you are whitelisted by developers`**

### 1. Configuration Files

-   There are two configuration files in this project:

    -   **`setup_config.ini`**: Located in the root directory, this file needs to be filled in first with setup configurations.
    -   **`config.ini`**: Located in the **`Server`** directory, this file contains server-specific settings like server name, port, and executable path. It should be configured after running the setup script.

-   Open the **`setup_config.ini`** file located in the root directory.
-   Edit this file to include any setup configurations you need for your server.

### 2. Running the Setup Script

1.  Open a command prompt or terminal.
2.  Navigate to the root directory of your project (**`Battlebit-Community-Server-Launcher`**).

3.  Run the setup script:

    ```bash
    python setup.py
    ```

    -   The script will read the configuration from setup_config.ini and set up the server according to the specified setup configurations.

### 3. Configuring the Server

-   Now that the initial setup is complete, open the **`config.ini`** file located in the Server directory.
-   Edit the **`[Server Settings]`** and **`[Server Configuration]`** sections to match your server's specifications. Fill in the required values such as server name, port, executable path, etc.

### 4. Running the Server

1.  Open a command prompt or terminal.

2.  Navigate to the root directory of your project (Battlebit-Community-Server-Launcher).

3.  Run the server script:

    ```bash
    python start.py
    ```

    -   The script will read the configuration from **`Server/config.ini`** and any additional setup configurations from **`setup_config.ini`**.
    -   It will then start the server executable with the specified options.
    -   A log file will be generated in the directory specified in the **`[Server Settings]`** section of **`config.ini`**.
    -   If any errors occur during execution, they will be displayed in the command prompt or terminal.

### 5. Stopping the Server

To stop the server, **press `Ctrl+C`** in the command prompt or terminal where the script is running. This will gracefully shut down the server.

### 6. Additional Notes

-   Ensure that the paths provided in the configuration files are correct and point to the actual server executable and working directory.

-   Make sure your server executable is compatible with the provided configuration.

-   If you encounter any issues or have questions, refer to the error messages in the command prompt or terminal for troubleshooting.

-   Always keep backups of your server data and configurations to avoid data loss.

Enjoy running your server with this setup script! **Make sure to add `BBCS` to your support message to recive support**