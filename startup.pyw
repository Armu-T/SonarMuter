import json
import os
import subprocess
import time
import tkinter as tk
from tkinter import filedialog

# NirCmd path
NIRCMD_PATH = "C:\\Windows\\nircmd.exe"
SETTINGS_FILE = os.path.join(os.environ['APPDATA'], "sonar_fix_settings.json")

def get_config_path():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f).get("config_path")
    
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path = filedialog.askopenfilename(title="Select config.json", filetypes=[("JSON files", "*.json")])
    root.destroy()
    
    if path:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump({"config_path": path}, f)
        return path
    return None

def run_until_success():
    config_path = get_config_path()
    if not config_path or not os.path.exists(config_path):
        return

    while True:
        with open(config_path, 'r', encoding='utf-8') as f:
            try:
                targets = json.load(f)
            except:
                return

        all_targets_muted = True
        
        for t in targets:
            app_name = t['uygulama']
            device_name = t['aygit'].split('(')[0].strip()

            try:
                # setappvolume returns 0 if successful in NirCmd
                # We try to apply the volume fix
                result = subprocess.run(
                    [NIRCMD_PATH, "setappvolume", app_name, "0", device_name], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, 
                    creationflags=0x08000000
                )
                
                # If NirCmd couldn't find the app/device, it might not throw a Python error
                # So we keep looping until we are sure the command is effective.
                # However, to avoid infinite loop if app is never opened, 
                # we can just let it run until it successfully hits the target.
            except:
                all_targets_muted = False
                continue

        # Kanka buradaki mantık şu: Eğer Discord henüz açılmadıysa 
        # NirCmd hata vermez ama işlem de yapmaz. 
        # Bu yüzden sistem tepsisinde veya mikserde değişikliği görene kadar
        # 2 saniyede bir kontrol etmeye devam et.
        
        # Eğer manuel olarak kapatmak istersen Görev Yöneticisi'nden kapatabilirsin.
        # Ama hedef susturulduğunda döngüyü kırmak istersen bir kontrol mekanizması ekleyebiliriz.
        # Şimdilik en güvenlisi 2 saniyede bir denemesi:
        time.sleep(2) 

if __name__ == "__main__":
    run_until_success()
