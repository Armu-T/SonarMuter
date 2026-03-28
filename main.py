import os
import sys
import subprocess
import json

# --- OTOMATİK KÜTÜPHANE KURULUMU ---
def install_requirements():
    requirements = ['pycaw', 'inquirer', 'comtypes']
    for lib in requirements:
        try:
            __import__(lib if lib != 'pycaw' else 'pycaw')
        except ImportError:
            print(f"[*] {lib} kuruluyor...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

install_requirements()

import inquirer
from pycaw.pycaw import AudioUtilities

# --- NIRCMD OTOMATİK İNDİRİCİ ---
def download_nircmd():
    nircmd_path = "C:\\Windows\\nircmd.exe"
    if not os.path.exists(nircmd_path):
        print("[*] NirCmd bulunamadı, indiriliyor...")
        import urllib.request
        import zipfile
        
        url = "https://www.nirsoft.net/utils/nircmd-x64.zip"
        zip_path = "nircmd.zip"
        urllib.request.urlretrieve(url, zip_path)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Sadece nircmd.exe'yi çıkart
            zip_ref.extract("nircmd.exe", "C:\\Windows")
        
        os.remove(zip_path)
        print("[✅] NirCmd başarıyla kuruldu.")

# Seçici çalışmadan önce NirCmd kontrolü
try: download_nircmd()
except: print("[!] NirCmd yetki hatası! Lütfen terminali yönetici olarak çalıştırın.")

CONFIG_FILE = "config.json"

def get_devices_clean():
    devices = []
    try:
        cmd = 'powershell "Get-PnpDevice -Class AudioEndpoint -Status OK | Select-Object FriendlyName, InstanceId"'
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, _ = proc.communicate()
        if out:
            lines = out.decode('cp857').splitlines()
            for line in lines:
                if "{" in line:
                    parts = line.split("{")
                    name = parts[0].strip()
                    guid = "{" + parts[-1].split("}")[0] + "}"
                    devices.append({"name": name, "id": guid})
    except: pass
    return devices

def get_apps_on_all_devices():
    apps = []
    try:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process: apps.append(session.Process.name())
    except: pass
    return list(set(apps))

def main():
    print("=== STEELSERIES SONAR FIX - CONFIG YAPICI ===\n")
    all_devices = get_devices_clean()
    if not all_devices: return

    device_choices = [d["name"] for d in all_devices]
    dev_ans = inquirer.list_input("Hangi aygıtta susturma yapılsın?", choices=device_choices)
    selected_device = next(d for d in all_devices if d["name"] == dev_ans)

    active_apps = get_apps_on_all_devices()
    if not active_apps:
        print("[!] Aktif uygulama bulunamadı. Discord açık mı?")
        return

    app_ans = inquirer.list_input("Susturulacak uygulamayı seçin", choices=active_apps)

    new_config = {"uygulama": app_ans, "aygit": selected_device["name"], "guid": selected_device["id"]}
    
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump([new_config], f, indent=4, ensure_ascii=False)

    print(f"\n[✅] Ayarlar kaydedildi! Şimdi startup.pyw'yi başlangıca atabilirsin.")

if __name__ == "__main__":
    main()
