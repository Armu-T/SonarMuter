import json
import os
import subprocess
import tkinter as tk
from tkinter import filedialog

# NirCmd yolu
NIRCMD_PATH = "C:\\Windows\\nircmd.exe"
SETTINGS_FILE = os.path.join(os.environ['APPDATA'], "sonar_fix_settings.json")

def get_config_path():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f).get("config_path")
    
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path = filedialog.askopenfilename(title="config.json dosyasını seçin", filetypes=[("JSON files", "*.json")])
    root.destroy()
    
    if path:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump({"config_path": path}, f)
        return path
    return None

def run_once():
    config_path = get_config_path()
    if not config_path or not os.path.exists(config_path): return
    if not os.path.exists(NIRCMD_PATH): return

    with open(config_path, 'r', encoding='utf-8') as f:
        try: targets = json.load(f)
        except: return

    for t in targets:
        app_name = t['uygulama']
        device_name = t['aygit'].split('(')[0].strip()
        try:
            # 0x08000000 bayrağı konsol penceresinin açılmasını engeller
            subprocess.run([NIRCMD_PATH, "setappvolume", app_name, "0", device_name], 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=0x08000000)
        except: continue

if __name__ == "__main__":
    run_once()
