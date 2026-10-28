import json
import os
import time
from datetime import datetime
from typing import List, Dict, Any, Optional

JOURNAL_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "journal.jsonl")

class ActionJournal:
    def __init__(self, journal_path: str = JOURNAL_FILE):
        self.journal_path = journal_path
        os.makedirs(os.path.dirname(self.journal_path), exist_ok=True)

    def log_action(self, category: str, target: str, forward_cmd: str, reverse_cmd: str, description: str):
        actions = self.load_all()
        next_id = len(actions) + 1
        entry = {
            "id": next_id,
            "timestamp": datetime.now().isoformat(),
            "category": category,
            "target": target,
            "forward_cmd": forward_cmd,
            "reverse_cmd": reverse_cmd,
            "description": description,
            "status": "applied"
        }
        with open(self.journal_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        return entry

    def load_all(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.journal_path):
            return []
        entries = []
        with open(self.journal_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
        return entries

    def rollback(self, adb, filter_category: Optional[str] = None, step_id: Optional[int] = None, since_id: Optional[int] = None) -> List[Dict[str, Any]]:
        entries = self.load_all()
        if not entries:
            print("[-] No actions found in journal to rollback.")
            return []

        # Determine which entries to rollback
        to_revert = []
        if step_id is not None:
            to_revert = [e for e in entries if e["id"] == step_id and e.get("status") == "applied"]
        elif since_id is not None:
            to_revert = [e for e in entries if e["id"] >= since_id and e.get("status") == "applied"]
        elif filter_category is not None:
            to_revert = [e for e in entries if e["category"] == filter_category and e.get("status") == "applied"]
        else:
            to_revert = [e for e in entries if e.get("status") == "applied"]

        # Revert in LIFO (reverse) order
        to_revert.reverse()
        reverted = []

        print(f"[*] Starting rollback of {len(to_revert)} actions...")
        for item in to_revert:
            rev_cmd = item.get("reverse_cmd")
            if not rev_cmd:
                print(f"[!] No reverse command for Step #{item['id']} ({item['target']}), skipping.")
                continue

            print(f"[<-] Reverting Step #{item['id']} [{item['category']}]: {item['description']}")
            code, out, err = adb.shell(rev_cmd)
            item["reverted_at"] = datetime.now().isoformat()
            item["revert_output"] = out.strip() if out else err.strip()
            item["status"] = "reverted"
            reverted.append(item)
            time.sleep(0.2)

        # Update journal file with reverted status
        reverted_ids = {r["id"] for r in reverted}
        updated_entries = []
        for e in entries:
            if e["id"] in reverted_ids:
                # Find matching reverted item
                matching = next(r for r in reverted if r["id"] == e["id"])
                updated_entries.append(matching)
            else:
                updated_entries.append(e)

        with open(self.journal_path, "w", encoding="utf-8") as f:
            for e in updated_entries:
                f.write(json.dumps(e) + "\n")

        print(f"[+] Successfully reverted {len(reverted)} actions.")
        return reverted
