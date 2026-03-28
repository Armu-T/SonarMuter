# 🎧 SonarMute Automator (SteelSeries Sonar Fix)

A lightweight Python-based automation tool designed for **SteelSeries Sonar** users. 

### 💡 The Problem
SteelSeries Sonar has a known issue where audio routing becomes "leaky" during screen sharing or streaming (e.g., on Discord). Other participants often hear their own voices echoed back or hear system sounds that should be isolated. This happens because Sonar fails to properly separate audio streams across virtual channels like *Gaming* and *Microphone* during active sessions.

### ✅ The Solution
**SonarMute Automator** solves this by automatically muting specific applications on designated virtual channels upon Windows startup. It ensures that apps like Discord remain silent on channels where they would otherwise cause feedback loops, effectively killing the echo once and for all.

---

## ✨ Features

* **Smart Device Selector:** Automatically lists all active audio devices and identifies applications currently using audio via an interactive terminal menu.
* **Precision Muting:** Targets a specific application on a specific virtual channel (e.g., muting Discord only on the 'Microphone' channel).
* **Ghost-Mode Execution:** Runs invisibly in the background without a console window.
* **Cursor-Safe Automation:** Specifically engineered to prevent the Windows "Loading" (blue circle) cursor from appearing during execution.
* **Zero-Footprint:** Executes the command once and terminates immediately, leaving **0% CPU and RAM usage** after the task is done.
* **Auto-Installer:** Handles all Python dependencies and installs `NirCmd` automatically if missing.

## 🚀 Installation & Usage

### 1. Prerequisites
Ensure you have [Python](https://www.python.org/) installed on your Windows machine.

### 2. Initial Configuration
1. Download the repository and navigate to the folder.
2. Run `gelismis_secici.py` as **Administrator**.
   * *Note: Admin rights are required for the script to automatically install bağımlılıklar and NirCmd into the system directory.*
3. Follow the interactive terminal prompts:
   * Select the **Audio Device** you want to target (e.g., `SteelSeries Sonar - Microphone`).
   * Select the **Application** you want to mute (e.g., `Discord.exe`).
4. This will generate a `config.json` file in your project directory.

### 3. Automating at Startup
1. Run `startup.pyw`.
2. On the first run, it will prompt you to locate your `config.json`. Select it, and the tool will remember this path for future boots.
3. To make this automatic:
   * Press `Win + R` -> Type `shell:startup` -> Enter.
   * Create a **Shortcut** of `startup.pyw` and move it into that folder.

## 🛠️ How It Works (Technical Deep Dive)

The core challenge with **SteelSeries Sonar** is its complex virtual routing. Standard audio libraries often fail to distinguish between virtual channels because they share the same process names. This tool bypasses those limitations:

### 1. GUID-Based Device Mapping
Instead of relying on fragile "Friendly Names," the tool uses **PowerShell Integration** to query the Windows Registry for unique **Endpoint GUIDs**. This ensures the script targets the exact virtual hardware ID assigned to Sonar channels with 100% accuracy.

### 2. Low-Level WASAPI Interaction
We utilize **NirCmd** as a high-performance backend to interact directly with the **Windows Audio Session API (WASAPI)**. This allows us to manipulate individual application "streams" within a specific audio endpoint at the kernel level.

### 3. Non-Persistent Execution & Ghost Mode
To maintain a seamless experience, `startup.pyw` uses specific Windows API flags:
* **`CREATE_NO_WINDOW` & `DETACHED_PROCESS`:** Prevents terminal flickering and background process ghosting.
* **`STARTUPINFO` Flags:** Prevents Windows from triggering the "Loading" cursor icon, making the automation feel like a native OS function.
* **Fire-and-Forget:** The script runs once, applies the mute, and closes itself immediately.

## 📦 Dependencies
The script automatically installs the following if missing:
* `pycaw` (Python Core Audio Windows Library)
* `inquirer` (For the terminal-based interactive menu)
* `comtypes` (For Windows COM interface communication)
* `NirCmd` (For system-level audio manipulation)

## ⚠️ Disclaimer
This tool mutes the volume of the selected application on a specific channel. If you wish to unmute it later, you must do so manually via the Windows Volume Mixer or by modifying the `config.json`.
