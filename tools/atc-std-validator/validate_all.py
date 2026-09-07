#!/usr/bin/env python3
# Copyright (c) 2026 Michael Wroblewski / ShivaCore / A-TownChain-Okosystems. All Rights Reserved.
"""ATC Standards Gesamt-Validierung (CI-Modus, ATC-STD-000 §7.11).

Laeuft ueber alle Standard-Dateien (governance/ + standards/), validiert je
Datei (S-01…S-16) und prueft dateiuebergreifend S-17 Duplicate Detection
(7.8) gegen die Registry (Allokations-Autoritaet).

Aufruf: python3 validate_all.py
Exit:   0 = alles COMPLIANT, 1 = mindestens ein FAIL.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
REGISTRY = os.path.join(ROOT, "registry", "standards.yaml")
CAND = ["governance", "standards"]


def collect():
    # Registry-getrieben (ATC-STD-000 §24): alle file:-Eintraege aus standards.yaml
    files = []
    try:
        with open(REGISTRY, encoding="utf-8") as fh:
            for line in fh:
                m = re.search(r"file:\s*([^},]+)", line)
                if m:
                    files.append(os.path.join(ROOT, m.group(1).strip()))
    except OSError:
        pass
    for d in CAND:
        base = os.path.join(ROOT, d)
        for dirpath, _dirs, names in os.walk(base):
            for n in names:
                if n.endswith(".md"):
                    f = os.path.join(dirpath, n)
                    if f not in files:
                        files.append(f)
    return sorted(files)


def file_id(path):
    try:
        head = open(path, encoding="utf-8").read(2500)
        m = re.search(r"^\s*id:\s*(ATC-STD-(?:BUG-)?[0-9]{3,})\s*$", head, re.M)
        return m.group(1) if m else None
    except Exception:
        return None


def main():
    files = [f for f in collect() if file_id(f)]
    if not files:
        print("Keine Standard-Dateien gefunden")
        return 1
    fails = 0
    print("== ATC Standards Gesamt-Validierung (CI) ==")
    for f in files:
        r = subprocess.run([sys.executable, os.path.join(HERE, "atc_std_validator.py"), f, "--registry", REGISTRY],
                           capture_output=True, text=True)
        line = [l for l in r.stdout.splitlines() if "COMPLIANT" in l or "NON-COMPLIANT" in l]
        status = line[0].split("|")[0].strip() if line else ("FAIL" if r.returncode else "?")
        print("%-52s %s" % (os.path.relpath(f, ROOT), status))
        if r.returncode:
            fails += 1
            for l in r.stdout.splitlines():
                if "[FAIL]" in l:
                    print("    " + l.strip())
    # S-17 Duplicate Detection (7.8): gleiche ID in mehreren Dateien = FAIL
    ids = {}
    for f in files:
        i = file_id(f)
        if i:
            ids.setdefault(i, []).append(os.path.relpath(f, ROOT))
    dups = {i: fs for i, fs in ids.items() if len(fs) > 1}
    print("S-17 Duplicate Detection (§7.8): " + ("PASS — keine Doppelvergaben" if not dups else "FAIL"))
    for i, fs in dups.items():
        print("  %s in: %s" % (i, ", ".join(fs)))
        fails += 1
    # Registry-Cross-Check: Registry-Eintraege muessen Dateien haben
    try:
        reg = open(REGISTRY, encoding="utf-8").read()
        reg_ids = set(re.findall(r"id:\s*(ATC-STD-[0-9]{3,})", reg))
        missing = reg_ids - set(ids)
        if missing:
            print("WARN: Registry ohne Datei: " + ", ".join(sorted(missing)))
    except Exception:
        pass
    print("RESULT: " + ("ALL COMPLIANT" if fails == 0 else "%d FAIL(s)" % fails))
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
