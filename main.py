import os
import sys
import time

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.adb import ADBClient
from core.journal import ActionJournal

# Import phase modules
from scripts import backup as phase1
from scripts import debloat as phase2
from scripts import optimize as phase3
from scripts import lockdown as phase4
from scripts import launcher as phase5

def measure_ram(adb: ADBClient):
    _, out, _ = adb.shell("dumpsys meminfo | grep -E 'Total RAM|Free RAM|Used RAM'")
    return out.strip()

def run_pipeline():
    print("=" * 65)
    print("         CLEAN MY FIRE TV - OPTIMIZATION & DEBLOAT PIPELINE       ")
    print("=" * 65)

    adb = ADBClient()
    journal = ActionJournal()

    print("[*] Connecting to Fire TV...")
    if not adb.connect():
        print("[-] Could not establish ADB connection. Make sure the TV is on and ADB debugging is enabled.")
        sys.exit(1)

    model = adb.get_prop("ro.product.model")
    build = adb.get_prop("ro.build.version.name")
    print(f"[+] Connected to: {model} ({build})")

    print("\n[*] Baseline Memory Status:")
    ram_before = measure_ram(adb)
    print(ram_before)
    print("-" * 65)

    # Phase 1: Pre-clean Backup
    print("\n--- PHASE 1: PRE-CLEAN BACKUP & STATE SNAPSHOT ---")
    backup_path = phase1.run_backup(adb)

    # Phase 2: Safe Debloat & Alexa Removal
    print("\n--- PHASE 2: SAFE DEBLOAT & TELEMETRY REMOVAL ---")
    phase2.run_debloat(adb, journal, disable_alexa=True)

    # Phase 3: System Settings & Performance Tuning
    print("\n--- PHASE 3: PRIVACY & SYSTEM OPTIMIZATION ---")
    phase3.run_optimize(adb, journal)

    # Phase 4: Soft OTA Block & Daemon Lockdown
    print("\n--- PHASE 4: SOFT OTA BLOCK & BACKGROUND RESTRICTIONS ---")
    phase4.run_lockdown(adb, journal)

    # Phase 5: DumbTV Home Launcher Setup
    print("\n--- PHASE 5: DUMBTV HOME LAUNCHER SETUP ---")
    phase5.run_launcher_setup(adb, journal)

    # Phase 6: Verification & Post-Clean RAM Measurement
    print("\n--- PHASE 6: FINAL VERIFICATION & PERFORMANCE METRICS ---")
    time.sleep(2)
    ram_after = measure_ram(adb)

    print("\n[*] MEMORY COMPARISON:")
    print("BEFORE OPTIMIZATION:")
    print(ram_before)
    print("\nAFTER OPTIMIZATION:")
    print(ram_after)

    disabled_pkgs = adb.get_disabled_packages()
    print(f"\n[+] Total currently disabled packages: {len(disabled_pkgs)}")
    print(f"[+] All actions recorded in journal: {journal.journal_path}")
    print(f"[+] Emergency rollback command: python scripts/rollback.py --all")

    print("\n" + "=" * 65)
    print("  FIRE TV CLEANUP & OPTIMIZATION COMPLETED SUCCESSFULLY!  ")
    print("=" * 65)

if __name__ == "__main__":
    run_pipeline()
