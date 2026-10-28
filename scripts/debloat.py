import os
import sys
import time

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.adb import ADBClient
from core.journal import ActionJournal
from core.lists import NEVER_DISABLE, PACKAGES_DEBLOAT, PACKAGES_ALEXA

def run_debloat(adb: ADBClient, journal: ActionJournal, disable_alexa: bool = True):
    print("[*] Starting safe debloat process...")
    if not adb.connect():
        print("[-] Device not connected.")
        return

    installed_packages = set(adb.get_installed_packages())
    disabled_packages = set(adb.get_disabled_packages())

    targets = list(PACKAGES_DEBLOAT)
    if disable_alexa:
        targets.extend(PACKAGES_ALEXA)

    print(f"[*] Candidate target packages to inspect: {len(targets)}")
    disabled_count = 0
    skipped_count = 0

    for pkg, desc in targets:
        # 1. HARD SAFETY CHECK
        if pkg in NEVER_DISABLE:
            print(f"[!] REFUSING to touch protected core package: {pkg}")
            skipped_count += 1
            continue

        # 2. Check if installed
        if pkg not in installed_packages:
            continue

        # 3. Check if already disabled
        if pkg in disabled_packages:
            continue

        # 4. Disable package safely
        print(f"[-] Disabling: {pkg:<45} ({desc})")
        code, out, err = adb.shell(f"pm disable-user --user 0 {pkg}")

        if "disabled-user" in out or "new state: disabled-user" in out:
            category = "alexa" if ("alexa" in desc.lower() or "aca" in pkg) else "debloat"
            journal.log_action(
                category=category,
                target=pkg,
                forward_cmd=f"pm disable-user --user 0 {pkg}",
                reverse_cmd=f"pm enable {pkg}",
                description=desc
            )
            disabled_count += 1
        elif "Cannot disable a protected package" in err or "Cannot disable a protected package" in out:
            print(f"[~] Amazon protected package (handled by lockdown): {pkg}")
        else:
            print(f"[?] Result for {pkg}: {out.strip() or err.strip()}")

        time.sleep(0.1)

    # Sync package state to disk
    adb.shell("sync")
    print(f"\n[+] Debloat phase complete: {disabled_count} packages disabled safely.")

if __name__ == "__main__":
    client = ADBClient()
    jrnl = ActionJournal()
    run_debloat(client, jrnl, disable_alexa=True)
