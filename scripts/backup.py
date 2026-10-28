import os
import sys
import json
from datetime import datetime

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.adb import ADBClient

def run_backup(adb: ADBClient) -> str:
    print("[*] Connecting to Fire TV for pre-clean backup...")
    if not adb.connect():
        print("[-] Failed to connect to Fire TV. Please make sure the device is on and authorized.")
        sys.exit(1)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backup", f"snapshot_{timestamp}")
    os.makedirs(backup_dir, exist_ok=True)

    print(f"[*] Creating full state snapshot in: {backup_dir}")

    # 1. Packages
    print("[1/5] Dumping package lists...")
    _, pkgs_all, _ = adb.shell("pm list packages -f")
    with open(os.path.join(backup_dir, "packages_all.txt"), "w", encoding="utf-8") as f:
        f.write(pkgs_all)

    _, pkgs_disabled, _ = adb.shell("pm list packages -d")
    with open(os.path.join(backup_dir, "packages_disabled_before.txt"), "w", encoding="utf-8") as f:
        f.write(pkgs_disabled)

    _, pkgs_3rd, _ = adb.shell("pm list packages -3")
    with open(os.path.join(backup_dir, "packages_third_party.txt"), "w", encoding="utf-8") as f:
        f.write(pkgs_3rd)

    # 2. System Settings
    print("[2/5] Dumping system settings (global, secure, system)...")
    _, set_global, _ = adb.shell("settings list global")
    with open(os.path.join(backup_dir, "settings_global.txt"), "w", encoding="utf-8") as f:
        f.write(set_global)

    _, set_secure, _ = adb.shell("settings list secure")
    with open(os.path.join(backup_dir, "settings_secure.txt"), "w", encoding="utf-8") as f:
        f.write(set_secure)

    _, set_system, _ = adb.shell("settings list system")
    with open(os.path.join(backup_dir, "settings_system.txt"), "w", encoding="utf-8") as f:
        f.write(set_system)

    # 3. Accessibility & Alarms
    print("[3/5] Dumping accessibility services & alarm configs...")
    _, a11y, _ = adb.shell("settings get secure enabled_accessibility_services")
    _, alarms, _ = adb.shell("settings get global alarm_manager_constants")
    config_dump = {
        "enabled_accessibility_services": a11y.strip(),
        "alarm_manager_constants": alarms.strip(),
        "model": adb.get_prop("ro.product.model"),
        "fireos_version": adb.get_prop("ro.build.version.name"),
        "sdk": adb.get_prop("ro.build.version.sdk"),
        "fingerprint": adb.get_prop("ro.build.description"),
        "timestamp": timestamp
    }
    with open(os.path.join(backup_dir, "device_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(config_dump, f, indent=2)

    # 4. Generate stand-alone emergency restore script
    print("[4/5] Generating standalone emergency restore script...")
    restore_py = os.path.join(backup_dir, "emergency_restore.py")
    with open(restore_py, "w", encoding="utf-8") as f:
        f.write(f'''# Standalone Emergency Restore Script
import subprocess
import os

ADB = r"{adb.adb_bin}"
SERIAL = "{adb.device_serial}"

def sh(cmd):
    subprocess.run([ADB, "-s", SERIAL, "shell", cmd])

print("[*] Restoring original disabled state...")
with open(os.path.join(os.path.dirname(__file__), "packages_disabled_before.txt"), "r") as f:
    originally_disabled = {{line.strip().replace("package:", "") for line in f if line.strip()}}

res = subprocess.run([ADB, "-s", SERIAL, "shell", "pm list packages -d"], capture_output=True, text=True)
current_disabled = {{line.strip().replace("package:", "") for line in res.stdout.splitlines() if line.strip()}}

to_re_enable = current_disabled - originally_disabled
for pkg in to_re_enable:
    print(f"Re-enabling: {{pkg}}")
    sh(f"pm enable {{pkg}}")

a11y = "{a11y.strip()}"
if a11y and a11y != "null":
    sh(f"settings put secure enabled_accessibility_services '{{a11y}}'")
else:
    sh("settings delete secure enabled_accessibility_services")

alarms = "{alarms.strip()}"
if alarms and alarms != "null":
    sh(f"settings put global alarm_manager_constants '{{alarms}}'")
else:
    sh("settings delete global alarm_manager_constants")

print("[+] Emergency restore completed.")
''')

    print("[5/5] Backup completed successfully!")
    print(f"[+] Snapshot saved to: {backup_dir}")
    return backup_dir

if __name__ == "__main__":
    client = ADBClient()
    run_backup(client)
