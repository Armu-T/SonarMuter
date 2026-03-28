import json
import os
import subprocess
import tkinter as tk
from tkinter import filedialog

# NirCmd yolu
NIRCMD_PATH = "C:\\Windows\\nircmd.exe"
# Ayarların saklandığı sistem klasörü
SETTINGS_FILE = os.path.join(os.environ['APPDATA'], "sonar_fix_settings.json")

# Windows'ta pencere açılmasını ve imleç değişimini engelleyen bayraklar
CREATE_NO_WINDOW = 0x08000000
DETACHED_PROCESS = 0x00000008

def get_config_path():
    """Config dosyasının yerini hatırlar, yoksa sorar."""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f).get("config_path")
        except:
            pass
    
    # Kullanıcıya config.json'u seçtir
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path = filedialog.askopenfilename(title="Lütfen config.json dosyasını seçin", filetypes=[("JSON files", "*.json")])
    root.destroy()
    
    if path:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump({"config_path": path}, f)
        return path
    return None

def main():
    config_path = get_config_path()
    if not config_path or not os.path.exists(config_path):
        return

    if not os.path.exists(NIRCMD_PATH):
        return

    # Config dosyasını oku
    with open(config_path, 'r', encoding='utf-8') as f:
        try:
            targets = json.load(f)
        except:
            return

    # Windows için ekstra görünmezlik ayarları
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    si.wShowWindow = subprocess.SW_HIDE

    # Her hedef için susturma komutunu bir kez gönder
    for t in targets:
        app_name = t['uygulama']
        device_name = t['aygit'].split('(')[0].strip()

        try:
            subprocess.run(
                [NIRCMD_PATH, "setappvolume", app_name, "0", device_name], 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL, 
                creationflags=CREATE_NO_WINDOW | DETACHED_PROCESS,
                startupinfo=si
            )
        except:
            continue

    # Görev bitti, program kapanıyor.

if __name__ == "__main__":
    main()
