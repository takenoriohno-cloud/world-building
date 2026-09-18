# -*- coding: utf-8 -*-
"""
SDD Approval Assertion & Token Management Tool
Checks if physical approval token exists before allowing subsequent phase execution.
If approval token does not exist, exits with code 1 to physically block AI progression.
"""

import sys
import os
import json
import argparse
from datetime import datetime

APPROVAL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".specify", "approvals")

def parse_args():
    parser = argparse.ArgumentParser(description="Assert or Issue SDD Human Approval Tokens")
    parser.add_argument("--action", choices=["assert", "issue"], default="assert", help="assert approval exists, or issue new approval")
    parser.add_argument("--id", required=True, help="Creature ID (e.g. 019_forest_mirage_chameleon)")
    parser.add_argument("--step", required=True, choices=["gate1", "gate2", "qgis", "final"], help="Workflow step for approval")
    parser.add_argument("--approver", default="Human User", help="Name or role of approver")
    parser.add_argument("--notes", default="", help="Approval comments or decision notes")
    return parser.parse_args()

def get_approval_path(creature_id, step):
    return os.path.join(APPROVAL_DIR, f"{creature_id}_{step}.json")

def do_assert(creature_id, step):
    path = get_approval_path(creature_id, step)
    if not os.path.exists(path):
        print(f"\n[BLOCKED / EXIT 1] Human Approval Token NOT FOUND: {path}")
        print(f"[REASON] Step '{step}' requires EXPLICIT human review and approval before proceeding.")
        print(f"[ACTION REQUIRED] Present the artifact/plan to the user, await 'Proceed/Approved', and run issue_approval.")
        sys.exit(1)
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not data.get("approved", False):
            print(f"\n[BLOCKED / EXIT 1] Human Approval Token status is NOT approved: {path}")
            sys.exit(1)
        print(f"[PASS] Human Approval Token verified: {path}")
        print(f"       Approver: {data.get('approver')} at {data.get('timestamp')}")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR / EXIT 1] Failed to read approval token {path}: {e}")
        sys.exit(1)

def do_issue(creature_id, step, approver, notes):
    os.makedirs(APPROVAL_DIR, exist_ok=True)
    path = get_approval_path(creature_id, step)
    data = {
        "creature_id": creature_id,
        "step": step,
        "approved": True,
        "approver": approver,
        "timestamp": datetime.now().isoformat(),
        "notes": notes
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[SUCCESS] Human Approval Token ISSUED: {path}")
    print(f"          Step: {step} | Approver: {approver}")
    sys.exit(0)

def main():
    args = parse_args()
    if args.action == "assert":
        do_assert(args.id, args.step)
    elif args.action == "issue":
        do_issue(args.id, args.step, args.approver, args.notes)

if __name__ == "__main__":
    main()
