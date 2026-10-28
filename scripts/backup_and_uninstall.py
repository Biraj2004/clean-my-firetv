import subprocess
import os
import json
import time
import shutil

def find_adb():
    if os.environ.get("ADB_PATH") and os.path.exists(os.environ["ADB_PATH"]):
        return os.environ["ADB_PATH"]
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    if local_app_data:
        candidate = os.path.join(local_app_data, "Android", "Sdk", "platform-tools", "adb.exe")
        if os.path.exists(candidate):
            return candidate
    adb_path = shutil.which("adb")
    if adb_path:
        return adb_path
    if os.path.exists(r"C:\adb\adb.exe"):
        return r"C:\adb\adb.exe"
    return "adb"

ADB = find_adb()
DEVICE = os.environ.get("FIRETV_IP", "192.168.0.236") + ":5555"

PACKAGES_TO_UNINSTALL = [
    "com.aajtak.firetv",
    "com.abp.firetv",
    "com.news18.ftv",
    "com.tv9live.tv9livetv",
    "com.republicworld.fire.tv",
    "com.republicworld.firetv.rbharat",
    "com.zeenews.tv",
    "com.onnet.systems.iptv.esto"
]

BACKUP_DIR = os.path.abspath("backup/uninstalled_apks")
os.makedirs(BACKUP_DIR, exist_ok=True)
JOURNAL_PATH = os.path.abspath("logs/journal.jsonl")

def run_adb(args):
    cmd = [ADB, "-s", DEVICE] + args
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stdout.strip(), res.stderr.strip(), res.returncode

def main():
    print("Connecting to device...")
    subprocess.run([ADB, "connect", DEVICE], capture_output=True)
    
    restore_cmds = []
    
    for pkg in PACKAGES_TO_UNINSTALL:
        # Check if installed
        out, err, code = run_adb(["shell", "pm", "path", pkg])
        if not out.startswith("package:"):
            print(f"[-] {pkg} is not installed, skipping.")
            continue
            
        apk_remote = out.replace("package:", "").strip()
        local_apk = os.path.join(BACKUP_DIR, f"{pkg}.apk")
        
        print(f"[+] Pulling APK for {pkg} from {apk_remote}...")
        p_out, p_err, p_code = run_adb(["pull", apk_remote, local_apk])
        if p_code != 0 or not os.path.exists(local_apk):
            print(f"[!] Failed to pull {pkg}: {p_err}")
            continue
            
        size = os.path.getsize(local_apk)
        print(f"    Saved {local_apk} ({size} bytes)")
        
        # Uninstall
        print(f"[*] Uninstalling {pkg}...")
        u_out, u_err, u_code = run_adb(["shell", "pm", "uninstall", pkg])
        print(f"    Result: {u_out}")
        
        # Log to journal
        entry = {
            "timestamp": time.time(),
            "action": "uninstall",
            "package": pkg,
            "backup_apk": local_apk,
            "size": size,
            "status": "success" if "Success" in u_out else "failed"
        }
        with open(JOURNAL_PATH, "a") as jf:
            jf.write(json.dumps(entry) + "\n")
            
        restore_cmds.append(f"adb -s {DEVICE} install -r \"{local_apk}\"")
        
    with open("scripts/restore_uninstalled_apps.ps1", "w") as rf:
        rf.write("# Restore script for uninstalled applications via Amazon Appstore Intent or APK\n")
        rf.write("$DEVICE_IP = if ($env:FIRETV_IP) { $env:FIRETV_IP } else { '192.168.1.100' }\n")
        rf.write("$DEVICE = \"$DEVICE_IP:5555\"\n")
        rf.write("if (Test-Path \"$env:LOCALAPPDATA\\Android\\Sdk\\platform-tools\") {\n")
        rf.write("    $env:PATH = \"$env:LOCALAPPDATA\\Android\\Sdk\\platform-tools;\" + $env:PATH\n")
        rf.write("}\n")
        rf.write("adb connect $DEVICE\n")
        for c in restore_cmds:
            rf.write(c + "\n")
            
    print("\n[+] Backup & Uninstall complete! Restore script written to scripts/restore_uninstalled_apps.ps1")

if __name__ == "__main__":
    main()
