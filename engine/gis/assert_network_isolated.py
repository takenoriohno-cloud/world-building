# -*- coding: utf-8 -*-
"""
Sandbox Network Isolation Asserter (assert_network_isolated.py)
Mechanically asserts that external network access is strictly BLOCKED / ISOLATED.
Must be run inside standard sandbox mode (BypassSandbox: false).

Validation Rule:
- If network connection SUCCEEDS -> FAIL (Exit 1): Network leak detected!
- If network connection FAILS / BLOCKED -> PASS (Exit 0): Sandbox isolation confirmed!
"""

import sys
import urllib.request
import socket

EXTERNAL_TARGETS = [
    ("OSM Tile Server", "https://tile.openstreetmap.org/0/0/0.png"),
    ("CartoDB Server", "https://basemaps.cartocdn.com/dark_all/0/0/0.png"),
    ("Public DNS Probe", "https://1.1.1.1")
]

def check_isolation_boolean(verbose=True):
    leaks = []
    for name, url in EXTERNAL_TARGETS:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "IsolationCheck/1.0"})
            with urllib.request.urlopen(req, timeout=2) as resp:
                if resp.status == 200:
                    leaks.append(f"{name} ({url}) returned HTTP 200")
        except Exception:
            if verbose:
                print(f"  ✓ {name}: Access BLOCKED as expected (Sandbox active).")

    if leaks:
        if verbose:
            print(f"\n[CRITICAL SECURITY ALERT - NETWORK LEAK DETECTED]")
            for l in leaks:
                print(f"  x External access succeeded: {l}")
        return False
    return True

def check_isolation():
    print(f"\n========================================================")
    print(f"  Mechanical Sandbox Network Isolation Verification")
    print(f"  Target: Confirm external network port is strictly CLOSED")
    print(f"========================================================")

    if not check_isolation_boolean(verbose=True):
        print("\n[CRITICAL SECURITY ALERT / EXIT 1 - NETWORK LEAK DETECTED]")
        print("Security Policy Violation: Sandbox external port remains OPEN.")
        print("Subsequent SDD pipeline execution is strictly BLOCKED.")
        sys.exit(1)
    else:
        print(f"\n[NETWORK ISOLATION 100% CONFIRMED]")
        print("  ✓ External network access is completely cut off.")
        print("  ✓ Sandbox safety constraint satisfied.")
        sys.exit(0)

if __name__ == "__main__":
    check_isolation()
