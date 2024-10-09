/*
 * This file is part of Battlebit-Community-Server-Launcher.
 *
 * Battlebit-Community-Server-Launcher is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Battlebit-Community-Server-Launcher is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Battlebit-Community-Server-Launcher.  If not, see <https://www.gnu.org/licenses/>.
 */
use eframe::{egui, App, NativeOptions};
use serde::{Deserialize, Serialize};
use std::fs;
use std::path::{Path, PathBuf};
use std::sync::Arc;
use std::process::{Command, Stdio};
use tokio;
use tokio::sync::Mutex;
use tokio::sync::RwLock;
use tokio::time::Instant;
use toml;
use rfd::FileDialog;
use std::io::{BufRead, BufReader};
#[cfg(windows)]
use winreg::enums::*;
#[cfg(windows)]
use winreg::RegKey;
use std::error::Error;

// Constants for SteamCMD URL and configuration
const STEAMCMD_URL: &str = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip";
const STEAMCMD_ZIP: &str = "steamcmd.zip";
const STEAMCMD_DIR: &str = "./steamcmd";
const CONFIG_FILE: &str = "config.toml";

// Struct for storing Steam credentials
#[derive(Serialize, Deserialize, Default, Clone)]
struct Credentials {
    username: String,
    password: String,
}

// Struct for storing the installation location of the server
#[derive(Serialize, Deserialize, Default, Clone)]
struct InstallLocation {
    path: PathBuf,
}

// Struct for storing game configuration settings
#[derive(Serialize, Deserialize, Default, Clone)]
struct GameConfig {
    port: String,
    hz: String,
    anticheat: String,
    max_ping: String,
    voxel_mode: String,
    api_endpoint: String,
}

// Overall config struct that holds game configuration, credentials, and installation location
#[derive(Serialize, Deserialize, Default, Clone)]
struct Config {
    #[serde(rename = "Game Config")]
    game_config: GameConfig,
    credentials: Credentials,
    install_location: InstallLocation,
}

// The main function to start the GUI application
#[tokio::main]
async fn main() -> Result<(), Box<dyn Error + Send + Sync>> {
    // Check if the configuration file exists, otherwise create it with default values
    if !Path::new(CONFIG_FILE).exists() {
        save_config(&Config::default())?;
    }

    // Detect Windows dark mode setting (only available on Windows)
    #[cfg(windows)]
    let is_dark_mode = {
        let hklm = RegKey::predef(HKEY_CURRENT_USER);
        let theme_key = hklm.open_subkey(r"Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize").ok();
        theme_key
            .and_then(|key| key.get_value::<u32, _>("AppsUseLightTheme").ok())
            .map(|value| value == 0)
            .unwrap_or(false)
    };
    
    #[cfg(not(windows))]
    let is_dark_mode = false;

    // Set the visual style (dark or light) based on the detected theme
    let options = NativeOptions::default();

    // Launch the eframe GUI application
    eframe::run_native(
        "BattleBit Server Launcher",
        options,
        Box::new(move |cc| {
            if is_dark_mode {
                cc.egui_ctx.set_visuals(egui::Visuals::dark());
            } else {
                cc.egui_ctx.set_visuals(egui::Visuals::light());
            }
            Ok(Box::new(MyApp::default()))
        }),
    )
    .map_err(|e| -> Box<dyn Error + Send + Sync> { Box::new(std::io::Error::new(std::io::ErrorKind::Other, e.to_string())) })?;
    
    Ok(())
}

// Struct to hold the application's state
struct MyApp {
    credentials: Credentials,
    status: Arc<Mutex<String>>,
    install_location: Arc<Mutex<PathBuf>>,
    active_tab: String,
    setup_complete: Arc<Mutex<bool>>,
    battlebit_console_output: Arc<RwLock<String>>,
    steamcmd_console_output: Arc<RwLock<String>>,
    console_input: String,
    uptime_timer: Arc<Mutex<Option<Instant>>>,
}

// Default implementation for MyApp, loading configuration or creating a default one
impl Default for MyApp {
    fn default() -> Self {
        let config = load_config().unwrap_or_default();

        Self {
            credentials: config.credentials,
            status: Arc::new(Mutex::new(String::from("Waiting for user input..."))),
            install_location: Arc::new(Mutex::new(config.install_location.path)),
            active_tab: String::from("Credentials"),
            setup_complete: Arc::new(Mutex::new(false)),
            battlebit_console_output: Arc::new(RwLock::new(String::new())),
            steamcmd_console_output: Arc::new(RwLock::new(String::new())),
            console_input: String::new(),
            uptime_timer: Arc::new(Mutex::new(None)),
        }
    }
}

// Implementation of the eframe App trait for MyApp to handle the GUI
impl App for MyApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        // Side panel for navigation between different tabs
        egui::SidePanel::left("side_panel").show(ctx, |ui| {
            ui.heading("Navigation");
            if ui
                .selectable_label(self.active_tab == "Credentials", "Credentials")
                .clicked()
            {
                self.active_tab = String::from("Credentials");
            }
            if ui
                .selectable_label(self.active_tab == "Setup", "Setup")
                .clicked()
            {
                self.active_tab = String::from("Setup");
            }
            if ui
                .selectable_label(self.active_tab == "Server", "Server")
                .clicked()
            {
                self.active_tab = String::from("Server");
            }
            if ui
                .selectable_label(self.active_tab == "About", "About")
                .clicked()
            {
                self.active_tab = String::from("About");
            }
        });

        // Central panel to display content based on the active tab
        egui::CentralPanel::default().show(ctx, |ui| {
            ui.heading("BattleBit Server Launcher");
            ui.separator();

            match self.active_tab.as_str() {
                "Credentials" => self.render_credentials_tab(ui, ctx),
                "Setup" => self.render_install_tab(ui, ctx),
                "Server" => self.render_server_tab(ui, ctx),
                "About" => self.render_about_tab(ui),
                _ => {}
            }
        });
    }
}

// Implementation of various render and helper methods for MyApp
impl MyApp {
    // Render the credentials tab for Steam username and password input
    fn render_credentials_tab(&mut self, ui: &mut egui::Ui, ctx: &egui::Context) {
        ui.label("Enter your Steam username:");
        ui.text_edit_singleline(&mut self.credentials.username);
        ui.label("Enter your Steam password:");
        ui.add(egui::TextEdit::singleline(&mut self.credentials.password).password(true));

        if ui.button("Save Credentials").clicked() {
            let install_location = self.install_location.clone();
            let config = Config {
                game_config: GameConfig::default(),
                credentials: self.credentials.clone(),
                install_location: InstallLocation {
                    path: tokio::task::block_in_place(|| install_location.blocking_lock().clone()),
                },
            };
            self.save_config_async(config, ctx);
        }
    }

    // Render the setup tab for SteamCMD and game server installation
    fn render_install_tab(&mut self, ui: &mut egui::Ui, ctx: &egui::Context) {
        if ui.button("Set Server Location").clicked() {
            if let Some(folder) = FileDialog::new().pick_folder() {
                let mut install_location = tokio::task::block_in_place(|| self.install_location.blocking_lock());
                *install_location = folder.clone();

                let config = Config {
                    game_config: GameConfig::default(),
                    credentials: self.credentials.clone(),
                    install_location: InstallLocation { path: folder },
                };
                self.save_config_async(config, ctx);
            }
        }

        if ui.button("Download and Server Setup").clicked() {
            self.download_and_install_steamcmd(ctx);
        }

        if ui.button("Install Game Server").clicked() {
            self.install_game_server(ctx);
        }

        if let Ok(setup_complete) = self.setup_complete.try_lock() {
            if *setup_complete {
                ui.horizontal(|ui| {
                    ui.label("Done!");
                });
            }
        }
    }

    // Render the server tab for launching, stopping, and monitoring the server
    fn render_server_tab(&mut self, ui: &mut egui::Ui, _ctx: &egui::Context) {
        ui.horizontal(|ui| {
            if ui.button("Launch Server").clicked() {
                let install_location = self.install_location.clone();
                let config = load_config().unwrap_or_default();
                let server_path = tokio::task::block_in_place(|| install_location.blocking_lock().join("battlebit.exe"));
                if server_path.exists() {
                    let port_arg = format!("-Port={}", config.game_config.port);
                    let hz_arg = format!("-Hz={}", config.game_config.hz);
                    let anticheat_arg = format!("-AntiCheat={}", config.game_config.anticheat);
                    let max_ping_arg = format!("-MaxPing={}", config.game_config.max_ping);
                    let voxel_mode_arg = format!("-VoxelMode={}", config.game_config.voxel_mode);
                    let api_endpoint_arg = format!("-ApiEndPoint={}", config.game_config.api_endpoint);
                    let args: Vec<&str> = vec![
                        "-batchmode", "-nographics",
                        &port_arg,
                        &hz_arg,
                        &anticheat_arg,
                        &max_ping_arg,
                        &voxel_mode_arg,
                        &api_endpoint_arg,
                    ];
                    let battlebit_console_output_ref = self.battlebit_console_output.clone();
                    let uptime_timer_ref = self.uptime_timer.clone();
                    let command = Command::new(&server_path)
                        .args(&args)
                        .stdout(Stdio::piped())
                        .stderr(Stdio::piped())
                        .spawn();
                    if let Ok(mut child) = command {
                        let stdout = BufReader::new(child.stdout.take().unwrap());
                        let stderr = BufReader::new(child.stderr.take().unwrap());
                        let battlebit_console_output_stdout = battlebit_console_output_ref.clone();
                        let battlebit_console_output_stderr = battlebit_console_output_ref.clone();

                        *tokio::task::block_in_place(|| uptime_timer_ref.blocking_lock()) = Some(Instant::now());

                        tokio::spawn(async move {
                            for line in stdout.lines() {
                                let line = line.unwrap_or_default();
                                let mut console = battlebit_console_output_stdout.write().await;
                                console.push_str(&format!("{}\n", line));
                            }
                        });

                        tokio::spawn(async move {
                            for line in stderr.lines() {
                                let line = line.unwrap_or_default();
                                let mut console = battlebit_console_output_stderr.write().await;
                                console.push_str(&format!("{}\n", line));
                            }
                        });
                    } else {
                        ui.label("Failed to launch server.");
                    }
                } else {
                    ui.label("Error: battlebit.exe not found in the installation directory.");
                }
            }

            if ui.button("Kill Server").clicked() {
                if let Err(e) = kill_battlebit_process() {
                    ui.label(&format!("Failed to kill server: {}", e));
                } else {
                    ui.label("Server process killed successfully.");
                    *tokio::task::block_in_place(|| self.uptime_timer.blocking_lock()) = None;
                }
            }
        });

        ui.separator();
        ui.label("Console Output:");
        ui.horizontal(|ui| {
            if let Some(start_time) = *tokio::task::block_in_place(|| self.uptime_timer.blocking_lock()) {
                let elapsed = Instant::now().duration_since(start_time);
                ui.label(format!("Uptime: {:.0?}", elapsed));
            } else {
                ui.label("Uptime: Server is not running.");
            }
        });
        egui::ScrollArea::vertical().max_height(200.0).show(ui, |ui| {
            let battlebit_console_output = self.battlebit_console_output.clone();
            let mut console_text = tokio::task::block_in_place(|| tokio::runtime::Handle::current().block_on(battlebit_console_output.read()).clone());
            ui.add(egui::TextEdit::multiline(&mut console_text).desired_rows(10).lock_focus(true).desired_width(f32::INFINITY));
        });

        ui.separator();
        ui.label("Console Input:");
        ui.text_edit_singleline(&mut self.console_input);
        if ui.button("Send Command").clicked() {
            let command = self.console_input.clone();
            self.console_input.clear();
            let mut console_output = tokio::task::block_in_place(|| tokio::runtime::Handle::current().block_on(self.battlebit_console_output.write()));
            console_output.push_str(&format!("> {}\n", command));
        }
    }

    // Render the about tab with some information about the app
    fn render_about_tab(&self, ui: &mut egui::Ui) {
        ui.label("BattleBit Server Launcher v1.0\nDeveloped by Jellisy");
        ui.label("This tool is designed to make managing game servers simple. It streamlines downloading SteamCMD, setting up game servers, and launching them effortlessly—all in one easy-to-use solution.");
    }

    // Asynchronous function to save the configuration to a file
    fn save_config_async(&self, config: Config, ctx: &egui::Context) {
        let status_ref = Arc::clone(&self.status);
        let ctx_clone = ctx.clone();
        tokio::spawn(async move {
            let mut status = status_ref.lock().await;
            if let Err(e) = save_config(&config) {
                *status = format!("Failed to save config: {}", e);
            } else {
                *status = String::from("Config saved successfully.");
            }
            ctx_clone.request_repaint();
        });
    }

    // Asynchronous function to download and install SteamCMD
    fn download_and_install_steamcmd(&self, ctx: &egui::Context) {
        let status_ref = Arc::clone(&self.status);
        let ctx_clone = ctx.clone();
        let setup_complete_ref = Arc::clone(&self.setup_complete);
        let steamcmd_console_output_ref = Arc::clone(&self.steamcmd_console_output);
        tokio::spawn(async move {
            {
                let mut status = status_ref.lock().await;
                *status = String::from("Downloading SteamCMD...");
            }

            match download_steamcmd().await {
                Ok(_) => {
                    {
                        let mut status = status_ref.lock().await;
                        *status = String::from("SteamCMD downloaded. Extracting...");
                    }

                    if let Err(e) = extract_steamcmd() {
                        let mut status = status_ref.lock().await;
                        *status = format!("Failed to extract SteamCMD: {}", e);
                    } else {
                        {
                            let mut status = status_ref.lock().await;
                            *status = String::from("SteamCMD extracted successfully. Running initial setup...");
                        }

                        if let Err(e) = run_steamcmd_once_with_output(steamcmd_console_output_ref.clone()).await {
                            let mut status = status_ref.lock().await;
                            *status = format!("Failed to run SteamCMD: {}", e);
                        } else {
                            let mut status = status_ref.lock().await;
                            *status = String::from("SteamCMD setup completed successfully.");
                            let mut setup_complete = setup_complete_ref.lock().await;
                            *setup_complete = true;
                        }
                    }
                }
                Err(e) => {
                    let mut status = status_ref.lock().await;
                    *status = format!("Failed to download SteamCMD: {}", e);
                }
            }

            ctx_clone.request_repaint();
        });
    }

    // Asynchronous function to install the game server using SteamCMD
    fn install_game_server(&self, ctx: &egui::Context) {
        let credentials = self.credentials.clone();
        let status_ref = Arc::clone(&self.status);
        let install_location_ref = Arc::clone(&self.install_location);
        let steamcmd_console_output_ref = Arc::clone(&self.steamcmd_console_output);
        let ctx_clone = ctx.clone();

        tokio::spawn(async move {
            let install_location = tokio::task::block_in_place(|| install_location_ref.blocking_lock().clone());
            let mut status = status_ref.lock().await;
            *status = String::from("Installing game server...");
            drop(status);

            let result = tokio::task::block_in_place(|| install_game_server_with_output(&credentials.username, &credentials.password, &install_location, steamcmd_console_output_ref.clone()));

            let mut status = status_ref.lock().await;
            match result {
                Ok(_) => {
                    *status = String::from("Server installed successfully.");
                }
                Err(e) => {
                    *status = format!("Failed to install server: {}", e);
                }
            }
            ctx_clone.request_repaint();
        });
    }
}

// Save the configuration to a TOML file
fn save_config(config: &Config) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    let toml_str = toml::to_string(config)?;
    fs::write(CONFIG_FILE, toml_str)?;
    Ok(())
}

// Load the configuration from a TOML file
fn load_config() -> Result<Config, Box<dyn std::error::Error + Send + Sync>> {
    if !Path::new(CONFIG_FILE).exists() {
        return Ok(Config::default());
    }
    let toml_str = fs::read_to_string(CONFIG_FILE)?;
    let config: Config = toml::from_str(&toml_str)?;
    Ok(config)
}

// Download SteamCMD using an HTTP request
async fn download_steamcmd() -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    let response = reqwest::get(STEAMCMD_URL).await?;
    let bytes = response.bytes().await?;
    fs::write(STEAMCMD_ZIP, &bytes)?;
    Ok(())
}

// Extract the downloaded SteamCMD zip file
fn extract_steamcmd() -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    let file = fs::File::open(STEAMCMD_ZIP)?;
    let mut archive = zip::ZipArchive::new(file)?;
    archive.extract(STEAMCMD_DIR)?;
    Ok(())
}

// Run SteamCMD once to complete its initial setup and log the output
async fn run_steamcmd_once_with_output(console_output: Arc<RwLock<String>>) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    let steamcmd_executable = format!("{}/steamcmd.exe", STEAMCMD_DIR);

    let mut child = Command::new(steamcmd_executable)
        .arg("+login")
        .arg("anonymous")
        .arg("+quit")
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()?;

    let stdout = BufReader::new(child.stdout.take().unwrap());
    let stderr = BufReader::new(child.stderr.take().unwrap());

    let console_output_stdout = console_output.clone();
    let console_output_stderr = console_output.clone();

    tokio::spawn(async move {
        for line in stdout.lines() {
            let line = line.unwrap_or_default();
            let mut console = console_output_stdout.write().await;
            console.push_str(&format!("{}\n", line));
        }
    });

    tokio::spawn(async move {
        for line in stderr.lines() {
            let line = line.unwrap_or_default();
            let mut console = console_output_stderr.write().await;
            console.push_str(&format!("{}\n", line));
        }
    });

    let output = child.wait_with_output()?;

    if !output.status.success() {
        return Err(format!(
            "Failed to run SteamCMD: {}",
            String::from_utf8_lossy(&output.stderr)
        )
        .into());
    }

    Ok(())
}

// Install the game server using SteamCMD and log the output
fn install_game_server_with_output(
    username: &str,
    password: &str,
    install_location: &Path,
    console_output: Arc<RwLock<String>>,
) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    let steamcmd_executable = format!("{}/steamcmd.exe", STEAMCMD_DIR);

    let mut child = Command::new(steamcmd_executable)
        .arg("+login")
        .arg(username)
        .arg(password)
        .arg("+force_install_dir")
        .arg(install_location.to_str().unwrap())
        .arg("+app_update")
        .arg("671860")
        .arg("validate")
        .arg("+quit")
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()?;

    let stdout = BufReader::new(child.stdout.take().unwrap());
    let stderr = BufReader::new(child.stderr.take().unwrap());

    for line in stdout.lines() {
        let line = line.unwrap_or_default();
        let mut console = tokio::task::block_in_place(|| tokio::runtime::Handle::current().block_on(console_output.write()));
        console.push_str(&format!("{}\n", line));
    }

    for line in stderr.lines() {
        let line = line.unwrap_or_default();
        let mut console = tokio::task::block_in_place(|| tokio::runtime::Handle::current().block_on(console_output.write()));
        console.push_str(&format!("{}\n", line));
    }

    let output = child.wait_with_output()?;

    if !output.status.success() {
        return Err(format!(
            "Failed to download server files: {}",
            String::from_utf8_lossy(&output.stderr)
        )
        .into());
    }

    Ok(())
}

// Kill the battlebit.exe process using taskkill (on Windows)
fn kill_battlebit_process() -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    let output = Command::new("taskkill")
        .args(&["/F", "/IM", "battlebit.exe"])
        .output()?;

    if !output.status.success() {
        return Err(format!(
            "Failed to kill battlebit.exe: {}",
            String::from_utf8_lossy(&output.stderr)
        )
        .into());
    }

    Ok(())
}
