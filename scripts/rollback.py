import os
import sys
import argparse

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.adb import ADBClient
from core.journal import ActionJournal

def main():
    parser = argparse.ArgumentParser(description="Clean My Fire TV - Granular Rollback & Undo Manager")
    parser.add_argument("--all", action="store_true", help="Revert all applied modifications back to original stock state")
    parser.add_argument("--category", type=str, choices=["debloat", "alexa", "settings", "ota", "launcher"], help="Revert actions in a specific category")
    parser.add_argument("--step", type=int, help="Revert a single specific step ID")
    parser.add_argument("--since", type=int, help="Revert all steps from this step ID up to the latest")
    parser.add_argument("--list", action="store_true", help="List all logged actions in the journal")

    args = parser.parse_args()

    client = ADBClient()
    journal = ActionJournal()

    if args.list:
        entries = journal.load_all()
        if not entries:
            print("[-] Journal is empty.")
            return
        print(f"\n{'ID':<5} {'Category':<10} {'Status':<10} {'Target':<35} {'Description'}")
        print("-" * 80)
        for e in entries:
            status = e.get("status", "unknown")
            print(f"{e['id']:<5} {e['category']:<10} {status:<10} {e['target'][:33]:<35} {e['description']}")
        print(f"\nTotal actions in journal: {len(entries)}")
        return

    if not (args.all or args.category or args.step or args.since):
        print("Please specify an undo action: --all, --category <cat>, --step <id>, --since <id>, or --list")
        parser.print_help()
        return

    if not client.connect():
        print("[-] Could not connect to Fire TV. Please make sure TV is on and connected.")
        sys.exit(1)

    journal.rollback(
        adb=client,
        filter_category=args.category,
        step_id=args.step,
        since_id=args.since
    )

if __name__ == "__main__":
    main()
