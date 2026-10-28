import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.adb import ADBClient
from core.journal import ActionJournal
from core.lists import PACKAGES_OTA_SOFT, PROTECTED_LOCKDOWN

def run_lockdown(adb: ADBClient, journal: ActionJournal):
    print("[*] Applying Soft OTA Block and background daemon lockdown...")
    if not adb.connect():
        print("[-] Device not connected.")
        return

    installed = set(adb.get_installed_packages())

    # 1. Disable OTA nag apps
    for pkg, desc in PACKAGES_OTA_SOFT:
        if pkg in installed:
            print(f"[-] Disabling OTA nag service: {pkg} ({desc})")
            adb.shell(f"pm disable-user --user 0 {pkg}")
            journal.log_action(
                category="ota",
                target=pkg,
                forward_cmd=f"pm disable-user --user 0 {pkg}",
                reverse_cmd=f"pm enable {pkg}",
                description=desc
            )

    # 2. Lock down protected background services (OTA daemons & analytics)
    for pkg, desc in PROTECTED_LOCKDOWN:
        if pkg in installed:
            print(f"[*] Starving background execution for: {pkg} ({desc})")
            adb.shell(f"cmd appops set {pkg} RUN_ANY_IN_BACKGROUND ignore")
            adb.shell(f"am force-stop {pkg}")

            journal.log_action(
                category="ota" if "ota" in pkg else "debloat",
                target=f"appops:{pkg}",
                forward_cmd=f"cmd appops set {pkg} RUN_ANY_IN_BACKGROUND ignore",
                reverse_cmd=f"cmd appops set {pkg} RUN_ANY_IN_BACKGROUND allow",
                description=f"Restrict background execution for {pkg}"
            )

    print("[+] Soft OTA and background daemon lockdown complete.")

if __name__ == "__main__":
    client = ADBClient()
    jrnl = ActionJournal()
    run_lockdown(client, jrnl)
