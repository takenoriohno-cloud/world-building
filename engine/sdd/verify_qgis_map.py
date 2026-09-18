# -*- coding: utf-8 -*-
"""
QGIS Tactical Map Output Validator & Human Gate (verify_qgis_map.py)
Mechanically checks if the generated QGIS range map is valid:
1. File existence at assets/creatures/<id>/<id>_range_map.png
2. File size verification (> 100KB)
3. PNG magic byte header integrity
4. Asserts human visual approval token (.specify/approvals/<id>_qgis.json)
"""

import sys
import os
import argparse
import json

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "engine", "gis"))

try:
    from engine.gis.assert_network_isolated import check_isolation_boolean
except ImportError:
    try:
        from assert_network_isolated import check_isolation_boolean  # type: ignore
    except ImportError:
        check_isolation_boolean = None

def parse_args():
    parser = argparse.ArgumentParser(description="QGIS Range Map Deterministic & Human Approval Validator")
    parser.add_argument("--id", required=True, help="Creature ID (e.g. 019_forest_mirage_chameleon)")
    parser.add_argument("--require-approval", action="store_true", help="Require human visual approval token to PASS")
    return parser.parse_args()

def check_qgis_map(creature_id, require_approval=False):
    errors = []

    # 0. Mechanical Sandbox Network Isolation Verification
    try:
        if check_isolation_boolean is not None:
            if not check_isolation_boolean(verbose=False):
                errors.append("Sandbox Network Leak Detected: External network port is OPEN! Must be strictly isolated.")
    except Exception as ie:
        errors.append(f"Failed to execute network isolation test: {ie}")
    
    # 1. Locate PNG
    map_path = os.path.join(ROOT_DIR, "assets", "creatures", creature_id, f"{creature_id}_range_map.png")
    if not os.path.exists(map_path):
        return False, [f"QGIS map file not found: {map_path}"]

    # 2. Check file size
    size_bytes = os.path.getsize(map_path)
    if size_bytes < 100 * 1024:
        errors.append(f"QGIS map file size too small ({size_bytes} bytes < 100KB threshold). Map generation likely failed or truncated.")

    # 3. Check PNG magic bytes
    try:
        with open(map_path, "rb") as f:
            header = f.read(8)
            if header != b"\x89PNG\r\n\x1a\n":
                errors.append(f"Invalid PNG header in {map_path}. Corrupted image format.")
    except Exception as e:
        errors.append(f"Failed to read image header: {e}")

    # 4. Check Human Visual Approval Token if requested
    if require_approval:
        approval_path = os.path.join(ROOT_DIR, ".specify", "approvals", f"{creature_id}_qgis.json")
        if not os.path.exists(approval_path):
            errors.append(f"Human Visual Approval Token NOT FOUND: {approval_path}. QGIS map must be visually reviewed and approved by the user before proceeding to article writing.")
        else:
            try:
                with open(approval_path, "r", encoding="utf-8") as af:
                    adata = json.load(af)
                if not adata.get("approved", False):
                    errors.append(f"Human Approval Token is marked false in {approval_path}.")
            except Exception as e:
                errors.append(f"Error reading approval token {approval_path}: {e}")

    is_pass = (len(errors) == 0)
    return is_pass, errors, size_bytes, map_path

def main():
    args = parse_args()
    print(f"\n========================================================")
    print(f"  QGIS Tactical Map Output Validation: {args.id}")
    print(f"========================================================")
    
    is_pass, errors, size_bytes, map_path = check_qgis_map(args.id, args.require_approval)

    if not is_pass:
        print("\n[QGIS MAP VALIDATION FAILED - STOPPING (HALT)]")
        for e in errors:
            print(f"  x {e}")
        print("\nEnsure QGIS tactical map is properly rendered and visually approved by the user.")
        sys.exit(1)
    else:
        print(f"\n[QGIS MAP VALIDATION 100% PASS]")
        print(f"  ✓ Image file verified: {map_path}")
        print(f"  ✓ File size: {size_bytes:,} bytes (> 100KB threshold)")
        print(f"  ✓ Valid PNG binary structure confirmed.")
        if args.require_approval:
            print(f"  ✓ Human visual approval token verified.")
        sys.exit(0)

if __name__ == "__main__":
    main()
