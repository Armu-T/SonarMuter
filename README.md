# 🎧 SonarMute Automator (SteelSeries Sonar Fix)

A lightweight Python-based automation tool designed for **SteelSeries Sonar** users. It solves the common issue of Discord audio leaking into multiple virtual channels (e.g., Gaming and Microphone) by automatically muting specific applications on designated channels upon Windows startup.

## ✨ Features

* **Smart Device Selector:** Automatically lists all active audio devices and identifies applications currently using audio.
* **Precision Muting:** Instead of muting the entire system, it targets a specific application on a specific virtual channel (e.g., muting Discord only on the 'Microphone' channel).
* **Zero-Footprint Execution:** Runs invisibly in the background without a console window, executes the command, and terminates immediately to save RAM.
* **Auto-Installer:** Handles all Python dependencies and installs `NirCmd` automatically if missing.

## 🚀 Installation & Usage

### 1. Prerequisites
Ensure you have [Python](https://www.python.org/) installed on your Windows machine.

### 2. Initial Configuration
1.  Download the repository and navigate to the folder.
2.  Run `gelismis_secici.py` as **Administrator**.
    * *Note: Admin rights are required for the script to automatically install NirCmd into the system directory.*
3.  Follow the terminal prompts:
    * Select the **Audio Device** you want to target (e.g., `SteelSeries Sonar - Microphone`).
    * Select the **Application** you want to mute (e.g., `Discord.exe`).
4.  This will generate a `config.json` file in your project directory.

### 3. Automating at Startup
1.  Run `startup.pyw`.
2.  On the first run, it will prompt you to locate your `config.json`. Select it.
3.  To make this automatic:
    * Press `Win + R` -> Type `shell:startup` -> Enter.
    * Create a **Shortcut** of `startup.pyw` and move it into that folder.

## 🛠️ How It Works (Technical Overview)

* **PowerShell Integration:** Fetches accurate Device GUIDs (Global Unique Identifiers) directly from Windows to avoid pointer errors common in standard Python libraries.
* **NirCmd Backend:** Utilizes low-level WASAPI (Windows Audio Session API) calls via NirCmd to perform device-specific application muting—a feat difficult to achieve with standard high-level libraries.
* **Efficient Logic:** The `startup.pyw` script is designed to run once and exit. It doesn't stay open in the background, ensuring no performance impact on your PC.

## 📦 Dependencies
The script automatically installs the following if they are missing:
* `pycaw` (Python Core Audio Windows Library)
* `inquirer` (For the terminal-based interactive menu)
* `comtypes` (For Windows COM interface communication)
* `NirCmd` (For system-level audio manipulation)

## ⚠️ Disclaimer
This tool mutes the volume of the selected application on a specific channel. If you wish to unmute it later, you must do so manually via the Windows Volume Mixer or by modifying the `config.json`.

---
**Developer:** [Your Name / GitHub Profile]  
**License:** MIT
