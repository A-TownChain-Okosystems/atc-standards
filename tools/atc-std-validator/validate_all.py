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
        m = re.search(r"^\s*id:\s*(ATC-STD-(?:BUG-|NET-|ZKP-|AI-DEV-|MD-|SC-|README-|DESC-|VERSION-|AUDIT-|AI-DECISION-|UPDATE-|COMPAT-|MILESTONE-)?[0-9]{3,}|ATC-AAS-[0-9]{3,}|ATC-ENT-[0-9]{3,})\s*$", head, re.M)
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
    # S-18 Registry-Parse-Check: standards.yaml muss strukturell gueltig sein
    # (AUD-001 Governance-Audit 07.09.2026: korrupte Registry wurde nicht erkannt)
    registry_ok = True
    try:
        import yaml
        # Voll-Modus (AUD-2026-0002 Nachtrag): ALLE Registry-Dateien strukturell pruefen
        import glob as _glob
        _reg_files = sorted(_glob.glob(os.path.join(ROOT, "registry", "*.yaml")))
        for _rf in _reg_files:
            with open(_rf, encoding="utf-8") as fh:
                yaml.safe_load(fh)  # wirft bei Strukturfehlern (z.B. Einrueckungs-Bruch)
        with open(REGISTRY, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        entries = data.get("standards", []) if isinstance(data, dict) else []
        if not entries:
            print("S-18 Registry-Parse: FAIL — standards.yaml enthaelt keine 'standards:'-Liste")
            registry_ok = False
        else:
            for e in entries:
                for req in ("id", "title", "version", "status", "owner", "file"):
                    if req not in e:
                        print("S-18 Registry-Parse: FAIL — %s fehlt Pflichtfeld '%s'" % (e.get("id", "?"), req))
                        registry_ok = False
            print("S-18 Registry-Parse: %s (%d Eintraege, %d Registry-Dateien geprueft)" % ("PASS" if registry_ok else "FAIL", len(entries), len(_reg_files)))
    except ImportError:
        # Fallback ohne PyYAML: Fluss-Mapping-Zeilen muessen Klammer-/Anfuehrungsbalanz haben
        for n, line in enumerate(open(REGISTRY, encoding="utf-8"), 1):
            s = line.strip()
            if s.startswith("- {") and not s.endswith("}"):
                print("S-18 Registry-Parse: FAIL — Zeile %d unbalanciert (kein '}' am Ende)" % n)
                registry_ok = False
            if s.count("{") != s.count("}") or s.count('"') % 2:
                print("S-18 Registry-Parse: FAIL — Zeile %d Klammer-/Quote-Balanz defekt" % n)
                registry_ok = False
        print("S-18 Registry-Parse: %s (Fallback-Modus, PyYAML fehlt)" % ("PASS" if registry_ok else "FAIL"))
    except Exception as e:
        print("S-18 Registry-Parse: FAIL — %s" % str(e)[:120])
        registry_ok = False
    if not registry_ok:
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

    # S-20 Milestone-Registry-Check (ATC-STD-MILESTONE-001 §17)
    milestone_ok = True
    MS_PATH = os.path.join(ROOT, "registry", "milestones.yaml")
    if not os.path.exists(MS_PATH):
        print("S-20 Milestones: PASS (keine milestones.yaml — Standard ohne Registry-Nutzung)")
    else:
        try:
            import yaml as _yaml
            ms_data = _yaml.safe_load(open(MS_PATH, encoding="utf-8")) or {}
            entries = ms_data.get("milestones", [])
            if not isinstance(entries, list) or not entries:
                print("S-20 Milestones: FAIL — milestones.yaml ohne 'milestones:'-Liste")
                milestone_ok = False
            else:
                required = ("id", "name", "category", "status", "owner", "goal", "scope",
                            "acceptance_criteria", "dependencies", "risk", "evidence",
                            "start", "target_date", "audit_ref")
                allowed_status = {"PLANNED","DEFINED","IN_PROGRESS","BLOCKED","FEATURE_COMPLETE",
                                  "VALIDATION","AUDIT","FAILED","ACCEPTED","RELEASED",
                                  "VERIFIED","CLOSED","SUPERSEDED"}
                ids, stat = set(), {}
                for m in entries:
                    mid = str(m.get("id", "?"))
                    for req in required:
                        if req not in m:
                            print("S-20 Milestones: FAIL — %s fehlt Pflichtfeld '%s'" % (mid, req)); milestone_ok = False
                    if not re.match(r"^ATC-M-(?:[A-Z]+-)?[0-9]{3,}$", mid):
                        print("S-20 Milestones: FAIL — %s: ID-Pattern verletzt" % mid); milestone_ok = False
                    if mid in ids:
                        print("S-20 Milestones: FAIL — %s: doppelte ID" % mid); milestone_ok = False
                    ids.add(mid); stat[mid] = m.get("status")
                    if m.get("category") not in {"M%d" % i for i in range(9)}:
                        print("S-20 Milestones: FAIL — %s: Kategorie %s ungueltig" % (mid, m.get("category"))); milestone_ok = False
                    if m.get("status") not in allowed_status:
                        print("S-20 Milestones: FAIL — %s: Status %s ungueltig" % (mid, m.get("status"))); milestone_ok = False
                    if not isinstance(m.get("risk"), dict) or "overall" not in (m.get("risk") or {}):
                        print("S-20 Milestones: FAIL — %s: risk.overall fehlt" % mid); milestone_ok = False
                for m in entries:
                    mid = str(m.get("id", "?"))
                    if m.get("status") in {"ACCEPTED", "RELEASED", "VERIFIED", "CLOSED"}:
                        if not m.get("evidence"):
                            print("S-20 Milestones: FAIL — %s: ACCEPTED ohne Evidence (§6)" % mid); milestone_ok = False
                        if not m.get("audit_result"):
                            print("S-20 Milestones: FAIL — %s: ACCEPTED ohne audit_result" % mid); milestone_ok = False
                        if not m.get("actual_completion"):
                            print("S-20 Milestones: FAIL — %s: ACCEPTED ohne actual_completion" % mid); milestone_ok = False
                        if m.get("compatibility_status") == "UNKNOWN":
                            print("S-20 Milestones: FAIL — %s: ACCEPTED mit compatibility UNKNOWN (COMPAT-001)" % mid); milestone_ok = False
                    for dep in m.get("dependencies") or []:
                        if str(dep).startswith("ATC-M-"):
                            if dep not in ids:
                                print("S-20 Milestones: FAIL — %s: unbekannte Dependency %s" % (mid, dep)); milestone_ok = False
                            elif stat.get(dep) not in (None, "ACCEPTED", "RELEASED", "VERIFIED", "CLOSED", "SUPERSEDED") and m.get("status") in {"ACCEPTED", "RELEASED", "VERIFIED", "CLOSED"}:
                                print("S-20 Milestones: FAIL — %s: ACCEPTED bei offener kritischer Dependency %s (%s) (§8)" % (mid, dep, stat.get(dep))); milestone_ok = False
                print("S-20 Milestones: %s (%d Eintraege, IDs: %s)" % ("PASS" if milestone_ok else "FAIL", len(entries), ", ".join(sorted(ids))))
        except ImportError:
            n_ok = sum(1 for l in open(MS_PATH, encoding="utf-8") if re.match(r"^\s*- id: ATC-M-(?:[A-Z]+-)?\d{3,}$", l))
            bal = all(l.count("{") == l.count("}") or ":" in l for l in open(MS_PATH, encoding="utf-8"))
            print("S-20 Milestones: %s (Fallback-Modus, PyYAML fehlt; %d ATC-M-Eintraege)" % ("PASS" if (n_ok and bal) else "WARN"))
        except Exception as e:
            print("S-20 Milestones: FAIL — %s" % str(e)[:120]); milestone_ok = False
    if not milestone_ok:
        fails += 1

    print("RESULT: " + ("ALL COMPLIANT" if fails == 0 else "%d FAIL(s)" % fails))

    # S-19 Mutationstest-Suite: Header-Drift-Erkennung muss zuverlaessig
    # funktionieren — gezielte Mutanten gegen echte Standards. Laeuft in
    # der CI automatisch mit (validate_all wird je Push/PR ausgefuehrt).
    suite = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "tests", "test_s19_mutation.py")
    if os.path.exists(suite):
        rc = subprocess.run([sys.executable, suite]).returncode
        if rc != 0:
            return rc
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
