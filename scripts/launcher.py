import os
import sys
import time

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.adb import ADBClient
from core.journal import ActionJournal

DUMBTV_PKG = "tv.dumbtv.home"
DUMBTV_ACTIVITY = "tv.dumbtv.home/.Home"
DUMBTV_GUARD = "tv.dumbtv.home/.Guard"
DUMBTV_RELEASE_URL = "https://github.com/Biraj2004/clean-my-firetv/releases/download/v1.0.1/dumbtv-enhanced-home-v1.0.1.apk"

def run_launcher_setup(adb: ADBClient, journal: ActionJournal, force_install: bool = False):
    print("[*] Starting DumbTV Home setup (sole, exclusive launcher)...")
    if not adb.connect():
        print("[-] Device not connected.")
        return

    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    apk_candidates = [
        os.path.join(root_dir, "dumbtv-enhanced-home-v1.0.1.apk"),
        os.path.join(root_dir, "dumbtv-enhanced-home.apk"),
        os.path.join(root_dir, "dumbtv-home.apk")
    ]
    apk_path = None
    for cand in apk_candidates:
        if os.path.exists(cand):
            apk_path = cand
            break

    conf_path = os.path.join(root_dir, "home.conf")
    wall_candidates = [
        os.path.join(root_dir, "assets", "wallpaper-dark-ambient.jpg"),
        os.path.join(root_dir, "assets", "wallpaper.jpg")
    ]
    wall_path = None
    for cand in wall_candidates:
        if os.path.exists(cand):
            wall_path = cand
            break

    is_installed = adb.is_package_installed(DUMBTV_PKG)
    if is_installed and not force_install:
        print(f"[*] Package {DUMBTV_PKG} is already installed and verified on device.")
        print("    Preserving existing installation and skipping re-flash to protect accessibility status.")
    else:
        # Download from GitHub Releases if not present locally
        if not apk_path:
            print("[*] Local APK not found in repo root. Fetching v1.0.1 from GitHub Releases...")
            import urllib.request, tempfile
            download_dest = os.path.join(tempfile.gettempdir(), "dumbtv-enhanced-home-v1.0.1.apk")
            try:
                req = urllib.request.Request(
                    DUMBTV_RELEASE_URL,
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                )
                with urllib.request.urlopen(req, timeout=20) as resp, open(download_dest, "wb") as f_out:
                    f_out.write(resp.read())
                apk_path = download_dest
                print(f"[+] Downloaded {os.path.basename(apk_path)} successfully.")
            except Exception as e:
                print(f"[-] Could not download release APK: {e}")
                print(f"    Please manually download dumbtv-enhanced-home-v1.0.1.apk from:")
                print(f"    https://github.com/Biraj2004/clean-my-firetv/releases")
                return

        print(f"[1/5] Installing {os.path.basename(apk_path)} (Universal v1.0.1 edition)...")
        code, out, err = adb.run(["-s", adb.device_serial, "install", "-r", apk_path])
        if "Success" in out:
            print("[+] DumbTV Home installed successfully.")
            journal.log_action(
                category="launcher",
                target=DUMBTV_PKG,
                forward_cmd=f"adb install -r {apk_path}",
                reverse_cmd=f"pm uninstall {DUMBTV_PKG}",
                description="Install DumbTV Home Launcher v1.0.1"
            )
        else:
            print(f"[!] Install output: {out} {err}")

    # 2. Push home.conf and wallpaper
    print("[2/5] Synchronizing home.conf and ambient wallpaper...")
    target_dir = "/sdcard/Android/data/tv.dumbtv.home/files"
    adb.shell(f"mkdir -p {target_dir}")
    if os.path.exists(conf_path):
        adb.run(["-s", adb.device_serial, "push", conf_path, f"{target_dir}/home.conf"])
        print("  [+] Pushed home.conf")
    if wall_path and os.path.exists(wall_path):
        adb.run(["-s", adb.device_serial, "push", wall_path, f"{target_dir}/wallpaper.jpg"])
        print(f"  [+] Pushed wallpaper from {os.path.basename(wall_path)}")

    # 3. Configure alarm_manager_constants min_futurity=0 (instant Home key reaction)
    print("[3/5] Optimizing Home button response speed (min_futurity=0)...")
    code, cur_alarms, _ = adb.shell("settings get global alarm_manager_constants")
    cur_alarms = cur_alarms.strip()

    new_alarms = "min_futurity=0"
    if cur_alarms and cur_alarms != "null":
        parts = [p for p in cur_alarms.split(",") if not p.startswith("min_futurity=")]
        parts.append("min_futurity=0")
        new_alarms = ",".join(parts)

    adb.shell(f"settings put global alarm_manager_constants '{new_alarms}'")

    rev_alarm_cmd = f"settings put global alarm_manager_constants '{cur_alarms}'" if cur_alarms != "null" else "settings delete global alarm_manager_constants"
    journal.log_action(
        category="launcher",
        target="global:alarm_manager_constants",
        forward_cmd=f"settings put global alarm_manager_constants '{new_alarms}'",
        reverse_cmd=rev_alarm_cmd,
        description="Set alarm_manager_constants min_futurity=0 for instant Home button switch"
    )

    # 4. Enable Guard Accessibility Service for Home button override
    print("[4/5] Activating DumbTV Guard accessibility service...")
    code, cur_services, _ = adb.shell("settings get secure enabled_accessibility_services")
    cur_services = cur_services.strip()

    services_list = []
    if cur_services and cur_services != "null":
        services_list = [s for s in cur_services.split(":") if s and s != DUMBTV_GUARD and not s.startswith("dev.plume")]
    services_list.insert(0, DUMBTV_GUARD)
    new_services = ":".join(services_list)

    adb.shell(f"settings put secure enabled_accessibility_services '{new_services}'")
    adb.shell("settings put secure accessibility_enabled 1")

    rev_a11y_cmd = f"settings put secure enabled_accessibility_services '{cur_services}'" if cur_services != "null" else "settings delete secure enabled_accessibility_services"
    journal.log_action(
        category="launcher",
        target="secure:enabled_accessibility_services",
        forward_cmd=f"settings put secure enabled_accessibility_services '{new_services}'",
        reverse_cmd=rev_a11y_cmd,
        description="Enable DumbTV Guard accessibility service"
    )

    # 5. Launch DumbTV Home
    print("[5/5] Launching DumbTV Home on Fire TV...")
    adb.shell(f"am start -n {DUMBTV_ACTIVITY}")
    time.sleep(1)

    print("\n[+] DumbTV Home setup complete! Sole authoritative launcher active.")

if __name__ == "__main__":
    client = ADBClient()
    jrnl = ActionJournal()
    run_launcher_setup(client, jrnl)
