#!/usr/bin/env python3
# Copyright (c) 2026 Michael Wroblewski / ShivaCore / A-TownChain-Okosystems. All Rights Reserved.
"""ATC Standard Validator v0.1.0 — Validator fuer ATC-STD-000 (Governance).

Prueft einen Standard gegen die Verfassung: Metadaten-Header, ID-Format,
SemVer, Lifecycle-Status, Abstract/Scope, REQ-IDs, normative Sprache,
Compliance/Security-Sektionen, Changelog, References, Registry-Eintrag
und Abhaengigkeitszyklen (registry/dependencies.yaml).

Aufruf: python3 atc_std_validator.py <standard.md> [--registry <standards.yaml>]
Exit:   0 = COMPLIANT, 1 = NON-COMPLIANT. Nur Python-stdlib.
"""
import argparse
import os
import re
import sys

VERSION = "0.1.0"
STATES = ["idea", "proposed", "draft", "review", "candidate", "approved",
          "stable", "deprecated", "retired"]
CATS = ["governance", "architecture", "repository", "development", "security",
        "protocol", "blockchain", "ai", "os", "infrastructure", "applications"]
REQ_RE = re.compile(r"REQ-[A-Z]+(?:-[A-Z]+)?-[0-9]{3}")


def read(p):
    try:
        with open(p, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return None


class V:
    def __init__(self):
        self.results = []

    def add(self, code, status, msg):
        self.results.append((code, status, msg))


def parse_meta(text):
    """Minimal-Parser fuer den YAML-Header (bis '---')."""
    m = re.match(r"^standard:\s*\n(.*?)\n---", text, re.S)
    if not m:
        return None
    meta = {}
    for line in m.group(1).splitlines():
        km = re.match(r"^\s*(id|title|version|status|category|owner|created|updated|normative|superseded_by):\s*(.+)$", line)
        if km:
            val = km.group(2).strip().strip('"').strip("'")
            meta[km.group(1)] = val
    return meta


def find_cycles(dep_text):
    """Zyklenerkennung im standards:-Graph der registry/dependencies.yaml."""
    sec = re.search(r"^standards:\s*\n(.*?)(?=\Z|^\w)", dep_text, re.S | re.M)
    if not sec:
        return None
    graph = {}
    for line in sec.group(1).splitlines():
        m = re.match(r"^\s*(ATC-STD-[0-9]+):\s*\{\s*depends:\s*\[(.*?)\]\s*\}", line)
        if m:
            graph[m.group(1)] = [d.strip() for d in m.group(2).split(",") if d.strip()]
    cycles = []
    state = {}
    def dfs(node, path):
        if state.get(node) == "ok":
            return
        if node in path:
            cycles.append(path[path.index(node):] + [node])
            return
        state[node] = "visiting"
        for dep in graph.get(node, []):
            dfs(dep, path + [node])
        state[node] = "ok"
    for n in graph:
        dfs(n, [])
    return cycles or ([], [])[0]


def validate(path, registry_path):
    v = V()
    name = os.path.basename(path)
    text = read(path) or ""
    meta = parse_meta(text)

    # S-01 Metadaten
    REQ_KEYS = ["id", "title", "version", "status", "category", "owner",
                "created", "updated", "normative"]
    if not meta:
        v.add("S-01", "FAIL", "Kein maschinenlesbarer Metadaten-Header (ATC-STD-000 §8)")
    else:
        fehlt = [k for k in REQ_KEYS if k not in meta]
        v.add("S-01", "FAIL" if fehlt else "PASS",
              "Metadaten: " + ("vollstaendig" if not fehlt else "fehlt: " + ", ".join(fehlt)))

    # S-02 ID-Format
    sid = meta.get("id", "")
    ok = re.match(r"^ATC-STD-[0-9]{3,}$", sid)
    v.add("S-02", "PASS" if ok else "FAIL",
          "ID-Format: %s" % (sid if ok else (sid or "FEHLT") + " (erwartet ATC-STD-XXX)"))

    # S-03 SemVer
    ver = meta.get("version", "")
    v.add("S-03", "PASS" if re.match(r"^\d+\.\d+\.\d+$", ver) else "FAIL",
          "Version: %s" % (ver if ver else "FEHLT"))

    # S-04 Lifecycle
    st = meta.get("status", "").lower()
    v.add("S-04", "PASS" if st in STATES else "FAIL",
          "Status: %s" % (st if st in STATES else st + " (ungueltig)"))

    # S-05 Kategorie
    kat = meta.get("category", "").lower()
    v.add("S-05", "PASS" if kat in CATS else "FAIL",
          "Kategorie: %s" % (kat if kat in CATS else kat + " (nicht in categories.yaml)"))

    # S-06 Abstract
    v.add("S-06", "PASS" if re.search(r"^##+\s.*Abstract", text, re.M | re.I) else "FAIL",
          "Abstract-Sektion")

    # S-07 Scope
    hat_scope = re.search(r"^##+\s.*Scope", text, re.M | re.I) or re.search(r"Scope:", text)
    v.add("S-07", "PASS" if hat_scope else "FAIL", "Scope (Gilt/Nicht-Gilt)")

    # S-08 REQ-IDs (Duplikat-Check nur auf id:-Deklarationen, nicht Prosa-Beispiele)
    reqs = REQ_RE.findall(text)
    decl = re.findall(r"id:\s*(REQ-[A-Z]+(?:-[A-Z]+)?-[0-9]{3})", text)
    dup = [r for r in set(decl) if decl.count(r) > 1]
    if dup:
        v.add("S-08", "FAIL", "Doppelte REQ-ID-Deklarationen: " + ", ".join(dup))
    elif decl:
        v.add("S-08", "PASS", "REQ-IDs: %d deklariert, %d Erwaehnungen, eindeutig" % (len(decl), len(reqs)))
    else:
        v.add("S-08", "WARN", "Keine REQ-ID-Deklarationen (ATC-STD-000 §11 empfiehlt REQ-<DOM>-NNN)")

    # S-09 Normative Sprache
    normativ = meta.get("normative", "")
    hat_rf = re.search(r"\b(MUST|SHOULD|MAY)\b", text)
    if normativ == "true":
        v.add("S-09", "PASS" if hat_rf else "FAIL",
              "RFC-2119-Terminologie" if hat_rf else "normativ: true ohne MUST/SHOULD/MAY")
    else:
        v.add("S-09", "PASS", "nicht normativ — Terminologie optional")

    # S-10 Compliance-Definition
    v.add("S-10", "PASS" if re.search(r"Compliance", text, re.I) else "WARN",
          "Compliance-Definition (Verfahren wie Einhaltung geprueft wird)")

    # S-11 Security Considerations
    v.add("S-11", "PASS" if re.search(r"^##+\s.*Security", text, re.M | re.I) else "WARN",
          "Security Considerations")

    # S-12 Changelog
    v.add("S-12", "PASS" if re.search(r"^##+\s.*Changelog", text, re.M | re.I) else "WARN",
          "Changelog-Sektion")

    # S-13 References
    v.add("S-13", "PASS" if re.search(r"^##+\s.*References", text, re.M | re.I) else "WARN",
          "References (kategorisiert NORMATIVE/INFORMATIVE/…)")

    # S-14 Registry-Eintrag
    if registry_path and os.path.exists(registry_path):
        reg = read(registry_path) or ""
        entry = re.search(r"\{\s*id:\s*%s\s*,(.*?)\}" % re.escape(sid), reg)
        if entry:
            zeile = entry.group(0)
            rv = re.search(r'version:\s*"([\d.]+)"', zeile)
            rs = re.search(r"status:\s*(\w+)", zeile)
            konsistent = (not rv or rv.group(1) == ver) and (not rs or rs.group(1) == st)
            v.add("S-14", "PASS" if konsistent else "FAIL",
                  "Registry-Eintrag: vorhanden, " + ("Version/Status konsistent" if konsistent else
                  "Divergenz Datei(%s/%s) vs Registry(%s/%s)" % (ver, st, rv.group(1) if rv else "?", rs.group(1) if rs else "?")))
        else:
            v.add("S-14", "FAIL", "KEIN Registry-Eintrag in standards.yaml (ATC-STD-000 §19: Kein Eintrag = kein Standard)")
    else:
        v.add("S-14", "WARN", "Registry-Check uebersprungen (keine standards.yaml)")

    # S-15 Abhaengigkeitszyklen
    dep_path = os.path.join(os.path.dirname(registry_path or ""), "dependencies.yaml") if registry_path else None
    dep = read(dep_path) if dep_path else None
    if dep and "standards:" in dep:
        cycles = find_cycles(dep)
        v.add("S-15", "PASS" if not cycles else "FAIL",
              "Standard-Abhaengigkeitsgraph: " + ("azyklisch" if not cycles else "ZYKLUS: " + " → ".join(cycles)))
    else:
        v.add("S-15", "WARN", "Zyklenerkennung uebersprungen (kein standards-Graph)")

    return v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("standard")
    ap.add_argument("--registry", default=None)
    args = ap.parse_args()
    reg = args.registry or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "../../registry/standards.yaml")
    v = validate(args.standard, reg)
    print("ATC STANDARD VALIDATION")
    print("=" * 60)
    print("Standard: %s | Validator v%s (ATC-STD-000)" % (os.path.basename(args.standard), VERSION))
    print()
    fails = warns = 0
    for code, status, msg in v.results:
        print("[%s] %s: %s" % (status, code, msg))
        fails += status == "FAIL"
        warns += status == "WARN"
    print()
    print("RESULT")
    print("=" * 60)
    print("%s | Fails: %d | Warns: %d" % ("COMPLIANT" if not fails else "NON-COMPLIANT", fails, warns))
    sys.exit(0 if not fails else 1)


if __name__ == "__main__":
    main()
