import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.adb import ADBClient
from core.journal import ActionJournal
from core.lists import SETTINGS_OPTIMIZATIONS

def run_optimize(adb: ADBClient, journal: ActionJournal):
    print("[*] Applying Fire TV privacy, UI speedup, and ad-muting settings...")
    if not adb.connect():
        print("[-] Device not connected.")
        return

    applied_count = 0
    for namespace, key, new_val, default_val, desc in SETTINGS_OPTIMIZATIONS:
        code, cur_val_out, _ = adb.shell(f"settings get {namespace} {key}")
        cur_val = cur_val_out.strip()

        if cur_val == new_val:
            continue

        print(f"[*] Setting [{namespace}] {key} = {new_val}  ({desc})")
        adb.shell(f"settings put {namespace} {key} {new_val}")

        if cur_val and cur_val != "null":
            reverse_cmd = f"settings put {namespace} {key} {cur_val}"
        else:
            reverse_cmd = f"settings delete {namespace} {key}"

        journal.log_action(
            category="settings",
            target=f"{namespace}:{key}",
            forward_cmd=f"settings put {namespace} {key} {new_val}",
            reverse_cmd=reverse_cmd,
            description=desc
        )
        applied_count += 1

    print(f"[+] Settings optimization phase complete: {applied_count} settings updated.")

if __name__ == "__main__":
    client = ADBClient()
    jrnl = ActionJournal()
    run_optimize(client, jrnl)
