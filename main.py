import os
import sys
import time
import argparse

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
from scripts import post_reboot_audit as audit_module
from scripts import sanity_test as sanity_module
from scripts import rollback as rollback_module

def measure_ram(adb: ADBClient):
    _, out, _ = adb.shell("dumpsys meminfo | grep -E 'Total RAM|Free RAM|Used RAM'")
    return out.strip()

def init_connection(device_ip: str = None) -> ADBClient:
    adb = ADBClient(device_ip=device_ip)
    print("[*] Connecting to Fire TV...")
    if not adb.connect():
        print(f"[-] Could not connect to Fire TV at {adb.device_serial}.")
        print("    Please ensure:")
        print("    1. Fire TV is powered on and connected to the same Wi-Fi network (or USB).")
        print("    2. 'ADB Debugging' is enabled in Settings > My Fire TV > Developer Options.")
        
        # Interactive prompt if in terminal
        if sys.stdin.isatty():
            custom_ip = input("\n[?] Enter Fire TV IP address (e.g. 192.168.1.50) or press Enter to cancel: ").strip()
            if custom_ip:
                adb = ADBClient(device_ip=custom_ip)
                if adb.connect():
                    return adb
        sys.exit(1)

    model = adb.get_prop("ro.product.model")
    build = adb.get_prop("ro.build.version.name")
    print(f"[+] Connected to: {model} ({build}) at {adb.device_serial}")
    return adb

def run_full_pipeline(adb: ADBClient, journal: ActionJournal):
    print("\n" + "=" * 65)
    print("      RUNNING COMPLETE FIRE TV OPTIMIZATION & DEBLOAT PIPELINE    ")
    print("=" * 65)

    print("\n[*] Baseline Memory Status:")
    ram_before = measure_ram(adb)
    print(ram_before)
    print("-" * 65)

    # Phase 1: Pre-clean Backup
    print("\n--- PHASE 1: PRE-CLEAN BACKUP & STATE SNAPSHOT ---")
    phase1.run_backup(adb)

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

    # Phase 6: Post-Clean RAM Measurement
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

def interactive_menu(adb: ADBClient, journal: ActionJournal):
    while True:
        model = adb.get_prop("ro.product.model")
        print("\n" + "=" * 70)
        print(f"       CLEAN MY FIRE TV - Universal Optimization Suite")
        print(f"       Connected: {model} on {adb.device_serial}")
        print("=" * 70)
        print("  1. Run Full Recommended Optimization (Phases 1 - 5)")
        print("  2. Setup DumbTV Home Launcher (Enhanced 4-chip edition)")
        print("  3. Run Safe Debloat (Disable ads, telemetry & Alexa)")
        print("  4. Apply Privacy & System Optimizations (DoT DNS, 0.5x anims)")
        print("  5. Apply Soft OTA Block (Starve update daemons)")
        print("  6. Create Pre-Clean System Snapshot / Backup")
        print("  7. Run Comprehensive Post-Reboot Audit & Service Inspection")
        print("  8. Run Sanity & Navigation Verification Test Suite")
        print("  9. Rollback / Emergency Restore All Changes")
        print("  0. Exit")
        print("-" * 70)

        choice = input("Select an option [0-9]: ").strip()
        if choice == "1":
            run_full_pipeline(adb, journal)
        elif choice == "2":
            phase5.run_launcher_setup(adb, journal)
        elif choice == "3":
            phase2.run_debloat(adb, journal, disable_alexa=True)
        elif choice == "4":
            phase3.run_optimize(adb, journal)
        elif choice == "5":
            phase4.run_lockdown(adb, journal)
        elif choice == "6":
            phase1.run_backup(adb)
        elif choice == "7":
            audit_module.run_audit(adb)
        elif choice == "8":
            sanity_module.run_sanity()
        elif choice == "9":
            rollback_module.main()
        elif choice == "0":
            print("[*] Exiting. Enjoy your clean Fire TV!")
            break
        else:
            print("[-] Invalid selection. Please enter a number between 0 and 9.")

def main():
    parser = argparse.ArgumentParser(
        description="Clean My Fire TV - Universal Fire TV Optimization & Debloat Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--ip", help="Target Fire TV IP address (defaults to FIRETV_IP env or auto-detect)")
    parser.add_argument("--all", action="store_true", help="Execute complete optimization pipeline (non-interactive)")
    parser.add_argument("--launcher", action="store_true", help="Deploy and configure DumbTV Home launcher")
    parser.add_argument("--debloat", action="store_true", help="Execute safe debloat and telemetry disabling")
    parser.add_argument("--optimize", action="store_true", help="Apply system privacy, DNS, and speed tuning")
    parser.add_argument("--lockdown", action="store_true", help="Starve background OTA update services")
    parser.add_argument("--backup", action="store_true", help="Create pre-clean state backup snapshot")
    parser.add_argument("--audit", action="store_true", help="Inspect device health, memory, and running services")
    parser.add_argument("--sanity", action="store_true", help="Run automated sanity and navigation tests")
    parser.add_argument("--rollback", action="store_true", help="Rollback all applied modifications from journal")

    args = parser.parse_args()

    adb = init_connection(device_ip=args.ip)
    journal = ActionJournal()

    # Route based on explicit arguments
    if args.all:
        run_full_pipeline(adb, journal)
    elif args.launcher:
        phase5.run_launcher_setup(adb, journal)
    elif args.debloat:
        phase2.run_debloat(adb, journal, disable_alexa=True)
    elif args.optimize:
        phase3.run_optimize(adb, journal)
    elif args.lockdown:
        phase4.run_lockdown(adb, journal)
    elif args.backup:
        phase1.run_backup(adb)
    elif args.audit:
        audit_module.run_audit(adb)
    elif args.sanity:
        sanity_module.run_sanity()
    elif args.rollback:
        rollback_module.main()
    else:
        # No flag supplied -> launch interactive menu if terminal, else run full
        if sys.stdin.isatty():
            interactive_menu(adb, journal)
        else:
            run_full_pipeline(adb, journal)

if __name__ == "__main__":
    main()
